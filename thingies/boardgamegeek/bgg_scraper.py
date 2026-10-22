#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
import csv
import gzip
import html
import io
import os.path
import pickle
import re
import sys
import time
from urllib import request
from urllib.request import Request
import zipfile
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
game_url_template = "https://boardgamegeek.com/xmlapi2/thing?id=%s&stats=1"
hot_url = "https://boardgamegeek.com/xmlapi2/hot?type=boardgame"
dump_url = "https://boardgamegeek.com/data_dumps/bg_ranks"
geeklist_url_template = "https://boardgamegeek.com/xmlapi/geeklist/%s"
geeklist_id = "298125"
geeklist_url = geeklist_url_template % geeklist_id
browse_url = "https://boardgamegeek.com/browse/boardgame"
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


def load_xml(url, timeout=15):
    req = Request(url, headers=headers)
    with request.urlopen(req, timeout=timeout) as resp:
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


def parse_top100_data(raw_data, max_ranks=top_ranks):
    if isinstance(raw_data, str):
        content = raw_data
    elif raw_data.startswith(b"PK\x03\x04"):
        with zipfile.ZipFile(io.BytesIO(raw_data)) as z:
            csv_files = [n for n in z.namelist() if n.endswith((".csv", ".xml", ".txt"))]
            target = csv_files[0] if csv_files else z.namelist()[0]
            content = z.read(target).decode("utf-8", errors="ignore")
    elif raw_data.startswith(b"\x1f\x8b"):
        content = gzip.decompress(raw_data).decode("utf-8", errors="ignore")
    else:
        content = raw_data.decode("utf-8", errors="ignore")

    stripped = content.lstrip()
    if stripped.startswith("<?xml") or "<geeklist" in stripped or "<items" in stripped:
        try:
            root = ElementTree.fromstring(content)
            items = root.findall(".//item")
            if items:
                ids = []
                for item in items:
                    oid = item.get("objectid") or item.get("id")
                    if oid and oid.isdigit() and oid not in ids:
                        ids.append(oid)
                    if len(ids) == max_ranks:
                        break
                if ids:
                    return ids
        except Exception:
            pass

    if stripped.startswith(("<html", "<!DOCTYPE", "<!doctype")):
        ids = []
        for match in re.findall(r'/boardgame/(\d+)', content):
            if match not in ids:
                ids.append(match)
            if len(ids) == max_ranks:
                break
        return ids

    f = io.StringIO(content.strip())
    reader = csv.reader(f)
    try:
        header = next(reader)
    except StopIteration:
        return []

    header_lower = [h.strip().lower() for h in header]
    id_idx = -1
    rank_idx = -1
    expansion_idx = -1

    for idx, col in enumerate(header_lower):
        if col in ("id", "game_id", "boardgame_id", "objectid"):
            id_idx = idx
        elif col in ("rank", "boardgame_rank", "bg_rank"):
            rank_idx = idx
        elif col in ("is_expansion", "expansion"):
            expansion_idx = idx

    if id_idx == -1:
        if len(header) > 0 and header[0].strip().isdigit():
            id_idx = 0
            f.seek(0)
            reader = csv.reader(f)
        else:
            return []

    entries = []
    for row_idx, row in enumerate(reader):
        if not row or len(row) <= id_idx:
            continue
        game_id_str = row[id_idx].strip()
        if not game_id_str.isdigit():
            continue
        if expansion_idx != -1 and len(row) > expansion_idx:
            is_exp = row[expansion_idx].strip()
            if is_exp in ("1", "true", "True", "yes"):
                continue

        rank_val = row_idx + 1
        if rank_idx != -1 and len(row) > rank_idx:
            rank_str = row[rank_idx].strip()
            if rank_str.isdigit():
                rank_val = int(rank_str)

        entries.append((rank_val, game_id_str))

    entries.sort(key=lambda x: x[0])
    ids = []
    for _, gid in entries:
        if gid not in ids:
            ids.append(gid)
        if len(ids) == max_ranks:
            break
    return ids


def fetch_top100(url=geeklist_url, top100_file="latest-top100", geeklist_id=None, source=None):
    if geeklist_id is not None:
        url = geeklist_url_template % geeklist_id
    elif source is not None:
        url = source
    elif url and not url.startswith("http://") and not url.startswith("https://") and top100_file == "latest-top100":
        if isinstance(url, int) or (isinstance(url, str) and url.isdigit()):
            url = geeklist_url_template % url
        elif not (url.endswith((".csv", ".zip", ".gz", ".xml", ".html")) and os.path.exists(url)):
            top100_file = url
            url = geeklist_url

    try:
        if url.startswith("http://") or url.startswith("https://"):
            req = Request(url, headers=headers)
            with request.urlopen(req, timeout=15) as resp:
                raw_data = resp.read()
        else:
            with open(url, "rb") as f:
                raw_data = f.read()

        ids = parse_top100_data(raw_data)
        if ids and top100_file:
            with open(top100_file, "w") as f:
                f.write("\n".join(ids) + "\n")
        return ids
    except Exception as e:
        print(f"Error fetching top 100: {e}")
        return []


def short_description(description):
    if not description:
        return ""
    paragraphs = description.split("&#10;&#10;")
    res = paragraphs[0]
    return html.unescape(res)


