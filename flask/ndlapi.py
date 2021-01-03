#!/usr/bin/python3
import requests as req
import sys
from bs4 import BeautifulSoup


req.packages.urllib3.disable_warnings()
req.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'


def searchByISBN(isbn):
    url = 'https://iss.ndl.go.jp/api/sru?operation=searchRetrieve&query=isbn=' + \
        str(isbn)
    res = req.get(url, verify=False)
    res = BeautifulSoup(res.text, 'lxml')
    res = res.records.find('recorddata')
    if res is None:
        res = None

    else:
        res = BeautifulSoup(res.text, 'lxml')

    # title = res.find('dc:title').text
    # author = res.find('dc:creator').text
    # publisher = res.find('dc:publisher').text

    return res


def searchByTitle(title):  # WIP
    url = 'https://iss.ndl.go.jp/api/sru?operation=searchRetrieve&query=title=' + \
        str(title)
    res = req.get(url, verify=False)
    res = BeautifulSoup(res.text, 'lxml')
    # res = res.records.find('recorddata')
    # res = BeautifulSoup(res.text, 'lxml')

    # title = res.find('dc:title').text
    # author = res.find('dc:creator').text
    # publisher = res.find('dc:publisher').text

    return res


if __name__ == '__main__':
    query = sys.argv[1]
    print(searchByISBN(query))
