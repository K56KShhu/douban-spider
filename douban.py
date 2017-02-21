import csv
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.error import HTTPError
# another wat of sorting
from operator import itemgetter


def getBooksInfo(tag):
    bookList = []
    pageNumber = 0

    headers = [{"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"},
               {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"},
               {"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0"},
               {"user-agent": "Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0"}]

    while True:
        time.sleep(1.5)
        url = "https://book.douban.com/tag/" + quote(tag) + "?start=" + str(pageNumber * 20)
        pageNumber += 1

        try:
            r = requests.get(url, headers=headers[pageNumber % len(headers)])
        except HTTPError as e:
            print(e)

        bs0bj = BeautifulSoup(r.text, "lxml")
        booksInOnePage = bs0bj.find("div", {"id":"subject_list"})

        print(pageNumber)
        stop = bs0bj.find("p", {"class":"pl2"}).get_text()
        if stop == "没有找到符合条件的图书":
            break
        for book in booksInOnePage.findAll("li", {"class":"subject-item"}):
            title = book.find("h2").get_text()
            try:
                ratingNums = book.find("span", {"class":"rating_nums"}).get_text()
            except:
                ratingNums = '0'
            try:
                comments = book.find("span", {"class":"pl"}).get_text()
            except:
                comments = '0'
            try:
                pubInfo = book.find("div", {"class":"pub"}).get_text()
            except:
                pubInfo = ' '

            bookList.append([title, ratingNums, comments, pubInfo])

    return booksCleaner(bookList)


def booksCleaner(dirtyBooks):
    tidyBooks = []
    for dirtyBook in dirtyBooks:
        # title
        M = []
        cleanTitle = dirtyBook[0].replace(" ", "").replace("\n", "")
        M.append(cleanTitle)
        # ratingNums
        cleanRatingNums = dirtyBook[1].strip()
        M.append(cleanRatingNums)
        # comments
        cleanComments = dirtyBook[2].strip(' (人评价)\n少于')
        M.append(cleanComments)
        # pubInfo
        pub = dirtyBook[3].split('/')
        author = ' '.join(pub[0:-3]).strip()
        M.append(author)
        others = ' '.join(pub[-3:]).strip()
        M.append(others)
        tidyBooks.append(M)
    
    return tidyBooks


def printSortedBooks(books):
#    for book in sorted(books, key=itemgetter(2), reverse=True):
    for book in sorted(books, key=lambda t: int(t[2]), reverse=True):
        print(book)
        

def saveToCsv(books, tag):
    filename = "books_" + tag + ".csv"
    path = "/home/xu/a-project/books-doubanSpider/" + filename
    with open(path, "w") as f:
        try:
            writer = csv.writer(f)
            writer.writerow(["name", "rating", "comments", "author/translator", "pub"])
            for book in books:
                writer.writerow(book)
        finally:
            f.close()
        

begin = time.time()

tag = "童话"
bookList = getBooksInfo(tag)
printSortedBooks(bookList)
saveToCsv(bookList, tag)

end = time.time()
time = end - begin
print("time: " + str(time))
