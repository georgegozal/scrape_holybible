import json
import requests
from bs4 import BeautifulSoup
from alive_progress import alive_bar

from book_titles_and_chapters import books


url = "https://holybible.ge/geo/bible/%E1%83%90%E1%83%AE%E1%83%90%E1%83%9A\
    %E1%83%98-%E1%83%92%E1%83%90%E1%83%93%E1%83%90%E1%83%9B%E1%83%A3%E1%83%\
    A8%E1%83%90%E1%83%95%E1%83%94%E1%83%91%E1%83%A3%E1%83%9A%E1%83%98-%E\
    1%83%92%E1%83%90%E1%83%9B%E1%83%9D%E1%83%AA%E1%83%94%E1%83%9B%E1%83%90-2015/{}/{}/0/0/1"


# goes through each chapter for each book
def get_book(num, book_name, chapter, filename="full_bible.json"):
    full_dict = {}
    full_dict[book_name] = {}
    full_dict[book_name][f"{chapter}_თავი"] = {}
    try:
        r = requests.get(
            "http://localhost:8050/render.html",
            params={
                "url": url.format(num, chapter),
                "wait": 2
            }
        )
        soup = BeautifulSoup(r.text, 'html.parser')
        # get all chapter verses
        verses = soup.findAll(class_='bible-text bible-text-v1')
        verses_text = [item.text for item in verses]
        # print(book_name, chapter, verses_text[0])
    except IndexError:
        pass
        # print(book_name, chapter, verses_text[0])

    for item in verses_text:
        items = item.split()
        index = int(items[0])
        text = " ".join(items[1:])
        full_dict[book_name][f"{chapter}_თავი"][index] = text

    try:
        # Open the JSON file for reading
        with open(filename, 'r') as f:
            # Load the JSON data into a Python variable
            data = json.load(f)

        try:
            data[book_name][f"{chapter}_თავი"] = full_dict[book_name][f"{chapter}_თავი"]
        except KeyError:
            data[book_name] = {}
            data[book_name][f"{chapter}_თავი"] = {}
            data[book_name][f"{chapter}_თავი"] = full_dict[book_name][f"{chapter}_თავი"]

        # Open the JSON file for writing
        # Writing to sample.json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except FileNotFoundError:
        # Open the JSON file for writing
        # # Writing to sample.json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(full_dict, f, ensure_ascii=False, indent=4)


def run():
    for index, value in enumerate(books, 4):
        with alive_bar(value[0], title='Downloading Bible Text') as bar:
            for i in range(1, value[0] + 1):
                get_book(num=index, book_name=value[1], chapter=i)
                bar.text = f"{value[1]}: {i} თავი ⇣"
                bar()


if __name__ == "__main__":
    run()
