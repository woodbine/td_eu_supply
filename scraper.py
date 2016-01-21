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
            RESPONSE_DEADLINE_clean = ""
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

        browser.visit(URL)
        htmlsoup = BeautifulSoup(browser.html, "html.parser")
        details = htmlsoup.find('frame', title='tender_details')

        NEW_URL = URL.encode('utf-8').split('/app')[0] + details['src']
        print NEW_URL
        browser.visit(NEW_URL)
        htmlsoup = BeautifulSoup(browser.html, "html.parser")

        try:
            SHORT_DESCRIPTION = htmlsoup.find('span', text="Short description").findNext('br').text
        except:
            SHORT_DESCRIPTION = ""
        try:
            DESCRIPTION = htmlsoup.find('span', text="Detailed description").findNext('br').text
        except:
            DESCRIPTION = ""

        clean_string = ['\xc2\xa0\xc2\xa0', '  ', '<br/>', '</br>', '</']
        try:
            CPV_CODES = htmlsoup.find('span', text="CPV codes").findNext('br')
            CPV_CODES = str(CPV_CODES).replace('\n', ': ').strip('<br>')
            for s in clean_string:
                CPV_CODES = CPV_CODES.replace(s, '')
            CPV_CODES = CPV_CODES.split('<br>')
            CPV_CODES = [x.encode('ascii','ignore') for x in CPV_CODES]
        except:
            CPV_CODES = ""
        try:
            ADDRESS = (htmlsoup.find('td', rowspan="3").findNext('span', {"class":"celllbl"}).findNext('br').text).strip('View profile')
        except:
            ADDRESS = ""
        try:
            CONTACT = htmlsoup.find('td', rowspan="3").findNext('span', {"class":"celllbl"}).findNext('span', {"class":"celllbl"}).findNext('br').contents
        except:
            CONTACT = ''
        try:
            CONTACT_NAME = CONTACT[0]#.encode('utf-8')
        except:
            CONTACT_NAME = ''
        try:
            CONTACT_DETAILS = CONTACT[1].text.replace('\n', '')
            CONTACT_DETAILS = CONTACT_DETAILS.replace('  ', '')
            CONTACT_DETAILS = CONTACT_DETAILS.replace('-', '')
            CONTACT_PHONE = (CONTACT_DETAILS.replace('Phone: ', ''))[:16]
            if not str(CONTACT_PHONE).find('www') == -1:
                CONTACT_PHONE = ''
        except:
            CONTACT_PHONE = ''


        data = {"RFT_ID" : unicode(RFT_ID).strip(),
                "REFERENCE": unicode(REFERENCE).strip(),
                "NAME": unicode(NAME).strip(),
                "URL": unicode(URL).strip(),
                "DATE_OF_PUBLICATION": unicode(DATE_OF_PUBLICATION).strip(),
                "DATE_OF_PUBLICATION_clean": unicode(DATE_OF_PUBLICATION_clean).strip(),
                "RESPONSE_DEADLINE": unicode(RESPONSE_DEADLINE).strip(),
                "RESPONSE_DEADLINE_clean": unicode(RESPONSE_DEADLINE_clean).strip(),
                "PROCESS": unicode(PROCESS).strip(),
                "BUYERS": unicode(BUYERS).strip(),
                "DESCRIPTION": unicode(DESCRIPTION),
                "SHORT_DESCRIPTION": unicode(SHORT_DESCRIPTION),
                "COUNTRIES": unicode(COUNTRIES),
                "CPV_CODES": unicode(CPV_CODES),
                "ADDRESS": unicode(ADDRESS),
                "CONTACT_NAME": unicode(CONTACT_NAME),
                "CONTACT_PHONE": unicode(CONTACT_PHONE)}

        scraperwiki.sqlite.save(unique_keys=['RFT_ID'], data = data )


def Navigation(link):
    with Browser("phantomjs", service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any']) as browser:
        browser.driver.set_window_size(1280, 1024)
        browser.visit(link)
        num_page = NumberPage(browser)
        for i in range(num_page):
            page_details(browser, link)
            time.sleep(random.uniform(0.5,2.9))
            browser.visit(link)
            button = browser.find_by_css("i[class='icon-forward']")
            button.click()

        browser.visit(link)
        browser.select('SearchFilter.PublishType', '2')
        browser.click_link_by_partial_text('Search')
        time.sleep(random.uniform(0.5,2.9))

        num_page = NumberPage(browser)
        for i in range(num_page):
            page_details(browser, link)
            time.sleep(random.uniform(0.5,2.9))
            browser.visit(link)
            button = browser.find_by_css("i[class='icon-forward']")
            button.click()



def main():
    urls = [
        #"https://nhssbs.eu-supply.com/ctm/supplier/publictenders?b=NHSSBS",\
        #"https://uk.eu-supply.com/ctm/supplier/publictenders?B=UK",\
        #"https://uk.eu-supply.com/ctm/supplier/publictenders?B=BLUELIGHT",\
        "https://uk.eu-supply.com/ctm/Supplier/PublicTenders",\
        "https://tactica-live.advanced365.com/ctm/Supplier/PublicTenders",
        #"https://eu.eu-supply.com/ctm/supplier/publictenders?B="
    ]

    for link in urls:
        Navigation(link)




if __name__ == '__main__':
    main()
