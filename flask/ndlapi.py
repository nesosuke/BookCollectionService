#!/usr/bin/python3
import requests as req
import sys
from bs4 import BeautifulSoup


req.packages.urllib3.disable_warnings()
req.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'


def searchNDL(query):
    if str.isdecimal(query) is True and (len(query) == 10 or len(query) == 13):
        url = 'https://iss.ndl.go.jp/api/opensearch?' \
            + 'isbn=' + str(query)
    else:
        count = 3
        url = 'https://iss.ndl.go.jp/api/opensearch?' \
            + 'cnt=' + str(count) + '&' \
            + 'title=' + str(query)

    res = req.get(url, verify=False)
    res = BeautifulSoup(res.text, 'lxml')
    res = res.channel.find('item')

    # if res is not None:
    #     title = res.find('dc:title').text
    #     author = res.find('dc:creator').text
    #     publisher = res.find('dc:publisher').text
    #     isbn = res.find('dc:identifier').text

    return res

if __name__ == '__main__':
    query = sys.argv[1]
    print(searchNDL(query))
