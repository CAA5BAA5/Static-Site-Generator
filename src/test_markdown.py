import unittest

from markdown import split_nodes_delimiter
from textnode import TextNode, TextType

class TestMarkdown(unittest.TestCase):
    def test_to_html_with_children(self):
        sample_text = "This is text with a `code block` word"
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([sample_text], "`", TextType.CODE), expected)

        sample_text = "This is text with a <italic block< word"
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([sample_text], "<", TextType.ITALIC), expected)

    if __name__ == "__main__":
        unittest.main()