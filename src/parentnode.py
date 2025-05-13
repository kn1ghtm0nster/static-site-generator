from htmlnode import HTMLNode


class ParentNode(HTMLNode):

    def __init__(self, tag: str, children: list, props: dict = None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("parent node must have a tag")

        if self.children is None:
            raise ValueError("children nodes must be provided")

        children_html = "".join(child.to_html() for child in self.children)

        props = self.props_to_html()

        if props:
            return f'<{self.tag} {props}>{children_html}</{self.tag}>'
        return f'<{self.tag}>{children_html}</{self.tag}>'
