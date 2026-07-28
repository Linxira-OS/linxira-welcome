import ast
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).parents[1]


class AboutMetadataTests(unittest.TestCase):
    def test_about_surface_and_appstream_urls(self):
        source = (ROOT / "src/linxira-welcome").read_text(encoding="utf-8")
        self.assertIn('"about_details"', source)
        self.assertIn("Linxira OS contributors", source)
        self.assertIn("MIT License", source)
        tree = ast.parse(source)
        self.assertIsNotNone(tree)

        component = ET.parse(ROOT / "data/org.linxira.Welcome.metainfo.xml").getroot()
        urls = {node.attrib["type"]: node.text for node in component.findall("url")}
        self.assertEqual(set(urls), {"homepage", "vcs-browser", "bugtracker", "help"})
        self.assertEqual(urls["vcs-browser"], "https://github.com/Linxira-OS/linxira-welcome")
        self.assertEqual(urls["bugtracker"], urls["vcs-browser"] + "/issues")


if __name__ == "__main__":
    unittest.main()
