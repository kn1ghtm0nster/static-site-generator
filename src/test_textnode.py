import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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

    def test_text_node_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_text_node_to_html_node_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_text_node_to_html_node_link(self):
        node = TextNode("This is a link node",
                        TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "https://www.google.com")

    def test_text_node_to_html_node_image(self):
        node = TextNode("This is an image node",
                        TextType.IMAGE, "https://www.google.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertIsNone(html_node.value)
        self.assertEqual(html_node.props["src"],
                         "https://www.google.com/image.png")
        self.assertEqual(html_node.props["alt"], "This is an image node")

    def test_text_node_to_html_node_invalid_type(self):
        node = TextNode("This is an invalid node", "invalid_type")

        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)

        self.assertEqual(str(context.exception), "Invalid text type")


if __name__ == "__main__":
    unittest.main()
