from dir_copy import copy_directory, generate_page, generate_pages_recursive
from split_nodes import extract_title
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    print(f"basepath = {basepath}")

    copy_directory('static', 'docs')

    generate_pages_recursive('content', 'template.html', 'docs', basepath)


if __name__ == "__main__":
    main()
