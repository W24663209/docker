import requests

get = requests.get("http://111.229.107.110:8087/ende/system/msmCode/login?telephone=15086183103&_=1589513760181")
print(get.text)
