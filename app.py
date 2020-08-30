import os
import argparse
import sys
import json
from datetime import datetime

from flask import Flask
from flask import request

from notion.client import *
from notion.block import *

app = Flask(__name__)



def setMultipleValues(row, key, value):
    values = []
    for val in value:
        values.append(val)
        try:
            setattr(row, key, values)
        except:
            pass




@app.route('/createSprintTask', methods=['POST'])
def createSprintTask():
    jsonRequest = request.json
    token_v2 = os.environ.get("TOKEN")
    collectionUrl = os.environ.get("NOTION_SPRINT_COLLECTION_URL")

    client = NotionClient(token_v2)
    cv = client.get_collection_view(collectionUrl)

    title = jsonRequest['title']
    jira_link = jsonRequest['jira_link']

# Check if ticket is already present in Notion. Skip if present. Else continue
    currentRows = cv.collection.get_rows(search=jira_link)
    for currentRow in currentRows:
        if getattr(currentRow,'jira_link') == jira_link:
            responseMessage = "Ticket " + jira_link + " already present on Notion"
            return json.dumps({'message': responseMessage, 'success': True, 'type': "skipped", 'row': currentRow.id})

    row = cv.collection.add_row()

# For every key in the createSprintTask request (except the ones added in list below), set value in the newly created row
    for key in jsonRequest.keys():
        if key not in ['collectionUrl']:
            try:
                if type(jsonRequest[key]) is list:
                    setMultipleValues(row,key,jsonRequest[key])
                else:
                    setattr(row, key, jsonRequest[key])
            except Exception as e:
                print(e)
    responseMessage = "Added " + title + " to Notion"
    return json.dumps({'message': responseMessage, 'success': True, 'type': "created", 'row': row.id})




@app.route('/editSprintTask', methods=['POST'])
def editSprintTask():
    jsonRequest = request.json
    token_v2 = os.environ.get("TOKEN")
    jira_host = os.environ.get("JIRA_HOST")
    collectionUrl = os.environ.get("NOTION_SPRINT_COLLECTION_URL")

    client = NotionClient(token_v2)
    cv = client.get_collection_view(collectionUrl)

    ticket = jsonRequest['ticket']
    jira_link = jira_host + '/browse/' + ticket

# Find rows in Notion with matching jira_link, verify exact match of jira_link, and then update every key in the editRequest (except the ones in the exlusion list below)
    rows = cv.collection.get_rows(search=jira_link)
    for row in rows:
        if getattr(row,'jira_link') == jira_link:
            for key in jsonRequest.keys():
                if key not in ['ticket','jira_link']:
                    try:
                        if type(jsonRequest[key]) is list:
                            setMultipleValues(row,key,jsonRequest[key])
                        else:
                            setattr(row, key, jsonRequest[key])
                    except Exception as e:
                        print(e)
    responseMessage = "Edited " + ticket + " in Notion"
    return json.dumps({'message': responseMessage, 'success': True, 'type': "edited", 'row': row.id})




@app.route('/genericCreateEntry', methods=['POST'])
def genericCreateEntry():
    jsonRequest = request.json
    token_v2 = os.environ.get("TOKEN")
    collectionUrl = jsonRequest['collectionUrl']

    client = NotionClient(token_v2)
    cv = client.get_collection_view(collectionUrl)

    title = jsonRequest['title']

    row = cv.collection.add_row()

# For every key in the genericCreateEntry request (except the ones added in list below), set value in the newly created row
    for key in jsonRequest.keys():
        if key not in ['collectionUrl']:
            try:
                if type(jsonRequest[key]) is list:
                    setMultipleValues(row,key,jsonRequest[key])
                else:
                    setattr(row, key, jsonRequest[key])
            except Exception as e:
                print(e)
    responseMessage = "Added " + title + " to Notion"
    return json.dumps({'message': responseMessage, 'success': True, 'type': "created", 'row': row.id})





@app.route('/genericEditEntry', methods=['POST'])
def genericEditEntry():
    jsonRequest = request.json
    token_v2 = os.environ.get("TOKEN")
    collectionUrl = jsonRequest['collectionUrl']
    searchQuery = jsonRequest['searchQuery']
    findBy = jsonRequest['findBy']

    client = NotionClient(token_v2)
    cv = client.get_collection_view(collectionUrl)

# Find rows in Notion with matching searchQuery, verify exact match with findBy, and then update every key in the genericEditEntry (except the ones in the exlusion list below)
    rows = cv.collection.get_rows(search=searchQuery)
    for row in rows:
        if getattr(row,findBy) == searchQuery:
            for key in jsonRequest.keys():
                if key not in ['collectionUrl','searchQuery']:
                    try:
                        if type(jsonRequest[key]) is list:
                            setMultipleValues(row,key,jsonRequest[key])
                        else:
                            setattr(row, key, jsonRequest[key])
                    except Exception as e:
                        print(e)
    responseMessage = "Edited " + row.title + " in Notion"
    return json.dumps({'message': responseMessage, 'success': True, 'type': "edited", 'row': row.id})





if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
