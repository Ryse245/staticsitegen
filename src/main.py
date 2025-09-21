import sys
from helper_functions import copy_directory
from generate_page import generate_pages_recursive

def main():
    
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_directory("static", "docs")
    generate_pages_recursive("content","template.html", "docs", basepath)
    


if __name__ == "__main__":
    main()