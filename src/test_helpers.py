import unittest

from textnode import TextNode, TextType
from helpers import split_nodes_delimiter


class TestHelperFunctions(unittest.TestCase):

    def test_split_nodes_delimiter_works(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]

        self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_raises_exception(self):
        node = TextNode("This is text with bad `delimter word", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_delimiter_plain_text(self):
        node = TextNode("This is a simple text node", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("This is a simple text node", TextType.TEXT)]
        self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_bold_text(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]

        self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_italic_text(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]

        self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_not_text_type(self):
        node = TextNode("This is already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.TEXT)
        expected_result = [
            TextNode("This is already bold", TextType.BOLD)
        ]

        self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_on_empty_space(self):
        node = TextNode("a `` b", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("a ", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode(" b", TextType.TEXT)
        ]
        self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_on_start_of_string(self):
        node = TextNode("`start` and end", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("", TextType.TEXT),
            TextNode("start", TextType.CODE),
            TextNode(" and end", TextType.TEXT)
        ]

        self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_on_end_of_string(self):
        node = TextNode("start and `end`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("start and ", TextType.TEXT),
            TextNode("end", TextType.CODE),
            TextNode("", TextType.TEXT)
        ]

        self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_on_multiple_delimiters(self):
        node = TextNode("start `middle` and `end`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("start ", TextType.TEXT),
            TextNode("middle", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("end", TextType.CODE),
            TextNode("", TextType.TEXT)
        ]

        self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This is a text node", TextType.TEXT)
        result = split_nodes_delimiter(
            old_nodes=[node], delimiter=None, text_type=TextType.CODE)
        expected_result = [
            TextNode("This is a text node", TextType.TEXT)
        ]


if __name__ == "__main__":
    unittest.main()
