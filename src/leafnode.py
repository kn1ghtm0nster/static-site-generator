from htmlnode import HTMLNode


class LeafNode(HTMLNode):

    def __init__(self, tag: str, value: str, props: dict = None) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("leaf node must have a value")

        if self.tag is None:
            return self.value

        props = self.props_to_html()

        if props:
            return f"<{self.tag} {props}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
