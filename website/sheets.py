import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)


sheet = client.open("eventRegistration").sheet1
canceledSheet = client.open("eventRegistrationCanceled").sheet1 

def getSpotsLeft():
    spots_left = 151 - len(sheet.col_values(1))
    return spots_left

def addToSheets(fN,lN,afl,confInt,email,phoneNum,accom,address,zip,date):
    addRow = [fN,lN,afl,confInt,email,phoneNum,accom,address,zip,date]
    sheet.append_row(addRow)

def checkEmail(email):
    return str(sheet.find(email)) != 'None'

def deleteSpot(email):
    cell = str(sheet.find(email))
    row = int(cell[7])
    wholeRow = sheet.row_values(row)
    sheet.delete_row(row)
    canceledSheet.append_row(wholeRow)

def checkIn(email):
    cell = sheet.find(email)
    sheet.update('K'+str(cell.row),'Yes')
