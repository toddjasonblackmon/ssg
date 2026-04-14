from enum import Enum
from htmlnode import LeafNode, ParentNode
from split_nodes import text_to_textnodes
from convert import text_node_to_html_node
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        # Just assume PARAGRAPH for now.
        if block_type == BlockType.PARAGRAPH:
            block = " ".join(block.split())
            text_nodes = text_to_textnodes(block)
            html_children = list(map(text_node_to_html_node, text_nodes))
            html_nodes.append(ParentNode('p', html_children))
        elif block_type == BlockType.CODE:
            text_node = TextNode(block[4:-3], TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            html_nodes.append(ParentNode('pre', [html_node]))
        else:
            pass

    # Create parent node
    top_node = ParentNode('div', html_nodes)

    return top_node






def markdown_to_blocks(markdown):
    raw = markdown.split('\n\n')
    # Strip each for whitespace
    stripped = map(str.strip, raw)
    # Remove empty blocks
    blocks = filter(lambda x: len(x) > 0, stripped)

    return list(blocks)


def block_to_block_type(block: str) -> BlockType:
    
    if block[0] == '#':
        count = 1
        for v in block[1:]:
            if v == '#':
                count += 1
                if count > 6:
                    break
            elif v == ' ':
                return BlockType.HEADING
            else:
                break
        return BlockType.PARAGRAPH

    elif block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE

    else:
        retval = None
        lines = block.splitlines()
        count = 1
        
        for line in lines:
            if line.startswith('>'):
                if retval is None:
                    retval = BlockType.QUOTE
                elif retval != BlockType.QUOTE:
                    return BlockType.PARAGRAPH

            elif line.startswith('- '):
                if retval is None:
                    retval = BlockType.UNORDERED_LIST
                elif retval != BlockType.UNORDERED_LIST:
                    return BlockType.PARAGRAPH

            elif line.startswith(f'{count}. '):
                count += 1
                if retval is None:
                    retval = BlockType.ORDERED_LIST
                elif retval != BlockType.ORDERED_LIST:
                    return BlockType.PARAGRAPH


            else:
                retval = BlockType.PARAGRAPH
                break
            


        return retval

