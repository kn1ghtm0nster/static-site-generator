from textnode import TextNode
from helpers import copy_static, generate_page


def main():
    copy_static("static", "public")

    generate_page(from_path="content/index.md",
                  template_path="template.html", dest_path="public/index.html")


if __name__ == "__main__":
    main()
