from flask import Flask
app = Flask(__name__)
import csv
import json

@app.route('/')
def hello():
    return "Ping"

@app.route('/tc-health-inspection/v1/')
def tc_health_inspection_root():
    # show the user profile for that user
    return 'Ping'

@app.route('/tc-health-inspection/v1/county')
def counties():
    # show counties
    response = ''
    with open('C:\\Users\\jdunn1\\git\\tc-health-inspections-api\\counties.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row_json = json.dumps(row)
            if response != '':
                response = response + "," + row_json
            else:
                response = row_json
    response = '[' + response + ']'
    return response

@app.route('/tc-health-inspection/v1/county/<countyname>')
def county(countyname):
    # show a county
    response = ''
    with open('C:\\Users\\jdunn1\\git\\tc-health-inspections-api\\counties.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["CountyName"] == countyname:
                response = json.dumps(row)
                break 
    response = '[' + response + ']'
    return response
    # show the health inspections for that county

@app.route('/tc-health-inspection/v1/failedfirstinspection')
def failed_first_inspections():
    # show failed inspections
    response = ''
    with open('C:\\Users\\jdunn1\\git\\tc-health-inspections-api\\failed_first_inspection.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row_json = json.dumps(row)
            if response != '':
                response = response + "," + row_json
            else:
                response = row_json
    response = '[' + response + ']'
    return response

@app.route('/tc-health-inspection/v1/failedfirstinspection/county/<countyname>')
def failed_first_inspection_county(countyname):
    # show failed inspection for county
    response = ''
    with open('C:\\Users\\jdunn1\\git\\tc-health-inspections-api\\failed_first_inspection.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (row["CountyName"] == countyname) or (row["CountyValue"] == countyname):
                response = json.dumps(row)
                break
    response = '[' + response + ']'
    return response

@app.route('/tc-health-inspection/v1/failedfirstinspection/business/<businessname>')
def failed_first_inspection_business(businessname):
    # show failed inspection for business
    response = ''
    with open('C:\\Users\\jdunn1\\git\\tc-health-inspections-api\\failed_first_inspection.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print (businessname)
            if row["Name"] == businessname:
                response = json.dumps(row)
                break
    response = '[' + response + ']'
    return response

if __name__ == '__main__':
    app.run()