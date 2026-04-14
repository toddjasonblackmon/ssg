from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5


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
    
    # Headings - 1-6 '#' and space
    # Multiline Code - '```\n' and end with ```
    # Quote block - Every line must start with >
    # Unordered list - Every line must start with '- '
    # Ordered list - Every line must start with a number, '.', then space
    #                 the number must start at one and increment for each line.
    # otherwise normal paragraph



    pass
