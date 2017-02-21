from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
# another wat of sorting
# from operator import itemgetter
import csv


def getBooksInfo(tag):
    bookList = []
    pageNumber = 0

    while True:
        url = "https://book.douban.com/tag/" + quote(tag) + "?start=" + str(pageNumber * 20)
        pageNumber += 1
        html = urlopen(url)
        bs0bj = BeautifulSoup(html, "lxml")
        booksInOnePage = bs0bj.find("div", {"id":"subject_list"})
        print(pageNumber)
        if pageNumber > 20:
            break
        if booksInOnePage == None:
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

            L = []
            L.append(title)
            L.append(ratingNums)
            L.append(comments)
            L.append(pubInfo)
            bookList.append(L)

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
        cleanComments = dirtyBook[2].strip(' (人评价)\n')
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
#   for book in sorted(books, key=itemgetter(1), reverse=True):
    for book in sorted(books, key=lambda t: t[1], reverse=True):
        print(book)
        



bookList = getBooksInfo("童话")
printSortedBooks(bookList)
