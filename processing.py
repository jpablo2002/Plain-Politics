import requests
import json
import datetime

def formatDate(date: datetime.datetime) -> str:
  formatted = str(date).split(' ')[0]
  return formatted

to_date = formatDate(datetime.datetime.now())
from_date = formatDate(datetime.datetime.now() - datetime.timedelta(days=1))

response = requests.get(f"https://api.govinfo.gov/published/{from_date}/{to_date}?offset=0&pageSize=100&collection=BILLS&api_key=nZioH35K5X3dPlPZCBjKhACC9CPU5ChXNvIXMCMh")

bills = response.json()["packages"]

bill_info = []
titles = []

for bill in bills:
	link = bill["packageLink"]
	info = requests.get(f"{link}?api_key=nZioH35K5X3dPlPZCBjKhACC9CPU5ChXNvIXMCMh")
	for committee in info.json()["committees"]:
		bill_info.append(committee["committeeName"])
	titles.append(info.json()["title"])

print(titles)
print(bill_info)