import unittest
import markdown
from textnode import TextNode, TextType

class TestMarkdown(unittest.TestCase):
    def test_to_html_with_children(self):
        sample_text = "This is text with a `code block` word"
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(markdown.split_nodes_delimiter([sample_text], "`", TextType.CODE), expected)

        sample_text = "This is text with a <italic block< word"
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(markdown.split_nodes_delimiter([sample_text], "<", TextType.ITALIC), expected)

    def test_extract_images(self):
        matches = markdown.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = markdown.extract_markdown_images(
            "This is text with an ![picture](../content/header.jpeg)"
        )
        self.assertListEqual([("picture", "../content/header.jpeg")], matches)

    def test_extract_links(self):
        matches = markdown.extract_markdown_links(
            "This is text with an [hyperlink](https://google.com)"
        )
        self.assertListEqual([("hyperlink", "https://google.com")], matches)

        matches = markdown.extract_markdown_links(
            "This is text with an [local link](../public/contact.html)"
        )
        self.assertListEqual([("local link", "../public/contact.html")], matches)

    def test_split_nodes_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = markdown.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        #node as raw text
        node = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
        new_nodes = markdown.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_linkss(self):
        node = TextNode(
         "This is text with a [hyperlink](https://google.com) and this is text with a [local link](../public/contact.html)",
        TextType.TEXT,
        )
        new_nodes = markdown.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("hyperlink", TextType.LINK, "https://google.com"),
                TextNode(" and this is text with a ", TextType.TEXT),
                TextNode("local link", TextType.LINK, "../public/contact.html"
                ),
            ],
            new_nodes,
        )

        #node as raw text
        node = "This is text with a [hyperlink](https://google.com) and this is text with a [local link](../public/contact.html)"
        new_nodes = markdown.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("hyperlink", TextType.LINK, "https://google.com"),
                TextNode(" and this is text with a ", TextType.TEXT),
                TextNode("local link", TextType.LINK, "../public/contact.html"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        test_sentence = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = markdown.text_to_textnodes([test_sentence])
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )
        

    if __name__ == "__main__":
        unittest.main()