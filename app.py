import os
import argparse
import sys
from datetime import datetime

from flask import Flask
from flask import request

from notion.client import *
from notion.block import *

app = Flask(__name__)



# ?fields=status,date,bullshit&values=

@app.route('/generic', methods=['POST'])
def genericRequest():
    content = request.json
    print(content.keys())
    print(content.values())
    return { "success": True }


def setMultipleValues(row, key, value):
    values = []
    for val in value:
        values.append(val)
        try:
            setattr(row, key, values)
        except:
            pass

# to create new task in sprint

@app.route('/createSprintTask', methods=['POST'])
def createSprintTask():
    json = request.json
    token_v2 = os.environ.get("TOKEN")
    client = NotionClient(token_v2)

    url = json['url']
    cv = client.get_collection_view(url)
    title = json['title']
    jira_link = json['jira_link']

    currentRows = cv.collection.get_rows(search=jira_link)
    for currentRow in currentRows:
        if getattr(row,'jira_link') == jira_link:
            return f'Ticket {jira_link} already present on Notion. Skipped'

    row = cv.collection.add_row()

    for key in json.keys():
        if key not in ['url']:
            try:
                if type(json[key]) is list:
                    setMultipleValues(row,key,json[key])
                else:
                    setattr(row, key, json[key])
            except Exception as e:
                print(e)
    return f'Added {title} to Notion'





@app.route('/editSprintTask', methods=['POST'])
def editSprintTask():
    json = request.json
    token_v2 = os.environ.get("TOKEN")
    client = NotionClient(token_v2)

    url = json['url']
    cv = client.get_collection_view(url)

    ticket = json['ticket']
    jira_link = 'https://quikrjira.quikrcorp.com/browse/' + ticket

    rows = cv.collection.get_rows(search=jira_link)
    print(rows)
    for row in rows:
        if getattr(row,'jira_link') == jira_link:
            for key in json.keys():
                if key not in ['url','ticket','jira_link']:
                    try:
                        if type(json[key]) is list:
                            setMultipleValues(row,key,json[key])
                        else:
                            setattr(row, key, json[key])
                    except Exception as e:
                        print(e)
    return f'Edited {ticket} in Notion'




if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
