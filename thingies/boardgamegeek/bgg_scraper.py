#!/usr/bin/env python3
import os.path
import pickle
import re
import sys
from functools import reduce
from itertools import groupby
from urllib import request, error

html_template_table_prefix = '''
            <table class="zui-table">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Title</th>
                        <th>Description</th>
                        <th>Rating</th>
                        <th>Votes</th>
                    </tr>
                </thead>                    
                <tbody>'''

html_template_page_prefix = '''<html>
        <head> <link rel="stylesheet" href="table.css">
        </head>
        <body>
            %s
        ''' % html_template_table_prefix

html_row_template_format = '''<tr">
        <td%s%3d %-6s</td>
        <td>
            <div class="container">
                <img  class="image" alt="%-40s" src="%s">
                <span class="img-tooltiptext">%s</span>
            </div>
        </td>
        <td>
            <div class="tooltip">%s<span> %s</span>
            <span class="tooltiptext">%s</span>
            </div>
        </td>
        <td%s>%2.3f %s</td>        
        <td>%7d %s</td>
    </tr>'''

html_template_table_suffix = '''</tbody>
            </table>
            <br/>
'''

html_template_page_suffix = '''%s
        </body>
    </html>''' % html_template_table_suffix

watchlist_template = "https://www.boardgamegeek.com/xmlapi/boardgame/%s?stats=1"


class BGGRow:
    def __init__(self, rank, name, year, description, image_link, rating, votes):
        self.rank = int(rank)
        self.rank_marker = "NEW!!"
        self.name = name
        self.year = year
        self.description = description
        self.image_link = image_link
        self.rating = float(rating)
        self.rating_marker = ""
        self.votes = int(votes)
        self.votes_marker = ""

    def update(self, other):
        self.set_rank_marker(other.rank)
        self.rank = other.rank
        self.year = other.year
        self.set_rating_marker(other.rating)
        self.rating = other.rating
        if self.description is not other.description:
            self.description = other.description
        if self.image_link is not other.image_link:
            self.image_link = other.image_link
        self.set_votes_marker(other.votes)
        self.votes = other.votes

    def set_votes_marker(self, new_votes):
        difference = new_votes - self.votes
        prefix = "+" if difference > 0 else ""
        self.votes_marker = "(" + prefix + ("%d" % difference) + ")"

    def set_rank_marker(self, new_rank):
        if new_rank > self.rank:
            self.rank_marker = '(v%2d)' % (new_rank - self.rank)
        elif new_rank < self.rank:
            self.rank_marker = '(^%2d)' % (self.rank - new_rank)
        else:
            self.rank_marker = ""

    def set_rating_marker(self, new_rating):
        diff = abs(new_rating - self.rating)
        if new_rating > self.rating:
            self.rating_marker = '(+%1.3f)' % diff
        elif new_rating < self.rating:
            self.rating_marker = '(-%1.3f)' % diff
        else:
            self.rating_marker = len('(+1.333)') * ' '

    def rank_class(self):
        if "^" in self.rank_marker and "+" in self.rating_marker:
            return ' class="up-rank">'
        elif "v" in self.rank_marker and "-" in self.rating_marker:
            return ' class="down-rank">'
        elif "NEW" in self.rank_marker:
            return ' class="new-rank">'
        else:
            return '>'

    def html_str(self, rating_bg=""):
        return html_row_template_format % (self.rank_class(), self.rank, self.rank_marker,
                                           self.name[:37] + "..." if len(self.name) > 37 else self.name,
                                           self.image_link,
                                           self.name,
                                           self.name[:37] + "..." if len(self.name) > 37 else self.name, self.year,
                                           self.description,
                                           rating_bg, self.rating, self.rating_marker,
                                           self.votes, self.votes_marker)

    def __str__(self):
        template = "%4d %-6s, %-40s %s, %2.3f %s, %7d %s"
        return template % (self.rank, self.rank_marker,
                           self.name[:37] + "..." if len(self.name) > 37 else self.name,
                           self.year,
                           self.rating, self.rating_marker,
                           self.votes, self.votes_marker)


def update_scoring(new_data, old_data):
    outdated_elements = []
    for k, e in old_data.items():
        if not (k in new_data):
            outdated_elements.append(k)
        else:
            e.update(new_data[k])
    outdated_elements = [old_data.pop(k, None) for k in outdated_elements]
    for new_key in [k for k in new_data if k not in old_data]:
        old_data[new_key] = new_data[new_key]
    return outdated_elements


