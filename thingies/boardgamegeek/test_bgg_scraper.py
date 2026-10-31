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

    def _create_mock_response(self, content_bytes, status_code=200):
        if isinstance(content_bytes, str):
            content_bytes = content_bytes.encode("utf-8")
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.content = content_bytes
        mock_resp.text = content_bytes.decode("utf-8", errors="ignore")
        return mock_resp

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_via_impersonation_default_url(self, mock_get):
        sample_html = '<html><a href="/boardgame/224517/brass"></a><a href="/boardgame/342942/ark"></a><a href="/boardgame/161936/pandemic"></a></html>'
        mock_get.return_value = self._create_mock_response(sample_html)

        ids = bgg_scraper.fetch_top100_via_impersonation()

        self.assertEqual(["224517", "342942", "161936"], ids)
        mock_get.assert_called_once_with(bgg_scraper.browse_url, impersonate="chrome")

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_from_xml(self, mock_get):
        sample_xml = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<items>\n'
            '    <item id="101" objecttype="thing" subtype="boardgame" objectid="224517" objectname="Brass: Birmingham" />\n'
            '    <item id="102" objecttype="thing" subtype="boardgame" objectid="342942" objectname="Ark Nova" />\n'
            '    <item id="103" objecttype="thing" subtype="boardgame" objectid="161936" objectname="Pandemic Legacy: Season 1" />\n'
            '</items>'
        )
        mock_get.return_value = self._create_mock_response(sample_xml)

        ids = bgg_scraper.fetch_top100(url="https://example.com/items.xml")

        self.assertEqual(["224517", "342942", "161936"], ids)
        mock_get.assert_called_once_with("https://example.com/items.xml", impersonate="chrome")

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_from_csv_dump(self, mock_get):
        sample_csv = (
            "id,name,yearpublished,rank,bayesaverage,average,usersrated,is_expansion\n"
            "174430,Gloomhaven,2017,1,8.566,8.8,37789,0\n"
            "161936,Pandemic Legacy: Season 1,2015,2,8.455,8.6,35000,0\n"
            "999999,Some Expansion,2020,3,8.400,8.5,1000,1\n"
            "224517,Brass: Birmingham,2018,4,8.390,8.7,40000,0\n"
        )
        mock_get.return_value = self._create_mock_response(sample_csv)

        ids = bgg_scraper.fetch_top100(url="https://example.com/ranks.csv")

        self.assertEqual(["174430", "161936", "224517"], ids)

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_from_zip_dump(self, mock_get):
        sample_csv = (
            "id,name,yearpublished,rank,bayesaverage,average,usersrated,is_expansion\n"
            "224517,Brass: Birmingham,2018,1,8.390,8.7,40000,0\n"
            "342942,Ark Nova,2021,2,8.355,8.6,38000,0\n"
        )
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("boardgames_ranks_2026-10-22.csv", sample_csv)
        zip_bytes = buf.getvalue()

        mock_get.return_value = self._create_mock_response(zip_bytes)

        ids = bgg_scraper.fetch_top100(url="https://example.com/ranks.zip")

        self.assertEqual(["224517", "342942"], ids)

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_from_gzip_dump(self, mock_get):
        sample_csv = (
            "id,name,rank\n"
            "1001,Game A,1\n"
            "1002,Game B,2\n"
        )
        gz_bytes = gzip.compress(sample_csv.encode("utf-8"))
        mock_get.return_value = self._create_mock_response(gz_bytes)

        ids = bgg_scraper.fetch_top100(url="https://example.com/ranks.csv.gz")

        self.assertEqual(["1001", "1002"], ids)

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_limits_and_sorts_by_rank(self, mock_get):
        rows = ["id,name,rank\n"]
        # Generate out of order ranks up to 150
        for r in range(150, 0, -1):
            rows.append(f"{r + 1000},Game {r},{r}\n")
        sample_csv = "".join(rows)

        mock_get.return_value = self._create_mock_response(sample_csv)

        ids = bgg_scraper.fetch_top100(url="https://example.com/ranks.csv")

        self.assertEqual(bgg_scraper.top_ranks, len(ids))
        self.assertEqual("1001", ids[0])  # rank 1
        self.assertEqual("1100", ids[-1])  # rank 100

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_saves_to_file(self, mock_get):
        sample_csv = "id,name,rank\n101,A,1\n102,B,2\n103,C,3\n"
        mock_get.return_value = self._create_mock_response(sample_csv)

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            ids = bgg_scraper.fetch_top100_via_impersonation(top100_file=tmp_path)
            self.assertEqual(["101", "102", "103"], ids)
            with open(tmp_path, "r") as f:
                content = f.read()
            self.assertEqual("101\n102\n103\n", content)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_saves_to_default_latest_top100(self, mock_get):
        sample_csv = "id,name,rank\n101,A,1\n102,B,2\n"
        mock_get.return_value = self._create_mock_response(sample_csv)

        default_file = "latest-top100"
        backup_content = None
        if os.path.exists(default_file):
            with open(default_file, "r") as f:
                backup_content = f.read()

        try:
            ids = bgg_scraper.fetch_top100_via_impersonation()
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

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_does_not_save_when_unsuccessful(self, mock_get):
        mock_get.side_effect = Exception("Network timeout")

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
            tmp_path = tmp_file.name
            tmp_file.write("existing_data\n")

        try:
            ids = bgg_scraper.fetch_top100_via_impersonation(top100_file=tmp_path)
            self.assertEqual([], ids)
            with open(tmp_path, "r") as f:
                content = f.read()
            self.assertEqual("existing_data\n", content)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_non_200_status(self, mock_get):
        mock_get.return_value = self._create_mock_response("Forbidden", status_code=403)

        ids = bgg_scraper.fetch_top100_via_impersonation()
        self.assertEqual([], ids)

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_positional_file_arg(self, mock_get):
        sample_csv = "id,name,rank\n500,Game,1\n"
        mock_get.return_value = self._create_mock_response(sample_csv)

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

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_handles_network_error(self, mock_get):
        mock_get.side_effect = Exception("Connection refused")

        ids = bgg_scraper.fetch_top100_via_impersonation()

        self.assertEqual([], ids)

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_custom_url(self, mock_get):
        custom_url = "https://example.com/custom_dump.csv"
        mock_get.return_value = self._create_mock_response("id,name,rank\n999,Test,1\n")

        ids = bgg_scraper.fetch_top100_via_impersonation(url=custom_url)

        self.assertEqual(["999"], ids)
        mock_get.assert_called_once_with(custom_url, impersonate="chrome")

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_empty_content(self, mock_get):
        mock_get.return_value = self._create_mock_response("")

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            ids = bgg_scraper.fetch_top100_via_impersonation(top100_file=tmp_path)
            self.assertEqual([], ids)
            with open(tmp_path, "r") as f:
                content = f.read()
            self.assertEqual("", content)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    @patch("curl_cffi.requests.get")
    def test_fetch_top100_with_target_html_fixture(self, mock_get):
        target_html_path = os.path.join(pkg_dir, "target.html")
        if not os.path.exists(target_html_path):
            self.skipTest("target.html fixture not found")

        with open(target_html_path, "r", encoding="utf-8") as f:
            target_html_content = f.read()

        mock_get.return_value = self._create_mock_response(target_html_content)

        ids = bgg_scraper.fetch_top100_via_impersonation()

        self.assertEqual(100, len(ids))
        self.assertEqual("174430", ids[0])
        self.assertEqual("161936", ids[1])
        self.assertEqual("224517", ids[2])
        self.assertEqual("167791", ids[3])


