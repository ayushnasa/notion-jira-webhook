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






# to create new task in sprint

@app.route('/createSprintTask', methods=['POST'])
def createSprintTask():
    json = request.json
    token_v2 = os.environ.get("TOKEN")
    client = NotionClient(token_v2)

    url = json['url']
    print(json)

    cv = client.get_collection_view(url)

    title = json['title']
    print(title)


    row = cv.collection.add_row()
    row.title = title
    row.jira_link = json['jira_link']
    row.status = json['status']
    row.priority = json['priority']
    row.assignee = json['assignee']
    row.dev_owner = json['dev_owner']
    row.qa_owner = json['qa_owner']
    try:
        row.labels = json['labels']
    except Exception as e:
        pass
    return f'Added {title} to Notion'





@app.route('/editSprintTask', methods=['POST'])
def editSprintTask():
    json = request.json
    token_v2 = os.environ.get("TOKEN")
    client = NotionClient(token_v2)

    url = json['url']
    cv = client.get_collection_view(url)

    jiraId = json['jiraId']
    return f'Edited {jiraId} in Notion'

#TODO fix below things
"""
    assert row in cv.collection.get_rows(search=jiraId)
    assert row.title = json['title']
    assert row.status = json['status']
    assert row.priority = json['priority']
    assert row.assignee = json['assignee']
    assert row.dev_owner = json['dev_owner']
    assert row.qa_owner = json['qa_owner']
    assert row.labels = json['labels')# fix above thing]

    return f'Edited {jiraId} in Notion'
"""
# fix above things




if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
