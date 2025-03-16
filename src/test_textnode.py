import unittest

from textnode import TextNode, TextType ,text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_str(self):
        node = TextNode("Text", TextType.IMAGE, "Link")
        expected_str = f"TextNode(Text, {TextType.IMAGE.value}, Link)"
        self.assertEqual(str(node), expected_str)

    def test_incomplete_constructor(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node,node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node!", TextType.BOLD)
        self.assertNotEqual(node,node2)
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node,node2)
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "")
        self.assertNotEqual(node,node2)

    def test_convert_to_htmlnode(self):
        #TEXT
        test_string = "This is a text node"
        node = text_node_to_html_node(TextNode(test_string, TextType.TEXT))
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, test_string)

        #BOLD = "Bold"
        test_string = "This is a bold node"
        node = text_node_to_html_node(TextNode(test_string, TextType.BOLD))
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.value, test_string)
        self.assertEqual(node.to_html(), "<b>This is a bold node</b>")

        #ITALIC = "Italic"
        test_string = "This is an italic node"
        node = text_node_to_html_node(TextNode(test_string, TextType.ITALIC))
        self.assertEqual(node.tag, "i")
        self.assertEqual(node.value, test_string)
        self.assertEqual(node.to_html(), "<i>This is an italic node</i>")

        #CODE = "Code"
        test_string = "This is a code node"
        node = text_node_to_html_node(TextNode(test_string, TextType.CODE))
        self.assertEqual(node.tag, "code")
        self.assertEqual(node.value, test_string)
        self.assertEqual(node.to_html(), "<code>This is a code node</code>")

        #LINK = "Link"
        test_string = "This is a link node"
        node = text_node_to_html_node(TextNode(test_string, TextType.LINK, "https://test.com"))
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, test_string)
        self.assertEqual(node.props, {"href": "https://test.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://test.com\">This is a link node</a>")

        #IMAGE = "Image"
        test_string = "This is an image node"
        node = text_node_to_html_node(TextNode(test_string, TextType.IMAGE, "../image.jpeg"))
        self.assertEqual(node.tag, "img")
        self.assertEqual(node.value, "")
        self.assertEqual(node.props, {"src": "../image.jpeg", "alt": "This is an image node"})
        self.assertEqual(node.to_html(), "<img src=\"../image.jpeg\" alt=\"This is an image node\"></img>")


if __name__ == "__main__":
    unittest.main()