from dir_copy import copy_directory, generate_page, generate_pages_recursive
from split_nodes import extract_title

def main():
    copy_directory('static', 'public')

    generate_pages_recursive('content', 'template.html', 'public')


if __name__ == "__main__":
    main()
