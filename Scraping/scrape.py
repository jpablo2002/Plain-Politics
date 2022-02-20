import mysql.connector
import datetime
from pprint import pprint
import requests
import json

mydb = mysql.connector.connect(
    host="34.139.89.202",
    user="plainpolitics",
    password="AH+PS@SN*rZ]%GAp^LXU>TH7aw{bQ/f3",
    database="plain-politics"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

print(mycursor)

api_key = "nZioH35K5X3dPlPZCBjKhACC9CPU5ChXNvIXMCMh"

def formatDate(date: datetime.datetime) -> str:
    formatted = str(date).split(' ')[0]
    return formatted

class Bill():
    summary: str
    committee: list
    link: str
    def __init__(self, summary: str, committee: list, link: str) -> None:
        self.summary = summary
        self.text = committee
        self.link = link

to_date = formatDate(datetime.datetime.now())
from_date = formatDate(datetime.datetime.now() - datetime.timedelta(days=1))

response = requests.get(f"https://api.govinfo.gov/published/{from_date}/{to_date}?offset=0&pageSize=100&collection=BILLS&api_key={api_key}")

packages = response.json()["packages"]

bill_list = []
#List of Bill Objects

for package in packages:
    texts = []
    link = package["packageLink"]
    info = requests.get(f"{link}?api_key={api_key}")
    texts.append(info.json()["download"]["xmlLink"])
    bill_list.append(Bill(info.json()["title"], texts, info.json()["detailsLink"]))
