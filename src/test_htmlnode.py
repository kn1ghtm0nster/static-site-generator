import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def setUp(self):
        self.node = HTMLNode(tag="div", value="Hello, World!",
                             children=[], props={"class": "greeting"})

    def test_initialization(self):
        self.assertEqual(self.node.tag, "div")
        self.assertEqual(self.node.value, "Hello, World!")
        self.assertEqual(self.node.children, [])
        self.assertEqual(self.node.props, {"class": "greeting"})

    def test_props_to_html(self):
        expected_props = 'class="greeting"'
        self.assertEqual(self.node.props_to_html(), expected_props)

    def test_repr(self):
        expected_repr = "HTMLNode(tag=div, value=Hello, World!, children=[], props={'class': 'greeting'})"
        self.assertEqual(repr(self.node), expected_repr)

    def test_to_html(self):
        # This method should be implemented in subclasses
        # the main class will raise NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.node.to_html()


if __name__ == "__main__":
    unittest.main()
