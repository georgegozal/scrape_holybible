import json
from alive_progress import alive_bar
from book_titles_and_chapters import books
from bible2015_v2 import get_book


def add_books_and_chapters(empty_book_list, data):
    for book in data.keys():
        chapters = data[book]
        for chapter in chapters.keys():
            chapter_data = chapters[chapter]
            if len(chapter_data) == 0:
                empty_book_list.append([chapter.split('_')[0], book])
    # print(len(empty_book_list)) # 63 chapter was empty
    if len(empty_book_list) != 0:
        print(f"Empty chapters found. {len(empty_book_list)}...")
        for value in empty_book_list:
            for item in books:
                if value[1] == item[1]:
                    value.append(item[2])
    else:
        print("No empty chapters found.")


def read_json(filename='full_bible.json'):
    empty_book_list = []

    with open(filename, 'r') as f:
        # Load the JSON data into a Python variable
        data = json.load(f)

    if len(data) != 66:
        # print(data.keys())
        for book in books:
            if book[1] not in data.keys():
                # print(book[1])
                data[book[1]] = {}
                for chapter in range(1, book[0] + 1):
                    data[book[1]][f"{chapter}_თავი"] = {}
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        add_books_and_chapters(empty_book_list, data)
    else:
        add_books_and_chapters(empty_book_list, data)
    return empty_book_list


def fill_empty_chapters(empty_book_list):
    with alive_bar(len(empty_book_list)) as bar:
        for value in empty_book_list:
            get_book(
                num=value[2],
                book_name=value[1],
                chapter=value[0],
                filename="full_bible.json"
                )
            bar.text = f"{value[1]}: {value[0]} თავი ⇣"
            bar()


def run():
    while True:
        empty_book_list = read_json()
        # print(empty_book_list)
        if len(empty_book_list) != 0:
            print("Filling empty chapters...")
            fill_empty_chapters(empty_book_list)
        else:
            break


if __name__ == "__main__":
    print("Scanning JSON file for empty chapters...")
    run()
    print("Done.")
