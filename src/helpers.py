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
