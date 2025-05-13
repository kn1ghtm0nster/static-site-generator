import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):

    def setUp(self):
        self.grand_child = LeafNode(tag="span", value="Grandchild", props={
                                    "class": "grandchild"})
        self.child = ParentNode(
            tag="p", children=[self.grand_child], props={"class": "child"})
        self.parent = ParentNode(tag="div", children=[
                                 self.child], props={"class": "parent"})

    def test_to_html_with_children(self):
        expected_html = '<div class="parent"><p class="child"><span class="grandchild">Grandchild</span></p></div>'
        self.assertEqual(self.parent.to_html(), expected_html)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_without_props(self):
        parent_node = ParentNode("div", [self.child])
        expected_html = "<div><p class=\"child\"><span class=\"grandchild\">Grandchild</span></p></div>"
        self.assertEqual(parent_node.to_html(), expected_html)

    def test_to_html_without_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [self.child]).to_html()

    def test_to_html_without_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()
