from enum import Enum

class TextType(Enum):
    NORMAL = "Normal"
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
            and self.TextType == textnode.TextType
            and self.url == textnode.url
        ):
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
