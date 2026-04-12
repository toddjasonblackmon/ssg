import unittest

from textnode import TextNode, TextType
from split_nodes import (split_nodes_delimiter, extract_markdown_images, 
                            extract_markdown_links)

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
        node = TextNode("This is **bolded text** with an __italics__ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
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

