"""import requests

r = requests.get(
    "http://127.0.0.1:8000/popas/5",
    params={
        "kaktus": "1893418",
        #"stars": 2
            }
)
print(r.text)"""

from users.models import User

user = User(name="John", password="1234", number="123456789")