def parse_games(root):
    data = {}
    items = root.findall("boardgame") + root.findall("item")
    for game in items:
        ratings = game.find("statistics/ratings")
        if ratings is None:
            continue
        rank_elem = ratings.find("ranks/rank[@name='boardgame']")
        rank = rank_elem.get("value") if rank_elem is not None else ""

        # Name: v1 uses <name primary="true">Text</name>, v2 uses <name type="primary" value="Text"/>
        name = game.findtext("name[@primary='true']")
        if not name:
            name_el = game.find("name[@type='primary']")
            if name_el is None:
                name_el = game.find("name")
            if name_el is not None:
                name = name_el.get("value") or name_el.text or ""
        name = name or ""

        # Year: v1 uses text, v2 uses value attribute
        year = game.findtext("yearpublished")
        if not year:
            year_el = game.find("yearpublished")
            if year_el is not None:
                year = year_el.get("value") or year_el.text or ""
        year_str = "(%s)" % year if year else "(?)"

        # Rating / Bayesaverage: v1 uses text, v2 uses value attribute
        bayes = ratings.findtext("bayesaverage")
        if not bayes:
            bayes_el = ratings.find("bayesaverage")
            bayes = bayes_el.get("value") if bayes_el is not None else "0"

        # Votes / Usersrated: v1 uses text, v2 uses value attribute
        votes = ratings.findtext("usersrated")
        if not votes:
            votes_el = ratings.find("usersrated")
            votes = votes_el.get("value") if votes_el is not None else "0"

        desc = game.findtext("description", "")
        thumb = game.findtext("thumbnail", "")

        obj_id = game.get("objectid") or game.get("id")
        data["/boardgame/%s" % obj_id] = BGGRow(
            rank if rank.isdigit() else 10000,
            name,
            year_str,
            short_description(desc),
            thumb,
            bayes,
            votes)
    return data


def fetch_games(game_ids, max_workers=5):
    game_ids = list(dict.fromkeys(game_ids))
    if not game_ids:
        return {}
    batches = [game_ids[i:i + 20] for i in range(0, len(game_ids), 20)]

    def fetch_batch(batch):
        try:
            return parse_games(load_xml(game_url_template % ",".join(batch)))
        except Exception as err:
            print(f"Error fetching batch: {err}")
            return {}

    data = {}
    if len(batches) == 1:
        data.update(fetch_batch(batches[0]))
    else:
        with ThreadPoolExecutor(max_workers=min(max_workers, len(batches))) as executor:
            for batch_result in executor.map(fetch_batch, batches):
                data.update(batch_result)
    return data


def game_id(key):
    return key[len("/boardgame/"):]


def match_existing_keys(actual_data, pickled_data):
    # try to keep original keys - /boardgame/123/name-of-the-game
    for old_k in pickled_data.keys():
        for new_k in [k for k in actual_data.keys() if old_k.startswith(k)]:
            actual_data[old_k] = actual_data.pop(new_k)


def fetch_actual_data(pickled_data, watchlist_ids):
    candidates = list(pickled_data.keys())
    candidates = [game_id(k) for k in candidates if pickled_data[k].rank <= top_ranks]

    # actual_ids = list(dict.fromkeys(candidates + fetch_hot_ids()))
    actual_ids = list(dict.fromkeys(candidates + watchlist_ids + fetch_hot_ids()))
    actual_data = fetch_games(actual_ids)
    match_existing_keys(actual_data, pickled_data)
    return actual_data


def write_file(fil, data, outdated):
    for e in sorted(data.values(), key=lambda e: e.rank):
        if e.rank <= top_ranks:
            fil.write(str(e) + "\n")
    if outdated:
        fil.write("\nOutdated:\n")
        for e in outdated:
            fil.write(str(e) + "\n")


def write_html_table(fil, title, elements, max_rating=10.0):
    fil.write("<h2>%s</h2>\n" % title)
    fil.write(html_template_table_prefix)
    prev = max_rating
    for e in elements:
        rating_bg = ""
        if prev - e.rating > 0.05:
            # rating_bg = ' style="border-top-style:dashed;border-top-color:red"'
            rating_bg = ' style="background-color:powderblue"'
        prev = e.rating
        fil.write(e.html_str(rating_bg))
    fil.write(html_template_table_suffix)


def write_html(fil, data, outdated):
    fil.write(html_template_page_prefix)
    write_html_table(fil, "Top %d" % top_ranks,
                     sorted([v for v in data.values() if v.rank <= top_ranks], key=lambda e: e.rank))

    write_html_table(fil, "Watchlist",
                     sorted([v for v in data.values() if v.rank > top_ranks], key=lambda e: e.rating, reverse=True))

    if outdated:
        write_html_table(fil, "Outdated", outdated)
    fil.write(html_template_page_suffix)


def main(data_dir):
    latest_watchlist = os.path.join(data_dir, "latest-watchlist")
    latest_top100 = os.path.join(data_dir, "latest-top100")
    # latest_gamelist = os.path.join(data_dir, "latest-gamelist")
    latest_rating_file = os.path.join(data_dir, "latest-ratings")
    latest_rating_html = os.path.join(data_dir, "latest-ratings.html")
    pickle_file = os.path.join(data_dir, "target.pickle")

    pickled_data = {}
    with open(pickle_file, 'rb') as fil:
        pickled_data = pickle.load(fil)

    # outdated = []
    # for k,v in pickled_data.items():
    #     outdated.append(v)
    #     if len(outdated) == 3:
    #         break

    top100_ids = fetch_top100(top100_file=latest_top100)

    # watchlist_ids = read_watchlist(latest_watchlist) + read_watchlist(latest_gamelist)
    actual_data = fetch_actual_data(pickled_data, read_watchlist(latest_watchlist) + (top100_ids if top100_ids else read_watchlist(latest_top100)))

    # Persist the actual ranked 1-100 IDs from fetched data to latest_top100
    top_ranked = sorted([v for v in actual_data.values() if v.rank <= top_ranks], key=lambda e: e.rank)
    if top_ranked:
        top_ids = [game_id(k) for k, v in actual_data.items() if v in top_ranked]
        if top_ids and latest_top100:
            with open(latest_top100, 'w') as fil:
                fil.write("\n".join(top_ids) + "\n")

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
