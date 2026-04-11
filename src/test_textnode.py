import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is an italic node", TextType.TEXT, "www.example.org")
        self.assertEqual(str(node), "TextNode(This is an italic node, text, www.example.org)")

    def test_empty_url(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        self.assertEqual(str(node), "TextNode(This is an italic node, italic, None)")

if __name__ == "__main__":
    unittest.main()

