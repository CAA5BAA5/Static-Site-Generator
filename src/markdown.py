from textnode import TextType, TextNode, text_node_to_html_node
from parentnode import ParentNode
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered_List"
    ORDERED_LIST = "Ordered_List"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes must be a list")

    count = 1
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            node = TextNode(node,TextType.TEXT)
        if delimiter in node.text:
            for segment in node.text.split(delimiter):
                if count % 2 == 1:
                    new_nodes.append(TextNode(segment, TextType.TEXT))
                elif count % 2 == 0:
                    new_nodes.append(TextNode(segment, text_type))
                count +=1
        else :
            new_nodes.append(node)
    
    return new_nodes

def split_nodes_on_media_regex(old_nodes, regex, text_type):
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes must be a list")
    
    count = 1
    new_nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode):
            node = TextNode(node,TextType.TEXT)
        if re.search(regex, node.text):
            for segment in re.split(regex, node.text):
                if count % 2 == 1:
                    if len(segment) > 0:
                        new_nodes.append(TextNode(segment, TextType.TEXT))
                elif count % 2 == 0:
                    sep = segment.split("](")
                    new_nodes.append(TextNode(sep[0], text_type, sep[1]))
                count +=1
        else :
            new_nodes.append(node)
    
    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_on_media_regex(old_nodes, r"!\[([^\[\]]*\]\([^\(\)]*)\)", TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes_on_media_regex(old_nodes, r"(?<!!)\[([^\[\]]*\]\([^\(\)]*)\)", TextType.LINK)

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def text_to_textnodes(text):
    text = split_nodes_delimiter(text, "**", TextType.BOLD)
    text = split_nodes_delimiter(text, "_", TextType.ITALIC)
    text = split_nodes_delimiter(text, "`", TextType.CODE)
    text = split_nodes_image(text)
    text = split_nodes_link(text)

    # text = [
    # TextNode(This is , Text, None), 
    # TextNode(text, Bold, None), 
    # TextNode( with an , Text, None), 
    # TextNode(italic, Italic, None), 
    # TextNode( word and a , Text, None), 
    # TextNode(code block, Code, None), 
    # TextNode( and an , Text, None), 
    # TextNode(obi wan image, Image, https://i.imgur.com/fJRm4Vk.jpeg), 
    # TextNode( and a , Text, None), 
    # TextNode(link, Link, https://boot.dev)]
    return text

def markdown_to_blocks(document):
    filtered_blocks = []
    for block in document.split("\n\n"):
        block = block.strip()
        block = re.sub(' +', ' ', block)
        block = block.replace("\n ", "\n")
        if len(block) > 0:
            filtered_blocks.append(block)

    return(filtered_blocks)

def block_to_block_type(markdown_block):
    markdown_block = str(markdown_block)
    if markdown_block.startswith(("# ","## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    
    md_lines = markdown_block.split("\n")
    if all(line.startswith(">") for line in md_lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in md_lines):
        return BlockType.UNORDERED_LIST
    elif all(re.search(r"^(\d+\. )", line) for line in md_lines):
        list_of_numbers = list(map(lambda x: int(x.split(".")[0]),re.findall(r"(\d+\. )", markdown_block)))
        if sorted(list_of_numbers) == list(range(min(list_of_numbers), max(list_of_numbers) + 1)):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    children = []
    for block in markdown_to_blocks(markdown):
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)
         
def block_to_html_node(block):
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            h_number = len(block.split(" ")[0])
            return heading_to_html_node(block, h_number)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return list_to_html_node(block, "ul", 2)
        case BlockType.ORDERED_LIST:
            return list_to_html_node(block, "ol", 3)

def text_to_children(text):
    text_nodes = text_to_textnodes([text])
    children = []
    for text_node in text_nodes:
        text_node
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block, level):
    text = block[level+1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}",children)

def code_to_html_node(block):
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def list_to_html_node(block, parent_tag, md_length):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[md_length:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode(parent_tag, html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def extract_title(markdown):
    html_string = markdown_to_html_node(markdown).to_html()
    if "h1" in html_string:
        start = html_string.find("<h1>") +4
        end = html_string.find("</h1>")
        return html_string[start:end]