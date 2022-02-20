import mysql.connector
import datetime
from pprint import pprint
import requests
import json
from bs4 import BeautifulSoup

# mydb = mysql.connector.connect(
#     host="34.139.89.202",
#     user="plainpolitics",
#     password="AH+PS@SN*rZ]%GAp^LXU>TH7aw{bQ/f3",
#     database="plain-politics"
# )

# mycursor = mydb.cursor()

# mycursor.execute("SHOW DATABASES")

api_key = "nZioH35K5X3dPlPZCBjKhACC9CPU5ChXNvIXMCMh"

def formatDate(date: datetime.datetime) -> str:
    formatted = str(date).split(' ')[0]
    return formatted

class Bill():
    summary: str
    committee: list
    link: str
    def __init__(self, summary: str, committee: list, link: str, id: str) -> None:
        self.summary = summary
        self.text = committee
        self.link = link
        self.id = id

to_date = formatDate(datetime.datetime.now())
from_date = formatDate(datetime.datetime.now() - datetime.timedelta(days=1))

response = requests.get(f"https://api.govinfo.gov/published/{from_date}/{to_date}?offset=0&pageSize=100&collection=BILLS&api_key={api_key}")

packages = response.json()["packages"]

bill_list = []
#List of Bill Objects

for package in packages:
    link = package["packageLink"]
    info = requests.get(f"{link}?api_key={api_key}")
    dic = info.json()
    text_link = dic["download"]["txtLink"]
    text_content = requests.get(f"{text_link}?api_key={api_key}").content
    soup = BeautifulSoup(text_content, 'html.parser')
    text = soup.pre.contents
    print(text)
    bill_list.append(Bill(dic["title"], text, dic["detailsLink"], dic["packageId"]))



# for bill in bill_list:
#     mycursor = mydb.cursor()

#     sql = "INSERT INTO BILLCOMMITIES (billId, title, summary, ) VALUES (%s, %s)"
#     val = ("John", "Highway 21")
#     mycursor.execute(sql, val)

#     mydb.commit()

#     print(mycursor.rowcount, "record inserted.")