class TestHTMLAndCSS(unittest.TestCase):

    def test_rank_range_calculation(self):
        self.assertEqual((1, 100), bgg_scraper.rank_range(1))
        self.assertEqual((1, 100), bgg_scraper.rank_range(50))
        self.assertEqual((1, 100), bgg_scraper.rank_range(100))
        self.assertEqual((101, 200), bgg_scraper.rank_range(101))
        self.assertEqual((101, 200), bgg_scraper.rank_range(200))
        self.assertEqual((201, 300), bgg_scraper.rank_range(201))
        self.assertEqual((201, 300), bgg_scraper.rank_range(300))
        self.assertEqual((301, 400), bgg_scraper.rank_range(301))
        self.assertEqual((901, 1000), bgg_scraper.rank_range(1000))
        self.assertEqual((1001, 1100), bgg_scraper.rank_range(1001))

        self.assertEqual("1-100", bgg_scraper.rank_range_str(1))
        self.assertEqual("1-100", bgg_scraper.rank_range_str(100))
        self.assertEqual("101-200", bgg_scraper.rank_range_str(101))
        self.assertEqual("201-300", bgg_scraper.rank_range_str(201))

    def test_image_attributes_in_html_row(self):
        row = bgg_scraper.BGGRow(
            rank=1,
            name="Brass: Birmingham",
            year="(2018)",
            description="Economic strategy game",
            image_link="https://example.com/brass.jpg",
            rating="8.390",
            votes="60000"
        )
        html_str = row.html_str()
        self.assertIn('class="image"', html_str)

    def test_write_html_table_adds_headers_for_each_100_ranks(self):
        rows = [
            bgg_scraper.BGGRow(1, "Game 1", "(2020)", "Desc 1", "img1.jpg", "8.5", "1000"),
            bgg_scraper.BGGRow(50, "Game 50", "(2020)", "Desc 50", "img50.jpg", "8.2", "800"),
            bgg_scraper.BGGRow(100, "Game 100", "(2020)", "Desc 100", "img100.jpg", "8.0", "700"),
            bgg_scraper.BGGRow(105, "Game 105", "(2020)", "Desc 105", "img105.jpg", "7.9", "600"),
            bgg_scraper.BGGRow(180, "Game 180", "(2020)", "Desc 180", "img180.jpg", "7.8", "500"),
            bgg_scraper.BGGRow(320, "Game 320", "(2020)", "Desc 320", "img320.jpg", "7.5", "400"),
        ]
        buf = io.StringIO()
        bgg_scraper.write_html_table(buf, "Test Rankings", rows)
        content = buf.getvalue()

        # Should contain the section title
        self.assertIn("<h2>Test Rankings</h2>", content)

        # Should contain rank range headers for ranges with games present
        self.assertIn("<h3>1-100</h3>", content)
        self.assertIn("<h3>101-200</h3>", content)
        self.assertIn("<h3>301-400</h3>", content)
        # Should not contain rank range header for range without games
        self.assertNotIn("<h3>201-300</h3>", content)

        # Count how many table headers (thead) are emitted:
        # 1-100 (contains 1, 50, 100) -> header 1
        # 101-200 (contains 105, 180) -> header 2
        # 201-300 (no games) -> no header
        # 301-400 (contains 320) -> header 3
        # Total table headers should be exactly 3
        table_count = content.count('<table class="zui-table">')
        self.assertEqual(3, table_count)
        thead_count = content.count('<thead>')
        self.assertEqual(3, thead_count)

    def test_write_html_multiple_sections(self):
        data = {
            "/boardgame/1": bgg_scraper.BGGRow(1, "Top Game", "(2021)", "Top", "top.jpg", "8.5", "1000"),
            "/boardgame/2": bgg_scraper.BGGRow(150, "Watchlist Game", "(2021)", "Watch", "watch.jpg", "7.5", "500"),
        }
        outdated = [
            bgg_scraper.BGGRow(200, "Old Game", "(2010)", "Old", "old.jpg", "7.0", "200")
        ]
        buf = io.StringIO()
        bgg_scraper.write_html(buf, data, outdated)
        content = buf.getvalue()

        self.assertIn("<h2>Top 100</h2>", content)
        self.assertIn("<h3>1-100</h3>", content)
        self.assertIn("<h2>Watchlist</h2>", content)
        self.assertIn("<h3>101-200</h3>", content)
        self.assertIn("<h2>Outdated</h2>", content)
        self.assertIn("<h3>101-200</h3>", content)
        self.assertIn('<img src="bgg_logo.jpg">', content)

    def test_bgg_logo_at_bottom_of_page(self):
        buf = io.StringIO()
        bgg_scraper.write_html(buf, {}, [])
        content = buf.getvalue()
        self.assertIn('<img src="bgg_logo.jpg">', content)
        # Ensure it appears towards the end of the HTML output
        self.assertTrue(content.find('<img src="bgg_logo.jpg">') > content.find('<body>'))
        self.assertTrue(content.find('<img src="bgg_logo.jpg">') < content.find('</html>'))

    def test_css_hover_enlarged_image_rules(self):
        css_path = os.path.join(pkg_dir, "table.css")
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        self.assertIn(".image:hover", css_content)
        self.assertIn("transform:", css_content)
        self.assertIn("max-width: 90px", css_content)
        self.assertIn("h2, h3", css_content)

    def test_css_description_tooltip_rules(self):
        css_path = os.path.join(pkg_dir, "table.css")
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        self.assertIn(".tooltip .tooltiptext", css_content)
        self.assertIn(".tooltip:hover", css_content)
        self.assertIn("z-index: 10000", css_content)
        self.assertIn("background-color: black", css_content)
        self.assertIn("max-width:", css_content)
        self.assertIn("white-space: pre-wrap", css_content)
        self.assertIn("word-wrap: break-word", css_content)
        self.assertIn("text-align: left", css_content)

    def test_css_table_layout_and_column_alignment_rules(self):
        css_path = os.path.join(pkg_dir, "table.css")
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        self.assertIn("table-layout: fixed", css_content)
        self.assertIn(".zui-table thead th:nth-child(1)", css_content)
        self.assertIn(".zui-table thead th:nth-child(2)", css_content)
        self.assertIn(".zui-table thead th:nth-child(3)", css_content)
        self.assertIn(".zui-table thead th:nth-child(4)", css_content)
        self.assertIn(".zui-table thead th:nth-child(5)", css_content)
        self.assertIn("text-align: left", css_content)

    def test_css_table_font_size_and_min_width(self):
        css_path = os.path.join(pkg_dir, "table.css")
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        # Verify larger font size (20px)
        self.assertIn("20px", css_content)
        # Verify table fills at least 75% of width
        self.assertIn("min-width: 75%", css_content)
        self.assertIn("width: 75%", css_content)
        # Verify row heights / padding extended
        self.assertIn("padding: 12px 10px", css_content)

    def test_bggrow_html_str_row_tag(self):
        row = bgg_scraper.BGGRow(
            rank=1,
            name="Brass: Birmingham",
            year="(2018)",
            description="Strategy game",
            image_link="brass.jpg",
            rating="8.390",
            votes="60000"
        )
        html_str = row.html_str()
        self.assertTrue(html_str.startswith("<tr>"))
        self.assertNotIn('<tr"', html_str)


