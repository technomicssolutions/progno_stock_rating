import urllib2
from lxml import etree
from io import StringIO, BytesIO

import urllib
from lxml.html import fromstring
from lxml import cssselect 
import csv, xlwt

month = {
	'01': 'JAN',
	'02': 'FEB',
	'03': 'MAR',
	'04': 'APR',
	'05': 'MAY',
	'06': 'JUN',
	'07': 'JUL',
	'08': 'AUG',
	'09': 'SEP',
	'10': 'OCT',
	'11': 'NOV',
	'12': 'DEC'
}
from datetime import datetime
 #url = 'http://microformats.org/'
# content = urllib.urlopen(url).read()
# doc = fromstring(content)
# doc.make_links_absolute(url)

# print dir(page)
# print type(page.read())
# page = page.read()
# parser = etree.HTMLParser()
# xml = etree.parse(page, parser)
# print page
# doc = fromstring(page)
# # xml = etree.
# print dir(doc.get_element_by_id('replacetext'))
# print doc.cssselect('div[class="download"]')
# site = "http://www.nseindia.com/products/content/equities/equities/homepage_eq.htm"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive',
       'Vary':'User-Agent'
      }
base_url = "http://www.nseindia.com/content/historical/EQUITIES/" #2014/OCT/cm29OCT2014bhav.csv.zip"
date = datetime.now().date()
directory = str(date.year)+"/"+month[str(date.month)]+"/"
filename = "cm"+str(date.day)+month[str(date.month)]+str(date.year)+"bhav.csv.zip"
url = base_url+directory+filename
site=url
req = urllib2.Request(site, headers=hdr)
file_name = url.split('/')[-1]
page = urllib2.urlopen(req)

f = open(file_name, 'wb')
meta = page.info()
file_size = int(meta.getheaders("Content-Length")[0])
print "Downloading: %s Bytes: %s" % (file_name, file_size)

file_size_dl = 0
block_sz = 8192
while True:
    buffer = page.read(block_sz)
    if not buffer:
        break

    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print status,

f.close()

import zipfile

zf = zipfile.ZipFile(filename, 'r')
print zf.namelist()
csv_file = zf.namelist()[0]
zf.extract(csv_file, '.')

f=open(csv_file, 'rb')
g = csv.reader ((f), delimiter=";")
wbk= xlwt.Workbook()
sheet = wbk.add_sheet("Sheet 1")

for rowi, row in enumerate(g):
    for coli, value in enumerate(row):
        sheet.write(rowi,coli,value)

wbk.save(csv_file + '.xls')