def fetch_actual_data(rank=None):
    if rank:
        rows = []
        objectid_regex = re.compile(r'.*href="/boardgame.*/(\d+)/')
        for start_rank, objectid_ranks in rank:
            objectids = [o_r[0] for o_r in objectid_ranks]
            rank_option = ("?rank=%s" % start_rank)
            # print(objectid_ranks)
            # print(objectids)
            rs = [row for row in load_actual_page(rank_option)
                  if objectid_regex.findall(row[5])[0] in objectids]
            rows += rs
    else:
        rows = load_actual_page("")
    # for row in rows:
    #     for idx, r in enumerate(row):
    #         print ("%02d : %s" % (idx, r))
    keys, names = fetch_names(rows)
    elements = list(zip(fetch_ranks(rows), names, fetch_year(rows), fetch_description(rows), fetch_image_links(rows),
                        fetch_rating(rows), fetch_votes(rows)))
    elements = [BGGRow(rank, name, year, description, image_link, rating, votes) for
                rank, name, year, description, image_link, rating, votes in elements]
    data = dict(zip(keys, elements))
    return data


def read_watchlist(watchlist_file):
    game_ids = [objectid.strip() for objectid in open(watchlist_file).readlines()]
    chunks = [game_ids[i:i+20] for i in range(0,len(game_ids), 20)]
    return [(watchlist_template % ",".join(chunk)) for chunk in chunks]


def load_watchlist_page(url):
    with request.urlopen(url) as resp:
        target_lines = [l.decode() for l in resp.readlines()]
        target_lines = [line.strip().replace('\t', '') for line in target_lines if len(line.strip())]
    return extract_table_rows(target_lines, "<boardgame objectid=", "</boardgame>")


def fetch_watchlist_rows(rows):
    objectid_regex = re.compile(r'.*<boardgame objectid="(\d+)">')
    rank_regex = re.compile(r'.*friendlyname="Board Game Rank" value="(.*)" bayesaverage=')
    # rank_regex = re.compile(r'.*friendlyname="Board Game Rank" value="(\d+)" bayesaverage=')
    # print(len(list(objectid_regex.findall(line)[0] for row in rows for line in row if objectid_regex.match(line))))
    # print(len(list((rank_regex.findall(line)[0] for row in rows for line in row if rank_regex.match(line)))))

    objectid_ranks = list(
        zip((objectid_regex.findall(line)[0] for row in rows for line in row if objectid_regex.match(line)),
            (rank_regex.findall(line)[0] for row in rows for line in row if rank_regex.match(line))))
    # print(objectid_ranks)
    objectid_ranks = [(o_r[0],o_r[1].replace("Not Ranked", "10000")) for o_r in objectid_ranks]
    # print(objectid_ranks)
    ranks = sorted(objectid_ranks, key=lambda o_r: int(o_r[1].zfill(3)[:-2]))
    # print(ranks)
    return fetch_actual_data(
        [("%d01" % k, list(v)) for k, v in groupby(ranks, key=lambda o_r: int(o_r[1].zfill(3)[:-2]))])


def fetch_actual_watchlist_data(watchlist):
    return fetch_watchlist_rows(load_watchlist_page(watchlist))


def load_actual_page(rank_option):
    target_url = "https://boardgamegeek.com/browse/boardgame" + rank_option
    try:
        with request.urlopen(target_url) as resp:
            target_lines = [l.decode() for l in resp.readlines()[274:]]
    except error.HTTPError as err:
        print(target_url)
        print (err)
        return []
    target_lines = [line.strip().replace('\t', '') for line in target_lines if len(line.strip()) > 0]
    return extract_table_rows(target_lines)


def extract_table_rows(target_lines, start_pattern="<tr id='row_'>", end_pattern="</tr>"):
    rows = []
    append = False
    for idx, line in enumerate(target_lines):
        if line.startswith(start_pattern):
            append = True
            row = []
        if append:
            row.append(line)
        if line.startswith(end_pattern) and append:
            append = False
            rows.append(row)
    return rows


def fetch_rating(rows):
    rating_regex = re.compile(r'(\d+.\d+)')
    return [rating_regex.findall(r[21] if r[18].startswith("</p") else r[18])[0] for r in rows]


def fetch_votes(rows):
    vote_regex = re.compile(r'(\d+)')
    return [vote_regex.findall(r[25] if r[18].startswith("</p") else r[22])[0] for r in rows]


