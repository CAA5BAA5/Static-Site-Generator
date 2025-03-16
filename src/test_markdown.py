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

    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        # stress testing chars
        self.assertEqual(markdown.block_to_block_type(1), markdown.BlockType.PARAGRAPH)
        self.assertEqual(markdown.block_to_block_type(""), markdown.BlockType.PARAGRAPH)

        # Heading
        self.assertEqual(markdown.block_to_block_type("# header"), markdown.BlockType.HEADING)
        self.assertEqual(markdown.block_to_block_type("#### header"), markdown.BlockType.HEADING)
        self.assertEqual(markdown.block_to_block_type("#header"), markdown.BlockType.PARAGRAPH)

        # Code
        self.assertEqual(markdown.block_to_block_type("```code```"), markdown.BlockType.CODE)
        self.assertEqual(markdown.block_to_block_type("``` code```"), markdown.BlockType.CODE)
        self.assertEqual(markdown.block_to_block_type("`` ##code ``"), markdown.BlockType.PARAGRAPH)

        # Quote
        quote = """> veni\n> vidi\n> vici"""
        self.assertEqual(markdown.block_to_block_type(quote), markdown.BlockType.QUOTE)
        quote = """> veni\n> vidi\nvici"""
        self.assertEqual(markdown.block_to_block_type(quote), markdown.BlockType.PARAGRAPH)
        quote = """veni\n> vidi\n> vici"""
        self.assertEqual(markdown.block_to_block_type(quote), markdown.BlockType.PARAGRAPH)

        # unordered_list
        ul = """- first\n- second\n- third"""
        self.assertEqual(markdown.block_to_block_type(ul), markdown.BlockType.UNORDERED_LIST)
        ul = """ - first\n- second\n- third"""
        self.assertEqual(markdown.block_to_block_type(ul), markdown.BlockType.PARAGRAPH)
        ul = """ first\n- second\n- third"""
        self.assertEqual(markdown.block_to_block_type(ul), markdown.BlockType.PARAGRAPH)
        ul = """ first\n- second\n - third"""
        self.assertEqual(markdown.block_to_block_type(ul), markdown.BlockType.PARAGRAPH)

        #ordered_list
        ol = """1. first\n2. second\n3. third"""
        self.assertEqual(markdown.block_to_block_type(ol), markdown.BlockType.ORDERED_LIST)
        ol = """1. first 2. second 3.  third"""
        self.assertEqual(markdown.block_to_block_type(ol), markdown.BlockType.ORDERED_LIST)
        ol = """1. first\n34. second\n4. third"""
        self.assertEqual(markdown.block_to_block_type(ol), markdown.BlockType.PARAGRAPH)
        ol = """ 1. first\n34. second\n4. third"""
        self.assertEqual(markdown.block_to_block_type(ol), markdown.BlockType.PARAGRAPH)
        ol = """1. first\n34 second\n4. third"""
        self.assertEqual(markdown.block_to_block_type(ol), markdown.BlockType.PARAGRAPH)
        ol = """ 1. first\n34.second\n 4. third"""
        self.assertEqual(markdown.block_to_block_type(ol), markdown.BlockType.PARAGRAPH)
        ol = """1.first\n34. second\n4.  third"""
        self.assertEqual(markdown.block_to_block_type(ol), markdown.BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    ## HEADER 2

    ##### HEADER 5

    """

        node = markdown.markdown_to_html_node(md)
    
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown.markdown_to_html_node(md)

    
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    if __name__ == "__main__":
        unittest.main()