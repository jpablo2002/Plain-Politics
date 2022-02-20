import functions_framework
import requests
import json
from pprint import pformat
import datetime

@functions_framework.http
def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
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
            self.committee = committee
            self.link = link

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
        bill_list.append(Bill(info.json()["title"], bill_committees, info.json()["detailsLink"]))
    return f'{bill_list[0].link}'