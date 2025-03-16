import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("h1","Header text")
        expected = "HTMLNode(h1, Header text, None, None)"
        self.assertEqual(str(node), expected)

    def test_empty(self):
        node = HTMLNode()
        expected = "HTMLNode(None, None, None, None)"
        self.assertEqual(str(node), expected)
    
    def test_props_to_html(self):
        node = HTMLNode("a","Link text", props={"href": "https://www.test.com", "target": "_blank"})
        expected = " href=\"https://www.test.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), expected)

if __name__ == "__main__":
    unittest.main()