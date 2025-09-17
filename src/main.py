from helper_functions import copy_directory
from helper_functions import create_directory_layout
from generate_page import generate_pages_recursive

def main():
    
    copy_directory("static", "public")
    #create_directory_layout("content", "public")
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content","template.html", "public" )
    


if __name__ == "__main__":
    main()