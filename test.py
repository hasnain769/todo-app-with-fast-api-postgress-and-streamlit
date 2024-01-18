import requests
r = requests.post('127.0.0.1:8000/signup' ,json={"name":"admin" , "email":"admin@a.com" ,"password":"password"})
print(r.status_code)