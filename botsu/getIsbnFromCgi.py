#!/usr/bin/python3
import cgi
import openbd_api

ISBN = 0

ISBN = cgi.FieldStorage()
ErrorMsg = []

if len(ISBN) != 13 or len(ISBN) != 10:
    ErrorMsg.append("ERROR")

## 途中