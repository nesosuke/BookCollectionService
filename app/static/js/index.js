import axios from 'axios';

const baseurl = 'http://localhost:5000';
async function findBookinfo() {
    const isbn = document.forms.inputISBN.isbn.value;
    const url = baseurl + '/book/' + isbn;
    const bookinfo = await fetch(url).then(response => response.json());

    const title = bookinfo['title'];
    const bookisbn = bookinfo['isbn'];
    document.getElementById('booktitle').textContent = title;
    document.getElementById('bookisbn').textContent = bookisbn;
}

async function updateReadingStatus() {
    const status = document.forms.updateStatus.status.value;
    const isbn = document.getElementById('bookisbn').textContent
    const uid = 'neso'
    const url=baseurl+'/status'
    const data={
        'isbn': isbn,
        'status': status,
        'uid': uid
    };
    const jsondata = JSON.stringify(data);
    console.log(jsondata);
    axios.post(url, jsondata)
}
