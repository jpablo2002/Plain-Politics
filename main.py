import functions_framework
import mysql.connector
from flask import jsonify
import requests
import json
from pprint import pformat
import datetime

mydb = mysql.connector.connect(
    host="34.139.89.202",
    user="plainpolitics",
    password="AH+PS@SN*rZ]%GAp^LXU>TH7aw{bQ/f3",
    database="plain-politics"
)


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
    search = request.args.get("search")

    cursor = mydb.cursor()
    sql2 = "SELECT bill_id, title, bill_link, blob_link FROM BILLCOMMITIES JOIN categories ON BILLCOMMITIES.id = categories.id WHERE " \
           "categories.categories = %s "
    val = (search,)
    cursor.execute(sql2, val)

    columns = ["bill_id", "title", "text_link", "blob_link"]
    result = []
    for row in cursor:
        drow = {}
        for i in range(len(columns)):
            drow[columns[i]] = row[i]
        result.append(drow)
    return jsonify(result)
