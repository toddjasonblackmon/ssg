import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):

    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        props = {"href": "https://google.com", "target": "_blank", }
        node = HTMLNode(props=props)

        expected = 'href="https://google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        props = {"href": "https://google.com", "target": "_blank", }
        node = HTMLNode(tag='h1', value='A dummy header', props=props)

        expected = ("HTMLNode(h1, A dummy header, None, "
                    "{'href': 'https://google.com', 'target': '_blank'})"
                   )
        
        self.assertEqual(str(node), expected)


class TestLeafNode(unittest.TestCase):

    def test_to_html_no_value(self):
        node = LeafNode('p', None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "The quick brown fox ...")
        self.assertEqual(node.to_html(), "The quick brown fox ...")

    def test_to_html_p_tag(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_href_tag(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_img_tag(self):
        node = LeafNode("img", "", {"src": "lena.jpg", "alt": "Description of image"})
        self.assertEqual(node.to_html(), '<img src="lena.jpg" alt="Description of image" />')

    def test_to_html_img_tag_no_alt(self):
        node = LeafNode("img", "", {"src": "lena.jpg"})
        self.assertEqual(node.to_html(), '<img src="lena.jpg" />')


if __name__ == "__main__":
    unittest.main()

