from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: TextNode, delimiter: str, text_type: TextType) -> list[TextNode]:
    retval = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            retval.append(old_node)
            continue

        sublist = old_node.text.split(delimiter)
        if len(sublist) < 2:
            retval.append(old_node)
            continue
        
        if len(sublist) % 2 != 1:
            raise Exception(f'Unmatched "{delimiter}" characters in {old_node.text}')
        new_toggle = False
        for sl in sublist:
            if new_toggle:
                retval.append(TextNode(sl, text_type))
            else:
                if len(sl) > 0:
                    retval.append(TextNode(sl, TextType.TEXT))

            new_toggle = not new_toggle

    return retval


# The format of a markdown image is:
#   	![alt text](image.jpg)
# This function should take a markdown text and return a list of tuples such as
#  [("alt text", "image.jpg"), ... ]
def extract_markdown_images(text):
    matches = re.findall(r'!\[(.*?)\]\((.*?)\)', text)

    return matches


# The format of a markdown link is:
#       [title](https://www.example.com)
# This function should take a markdown text and return a list of tuples such as
#  [("title", "https://www.example.com"), ... ]
def extract_markdown_links(text):
    
    matches = re.findall(r'(?<!!)\[(.*?)\]\((.*?)\)', text)

    return matches


