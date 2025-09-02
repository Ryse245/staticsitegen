from enum import Enum

class TextType(Enum):
    PLAIN = 0
    BOLD = 1
    ITALIC = 2
    CODE = 3
    LINK = 4
    IMAGE = 5

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, value):
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"