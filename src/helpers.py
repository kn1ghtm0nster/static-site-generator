"""
module contains helper functions for the project
"""
import re
import os
import shutil
from enum import Enum

from textnode import TextNode, TextType
from parentnode import ParentNode
from htmlnode import HTMLNode
from leafnode import LeafNode


class BlockType(Enum):
    """
    Enum class for valid markdown types.
    """
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
    Function takes a list of `TextNode` objects, a `delimiter` string, and a `TextType` enum.
    It splits the text of each `TextNode` in the list by the `delimiter` and creates new list of `TextNode` objects
    using delimiter as a separator.

    Will raise `Exception` if the number of segments is even, meaning that the delimiter is not matched.

    Args:
        old_nodes (list[TextNode]): List of `TextNode` objects to be split.
        delimiter (str): The delimiter string used to split the text.
        text_type (TextType): The `TextType` enum used to create new `TextNode` objects.
    Returns:
        list[TextNode]: A new list of `TextNode` objects created by splitting the text of the old nodes.
    """
    new_nodes = []

    for node in old_nodes:

        match node.text_type:
            case TextType.TEXT:
                text_segments = node.text.split(delimiter)
                if len(text_segments) % 2 == 0:
                    raise Exception(
                        f"Unmatched delimiter in text: {node.text}")
                for i in range(len(text_segments)):
                    if i % 2 == 0:
                        new_nodes.append(
                            TextNode(text_segments[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(text_segments[i], text_type))
            case _:
                new_nodes.extend([node])

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Function takes a text `string` and extracts all the markdown image links from it.

    It returns a `list` of `tuples` containing the image link and the alt text.

    Args:
        text (str): The input text string containing markdown image links.
    Returns:
        list[tuple[str, str]]: A list of tuples containing the image link and the alt text.
    """
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_pattern, text)
    return [(match[0], match[1]) for match in matches]


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Function takes a text `string` and extracts all the markdown links from it.

    It returns a `list` of `tuples` containing the link and the anchor text.

    Args:
        text (str): The input text string containing markdown links.
    Returns:
        list[tuple[str, str]]: A list of tuples containing the link and the anchor text.
    """
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(link_pattern, text)
    return [(match[0], match[1]) for match in matches]


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Function takes a list of `TextNode` objects and splits the test of each image node and returns a new list of `TextNode` objects.

    It extracts the image links and alt text from the original nodes and creates new `TextNode` objects for each image. The original text is also preserved in the new nodes.

    Args:
        old_nodes (list[TextNode]): List of `TextNode` objects to be split.
    Returns:
        list[TextNode]: A new list of `TextNode` objects created by splitting the image nodes.
    """

    new_nodes = []

    for node in old_nodes:
        match node.text_type:
            case TextType.TEXT:
                text = node.text
                images = extract_markdown_images(text)
                if not images:
                    new_nodes.append(node)
                    continue
                curr_idx = 0
                for alt, url in images:
                    # Build the markdown string for this image
                    image_md = f"![{alt}]({url})"
                    # Find where this image markdown appears in the text
                    idx = text.find(image_md, curr_idx)
                    if idx == -1:
                        continue  # Shouldn't happen, but safety
                    # Text before the image
                    before = text[curr_idx:idx]
                    if before:
                        new_nodes.append(TextNode(before, TextType.TEXT))
                    # The image node
                    new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                    # Move past this image
                    curr_idx = idx + len(image_md)
                # Any text after the last image
                after = text[curr_idx:]
                if after:
                    new_nodes.append(TextNode(after, TextType.TEXT))
            case _:
                new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Function takes a list of `TextNode` objects and splits the test of each link node and returns a new list of `TextNode` objects.

    It extracts the link and anchor text from the original nodes and creates new `TextNode` objects for each link. The original text is also preserved in the new nodes.

    Args:
        old_nodes (list[TextNode]): List of `TextNode` objects to be split.
    Returns:
        list[TextNode]: A new list of `TextNode` objects created by splitting the link nodes.
    """

    new_nodes = []

    for node in old_nodes:

        match node.text_type:
            case TextType.TEXT:
                text = node.text
                links = extract_markdown_links(text)
                if not links:
                    new_nodes.append(node)
                    continue
                current_idx = 0
                for anchor, url in links:
                    link_md = f"[{anchor}]({url})"
                    index = text.find(link_md, current_idx)
                    if index == -1:
                        continue  # Shouldn't happen, but just in case
                    # slice the text before the link
                    before = text[current_idx:index]
                    if before:
                        new_nodes.append(TextNode(before, TextType.TEXT))
                    new_nodes.append(TextNode(anchor, TextType.LINK, url))
                    current_idx = index + len(link_md)  # move past this link
                after = text[current_idx:]
                if after:
                    new_nodes.append(TextNode(after, TextType.TEXT))
            case _:
                new_nodes.append(node)

    return new_nodes


def text_to_text_nodes(text: str) -> list[TextNode]:
    """
    Function takes a text `string` and converts it into a list of `TextNode` objects.

    It splits the text into segments based on the delimiters and creates new `TextNode` objects for each segment.

    Args:
        text (str): The input text string to be converted.
    Returns:
        list[TextNode]: A list of `TextNode` objects created from the input text.
    """
    starting_node = TextNode(text, TextType.TEXT)
    nodes = [starting_node]

    # split nodes for specific delimiters
    nodes = split_nodes_delimiter(nodes, "`",  TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(text: str) -> list[str]:
    """
    Function takes a markdown `string` and splits it into blocks based on the markdown syntax.

    It returns a `list` of blocks, where each block is a string containing the text inside it.

    Args:
        text (str): The input markdown string to be split into blocks.
    Returns:
        list[str]: A list of blocks, where each block is a string containing the text inside it.
    """
    # Split on any line that is empty or contains only whitespace
    blocks = re.split(r'(?:\r?\n\s*\n)+', text)
    cleaned_blocks = []
    for block in blocks:
        # Strip each line in the block, then join back with \n
        lines = block.splitlines()
        stripped_lines = [line.strip() for line in lines]
        # remove leading/trailing whitespace
        cleaned_block = "\n".join(stripped_lines).strip()
        if cleaned_block:
            cleaned_blocks.append(cleaned_block)
    return cleaned_blocks


def block_to_block_type(block: str) -> BlockType:
    """
    Function takes a markdown `block` and determines its type based on the markdown syntax.

    It returns a `BlockType` enum value representing the type of the block.

    Args:
        block (str): The input markdown block to be classified.
    Returns:
        BlockType: The `BlockType` enum value representing the type of the block.
    """
    heading_pattern = r"^#{1,6} .*"
    code_pattern = r"^```.*```$"
    quote_pattern = r"^> .*"
    unordered_list_pattern = r"^\s*-\s.*"
    ordered_list_patter = r"^\s*(\d+)\.\s.*"

    # to be used with multiline markdown blocks such as quotes, lists, etc.
    lines = block.splitlines()

    # Ensure heading starts with # but is between 1 and 6 #s
    if re.match(heading_pattern, block):
        return BlockType.HEADING
    # Ensure codeblocks start with ``` and end with ```
    elif re.match(code_pattern, block, re.DOTALL):
        return BlockType.CODE
    # Ensure quotes start with > and are followed by a space
    elif all(re.match(quote_pattern, line) for line in lines):
        return BlockType.QUOTE
    # Ensure unordered lists start with - followed by a space (* is NOT supported)
    elif all(re.match(unordered_list_pattern, line) for line in lines):
        return BlockType.UNORDERED_LIST
    # Ensure ordered lists start with 1. followed by a space (the dot is VERY important). Each item increments by 1.
    elif all(re.match(ordered_list_patter, line) for line in lines):
        expected_number = 1
        for line in lines:
            match = re.match(ordered_list_patter, line)
            if not match or int(match.group(1)) != expected_number:
                break
            expected_number += 1
        return BlockType.ORDERED_LIST
    # Ensure paragraphs for all other cases
    else:
        return BlockType.PARAGRAPH


def text_node_to_html_node(node: TextNode) -> LeafNode:
    """
    Function converts a `TextNode` object representing inline markdown
    into the corresponding HTML node.

    Args:
        node (TextNode): The `TextNode` object to be converted.
    Returns:
        LeafNode: The corresponding `LeafNode` object.

    Raises:
        Exception: If the text type of the node is unknown.
    """
    match node.text_type:
        case TextType.TEXT:
            return LeafNode(None, node.text)
        case TextType.CODE:
            return LeafNode("code", node.text)
        case TextType.BOLD:
            return LeafNode("b", node.text)
        case TextType.ITALIC:
            return LeafNode("i", node.text)
        case TextType.IMAGE:
            return LeafNode("img", node.text, {"src": node.url})
        case TextType.LINK:
            return LeafNode("a", node.text, {"href": node.url})
        case _:
            raise Exception(f"Unknown text type: {node.text_type}")


def text_to_children(text: str) -> list[HTMLNode]:
    """
    Function converts a string of markdown text into a list of `HTMLNode` objects.
    representing inline elements such as links, images, and text.

    Args:
        text (str): The input markdown text to be converted.
    Returns:
        list[HTMLNode]: A list of `HTMLNode` objects representing inline elements.
    """
    text_nodes = text_to_text_nodes(text)
    html_nodes = [
        text_node_to_html_node(node)
        for node in text_nodes
        if not (node.text_type == TextType.TEXT and node.text == "")
    ]
    return html_nodes


def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Converts a markdown document into a single `ParentNode` object 
    representing the HTML structure.

    Splits the markdown into blocks, determines the type of each block,
    and creates the corresponding HTML nodes.

    All block nodes are nested under a single `<div>` `ParentNode`.

    Args:
        markdown (str): The input markdown string to be converted.
    Returns:
        ParentNode: A `ParentNode` object representing the HTML structure of the markdown.
    """
    markdown_blocks = markdown_to_blocks(markdown)

    children = []

    for block in markdown_blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                children.append(ParentNode(
                    "p", text_to_children(block.replace("\n", " "))))
            case BlockType.CODE:
                # remove the starting and ending ``` from the block
                code_content = block.strip().removeprefix(
                    "```").removesuffix("```").strip() + "\n"
                code_node = TextNode(code_content, TextType.CODE)
                code_html = text_node_to_html_node(code_node)
                children.append(ParentNode("pre", [code_html]))
            case BlockType.HEADING:
                # group the markdown #s and the text separately
                match_heading = re.match(r"^(#{1,6}) (.*)", block)
                if match_heading:
                    # count the number of #s at the start of the block
                    tag = f"h{len(match_heading.group(1))}"
                    heading_text = match_heading.group(2)
                    children.append(ParentNode(
                        tag, text_to_children(heading_text)))
            case BlockType.QUOTE:
                # remove the starting > AND space from the block
                quote_text = [line[2:] if line.startswith(
                    "> ") else line[1:] for line in block.splitlines()]
                quote_text = "\n".join(quote_text)
                quote_children = text_to_children(quote_text)
                children.append(ParentNode("blockquote", quote_children))
            case BlockType.UNORDERED_LIST:
                items = []
                for line in block.splitlines():
                    # remove the starting - AND space from the line
                    item_text = line[2:] if line.startswith("- ") else line
                    items.append(ParentNode("li", text_to_children(item_text)))
                children.append(ParentNode("ul", items))
            case BlockType.ORDERED_LIST:
                items = []
                for line in block.splitlines():
                    # remove the starting number AND dot AND space from the line
                    item_text = re.sub(r"^\s*\d+\.\s+", "", line)
                    items.append(ParentNode("li", text_to_children(item_text)))
                children.append(ParentNode("ol", items))

    return ParentNode("div", children)


def copy_static(src: str, dest: str) -> None:
    """
    Recursively copies the contents of the source directory to the destination directory.

    Deletes all contents of the destination directory before copying.

    Logs each file copied.

    Args:
        src (str): The source directory to copy from.
        dest (str): The destination directory to copy to.
    Returns:
        None
    """

    # check if the destination directory exists and delete if so
    if os.path.exists(dest):
        shutil.rmtree(dest)
        print(f"Deleted existing directory: {dest}")

    # Recursively copy src to dest
    def _copy_recursive(current_src: str, current_dest: str) -> None:
        if not os.path.exists(current_dest):
            os.mkdir(current_dest)
            print(f"Created directory: {current_dest}")
        for entry in os.listdir(current_src):
            src_path = os.path.join(current_src, entry)
            dest_path = os.path.join(current_dest, entry)
            if os.path.isdir(src_path):
                _copy_recursive(src_path, dest_path)
            else:
                shutil.copy(src_path, dest_path)
                print(f"Copied file: {src_path} to {dest_path}")

    _copy_recursive(src, dest)
