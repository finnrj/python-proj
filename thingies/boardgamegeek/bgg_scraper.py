#!/usr/bin/env python3
import pickle
import re
import sys
import os.path
from functools import reduce
from urllib import request

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


def load_watchlist_pages(watchlist):
    lines = []
    for url in watchlist:
        with request.urlopen(url) as resp:
            target_lines = [l.decode() for l in resp.readlines()]
            target_lines = [line.strip().replace('\t', '') for line in target_lines if len(line.strip())]
            lines.append(target_lines)
    return lines

def fetch_watchlist_names(rows):
    objectid_regex = re.compile(r'<boardgame objectid="(\d*)">')
    name_regex = re.compile(r'.*<name primary="true" sortindex="1">(.*)</name>')
    result = []
    for row in rows:
        for line in row:
            if objectid_regex.match(line):
                objectid = objectid_regex.findall(line)[0]
            if name_regex.match(line):
                name = name_regex.findall(line)[0]
        result.append((objectid, name))
    return result

# <boardgame objectid="162886">
    # <name primary="true" sortindex="1">Spirit Island</name>
    # pass


def fetch_watchlist_ranks(rows):
    rank_rating_regex = re.compile(r'.*friendlyname="Board Game Rank" value="(\d+)" bayesaverage="(\d+\.\d+)".*/>')
    ranks_ratings = [(rank_rating_regex.findall(line)[0][0], rank_rating_regex.findall(line)[0][1]) for row in rows for line in row if rank_rating_regex.match(line)]
    # <rank type="subtype" id="1" name="boardgame" friendlyname="Board Game Rank" value="11" bayesaverage="8.12664" />
    return ranks_ratings


def fetch_watchlist_year(rows):
    # <yearpublished>2017</yearpublished>
    pass


def fetch_watchlist_description(rows):
    # <description>In the most distant reaches of the world, magic still exists, embodied by spirits of the land, of the sky, and of every natural thing. As the great powers of Europe stretch their colonial empires further and further, they will inevitably lay claim to a place where spirits still hold power - and when they do, the land itself will fight back alongside the islanders who live there.&lt;br/&gt;&lt;br/&gt;Spirit Island is a complex and thematic cooperative game about defending your island home from colonizing Invaders. Players are different spirits of the land, each with its own unique elemental powers. Every turn, players simultaneously choose which of their power cards to play, paying energy to do so. Using combinations of power cards that match a spirit's elemental affinities can grant free bonus effects. Faster powers take effect immediately, before the Invaders spread and ravage, but other magics are slower, requiring forethought and planning to use effectively. In the Spirit phase, spirits gain energy, and choose how / whether to Grow: to reclaim used power cards, to seek for new power, or to spread presence into new areas of the island.&lt;br/&gt;&lt;br/&gt;The Invaders expand across the island map in a semi-predictable fashion. Each turn they explore into some lands (portions of the island); the next turn, they build in those lands, forming settlements and cities. The turn after that, they ravage there, bringing blight to the land and attacking any native islanders present.&lt;br/&gt;&lt;br/&gt;The islanders fight back against the Invaders when attacked, and lend the spirits some other aid, but may not always do so exactly as you'd hoped. Some Powers work through the islanders, helping them (eg) drive out the Invaders or clean the land of blight.&lt;br/&gt;&lt;br/&gt;The game escalates as it progresses: spirits spread their presence to new parts of the island and seek out new and more potent powers, while the Invaders step up their colonization efforts. Each turn represents 1-3 years of alternate-history.&lt;br/&gt;&lt;br/&gt;At game start, winning requires destroying every last settlement and city on the board - but as you frighten the Invaders more and more, victory becomes easier: they'll run away even if some number of settlements or cities remain. Defeat comes if any spirit is destroyed, if the island is overrun by blight, or if the Invader deck is depleted before achieving victory.&lt;br/&gt;&lt;br/&gt;The game includes different adversaries to fight against (eg: a Swedish Mining Colony, or a Remote British Colony). Each changes play in different ways, and offers a different path of difficulty boosts to keep the game challenging as you gain skill.&lt;br/&gt;&lt;br/&gt;</description>
    pass


def fetch_watchlist_image_links(rows):
    # <image>https://cf.geekdo-images.com/a13ieMPP2s0KEaKNYmtH5w__original/img/nuQlvKPSBG3jsVzaTgZTpNSjlTw=/0x0/filters:format(png)/pic3615739.png</image>
    # <thumbnail>https://cf.geekdo-images.com/a13ieMPP2s0KEaKNYmtH5w__thumb/img/SKiHQ4zAj8uVdtwxOYKIveY9jCo=/fit-in/200x150/filters:strip_icc()/pic3615739.png</thumbnail>
    pass


def fetch_watchlist_rating(rows):
    # <bayesaverage>8.12664</bayesaverage>
    pass


def fetch_watchlist_votes(rows):
    # <usersrated>30634</usersrated>
    pass


def fetch_actual_watchlist_data(watchlist):
    rows = load_watchlist_pages(watchlist)
    # keys, names = fetch_watchlist_names(rows)
    # rank, rating = fetch_watchlist_ranks(rows)
    print(list(zip(fetch_watchlist_names(rows), fetch_watchlist_ranks(rows))))
    # elements = list(zip(fetch_watchlist_ranks(rows), names, fetch_watchlist_year(rows), fetch_watchlist_description(rows), fetch_watchlist_image_links(rows),
    #                     fetch_watchlist_rating(rows), fetch_watchlist_votes(rows)))
    # elements = [BGGRow(rank, name, year, description, image_link, rating, votes) for
    #             rank, name, year, description, image_link, rating, votes in elements]
    # data = dict(zip(keys, elements))
    # return data


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


def write_html(fil, old_data, page_prefix = True, page_suffix = True):
    fil.write(html_template_page_prefix if page_prefix else html_template_table_prefix)
    rank_sorted = sorted(old_data, key=lambda e: e.rank)
    largest_diff = largest_rating_diff(rank_sorted)
    row: BGGRow
    for row in rank_sorted:
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
    load_watchlist_pages(["https://www.boardgamegeek.com/xmlapi/boardgame/162886?stats=1",
                          "https://www.boardgamegeek.com/xmlapi/boardgame/314491?stats=1"])
    # load_watchlist(["https://boardgamegeek.com/boardgame/314491/meadow"])


    # pickle_file = os.path.join(basename, "target.pickle")
    # latest_rating_file = os.path.join(basename, "latest-ratings")
    # latest_rating_html = os.path.join(basename, "latest-ratings.html")
    #
    # with open(pickle_file, 'rb') as fil:
    #     old_data = pickle.load(fil)

    # outdated = []
    # for k,v in old_data.items():
    #     outdated.append(v)
    #     if len(outdated) == 3:
    #         break
    # outdated = update_scoring(fetch_actual_data(), old_data)
    # with open(latest_rating_file, 'w') as fil:
    #     write_file(fil, old_data, outdated)
    #
    # with open(latest_rating_html, 'w') as fil:
    #     if outdated:
    #         write_html(fil, outdated, outdated, not outdated)
    #     write_html(fil, old_data.values(), not outdated)
    #
    # with open(pickle_file, 'wb') as fil:
    #     pickle.dump(old_data, fil)


if __name__ == '__main__':
    main(os.path.dirname(sys.argv[0]))
