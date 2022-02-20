import mysql.connector
import datetime
import requests


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

to_date = formatDate(datetime.datetime.now())
from_date = formatDate(datetime.datetime.now() - datetime.timedelta(days=10))

response = requests.get(f"https://api.govinfo.gov/published/{from_date}/{to_date}?offset=0&pageSize=100&collection=BILLS&api_key={api_key}")

packages = response.json().get("packages", [])

bill_list = []
#List of Bill Objects

for package in packages:
    link = package.get("packageLink")
    if link is None:
        continue
    try:
        info = requests.get(f"{link}?api_key={api_key}")
        bill_list.append(info.json())
    except requests.exceptions.RequestException as err:
        print("Something went wrong: {}".format(err))

    # text_link = dic.get("download").get("txtLink")
    # text_content = requests.get(f"{text_link}?api_key={api_key}").content
    # soup = BeautifulSoup(text_content, 'html.parser')
    # text = soup.pre.contents
    # bill_list.append(dic["title"], text[0], dic["detailsLink"], dic["packageId"])

for bill in bill_list:
    try:
        if bill is None:
            continue
        elif any(bill.get(key) is None for key in bill):
            continue
        mycursor = mydb.cursor()

        short_title = bill.get("shortTitle")
        short_title = short_title[0].get("title") if short_title is not None else bill.get('title')
        sql = "INSERT INTO BILLCOMMITIES (`bill_id`, `title`, `text_link`, `bill_link`) VALUES (%s, %s, %s, %s)"
        val = (bill.get("billNumber"), short_title, bill.get("download").get("txtLink"), bill.get("detailsLink"))
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))