"""
module contains helper functions for the project
"""
import re

from textnode import TextNode, TextType


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