class TestCleanDescription(unittest.TestCase):

    def test_remove_publisher_description_variants(self):
        cases = [
            ("Game summary.\n\n—description from the publisher", "Game summary."),
            ("Game summary.\n\n— description from the publisher\n\n", "Game summary."),
            ("Game summary.\n\n-description from the publisher", "Game summary."),
            ("Game summary.\n\n--description from the publisher", "Game summary."),
            ("Game summary.\n\n—description from publisher", "Game summary."),
            ("Game summary.\n\n-description from publisher", "Game summary."),
            ("Game summary.\n\n—description from the publisher (German)", "Game summary."),
            ("Game summary.\n\n—description from the publisher (translated).", "Game summary."),
            ("Game summary.\n\n- from the publisher's website", "Game summary."),
            ("Game summary.\n\nDescription from the publisher:", "Game summary."),
        ]
        for input_desc, expected in cases:
            self.assertEqual(expected, bgg_scraper.clean_description(input_desc))

    def test_clean_description_preserves_regular_text(self):
        desc = "A thrilling adventure across multiple scenarios."
        self.assertEqual(desc, bgg_scraper.clean_description(desc))

    def test_clean_description_empty_and_none(self):
        self.assertEqual("", bgg_scraper.clean_description(""))
        self.assertEqual("", bgg_scraper.clean_description(None))

    def test_bggrow_html_str_removes_publisher_line(self):
        row = bgg_scraper.BGGRow(
            rank=1,
            name="Ark Nova",
            year="(2021)",
            description="In Ark Nova, you will plan and design a modern zoo.\n\n—description from the publisher\n\n",
            image_link="ark_nova.jpg",
            rating="8.355",
            votes="60000"
        )
        html_str = row.html_str()
        self.assertNotIn("—description from the publisher", html_str)
        self.assertNotIn("description from the publisher", html_str)
        self.assertIn("In Ark Nova, you will plan and design a modern zoo.", html_str)


