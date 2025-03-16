from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "Text"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Image"

class TextNode():
    def __init__(self, text, text_type : TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, textnode):
        if(
            self.text == textnode.text
            and self.text_type == textnode.text_type
            and self.url == textnode.url
        ):
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def text_node_to_html_node(self):
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text,{"href": self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt" : self.text})
            case _:
                raise Exception("LeafNode has an unknown text_type")
    
