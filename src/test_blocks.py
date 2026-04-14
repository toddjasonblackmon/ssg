import unittest

from blocks import markdown_to_blocks, block_to_block_type, BlockType




class TestBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blockType_code(self):
        block = """```
1. Open the file.
2. Find the following code block on line 21:

        <html>
          <head>
            <title>Test</title>
          </head>

3. Update the title to match the name of your website.```"""
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.CODE)

    def test_block_to_blockType_H1(self):
        block = '# Heading level 1'
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.HEADING)

    def test_block_to_blockType_H6(self):
        block = '###### Heading level 6'
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.HEADING)

    def test_block_to_blockType_H7_is_paragraph(self):
        block = '####### Heading level 7'
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.PARAGRAPH)

    def test_block_to_blockType_H1_no_space(self):
        block = '#Heading level 1'
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.PARAGRAPH)

    def test_block_to_blockType_quote(self):
        block = """> Dorothy followed her through many of the beautiful rooms in her castle.
>
> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
"""
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.QUOTE)

    def test_block_to_blockType_quote_missing_line(self):
        block = """> Dorothy followed her through many of the beautiful rooms in her castle.
>
  The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
"""
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.PARAGRAPH)

    def test_block_to_blockType_doublequote(self):
        block = """> Dorothy followed her through many of the beautiful rooms in her castle.
>
>> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
"""
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.QUOTE)

    def test_block_to_blockType_unordered(self):
        block = """- Dorothy followed her through many of the beautiful rooms in her castle.
- 
- The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
"""
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.UNORDERED_LIST)

    def test_block_to_blockType_unordered_missing_line(self):
        block = """- Dorothy followed her through many of the beautiful rooms in her castle.
-
  The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
"""
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.PARAGRAPH)

    def test_block_to_blockType_unordered_no_space(self):
        block = """- Dorothy followed her through many of the beautiful rooms in her castle.
-
-The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
"""
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.PARAGRAPH)

    def test_block_to_blockType_ordered(self):
        block = """1. Dorothy followed her through many of the beautiful rooms in her castle.
2. 
3. The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
"""
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.ORDERED_LIST)

    def test_block_to_blockType_ordered_missing_line(self):
        block = """1. Dorothy followed her through many of the beautiful rooms in her castle.
2. 
  The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
"""
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.PARAGRAPH)

    def test_block_to_blockType_ordered_no_space(self):
        block = """1. Dorothy followed her through many of the beautiful rooms in her castle.
2.
3. The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
"""
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.PARAGRAPH)

    def test_block_to_blockType_ordered_out_of_order(self):
        block = """1. Dorothy followed her through many of the beautiful rooms in her castle.
3. 
2. The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
"""
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.PARAGRAPH)









































