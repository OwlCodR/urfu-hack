from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

FORMS_SPREADSHEET_ID = '1I2iQj0QlDhvUw-313wvLI_7LXiTLSlqwo38URr3R5q8'
TABLE_SPREADSHEET_ID = '1OMjENvfDnax3xV9saBWAbM111KxTskO-CBaNUTYfQTk'
SAMPLE_RANGE = '!A1:CC'
SERVICE_ACCOUNT_FILE = 'internship-311710.json'

def getService():
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
    return build('sheets', 'v4', credentials=creds)


def getSheetName(id):
    name = getService().spreadsheets().get(spreadsheetId=id, fields='sheets(properties(title))').execute()
    print(name['sheets'][0]['properties']['title'])
    return name['sheets'][0]['properties']['title']


def getValues(id, custom_range):
    sheets = getService().spreadsheets()
    result = sheets.values().get(spreadsheetId=id, range=custom_range).execute()
    return result.get('values', [])


def updateTable():
    valuesForm = getValues(FORMS_SPREADSHEET_ID, getSheetName(FORMS_SPREADSHEET_ID) + SAMPLE_RANGE)
    valuesTable = [['' for i in range(len(valuesForm))] for j in range(len(valuesForm[0]))]
    printValues(valuesForm)

    for i in range(len(valuesForm)):
        for j in range(len(valuesForm[i])):
            valuesTable[j][i] = valuesForm[i][j]
    setData(TABLE_SPREADSHEET_ID, valuesTable)


def printValues(values):
    if not values:
        print('No data found.')
        return

    for row in values:
        print(row)


def appendData(id, values):
    body = {
        'values': values
    }
    result = getService().spreadsheets().values().append(
        spreadsheetId = id, 
        range = SAMPLE_RANGE,
        valueInputOption = 'RAW', 
        body = body
    ).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


def setData(id, values):
    body = {
        'values': values
    }
    result = getService().spreadsheets().values().update(
        spreadsheetId = id, 
        range = SAMPLE_RANGE,
        valueInputOption = 'RAW', 
        body = body
    ).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


def main():

    service = getService()

    sheets = service.spreadsheets()

    printValues(getValues(TABLE_SPREADSHEET_ID, getSheetName(TABLE_SPREADSHEET_ID) + SAMPLE_RANGE))
    
    updateTable()


if __name__ == '__main__':
    main()