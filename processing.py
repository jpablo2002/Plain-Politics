import requests
import json
import datetime


api_key = "nZioH35K5X3dPlPZCBjKhACC9CPU5ChXNvIXMCMh"

def formatDate(date: datetime.datetime) -> str:
  formatted = str(date).split(' ')[0]
  return formatted

class Bill():
    def __init__(self, summary: str, committee) -> None:
        self.summary = summary
        self.committee = committee

to_date = formatDate(datetime.datetime.now())
from_date = formatDate(datetime.datetime.now() - datetime.timedelta(days=1))

response = requests.get(f"https://api.govinfo.gov/published/{from_date}/{to_date}?offset=0&pageSize=100&collection=BILLS&api_key={api_key}")

packages = response.json()["packages"]

bill_list = []
#List of Bill Objects

for package in packages:
	bill_committees = []
	link = package["packageLink"]
	info = requests.get(f"{link}?api_key={api_key}")
	for committee in info.json()["committees"]:
		bill_committees.append(committee["committeeName"])
	bill_list.append(Bill(info.json()["title"], bill_committees))

print(bill_list[0].summary)