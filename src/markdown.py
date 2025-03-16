from textnode import TextType, TextNode
import re

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