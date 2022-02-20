import mysql.connector
import datetime
import requests
from bs4 import BeautifulSoup


mydb = mysql.connector.connect(
    host="34.139.89.202",
    user="plainpolitics",
    password="AH+PS@SN*rZ]%GAp^LXU>TH7aw{bQ/f3",
    database="plain-politics"
)

api_key = "nZioH35K5X3dPlPZCBjKhACC9CPU5ChXNvIXMCMh"

def formatDate(date: datetime.datetime) -> str:
    formatted = str(date).split(' ')[0]
    return formatted

class Bill():
    summary: str
    committee: list
    link: str
    def __init__(self, title: str, summary: str, link: str, id: str) -> None:
        self.title = title
        self.summary = summary
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
    bill_list.append(Bill(dic["title"], text, dic["detailsLink"], dic["packageId"]))

for bill in bill_list:
    mycursor = mydb.cursor()

    sql = "INSERT INTO BILLCOMMITIES (title, summary, link, billId) VALUES (%s, %s, %s, %s)"
    val = (bill.title, bill.summary, bill.link, bill.id)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")