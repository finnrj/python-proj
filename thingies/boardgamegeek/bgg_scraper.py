#!/usr/bin/env python3
import pickle
import re
import sys
import os.path
from functools import reduce
from urllib import request

html_template_prefix = '''<html>
        <head> <link rel="stylesheet" href="table.css">
        </head>
        <body>
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

html_template_suffix = '''</tbody>
            </table>
        </body>
    </html>'''


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
        if "^" in self.rank_marker  and "+" in self.rating_marker:
            return ' class="up-rank">'
        elif "v" in self.rank_marker  and "-" in self.rating_marker:
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
        template = "%3d %-6s, %-40s %s, %2.3f %s, %7d %s"
        return template % (self.rank, self.rank_marker,
                           self.name[:37] + "..." if len(self.name) > 37 else self.name,
                           self.year,
                           self.rating, self.rating_marker,
                           self.votes, self.votes_marker)


def update_scoring(data, old_data):
    outdated_elements = []
    for k, e in old_data.items():
        if not (k in data):
            outdated_elements.append(k)
        else:
            e.update(data[k])
    outdated_elements = [old_data.pop(k, None) for k in outdated_elements]
    for new_key in [k for k in data if k not in old_data]:
        old_data[new_key] = data[new_key]
    return outdated_elements


def fetch_actual_data():
    rows = load_actual_page()
    keys, names = fetch_names(rows)
    elements = list(zip(fetch_ranks(rows), names, fetch_year(rows), fetch_description(rows), fetch_image_links(rows),
                        fetch_rating(rows), fetch_votes(rows)))
    elements = [BGGRow(rank, name, year, description, image_link, rating, votes) for
                rank, name, year, description, image_link, rating, votes in elements]
    data = dict(zip(keys, elements))
    return data


def load_actual_page():
    target_url = "https://boardgamegeek.com/browse/boardgame"
    with request.urlopen(target_url) as resp:
        target_lines = [l.decode() for l in resp.readlines()[274:]]
    target_lines = [line.strip().replace('\t', '') for line in target_lines if len(line.strip()) > 0]
    return extract_tablerows(target_lines)


def extract_tablerows(target_lines):
    rows = []
    append = False
    for idx, line in enumerate(target_lines):
        if line.startswith("<tr id='row_'>"):
            append = True
            row = []
        if append:
            row.append(line)
        if line.startswith("</tr>") and append:
            append = False
            rows.append(row)
    return rows


def fetch_rating(rows):
    rating_regex = re.compile('(\d+.\d+)')
    return [rating_regex.findall(r[21])[0] for r in rows]


def fetch_votes(rows):
    vote_regex = re.compile('(\d+)')
    return [vote_regex.findall(r[25])[0] for r in rows]


def fetch_description(rows):
    return [r[17] for r in rows]


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
    for row in rank_sorted:
        print(row)
        fil.write(str(row))
        fil.write("\n")


def write_html(fil, old_data):
    fil.write(html_template_prefix)
    rank_sorted = sorted(old_data.values(), key=lambda e: e.rank)
    largest_diff = largest_rating_diff(rank_sorted)
    row: BGGRow
    for row in rank_sorted:
        rating_class = ' class="rating-gap"' if row.name in largest_diff else ""
        fil.write(row.html_str(rating_class))
        fil.write("\n")
    fil.write(html_template_suffix)


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

    with open(pickle_file, 'rb') as fil:
        old_data = pickle.load(fil)

    outdated = update_scoring(fetch_actual_data(), old_data)
    with open(latest_rating_file, 'w') as fil:
        write_file(fil, old_data, outdated)

    # outdated = []
    with open(latest_rating_html, 'w') as fil:
        if outdated:
            write_html(fil, outdated)
        write_html(fil, old_data)

    with open(pickle_file, 'wb') as fil:
        pickle.dump(old_data, fil)


if __name__ == '__main__':
    main(os.path.dirname(sys.argv[0]))