import requests

try:
    resp = requests.post('http://localhost:8005/format', files={'resume': ('test.txt', 'John Doe\nPython Developer\nExp: 5 years'), 'template': ('test.docx', b'P1\nP2\nP3')})
    print(resp.status_code)
    print(resp.text)
except Exception as e:
    print(e)