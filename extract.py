#!/usr/bin/env python
# coding: utf-8

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import csv

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)
    
def scrapeDetailsPage(link):
    raw_link = simple_get(link)
    htmlSouped = BeautifulSoup(raw_link, 'html.parser')
    return(htmlSouped)
  
def extractDetailAddress(htmlSouped):
    storeDivs = htmlSouped.find_all('div', class_ = 'tab_detail_inner')
    for x in storeDivs[0].find_all('ul'):
        for y in x.find_all('li'):
            if y.text.startswith('Business:'):
                #print('Found business'+y.text.replace('Business: ','').replace('\t',''))
                business = y.text.replace('Business: ','').replace('\t','').replace('\n',' ').replace('  ',' ')
                                   
    return business

def failedInspections(countyName,countyValue,ff_writer):
    
    raw_html = simple_get('https://data.tcpalm.com/restaurant-inspections/' + countyValue + '/')
    html = BeautifulSoup(raw_html, 'html.parser')

    containers = html.find_all('div', class_ = 'panel panel-danger')
    first_rest = containers[0]
    counter=0
    
    for b in first_rest.find_all('ul'):
        for c in b.find_all('li', class_ = 'list-group-item bot-dotted'):
            counter = counter + 1
            #print('Found LI'+str(c))
            #print(c.h5)
            businessName = c.a.text.replace('\n','')
            violation = c.span.text.replace('\n','')
            date = c.p.br.nextSibling

            url = "https://data.tcpalm.com"+c.a['href']
            # get the detail page
            detailHTMLSouped = scrapeDetailsPage(url)
            #print(detailHTMLSouped)
            businessAddress = extractDetailAddress(detailHTMLSouped).rstrip(' ').rstrip('.')
            print(businessName)
            print(date)
            print(violation)
            print(businessAddress)
            print()
            ff_writer.writerow([businessName, date, violation, businessAddress, countyName, countyValue])

            #if counter>5:
                #break
       
    return

raw_html_cty = simple_get('https://data.tcpalm.com/restaurant-inspections/st-lucie/')
html_cty = BeautifulSoup(raw_html_cty, 'html.parser')

cty_file = open('counties_stage.csv',mode='w')
cty_writer = csv.writer(cty_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
cty_writer.writerow(['CountyName', 'CountyValue'])

ff_file = open('failed_first_inspection_stage.csv',mode='w')
ff_writer = csv.writer(ff_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
ff_writer.writerow(['Name', 'Date', 'Violation', 'Address', 'CountyName', 'CountyValue'])
    
containers = html_cty.find_all('select', class_ = 'form-control')
first_list = containers[0]

counter = 0
for b in first_list.find_all('option'):
    print(b['value'])
    failedInspections(b.text, b['value'],ff_writer)
    counter=counter+1    
    #if counter == 2:
        #break
ff_file.close()  

for b in first_list.find_all('option'):
    print(b.text)
    cty_writer.writerow([b.text,b['value']])
cty_file.close()        
