import functions_framework
import mysql.connector
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
    sql = 'SELECT * FROM mydb WHERE title = %s'
    args = ['%' + search + '%']
    cursor.execute(sql, args)
    mydb.commit()
