from textnode import TextNode, TextType

def main():
    tnode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(tnode)


if __name__ == "__main__":
    main()