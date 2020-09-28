import pickle
import re
from functools import reduce
import json

import requests
from bs4 import BeautifulSoup


class BGGRow:
    def __init__(self, rank, name, description, image_link, rating, votes):
        self.rank = int(rank)
        self.rank_marker = ""
        self.name = name
        self.description = description
        self.image_link = image_link
        self.rating = float(rating)
        self.rating_marker = ""
        self.votes = int(votes)

    def update(self, other):
        self.set_rank_marker(other.rank)
        self.rank = other.rank
        self.set_rating_marker(other.rating)
        self.rating = other.rating
        if not self.description is other.description:
            self.description = other.description
        if not self.image_link is other.image_link:
            self.image_link = other.image_link
        self.votes = other.votes

    def set_rank_marker(self, new_rank):
        if new_rank > self.rank:
            self.rank_marker = '(^^)'
        elif new_rank < self.rank:
            self.rank_marker = '(vv)'
        else:
            self.rank_marker = ""

    def set_rating_marker(self, new_rating):
        if new_rating > self.rank:
            self.rating_marker = '(++)'
        elif new_rating < self.rank:
            self.rating_marker = '(--)'
        else:
            self.rating_marker = ""

    def __str__(self):
        template = "%3d %4s,%-30s, %2.3f, %7d"
        return template % (self.rank, self.rank_marker,
                           self.name, self.rating, self.votes)



def main():
    target_url = "https://boardgamegeek.com/browse/boardgame"
    # with request.urlopen(target_url) as resp:
    #     with tempfile.NamedTemporaryFile(delete=False) as fil:
    #         shutil.copyfileobj(resp, fil)
    #         filename = fil.name

    target_lines = open("target.html").readlines()[274:]
    target_lines = [line.strip().replace('\t', '') for line in target_lines if len(line.strip()) > 0]
    rows = []
    append = False
    for idx, line in enumerate(target_lines):
        if line.startswith("<tr id='row_'>"):
            append = True
            row = []
        if append:
            row.append(line)
        if line.startswith("</tr>") and append is True:
            append = False
            rows.append(row)

    keys, names = fetch_names(rows)
    elements = list(zip(fetch_ranks(rows), names, fetch_description(rows), fetch_image_links(rows),
                        fetch_rating(rows), fetch_votes(rows)))
    elements = [BGGRow(rank, name, description, image_link, rating, votes) for rank, name, description, image_link, rating, votes in elements]
    data = dict(zip(keys, elements))
    print(data)
    for k,e in data.items():
        if e.rank <= 3:
            print(k)
            print(e)

    with open("target.pickle", 'wb') as fil:
        pickle.dump(data, fil)


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


def fetch_names(rows):
    name_lines = [line[13] for line in rows]
    name_regex = re.compile(r'href="(.*)".*>(.*)</a>')
    tuples = [name_regex.findall(line) for line in name_lines]
    dd = reduce(lambda l1, l2: l1 + l2, tuples)
    return zip(*dd)


if __name__ == '__main__':
    main()


# def main_soup():
#     target_url = "https://boardgamegeek.com/browse/boardgame"
#     html_text = requests.get(target_url).text
#     soup = BeautifulSoup(html_text, 'html.parser')
#     rs = [child for row in soup.find_all(id='row_')[:] for child in row.children]
#     print(rs)
