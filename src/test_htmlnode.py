import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()

