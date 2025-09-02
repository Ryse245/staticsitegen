from textnode import TextNode
from textnode import TextType

def main():
    node = TextNode("this is dummy text", TextType.LINK, "https://benhubner.com")
    print(node)

if __name__ == "__main__":
    main()