def fetch_description(rows):
    return [r[17] if r[16].startswith("<p") else "no description" for r in rows]


def fetch_ranks(rows):
    rank_regex = re.compile(r'.*name="(\d+)">')
    return [rank_regex.findall(r[2])[0] for r in rows]


def fetch_image_links(rows):
    image_regex = re.compile(r'.*src="(.*)"></a>')
    return [image_regex.findall(r[5])[0] for r in rows]


def fetch_year(rows):
    rank_regex = re.compile(r'.*(\(\d+\))</span>')
    return [rank_regex.findall(r[14])[0] for r in rows]


def fetch_names(rows):
    name_lines = [line[13] for line in rows]
    name_regex = re.compile(r'href="(.*)".*>(.*)</a>')
    tuples = [name_regex.findall(line) for line in name_lines]
    dd = reduce(lambda l1, l2: l1 + l2, tuples)
    return zip(*dd)


def write_file(fil, old_data, outdated):
    write_outdated(fil, outdated)
    row: BGGRow
    rank_sorted = sorted(old_data.values(), key=lambda e: e.rank)
    factor = 0
    for row in rank_sorted:
        actual_factor = (row.rank - 1) // 100
        if factor < actual_factor:
            factor = actual_factor
            print()
            fil.write("\n")
        print(row)
        fil.write(str(row))
        fil.write("\n")


def write_html(fil, old_data, page_prefix=True, page_suffix=True):
    fil.write(html_template_page_prefix if page_prefix else html_template_table_prefix)
    rank_sorted = sorted(old_data, key=lambda e: e.rank)
    largest_diff = largest_rating_diff(rank_sorted[:100])
    row: BGGRow
    factor = 0
    for row in rank_sorted:
        actual_factor = (row.rank - 1) // 100
        if factor < actual_factor:
            factor = actual_factor
            fil.write(html_template_table_suffix)
            fil.write(html_template_page_prefix)
        rating_class = ' class="rating-gap"' if row.name in largest_diff else ""
        fil.write(row.html_str(rating_class))
        fil.write("\n")
    fil.write(html_template_page_suffix if page_suffix else html_template_table_suffix)


def largest_rating_diff(rank_sorted):
    largest_diff = [t[1] for t in
                    sorted([(rank_sorted[idx].rating - rank_sorted[idx + 1].rating, rank_sorted[idx].name) for idx in
                            range(len(rank_sorted) - 1)]
                           , reverse=True)[:10]]
    return largest_diff


def write_outdated(fil, outdated):
    if len(outdated):
        fil.write("Outdated:")
        fil.write("\n")
        for o in outdated:
            fil.write(str(o))
            fil.write("\n")
        fil.write("\n")


def main(basename):
    pickle_file = os.path.join(basename, "target.pickle")
    latest_rating_file = os.path.join(basename, "latest-ratings")
    latest_rating_html = os.path.join(basename, "latest-ratings.html")
    latest_watchlist = os.path.join(basename, "latest-watchlist")
    # latest_gamelist = os.path.join(basename, "latest-gamelist")

    with open(pickle_file, 'rb') as fil:
        pickled_data = pickle.load(fil)

    # outdated = []
    # for k,v in pickled_data.items():
    #     outdated.append(v)
    #     if len(outdated) == 3:
    #         break

    # gamelist = fetch_actual_watchlist_data(read_watchlist(latest_gamelist))
    # print([fetch_actual_watchlist_data(url) for url in read_watchlist(latest_watchlist)])
    # print(len(read_watchlist(latest_watchlist)))
    watchlist = reduce(lambda dct1, dct2 : dct1 | dct2, [fetch_actual_watchlist_data(url) for url in read_watchlist(latest_watchlist)])
    # print(len(watchlist.keys()))
    actual_data = fetch_actual_data()
    # print([l for l in watchlist])
    actual_data.update(watchlist)
    # actual_data.update(gamelist)
    # pickled_data = actual_data
    outdated = update_scoring(actual_data, pickled_data)

    with open(latest_rating_file, 'w') as fil:
        write_file(fil, pickled_data, outdated)

    with open(latest_rating_html, 'w') as fil:
        if outdated:
            write_html(fil, outdated, outdated is None, not outdated)
        write_html(fil, pickled_data.values(), not outdated)

    with open(pickle_file, 'wb') as fil:
        pickle.dump(pickled_data, fil)


if __name__ == '__main__':
    main(os.path.dirname(sys.argv[0]))
