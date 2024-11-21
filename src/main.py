from textnode import TextNode, TextType
from filefunctions import update_files
def main():
    files_updated = update_files("static", "public")
    if len(files_updated) == 0:
        print(f"{files_updated} - updated")
    else:
        print("failed to update")


if __name__ == "__main__":
    main()
