from textnode import TextNode
from textnode import TextType
from helper_functions import copy_directory

def main():
    
    copy_directory("static", "public")

if __name__ == "__main__":
    main()