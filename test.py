import requests
email ="moni@gmail.com"
password ="aaaa9999"
r = requests.post('http://127.0.0.1:8000/login' ,json={"email":email ,"password":password})
print(r.status_code)