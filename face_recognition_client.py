import requests

url = "http://127.0.0.1:8000/recognize"
files = {"file": open("Face-recognition-bug-fixes/Images/hien.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
