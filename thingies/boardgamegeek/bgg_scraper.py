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
    rs = [child  for row in soup.find_all(id='row_')[:] for child in row.children]
    print(rs)

def main():
    target_url = "https://boardgamegeek.com/browse/boardgame"
    # with request.urlopen(target_url) as resp:
    #     with tempfile.NamedTemporaryFile(delete=False) as fil:
    #         shutil.copyfileobj(resp, fil)
    #         filename = fil.name

    # with open(filename) as html:
    #     lines = html.readlines()
    #     print(len(lines))
    # <a href="/boardgame/161936/pandemic-legacy-season-1" class="primary">Pandemic Legacy: Season 1</a>
    # Pandemic Legacy: Season 1
    # /html/body/div[2]/main/div/div[1]/div[1]/div/div/div[2]/div[3]/table/tbody/tr[3]/td[3]/div[2]/a

    # <div id="results_objectname2" style="z-index:1000;" onclick="">
    # <a href="/boardgame/161936/pandemic-legacy-season-1" class="primary">Pandemic Legacy: Season 1</a>
    # <span class="smallerfont dull">(2015)</span>
    # </div>
    # name_regex = re.compile('<div id="results_objectname.*</div>"')
    # print(name_regex.search(target_lines))
    # name_lines = name_regex.findall(target_lines)
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

    name_lines = [line for line in target_lines if line.strip().startswith('<a  href="/boardgame/')]
    print(name_lines[0])
    name_regex = re.compile(r'href="(.*)".*>(.*)</a>')
    tuples = [name_regex.findall(line) for line in name_lines]
    dd = reduce(lambda l1, l2: l1 + l2, tuples)
    d = dict(dd)
    print(d)
    print(rows[0])
    for idx, r in enumerate(rows[1]):
        print("%2d:%s" % (idx,r))
    # print(rows[1])

if __name__ == '__main__':
    main()