import time
import requests
from lxml import html
from threading import Thread


def get_tree(url):
    r = requests.get(url)
    tree = html.fromstring(r.text)
    return tree


def get_movies():
    xpath_title = '//div[@class="article"]//div[@class="hd"]//span[@class="title"][1]/text()'
    movies = []

    def foo(url):
        tree = get_tree(new_link)
        for title in tree.xpath(xpath_title):
            movies.append(title)

    threads = []
    for i in range(10):
        new_link = "https://movie.douban.com/top250?start=" + str(25*i)
        t = Thread(target=foo, args=[new_link])
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    

    for i, movie in enumerate(movies, 1):
        print(i, movie)


def main():
    begin = time.time()
    get_movies()
    end = time.time()
    print("cost {}" .format((end - begin)))


if __name__ == '__main__':
    main()