class TestDesignerTooltipAndParsing(unittest.TestCase):

    def test_bggrow_tooltip_text_with_designer(self):
        row = bgg_scraper.BGGRow(
            rank=1,
            name="Brass: Birmingham",
            year="(2018)",
            description="Brass: Birmingham is an economic strategy game.",
            image_link="brass.jpg",
            rating="8.390",
            votes="60000",
            designer="Gavan Brown, Matt Tolman, Martin Wallace"
        )
        tooltip = row.tooltip_text()
        self.assertTrue(tooltip.startswith("Designer: Gavan Brown, Matt Tolman, Martin Wallace\n\n"))
        self.assertIn("Brass: Birmingham is an economic strategy game.", tooltip)

        html_str = row.html_str()
        self.assertIn("Designer: Gavan Brown, Matt Tolman, Martin Wallace\n\nBrass: Birmingham is an economic strategy game.", html_str)

    def test_bggrow_tooltip_text_without_designer(self):
        row = bgg_scraper.BGGRow(
            rank=2,
            name="Mystery Game",
            year="(2020)",
            description="A game without known designer.",
            image_link="mystery.jpg",
            rating="7.5",
            votes="1000",
            designer=""
        )
        self.assertEqual("A game without known designer.", row.tooltip_text())

    def test_bggrow_tooltip_text_already_prefixed_designer(self):
        row = bgg_scraper.BGGRow(
            rank=3,
            name="Card Game",
            year="(2022)",
            description="Fun card game.",
            image_link="card.jpg",
            rating="8.0",
            votes="2000",
            designer="Designer: Jane Doe"
        )
        self.assertEqual("Designer: Jane Doe\n\nFun card game.", row.tooltip_text())

    def test_bggrow_update_preserves_and_updates_designer(self):
        row1 = bgg_scraper.BGGRow(
            rank=1,
            name="Game",
            year="(2020)",
            description="Old desc",
            image_link="img.jpg",
            rating="8.0",
            votes="1000"
        )
        row2 = bgg_scraper.BGGRow(
            rank=1,
            name="Game",
            year="(2020)",
            description="New desc",
            image_link="img.jpg",
            rating="8.1",
            votes="1100",
            designer="Famous Designer"
        )
        row1.update(row2)
        self.assertEqual("Famous Designer", row1.designer)
        self.assertTrue(row1.tooltip_text().startswith("Designer: Famous Designer\n\n"))

    def test_parse_games_xmlapi2_designers(self):
        xml_content = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<items termsofuse="https://boardgamegeek.com/xmlapi/termsofuse">\n'
            '  <item type="boardgame" id="224517">\n'
            '    <name type="primary" value="Brass: Birmingham" />\n'
            '    <yearpublished value="2018" />\n'
            '    <description>Brass: Birmingham description.</description>\n'
            '    <thumbnail>https://example.com/brass.jpg</thumbnail>\n'
            '    <link type="boardgamedesigner" id="3307" value="Gavan Brown" />\n'
            '    <link type="boardgamedesigner" id="87740" value="Matt Tolman" />\n'
            '    <link type="boardgamedesigner" id="429" value="Martin Wallace" />\n'
            '    <link type="boardgameartist" id="1" value="Some Artist" />\n'
            '    <statistics page="1">\n'
            '      <ratings>\n'
            '        <usersrated value="60000" />\n'
            '        <bayesaverage value="8.390" />\n'
            '        <ranks>\n'
            '          <rank type="subtype" id="1" name="boardgame" value="1" />\n'
            '        </ranks>\n'
            '      </ratings>\n'
            '    </statistics>\n'
            '  </item>\n'
            '</items>'
        )
        from xml.etree import ElementTree
        root = ElementTree.fromstring(xml_content)
        games = bgg_scraper.parse_games(root)

        self.assertIn("/boardgame/224517", games)
        game_row = games["boardgame/224517" if "boardgame/224517" in games else "/boardgame/224517"]
        self.assertEqual("Gavan Brown, Matt Tolman, Martin Wallace", game_row.designer)
        self.assertTrue(game_row.tooltip_text().startswith("Designer: Gavan Brown, Matt Tolman, Martin Wallace\n\n"))

    def test_parse_games_xmlapi1_designers(self):
        xml_content = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<boardgames termsofuse="https://boardgamegeek.com/xmlapi/termsofuse">\n'
            '  <boardgame objectid="174430">\n'
            '    <name primary="true">Gloomhaven</name>\n'
            '    <yearpublished>2017</yearpublished>\n'
            '    <description>Gloomhaven description.</description>\n'
            '    <thumbnail>https://example.com/gloom.jpg</thumbnail>\n'
            '    <boardgamedesigner objectid="69802">Isaac Childres</boardgamedesigner>\n'
            '    <statistics page="1">\n'
            '      <ratings>\n'
            '        <usersrated>68000</usersrated>\n'
            '        <bayesaverage>8.288</bayesaverage>\n'
            '        <ranks>\n'
            '          <rank type="subtype" id="1" name="boardgame" value="4" />\n'
            '        </ranks>\n'
            '      </ratings>\n'
            '    </statistics>\n'
            '  </boardgame>\n'
            '</boardgames>'
        )
        from xml.etree import ElementTree
        root = ElementTree.fromstring(xml_content)
        games = bgg_scraper.parse_games(root)

        self.assertIn("/boardgame/174430", games)
        game_row = games["/boardgame/174430"]
        self.assertEqual("Isaac Childres", game_row.designer)
        self.assertTrue(game_row.tooltip_text().startswith("Designer: Isaac Childres\n\n"))


