#!/usr/bin/env python3
import gzip
import io
import os
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import MagicMock, patch
from urllib.error import URLError

# Ensure module can be imported whether run from root or subfolder
pkg_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(pkg_dir, "..", ".."))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from thingies.boardgamegeek import bgg_scraper
except ImportError:
    import bgg_scraper


class TestFetchTop100(unittest.TestCase):

    def setUp(self):
        self.default_top100 = "latest-top100"
        self._had_top100 = os.path.exists(self.default_top100)
        self._top100_content = None
        if self._had_top100:
            with open(self.default_top100, "r") as f:
                self._top100_content = f.read()

    def tearDown(self):
        if self._had_top100:
            with open(self.default_top100, "w") as f:
                f.write(self._top100_content)
        elif os.path.exists(self.default_top100):
            os.remove(self.default_top100)

    def _create_mock_response(self, content_bytes):
        if isinstance(content_bytes, str):
            content_bytes = content_bytes.encode("utf-8")
        mock_resp = MagicMock()
        mock_resp.read.return_value = content_bytes
        mock_resp.__enter__.return_value = mock_resp
        return mock_resp

    @patch("urllib.request.urlopen")
    def test_fetch_top100_from_geeklist_xml(self, mock_urlopen):
        sample_xml = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<geeklist id="271616" termsofuse="https://boardgamegeek.com/xmlapi/termsofuse">\n'
            '    <item id="101" objecttype="thing" subtype="boardgame" objectid="224517" objectname="Brass: Birmingham" />\n'
            '    <item id="102" objecttype="thing" subtype="boardgame" objectid="342942" objectname="Ark Nova" />\n'
            '    <item id="103" objecttype="thing" subtype="boardgame" objectid="161936" objectname="Pandemic Legacy: Season 1" />\n'
            '</geeklist>'
        )
        mock_urlopen.return_value = self._create_mock_response(sample_xml)

        ids = bgg_scraper.fetch_top100()

        self.assertEqual(["224517", "342942", "161936"], ids)
        called_req = mock_urlopen.call_args[0][0]
        self.assertEqual(bgg_scraper.geeklist_url, called_req.full_url)

    @patch("urllib.request.urlopen")
    def test_fetch_top100_with_geeklist_id(self, mock_urlopen):
        sample_xml = (
            '<geeklist id="99999">\n'
            '    <item id="1" objectid="174430" objectname="Gloomhaven" />\n'
            '</geeklist>'
        )
        mock_urlopen.return_value = self._create_mock_response(sample_xml)

        ids = bgg_scraper.fetch_top100(geeklist_id="99999")

        self.assertEqual(["174430"], ids)
        called_req = mock_urlopen.call_args[0][0]
        self.assertEqual("https://boardgamegeek.com/xmlapi/geeklist/99999", called_req.full_url)

    @patch("urllib.request.urlopen")
    def test_fetch_top100_from_csv_dump(self, mock_urlopen):
        sample_csv = (
            "id,name,yearpublished,rank,bayesaverage,average,usersrated,is_expansion\n"
            "174430,Gloomhaven,2017,1,8.566,8.8,37789,0\n"
            "161936,Pandemic Legacy: Season 1,2015,2,8.455,8.6,35000,0\n"
            "999999,Some Expansion,2020,3,8.400,8.5,1000,1\n"
            "224517,Brass: Birmingham,2018,4,8.390,8.7,40000,0\n"
        )
        mock_urlopen.return_value = self._create_mock_response(sample_csv)

        ids = bgg_scraper.fetch_top100()

        self.assertEqual(["174430", "161936", "224517"], ids)

    @patch("urllib.request.urlopen")
    def test_fetch_top100_from_zip_dump(self, mock_urlopen):
        sample_csv = (
            "id,name,yearpublished,rank,bayesaverage,average,usersrated,is_expansion\n"
            "224517,Brass: Birmingham,2018,1,8.390,8.7,40000,0\n"
            "342942,Ark Nova,2021,2,8.355,8.6,38000,0\n"
        )
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("boardgames_ranks_2026-10-22.csv", sample_csv)
        zip_bytes = buf.getvalue()

        mock_urlopen.return_value = self._create_mock_response(zip_bytes)

        ids = bgg_scraper.fetch_top100()

        self.assertEqual(["224517", "342942"], ids)

    @patch("urllib.request.urlopen")
    def test_fetch_top100_from_gzip_dump(self, mock_urlopen):
        sample_csv = (
            "id,name,rank\n"
            "1001,Game A,1\n"
            "1002,Game B,2\n"
        )
        gz_bytes = gzip.compress(sample_csv.encode("utf-8"))
        mock_urlopen.return_value = self._create_mock_response(gz_bytes)

        ids = bgg_scraper.fetch_top100()

        self.assertEqual(["1001", "1002"], ids)

    @patch("urllib.request.urlopen")
    def test_fetch_top100_limits_and_sorts_by_rank(self, mock_urlopen):
        rows = ["id,name,rank\n"]
        # Generate out of order ranks up to 150
        for r in range(150, 0, -1):
            rows.append(f"{r + 1000},Game {r},{r}\n")
        sample_csv = "".join(rows)

        mock_urlopen.return_value = self._create_mock_response(sample_csv)

        ids = bgg_scraper.fetch_top100()

        self.assertEqual(bgg_scraper.top_ranks, len(ids))
        self.assertEqual("1001", ids[0])  # rank 1
        self.assertEqual("1100", ids[-1])  # rank 100

    @patch("urllib.request.urlopen")
    def test_fetch_top100_saves_to_file(self, mock_urlopen):
        sample_csv = "id,name,rank\n101,A,1\n102,B,2\n103,C,3\n"
        mock_urlopen.return_value = self._create_mock_response(sample_csv)

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            ids = bgg_scraper.fetch_top100(top100_file=tmp_path)
            self.assertEqual(["101", "102", "103"], ids)
            with open(tmp_path, "r") as f:
                content = f.read()
            self.assertEqual("101\n102\n103\n", content)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    @patch("urllib.request.urlopen")
    def test_fetch_top100_saves_to_default_latest_top100(self, mock_urlopen):
        sample_csv = "id,name,rank\n101,A,1\n102,B,2\n"
        mock_urlopen.return_value = self._create_mock_response(sample_csv)

        default_file = "latest-top100"
        backup_content = None
        if os.path.exists(default_file):
            with open(default_file, "r") as f:
                backup_content = f.read()

        try:
            ids = bgg_scraper.fetch_top100()
            self.assertEqual(["101", "102"], ids)
            self.assertTrue(os.path.exists(default_file))
            with open(default_file, "r") as f:
                self.assertEqual("101\n102\n", f.read())
        finally:
            if backup_content is not None:
                with open(default_file, "w") as f:
                    f.write(backup_content)
            elif os.path.exists(default_file):
                os.remove(default_file)

    @patch("urllib.request.urlopen")
    def test_fetch_top100_does_not_save_when_unsuccessful(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("Network timeout")

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
            tmp_path = tmp_file.name
            tmp_file.write("existing_data\n")

        try:
            ids = bgg_scraper.fetch_top100(top100_file=tmp_path)
            self.assertEqual([], ids)
            with open(tmp_path, "r") as f:
                content = f.read()
            self.assertEqual("existing_data\n", content)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    @patch("urllib.request.urlopen")
    def test_fetch_top100_positional_file_arg(self, mock_urlopen):
        sample_csv = "id,name,rank\n500,Game,1\n"
        mock_urlopen.return_value = self._create_mock_response(sample_csv)

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            ids = bgg_scraper.fetch_top100(tmp_path)
            self.assertEqual(["500"], ids)
            with open(tmp_path, "r") as f:
                content = f.read()
            self.assertEqual("500\n", content)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_fetch_top100_from_local_file(self):
        sample_csv = "id,name,rank\n201,Game X,1\n202,Game Y,2\n"
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False) as src_file:
            src_file.write(sample_csv)
            src_path = src_file.name

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as out_file:
            out_path = out_file.name

        try:
            ids = bgg_scraper.fetch_top100(url=src_path, top100_file=out_path)
            self.assertEqual(["201", "202"], ids)
            with open(out_path, "r") as f:
                content = f.read()
            self.assertEqual("201\n202\n", content)
        finally:
            if os.path.exists(src_path):
                os.remove(src_path)
            if os.path.exists(out_path):
                os.remove(out_path)

    @patch("urllib.request.urlopen")
    def test_fetch_top100_handles_network_error(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("Connection refused")

        ids = bgg_scraper.fetch_top100()

        self.assertEqual([], ids)

    @patch("urllib.request.urlopen")
    def test_fetch_top100_custom_url(self, mock_urlopen):
        custom_url = "https://example.com/custom_dump.csv"
        mock_urlopen.return_value = self._create_mock_response("id,name,rank\n999,Test,1\n")

        ids = bgg_scraper.fetch_top100(url=custom_url)

        self.assertEqual(["999"], ids)
        called_req = mock_urlopen.call_args[0][0]
        self.assertEqual(custom_url, called_req.full_url)

    @patch("urllib.request.urlopen")
    def test_fetch_top100_empty_content(self, mock_urlopen):
        mock_urlopen.return_value = self._create_mock_response("")

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            ids = bgg_scraper.fetch_top100(top100_file=tmp_path)
            self.assertEqual([], ids)
            with open(tmp_path, "r") as f:
                content = f.read()
            self.assertEqual("", content)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    @patch("urllib.request.urlopen")
    def test_fetch_top100_with_target_html_fixture(self, mock_urlopen):
        target_html_path = os.path.join(pkg_dir, "target.html")
        if not os.path.exists(target_html_path):
            self.skipTest("target.html fixture not found")

        with open(target_html_path, "r", encoding="utf-8") as f:
            target_html_content = f.read()

        mock_urlopen.return_value = self._create_mock_response(target_html_content)

        ids = bgg_scraper.fetch_top100()

        self.assertEqual(100, len(ids))
        self.assertEqual("174430", ids[0])
        self.assertEqual("161936", ids[1])
        self.assertEqual("224517", ids[2])
        self.assertEqual("167791", ids[3])


if __name__ == "__main__":
    unittest.main()
