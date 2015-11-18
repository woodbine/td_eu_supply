from splinter import Browser
from bs4 import BeautifulSoup
import time 
import random
import scraperwiki


def replacetext(text):
    text = text.replace("\t", "")
    text = text.replace("\n", "")
    text = text.replace("\u", " ")
    text = text.strip(" ")
    return text

def formatdate1(date):
    date = replacetext(date)
    date.strip(" ")
    liste = date.split("/")
    date = liste[2].strip(" ") + "-" + liste[1].strip(" ") + "-" + liste[0].strip(" ")
    return date

def formatdate2(date):
    date = replacetext(date)
    liste = date.split("/")
    l = liste[2].split(" ")
    year = l[0]
    date = year.strip(" ") + "-" + liste[1].strip(" ") + "-" + liste[0].strip(" ")
    return date

def  get_url(el, link):
    a = el.find('a')
    href = a.get('href')
    l = link.split("/")
    url = l[0] + "//" + l[2] + href
    return url

def NumberPage(browser):
    htmltext = BeautifulSoup(browser.html, "html.parser")
    table = htmltext.find('ul',{'class':'ctm-pager-info'})
    text = table.text
    l = text.split(" ")
    return int(l[1])


def page_details(browser, link):
    htmltext = BeautifulSoup(browser.html, "html.parser")
    table = htmltext.find('table',{'class':'table table-striped table-bordered sorter'})
    tbody = table.find('tbody')
    tends = tbody.findAll('tr')
    for tend in tends:
        col = tend.findAll('td')
        try:
            RFT_ID = col[0].text.encode('ascii','ignore')
        except:
            RFT_ID = ""
        try:
            REFERENCE = col[1].text.encode('ascii','ignore')
        except:
            REFERENCE = ""
        try:
            NAME = col[2].text.encode('ascii','ignore')
        except:
            NAME = ""
        try:
            URL = get_url(col[2], link)
        except:
            URL = ""
        try:
            DATE_OF_PUBLICATION = col[3].text.encode('ascii','ignore')
        except:
            DATE_OF_PUBLICATION = ""
        try:
            DATE_OF_PUBLICATION_clean = formatdate1(DATE_OF_PUBLICATION)
        except:
            DATE_OF_PUBLICATION_clean = ""
        try:
            RESPONSE_DEADLINE = col[4].text.encode('ascii','ignore')
        except:
            RESPONSE_DEADLINE = ""
        try:
            RESPONSE_DEADLINE_clean = formatdate2(RESPONSE_DEADLINE)
        except:
            RESPONSE_DEADLINE_clean
        try:
            PROCESS = col[5].text.encode('ascii','ignore')
        except:
            PROCESS = ""
        try:
            BUYERS = col[6].text.encode('ascii','ignore')
        except:
            BUYERS = ""
        try:
            COUNTRIES = col[7].text.encode('ascii','ignore')
        except:
            COUNTRIES = ""


        data = {"RFT_ID" : unicode(RFT_ID) ,\
            "REFERENCE": unicode(REFERENCE) ,\
            "NAME": unicode(NAME), \
            "URL": unicode(URL), \
            "DATE_OF_PUBLICATION": unicode(DATE_OF_PUBLICATION), \
            "DATE_OF_PUBLICATION_clean": unicode(DATE_OF_PUBLICATION_clean), \
            "RESPONSE_DEADLINE": unicode(RESPONSE_DEADLINE), \
            "RESPONSE_DEADLINE_clean": unicode(RESPONSE_DEADLINE_clean), \
            "PROCESS": unicode(PROCESS), \
            "BUYERS": unicode(BUYERS), \
            "COUNTRIES": unicode(COUNTRIES)}

        scraperwiki.sqlite.save(unique_keys=['RFT_ID'], data = data )


def Navigation(link):
    with Browser("phantomjs", service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any']) as browser:
        browser.driver.set_window_size(1280, 1024)
        browser.visit(link)
        num_page = NumberPage(browser)
        for i in range(num_page):
            page_details(browser, link)
            time.sleep(random.uniform(0.5,2.9))
            button = browser.find_by_css("i[class='icon-forward']")
            button.click()

def main():
    urls = [
        "https://nhssbs.eu-supply.com/ctm/supplier/publictenders?b=NHSSBS",
        "https://uk.eu-supply.com/ctm/supplier/publictenders?B=UK",
        "https://uk.eu-supply.com/ctm/supplier/publictenders?B=BLUELIGHT",
        "https://uk.eu-supply.com/ctm/Supplier/PublicTenders",
        "https://tactica-live.advanced365.com/ctm/Supplier/PublicTenders"
        ]

    for link in urls:
        Navigation(link)




if __name__ == '__main__':
    main()