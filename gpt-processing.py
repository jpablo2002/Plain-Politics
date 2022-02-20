import re
from urllib import response
from urllib.request import Request
import summary_repositories
import requests
import os
import openai
from summary_repositories import insert_to_table2
import time



def compress_bills() -> None:
    bill_links = summary_repositories.get_links()
    bills = []
    for bill_link in bill_links:
        res = requests.get(url=bill_link[1])
        if len(res.text) < 10000:
            issue = gpt3_request(res.text)
            issue = issue.lstrip()
           # bills.append((bill_link[0], issue))
            insert_to_table2((bill_link[0], issue))
            print(str((bill_link[0], issue)))
            time.sleep(1)

   # return bills


def gpt3_request(text: str) -> str:
    openai.api_key = ""

    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt='Which one of the following: "Foreign Issues", "Social Issues", "Economic Issues" best describes this United States Congress bill: \n ' + text,
        temperature=0.4,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

    return response.to_dict()['choices'][0]['text']


    

        
