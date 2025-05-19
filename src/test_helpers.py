import unittest

from htmlnode import HTMLNode
from textnode import TextNode, TextType
from leafnode import LeafNode
from helpers import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_text_nodes, markdown_to_blocks, block_to_block_type, text_node_to_html_node, text_to_children, markdown_to_html_node, BlockType


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

    def test_extract_markdown_images_works(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected_result = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]

        self.assertEqual(result, expected_result)

    def test_extract_markdown_images_no_images(self):
        text = "This text contains no images!"
        result = extract_markdown_images(text)

        self.assertEqual(result, [])

    def test_extract_markdown_images_empty_string(self):
        text = ""
        result = extract_markdown_images(text)

        self.assertEqual(result, [])

    def test_extract_markdown_images_no_alt_text(self):
        text = "This is text with a ![](https://i.imgur.com/aKaOqIh.gif) and ![](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected_result = [
            ("", "https://i.imgur.com/aKaOqIh.gif"),
            ("", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]

        self.assertEqual(result, expected_result)

    def test_extract_markdown_images_no_link(self):
        text = "This is text with a ![rick roll]() and ![obi wan]()"
        result = extract_markdown_images(text)
        expected_result = [
            ("rick roll", ""),
            ("obi wan", "")
        ]

        self.assertEqual(result, expected_result)

    def test_extract_markdown_links_works(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected_result = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]

        self.assertEqual(result, expected_result)

    def test_extract_markdown_links_no_links(self):
        text = "This text contains no links either!"
        result = extract_markdown_links(text)

        self.assertEqual(result, [])

    def test_extract_markdown_links_empty_string(self):
        text = ""
        result = extract_markdown_links(text)

        self.assertEqual(result, [])

    def test_extract_markdown_links_no_anchor_text(self):
        text = "This is text with a link [](https://www.boot.dev) and [](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected_result = [
            ("", "https://www.boot.dev"),
            ("", "https://www.youtube.com/@bootdotdev")
        ]

        self.assertEqual(result, expected_result)

    def test_extract_markdown_links_no_link(self):
        text = "This is text with a link [to boot dev]() and [to youtube]()"
        result = extract_markdown_links(text)
        expected_result = [
            ("to boot dev", ""),
            ("to youtube", "")
        ]

        self.assertEqual(result, expected_result)

    def test_split_nodes_image_works(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_empty_list(self):
        nodes = []
        result = split_nodes_image(nodes)
        self.assertEqual(result, [])

    def test_split_nodes_image_no_images(self):
        node = TextNode(
            "This is text without any images",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected_result = [
            TextNode("This is text without any images", TextType.TEXT)
        ]
        self.assertEqual(result, expected_result)

    def test_split_nodes_image_no_alt_text(self):
        node = TextNode(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png) and another ![](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("", TextType.IMAGE,
                         "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_no_link(self):
        node = TextNode(
            "This is text with an ![image]() and another ![second image]()",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, ""),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, ""),
            ],
            new_nodes,
        )

    def test_split_nodes_image_no_link_no_alt_text(self):
        node = TextNode(
            "This is text with an ![]() and another ![]()",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("", TextType.IMAGE, ""),
                TextNode(" and another ", TextType.TEXT),
                TextNode("", TextType.IMAGE, ""),
            ],
            new_nodes,
        )

    def test_split_nodes_image_different_text_type(self):
        node = TextNode(
            "This is code text",
            TextType.CODE,
        )
        result = split_nodes_image([node])
        expected_result = [
            TextNode("This is code text", TextType.CODE)
        ]
        self.assertEqual(result, expected_result)

    def test_split_nodes_link_works(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK,
                     "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(result, expected_result)

    def test_split_nodes_link_empty_list(self):
        nodes = []
        result = split_nodes_link(nodes)
        self.assertEqual(result, [])

    def test_split_nodes_link_no_links(self):
        node = TextNode(
            "This is text without any links",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected_result = [
            TextNode("This is text without any links", TextType.TEXT)
        ]
        self.assertEqual(result, expected_result)

    def test_split_nodes_link_no_anchor_text(self):
        node = TextNode(
            "This is text with a link [](https://www.boot.dev) and [](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(result, expected_result)

    def test_split_nodes_link_no_link(self):
        node = TextNode(
            "This is text with a link [to boot dev]() and [to youtube]()",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, ""),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, ""),
        ]
        self.assertEqual(result, expected_result)

    def test_split_nodes_link_no_link_no_anchor_text(self):
        node = TextNode(
            "This is text with a link []() and []()",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("", TextType.LINK, ""),
            TextNode(" and ", TextType.TEXT),
            TextNode("", TextType.LINK, ""),
        ]
        self.assertEqual(result, expected_result)

    def test_split_nodes_link_different_text_type(self):
        node = TextNode(
            "This is code text",
            TextType.CODE,
        )
        result = split_nodes_link([node])
        expected_result = [
            TextNode("This is code text", TextType.CODE)
        ]
        self.assertEqual(result, expected_result)

    def test_text_to_text_nodes_works(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_text_nodes(text)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected_result)

    def test_text_to_text_nodes_empty_string(self):
        text = ""
        result = text_to_text_nodes(text)
        expected_result = [
            TextNode("", TextType.TEXT)
        ]
        self.assertEqual(result, expected_result)

    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_leading_and_trailing_whitespace(self):
        md = "   \nThis is a block with leading whitespace\n   \n\n   This is a second block with trailing whitespace   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a block with leading whitespace",
                "This is a second block with trailing whitespace"
            ]
        )

    def test_markdown_to_blocks_multiple_blank_lines(self):
        md = "Block one\n\n\n\nBlock two\n\n\nBlock three"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block one",
                "Block two",
                "Block three"
            ]
        )

    def test_markdown_to_blocks_block_with_only_whitespace_lines(self):
        md = "Block one\n   \n   \nBlock two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block one",
                "Block two"
            ]
        )

    def test_markdown_to_blocks_list_items_with_indentation(self):
        md = """
        - Item one
            - Item two
        - Item three

        Paragraph after list
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- Item one\n- Item two\n- Item three",
                "Paragraph after list"
            ]
        )

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n   \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_block_multiline(self):
        md = "Line one\nLine two\nLine three"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Line one\nLine two\nLine three"]
        )

    def test_markdown_to_blocks_blocks_with_mixed_content(self):
        md = """
        # Header

        Some text with **bold** and _italic_.

        - List item 1
        - List item 2

        > Blockquote

        Final paragraph.
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Header",
                "Some text with **bold** and _italic_.",
                "- List item 1\n- List item 2",
                "> Blockquote",
                "Final paragraph."
            ]
        )

    def test_block_to_block_type_headings(self):
        headings = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6"
        ]

        for heading in headings:
            block_type = block_to_block_type(heading)
            self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_missing_heading_space(self):
        heading = "#Heading 1"
        block_type = block_to_block_type(heading)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_invalid_heading(self):
        invalid_heading = "####### Invalid Heading"
        block_type = block_to_block_type(invalid_heading)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_empty_heading(self):
        empty_heading = "# "
        block_type = block_to_block_type(empty_heading)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code_works(self):
        code_block = "```print('Hello, World!')```"
        block_type = block_to_block_type(code_block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_code_multiline(self):
        code_block = """```
        Python
        
        def hello_world():
            print('Hello, World!')
        ```"""
        block_type = block_to_block_type(code_block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_code_missing_trailing_back_ticks(self):
        invalid_code_block = "```print('Hello, World!')"
        block_type = block_to_block_type(invalid_code_block)
        self.assertNotEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_code_missing_leading_back_ticks(self):
        invalid_code_block = "print('Hello, World!')```"
        block_type = block_to_block_type(invalid_code_block)
        self.assertNotEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_empty_code_block(self):
        empty_code_block = "``` ```"
        block_type = block_to_block_type(empty_code_block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote_works(self):
        quote_block = "> This is a quote"
        block_type = block_to_block_type(quote_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_quote_multiline(self):
        quote_block = "> This is a quote\n> that spans multiple lines"
        block_type = block_to_block_type(quote_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_quote_missing_greater_than(self):
        invalid_quote_block = "This is a quote"
        block_type = block_to_block_type(invalid_quote_block)
        self.assertNotEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_empty_quote(self):
        empty_quote_block = "> "
        block_type = block_to_block_type(empty_quote_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list_works(self):
        unordered_list_block = "- Item 1\n- Item 2\n- Item 3"
        block_type = block_to_block_type(unordered_list_block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_multiline(self):
        unordered_list_block = "- Item 1\n  - Subitem 1\n- Item 2"
        block_type = block_to_block_type(unordered_list_block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_invalid_unordered_list(self):
        invalid_unordered_list_block = "- Item 1\n* Item 2\n- Item 3"
        block_type = block_to_block_type(invalid_unordered_list_block)
        self.assertNotEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_missing_dash(self):
        invalid_unordered_list_block = "Item 1\n- Item 2\n- Item 3"
        block_type = block_to_block_type(invalid_unordered_list_block)
        self.assertNotEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_empty_unordered_list(self):
        empty_unordered_list_block = "- "
        block_type = block_to_block_type(empty_unordered_list_block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_blocK_to_block_type_ordered_list_works(self):
        ordered_list_block = "1. Item 1\n2. Item 2\n3. Item 3"
        block_type = block_to_block_type(ordered_list_block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_multiline(self):
        ordered_list_block = "1. Item 1\n   1. Subitem 1\n2. Item 2"
        block_type = block_to_block_type(ordered_list_block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_invalid_ordered_list(self):
        invalid_ordered_list_block = "1. Item 3. \n- Item 2\n5. Item 3"
        block_type = block_to_block_type(invalid_ordered_list_block)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_missing_number(self):
        invalid_ordered_list_block = "Item 1\n2. Item 2\n3. Item 3"
        block_type = block_to_block_type(invalid_ordered_list_block)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_empty_ordered_list(self):
        empty_ordered_list_block = "1. "
        block_type = block_to_block_type(empty_ordered_list_block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph_works(self):
        paragraph_block = "This is a paragraph with some text."
        block_type = block_to_block_type(paragraph_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_multiline(self):
        paragraph_block = "This is a paragraph\nwith some text.\nAnd another line."
        block_type = block_to_block_type(paragraph_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_with_special_characters(self):
        paragraph_block = "This is a paragraph with special characters: !@#$%^&*()"
        block_type = block_to_block_type(paragraph_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_empty_paragraph(self):
        empty_paragraph_block = "   "
        block_type = block_to_block_type(empty_paragraph_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_markdown_to_html_node_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_markdown_to_html_node_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_node_heading(self):
        md = """
        # This is a heading
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><h1>This is a heading</h1></div>"
        self.assertEqual(html, expected_html)

    def test_markdown_to_html_node_quote(self):
        md = """
        > This is a simple quote dawg
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><blockquote>This is a simple quote dawg</blockquote></div>"
        self.assertEqual(html, expected_html)

    def test_markdown_to_html_node_unordered_list(self):
        md = """
        - This is a list
        - with many
        - items
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><ul><li>This is a list</li><li>with many</li><li>items</li></ul></div>"
        self.assertEqual(html, expected_html)

    def test_markdown_to_html_node_ordered_list(self):
        md = """
        1. This is an ordered
        2. list with
        3. many items
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><ol><li>This is an ordered</li><li>list with</li><li>many items</li></ol></div>"
        self.assertEqual(html, expected_html)

    def test_markdown_to_html_node_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div></div>"
        self.assertEqual(html, expected_html)

    def test_text_node_to_html_node_works(self):
        node = TextNode("This is a text node", TextType.TEXT)
        result = text_node_to_html_node(node)
        expected_result = HTMLNode(
            tag=None, value="This is a text node", children=None, props=None)
        self.assertEqual(result, expected_result)

    def test_text_node_to_html_node_raises_exception(self):
        node = TextNode("This node is invalid", "hehexd")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_text_node_to_html_node_code(self):
        node = TextNode("This is a code block", TextType.CODE)
        result = text_node_to_html_node(node)
        expected_result = HTMLNode(
            tag="code", value="This is a code block", children=None, props=None)
        self.assertEqual(result, expected_result)

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is a BOLD block", TextType.BOLD)
        result = text_node_to_html_node(node)
        expected_result = HTMLNode(
            tag="b", value="This is a BOLD block", children=None, props=None)
        self.assertEqual(result, expected_result)

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is an italic block", TextType.ITALIC)
        result = text_node_to_html_node(node)
        expected_result = HTMLNode(
            tag="i", value="This is an italic block", children=None, props=None)
        self.assertEqual(result, expected_result)

    def test_text_node_to_html_node_image(self):
        node = TextNode("This is an image", TextType.IMAGE,
                        "https://i.imgur.com/aKaOqIh.gif")
        result = text_node_to_html_node(node)
        expected_result = HTMLNode(
            tag="img", value="This is an image", children=None, props={"src": "https://i.imgur.com/aKaOqIh.gif"})
        self.assertEqual(result, expected_result)

    def test_text_node_to_html_node_link(self):
        node = TextNode("This is a link", TextType.LINK,
                        "https://www.boot.dev")
        result = text_node_to_html_node(node)
        expected_result = HTMLNode(
            tag="a", value="This is a link", children=None, props={"href": "https://www.boot.dev"})
        self.assertEqual(result, expected_result)

    def test_text_to_children_plain_text(self):
        nodes = text_to_children("Just some text.")
        self.assertEqual(nodes, [LeafNode(None, "Just some text.")])

    def test_text_to_children_bold(self):
        nodes = text_to_children("This is **bold** text.")
        self.assertEqual(
            nodes,
            [LeafNode(None, "This is "), LeafNode(
                "b", "bold"), LeafNode(None, " text.")]
        )

    def test_text_to_children_italic(self):
        nodes = text_to_children("This is _italic_ text.")
        self.assertEqual(
            nodes,
            [LeafNode(None, "This is "), LeafNode(
                "i", "italic"), LeafNode(None, " text.")]
        )

    def test_text_to_children_code(self):
        nodes = text_to_children("Here is `code`.")
        self.assertEqual(
            nodes,
            [LeafNode(None, "Here is "), LeafNode(
                "code", "code"), LeafNode(None, ".")]
        )

    def test_text_to_children_link(self):
        nodes = text_to_children("A [link](https://example.com).")
        self.assertEqual(
            nodes,
            [LeafNode(None, "A "), LeafNode("a", "link", {
                "href": "https://example.com"}), LeafNode(None, ".")]
        )

    def test_text_to_children_image(self):
        nodes = text_to_children("An image: ![alt](img.png)")
        self.assertEqual(
            nodes,
            [LeafNode(None, "An image: "), LeafNode(
                "img", "alt", {"src": "img.png"})]
        )

    def test_text_to_children_mixed(self):
        nodes = text_to_children(
            "**Bold** and _italic_ with `code` and a [link](url).")
        self.assertEqual(
            nodes,
            [
                LeafNode("b", "Bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " with "),
                LeafNode("code", "code"),
                LeafNode(None, " and a "),
                LeafNode("a", "link", {"href": "url"}),
                LeafNode(None, "."),
            ]
        )


if __name__ == "__main__":
    unittest.main()
