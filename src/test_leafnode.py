import unittest

from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node = LeafNode("a", "Link", {"href":"https://test.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://test.com\">Link</a>")
    
    def test_repr(self):
        node = LeafNode("a", "Link", {"href":"https://test.com"})
        expected = "LeafNode(a, Link, {'href': 'https://test.com'})"
        self.assertEqual(str(node), expected)
    



if __name__ == "__main__":
    unittest.main()