class TestWriteFileAndPlainTextOutput(unittest.TestCase):

    def test_write_file_table_adds_headers_for_each_100_ranks(self):
        rows = [
            bgg_scraper.BGGRow(1, "Game 1", "(2020)", "Desc 1", "img1.jpg", "8.5", "1000"),
            bgg_scraper.BGGRow(50, "Game 50", "(2020)", "Desc 50", "img50.jpg", "8.2", "800"),
            bgg_scraper.BGGRow(100, "Game 100", "(2020)", "Desc 100", "img100.jpg", "8.0", "700"),
            bgg_scraper.BGGRow(105, "Game 105", "(2020)", "Desc 105", "img105.jpg", "7.9", "600"),
            bgg_scraper.BGGRow(180, "Game 180", "(2020)", "Desc 180", "img180.jpg", "7.8", "500"),
            bgg_scraper.BGGRow(320, "Game 320", "(2020)", "Desc 320", "img320.jpg", "7.5", "400"),
        ]
        buf = io.StringIO()
        bgg_scraper.write_file_table(buf, "Test Section", rows)
        content = buf.getvalue()

        # Should contain section title
        self.assertTrue(content.startswith("Test Section\n"))

        # Should contain rank range headers for ranges with games present
        self.assertIn("1-100\n", content)
        self.assertIn("101-200\n", content)
        self.assertIn("301-400\n", content)
        # Should not contain rank range header for range without games
        self.assertNotIn("201-300", content)

        # Check order of headers
        pos_title = content.find("Test Section")
        pos_100 = content.find("1-100")
        pos_200 = content.find("101-200")
        pos_400 = content.find("301-400")
        self.assertTrue(pos_title < pos_100 < pos_200 < pos_400)

    def test_write_file_multiple_sections(self):
        data = {
            "/boardgame/1": bgg_scraper.BGGRow(1, "Top Game", "(2021)", "Top", "top.jpg", "8.5", "1000"),
            "/boardgame/2": bgg_scraper.BGGRow(150, "Watchlist Game", "(2021)", "Watch", "watch.jpg", "7.5", "500"),
        }
        outdated = [
            bgg_scraper.BGGRow(200, "Old Game", "(2010)", "Old", "old.jpg", "7.0", "200")
        ]
        buf = io.StringIO()
        bgg_scraper.write_file(buf, data, outdated)
        content = buf.getvalue()

        self.assertIn("Top 100\n", content)
        self.assertIn("1-100\n", content)
        self.assertIn("Watchlist\n", content)
        self.assertIn("101-200\n", content)
        self.assertIn("Outdated\n", content)
        self.assertIn("101-200\n", content)

        # Verify games are listed under appropriate sections
        pos_top = content.find("Top 100")
        pos_top_game = content.find("Top Game")
        pos_watch = content.find("Watchlist")
        pos_watch_game = content.find("Watchlist Game")
        pos_outdated = content.find("Outdated")
        pos_old_game = content.find("Old Game")

        self.assertTrue(pos_top < pos_top_game < pos_watch < pos_watch_game < pos_outdated < pos_old_game)

    def test_write_file_equivalence_with_write_html_sections_and_ranges(self):
        data = {
            "/boardgame/1": bgg_scraper.BGGRow(1, "Top Game", "(2021)", "Top", "top.jpg", "8.5", "1000"),
            "/boardgame/150": bgg_scraper.BGGRow(150, "Watchlist 1", "(2021)", "W1", "w1.jpg", "7.5", "500"),
            "/boardgame/250": bgg_scraper.BGGRow(250, "Watchlist 2", "(2021)", "W2", "w2.jpg", "7.2", "300"),
        }
        outdated = [
            bgg_scraper.BGGRow(500, "Old Game", "(2010)", "Old", "old.jpg", "7.0", "200")
        ]
        text_buf = io.StringIO()
        html_buf = io.StringIO()

        bgg_scraper.write_file(text_buf, data, outdated)
        bgg_scraper.write_html(html_buf, data, outdated)

        text_content = text_buf.getvalue()
        html_content = html_buf.getvalue()

        # Both have Top 100 and 1-100
        self.assertIn("Top 100", text_content)
        self.assertIn("<h2>Top 100</h2>", html_content)
        self.assertIn("1-100", text_content)
        self.assertIn("<h3>1-100</h3>", html_content)

        # Both have Watchlist and 101-200, 201-300
        self.assertIn("Watchlist", text_content)
        self.assertIn("<h2>Watchlist</h2>", html_content)
        self.assertIn("101-200", text_content)
        self.assertIn("<h3>101-200</h3>", html_content)
        self.assertIn("201-300", text_content)
        self.assertIn("<h3>201-300</h3>", html_content)

        # Both have Outdated and 401-500
        self.assertIn("Outdated", text_content)
        self.assertIn("<h2>Outdated</h2>", html_content)
        self.assertIn("401-500", text_content)
        self.assertIn("<h3>401-500</h3>", html_content)

    def test_write_file_empty(self):
        buf = io.StringIO()
        bgg_scraper.write_file(buf, {}, [])
        self.assertEqual("", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
