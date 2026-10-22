#!/usr/bin/env python3
import html
import os.path
import pickle
import re
import sys
import time
from urllib import request
from urllib.request import Request
from xml.etree import ElementTree

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
        '''

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

html_template_page_suffix = '''
        </body>
    </html>'''

# watchlist_template = "https://www.boardgamegeek.com/xmlapi/boardgame/%s?stats=1"
game_url_template = "https://boardgamegeek.com/xmlapi/boardgame/%s?stats=1"
hot_url = "https://boardgamegeek.com/xmlapi2/hot?type=boardgame"
top_ranks = 100

# token = "2a3f21d5-645e-4bd3-b8e5-9a5cd4c484d6"
# token = "6580d55c-6752-4089-a577-626702d2cdd8"
token = "fc4021d4-3c12-4b9a-bebd-6f82a1fe8419"
headers = {"Authorization": f"Bearer {token}"}

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


def read_watchlist(watchlist_file):
    return [objectid.strip() for objectid in open(watchlist_file).readlines() if objectid.strip()]


def load_xml(url):
    req = Request(url, headers=headers)
    with request.urlopen(req) as resp:
        return ElementTree.fromstring(resp.read())

def child_value(element, tag, default="?"):
    # hot list items keep their data in a value attribute, and some lack e.g. yearpublished
    child = element.find(tag)
    return child.get("value", default) if child is not None else default


def fetch_hot_ids():
    hots = load_xml(hot_url)
    for i in hots.findall("item"):
        print(i.get("rank"), i.get("id"), child_value(i, "name"), child_value(i, "yearpublished"))
    return [item.get("id") for item in hots.findall("item")]
#
# def fetch_top100():
#     return [item.get("id") for item in hots.findall("item")]


def short_description(description):
    # the xml api only has the full description, so use its first sentence
    first_line = html.unescape(description or "").strip().split("\n")[0]
    sentence = re.split(r'(?<=[.!?])\s', first_line, maxsplit=1)[0]
    return " ".join(sentence.split())[:150] or "no description"


def parse_games(root):
    data = {}
    for game in root.findall("boardgame"):
        ratings = game.find("statistics/ratings")
        if ratings is None:
            continue
        rank = ratings.find("ranks/rank[@name='boardgame']")
        rank = rank.get("value") if rank is not None else ""
        data["/boardgame/%s" % game.get("objectid")] = BGGRow(
            rank if rank.isdigit() else 10000,
            game.findtext("name[@primary='true']"),
            "(%s)" % game.findtext("yearpublished"),
            short_description(game.findtext("description")),
            game.findtext("thumbnail", ""),
            ratings.findtext("bayesaverage"),
            ratings.findtext("usersrated"))
    return data


def fetch_games(game_ids):
    game_ids = list(dict.fromkeys(game_ids))
    data = {}
    for i in range(0, len(game_ids), 20):
        if i:
            time.sleep(2)  # stay below the xml api rate limit
        data.update(parse_games(load_xml(game_url_template % ",".join(game_ids[i:i + 20]))))
    return data


def game_id(key):
    return key.split("/")[2]


def match_existing_keys(new_data, old_data):
    # xml api keys lack the name slug of the old browse page links, so reuse existing keys
    old_keys = {game_id(k): k for k in old_data}
    return {old_keys.get(game_id(k), k): v for k, v in new_data.items()}


def fetch_actual_data(old_data, watchlist_ids):
    # the xml api has no ranking list, so check every known game plus the hot ones for the top ranks
    candidate_ids = watchlist_ids + [game_id(k) for k in old_data] + fetch_hot_ids()
    games = fetch_games(candidate_ids)
    actual_data = {k: v for k, v in games.items() if v.rank <= top_ranks or game_id(k) in watchlist_ids}
    return match_existing_keys(actual_data, old_data)


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


def write_html(fil, old_data, outdated):
    fil.write(html_template_page_prefix)
    if outdated:
        fil.write("<h2>Outdated</h2>\n")
        write_html_table(fil, outdated)
        fil.write("<h2>Ranking</h2>\n")
    write_html_table(fil, old_data.values())
    fil.write(html_template_page_suffix)


def write_html_table(fil, rows):
    fil.write(html_template_table_prefix)
    rank_sorted = sorted(rows, key=lambda e: e.rank)
    largest_diff = largest_rating_diff(rank_sorted[:100])
    row: BGGRow
    factor = 0
    for row in rank_sorted:
        actual_factor = (row.rank - 1) // 100
        if factor < actual_factor:
            factor = actual_factor
            fil.write(html_template_table_suffix)
            fil.write(html_template_table_prefix)
        rating_class = ' class="rating-gap"' if row.name in largest_diff else ""
        fil.write(row.html_str(rating_class))
        fil.write("\n")
    fil.write(html_template_table_suffix)


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
        for o in sorted(outdated, key=lambda e: e.rank):
            fil.write(str(o))
            fil.write("\n")
        fil.write("\n")


def main(basename):
    pickle_file = os.path.join(basename, "target.pickle")
    latest_rating_file = os.path.join(basename, "latest-ratings")
    latest_rating_html = os.path.join(basename, "latest-ratings.html")
    latest_watchlist = os.path.join(basename, "latest-watchlist")
    latest_top100 = os.path.join(basename, "latest-top100")
    # latest_gamelist = os.path.join(basename, "latest-gamelist")

    with open(pickle_file, 'rb') as fil:
        pickled_data = pickle.load(fil)

    # outdated = []
    # for k,v in pickled_data.items():
    #     outdated.append(v)
    #     if len(outdated) == 3:
    #         break

    # watchlist_ids = read_watchlist(latest_watchlist) + read_watchlist(latest_gamelist)
    actual_data = fetch_actual_data(pickled_data, read_watchlist(latest_watchlist) + read_watchlist(latest_top100))
    # pickled_data = actual_data
    outdated = update_scoring(actual_data, pickled_data)

    with open(latest_rating_file, 'w') as fil:
        write_file(fil, pickled_data, outdated)

    with open(latest_rating_html, 'w') as fil:
        write_html(fil, pickled_data, outdated)

    with open(pickle_file, 'wb') as fil:
        pickle.dump(pickled_data, fil)


if __name__ == '__main__':
    main(os.path.dirname(sys.argv[0]))
