from src.functions import get_pages, get_page_links, writeJson

def main():
    PAGES = get_pages()
    for page in PAGES:
        writeJson(get_page_links(page))
    print("Finished")

if __name__ == "__main__":
    main()