import shutil
import tempfile

import requests
from bs4 import BeautifulSoup
from urllib import request, response
from functools import reduce

import re


def main_soup():
    target_url = "https://boardgamegeek.com/browse/boardgame"
    html_text = requests.get(target_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    rs = [child for row in soup.find_all(id='row_')[:] for child in row.children]
    print(rs)


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

    fetch_names(rows)
    fetch_ranks(rows)
    fetch_description(rows)
    fetch_rating(rows)
    fetch_votes(rows)

    # for idx, r in enumerate(rows[1]):
    #     print("%2d:%s" % (idx, r))
    # print(rows[1])


def fetch_rating(rows):
    rating_regex = re.compile('(\d+.\d+)')
    rating = [rating_regex.findall(r[21])[0] for r in rows]
    print(rating)


def fetch_votes(rows):
    vote_regex = re.compile('(\d+)')
    votes = [vote_regex.findall(r[25])[0] for r in rows]
    print(votes)


def fetch_description(rows):
    description = [r[17] for r in rows]
    print(description)


def fetch_ranks(rows):
    rank_regex = re.compile(r'.*name="(\d+)">')
    ranks = [rank_regex.findall(r[2])[0] for r in rows]
    print(ranks)


def fetch_names(rows):
    name_lines = [line[13] for line in rows]
    print(name_lines[0])
    name_regex = re.compile(r'href="(.*)".*>(.*)</a>')
    tuples = [name_regex.findall(line) for line in name_lines]
    dd = reduce(lambda l1, l2: l1 + l2, tuples)
    d = dict(dd)
    print(d)


if __name__ == '__main__':
    main()
