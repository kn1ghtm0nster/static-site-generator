from textnode import TextNode


def main():
    dummy_node = TextNode("This is some anchor text",
                          "link", "https://www.google.com")
    print(dummy_node)


if __name__ == "__main__":
    main()
