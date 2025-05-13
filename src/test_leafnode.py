import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def setUp(self):
        self.node = LeafNode(tag="p", value="Hello, World!",
                             props={"class": "greeting"})

    def test_initialization(self):
        self.assertEqual(self.node.tag, "p")
        self.assertEqual(self.node.value, "Hello, World!")
        self.assertEqual(self.node.props, {"class": "greeting"})
        self.assertIsNone(self.node.children)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "this is a div", {"id": "my-div"})
        self.assertEqual(
            node.to_html(), '<div id="my-div">this is a div</div>')

    def test_leaf_to_html_anchor(self):
        node = LeafNode("a", "link tag", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">link tag</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "no tag")
        self.assertEqual(node.to_html(), "no tag")

    def test_leaf_to_html_no_value_raises_exception(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_props(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


if __name__ == "__main__":
    unittest.main()
