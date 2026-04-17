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
        #print("block_type", block_type)

        if block_type == BlockType.PARAGRAPH:
            block = " ".join(block.split())
            text_nodes = text_to_textnodes(block)
            html_children = list(map(text_node_to_html_node, text_nodes))
            html_nodes.append(ParentNode('p', html_children))
        elif block_type == BlockType.HEADING:
            block_strip = block.lstrip('#')
            heading_num = len(block) - len(block_strip)
            block_strip = " ".join(block_strip.split())
            text_nodes = text_to_textnodes(block_strip)
            html_children = list(map(text_node_to_html_node, text_nodes))
            html_nodes.append(ParentNode(f'h{heading_num}', html_children))
        elif block_type == BlockType.QUOTE:
            block_lines = block.split('\n')
            stripped_lines = []
            for line in block_lines:
                line = line.lstrip('>')
                stripped_lines.append(line.strip())
            block_strip = " ".join(stripped_lines)
            text_nodes = text_to_textnodes(block_strip)
            html_children = list(map(text_node_to_html_node, text_nodes))
            html_nodes.append(ParentNode(f'blockquote', html_children))
        elif block_type == BlockType.UNORDERED_LIST:
            html_nodes.append(text_to_unordered_textnodes(block))
        elif block_type == BlockType.ORDERED_LIST:
            html_nodes.append(text_to_ordered_textnodes(block))
        else:   # Unimplemented blocks are executed similar to code
            #elif block_type == BlockType.CODE:
            if block_type == BlockType.CODE:
                text_node = TextNode(block[4:-3], TextType.CODE)
            else:
                print(f"HACK! {block[:20]}")
                text_node = TextNode(block, TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            html_nodes.append(ParentNode('pre', [html_node]))

    # Create parent node
    top_node = ParentNode('div', html_nodes)

    return top_node


# We know the block text represents and unordered list
# So we need to strip the head of each line and generate
# an 'li' HTMLnode and finally wrap them all in a parent 'ul' node.
def text_to_unordered_textnodes(block):
    unordered_children = []
    for line in block.split('\n'):
        # Remove prefix.
        line = line[2:]
        text_nodes = text_to_textnodes(line.strip())
        html_children = list(map(text_node_to_html_node, text_nodes))
        unordered_children.append(ParentNode('li', html_children))
    return ParentNode('ul', unordered_children)

# We know the block text represents and unordered list
# So we need to strip the head of each line and generate
# an 'li' HTMLnode and finally wrap them all in a parent 'ul' node.
def text_to_ordered_textnodes(block):
    ordered_children = []
    for line in block.split('\n'):
        # Remove prefix.
        line = line.lstrip('0123456789.')
        text_nodes = text_to_textnodes(line.strip())
        html_children = list(map(text_node_to_html_node, text_nodes))
        ordered_children.append(ParentNode('li', html_children))
    return ParentNode('ol', ordered_children)




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

