import unittest

from textnode import TextNode, TextType
from split_nodes import (split_nodes_delimiter, extract_markdown_images, 
                            extract_markdown_links, split_nodes_image,
                            split_nodes_link, text_to_textnodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_example_text(self):
        text = ("This is **text** with an _italic_ word and a `code block` and "
                "an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
                "and a [link](https://boot.dev)")
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_example_text_alt_bold_italics(self):
        text = ("This is __text__ with an *italic* word and a `code block` and "
                "an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
                "and a [link](https://boot.dev)")
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)



class TestSplitNodes(unittest.TestCase):

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold_italic(self):
        node = TextNode("This is **bolded text** with an _italics_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bolded text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_start_bold(self):
        node = TextNode("**Bolded** word!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Bolded", TextType.BOLD),
            TextNode(" word!", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


    def test_split_images(self):
        node = TextNode(
            ("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another "
             "![second image](https://i.imgur.com/3elNhQu.png)"),
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_dbl_bug(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
            ("This is text with a link [to boot dev](https://www.boot.dev) and "
             "[to youtube](https://www.youtube.com/@bootdotdev)"),
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]

        self.assertListEqual(expected, new_nodes)


    def test_split_images_and_link(self):
        node = TextNode(
                ("This is some [boot dev](https://www.boot.dev) text with an "
                 "![image](https://i.imgur.com/zjjcJKZ.png) and another "
                 "![second image](https://i.imgur.com/3elNhQu.png)"),
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is some ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    # Swap the order
    def test_split_link_and_images(self):
        node = TextNode(
                ("This is some [boot dev](https://www.boot.dev) text with an "
                 "![image](https://i.imgur.com/zjjcJKZ.png) and another "
                 "![second image](https://i.imgur.com/3elNhQu.png)"),
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is some ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )










class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")] 
        self.assertListEqual(expected, matches)

    def test_extract_markdown_rickroll(self):
        matches = extract_markdown_images(
            ("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and "
             "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        )
        expected = [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            ("This is text with a link [to boot dev](https://www.boot.dev) and "
             "[to youtube](https://www.youtube.com/@bootdotdev)")
        )
        expected = [
                ("to boot dev", "https://www.boot.dev"), 
                ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)


#        node = TextNode("This is a text node", TextType.TEXT)
#        html_node = text_node_to_html_node(node)
#        self.assertEqual(html_node.tag, None)
#        self.assertEqual(html_node.value, "This is a text node")
#
#    def test_bold(self):
#        node = TextNode("This is a bold node", TextType.BOLD)
#        html_node = text_node_to_html_node(node)
#        self.assertEqual(html_node.tag, 'b')
#        self.assertEqual(html_node.value, "This is a bold node")
#
#    def test_italic(self):
#        node = TextNode("This is an italic node", TextType.ITALIC)
#        html_node = text_node_to_html_node(node)
#        self.assertEqual(html_node.tag, 'i')
#        self.assertEqual(html_node.value, "This is an italic node")
#
#    def test_code(self):
#        node = TextNode("This is a code node", TextType.CODE)
#        html_node = text_node_to_html_node(node)
#        self.assertEqual(html_node.tag, 'code')
#        self.assertEqual(html_node.value, "This is a code node")
#
#    def test_link(self):
#        node = TextNode("This is the anchor text", TextType.LINK, url='http://google.com')
#        html_node = text_node_to_html_node(node)
#        self.assertEqual(html_node.tag, 'a')
#        self.assertEqual(html_node.value, "This is the anchor text")
#        self.assertEqual(html_node.props, {'href': 'http://google.com'})
#
#    def test_image(self):
#        node = TextNode("This is the alt text", TextType.IMAGE, url='lena.png')
#        html_node = text_node_to_html_node(node)
#        self.assertEqual(html_node.tag, 'img')
#        self.assertEqual(html_node.value, "")
#        self.assertEqual(html_node.props,
#                {'src': 'lena.png', 'alt': 'This is the alt text'})
#

