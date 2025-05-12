import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node_1 = TextNode("This is a text node", TextType.BOLD.value)
        node_2 = TextNode("This is a text node", TextType.BOLD.value)

        self.assertEqual(node_1, node_2)

    def test_eq_different_nodes(self):
        node_1 = TextNode("This is a text node", TextType.BOLD.value)
        node_2 = TextNode("This is a different italic node",
                          TextType.ITALIC.value)

        self.assertNotEqual(node_1, node_2)

    def test_url_is_none(self):
        test_node = TextNode("This is a text node", TextType.BOLD.value)

        self.assertIsNone(test_node.url)

    def test_url_is_not_none(self):
        test_node = TextNode("This is a link node",
                             TextType.LINK.value, "https://www.google.com")

        self.assertEqual(test_node.url, "https://www.google.com")

    def test_repr(self):
        test_node = TextNode("This is a link node",
                             TextType.LINK.value, "https://www.google.com")

        self.assertEqual(
            repr(test_node),
            "TextNode(This is a link node, link, https://www.google.com)"
        )


if __name__ == "__main__":
    unittest.main()
