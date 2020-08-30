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
    json = request.jsons
    token_v2 = os.environ.get("TOKEN")
    client = NotionClient(token_v2)

    url = request.args.get('url')
    cv = client.get_collection_view(url)

    title = request.args.get('title')

    row = cv.collection.add_row()
    row.title = title
    row.jira_link = request.args.get('jira_link')
    row.status = request.args.get('status')
    row.priority = request.args.get('priority')
    row.assignee = request.args.get('assignee')
    row.dev_owner = request.args.get('dev_owner')
    row.qa_owner = request.args.get('qa_owner')
    row.labels = request.args.get('labels')

    return f'Added {title} to Notion'





@app.route('/editSprintTask', methods=['POST'])
def editSprintTask():
    json = request.json
    token_v2 = os.environ.get("TOKEN")
    client = NotionClient(token_v2)

    url = request.args.get('url')
    cv = client.get_collection_view(url)

    jiraId = request.args.get('jiraId')
    return f'Edited {jiraId} in Notion'

#TODO fix below things
"""
    assert row in cv.collection.get_rows(search=jiraId)
    assert row.title = request.args.get('title')
    assert row.status = request.args.get('status')
    assert row.priority = request.args.get('priority')
    assert row.assignee = request.args.get('assignee')
    assert row.dev_owner = request.args.get('dev_owner')
    assert row.qa_owner = request.args.get('qa_owner')
    assert row.labels = request.args.get('labels')# fix above things

    return f'Edited {jiraId} in Notion'
"""
# fix above things




if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
