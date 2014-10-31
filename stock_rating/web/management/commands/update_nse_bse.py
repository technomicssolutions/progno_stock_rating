
import urllib2
import csv, xlwt
import zipfile
import os

from django.db.models import Q
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand

from web.models import Company, NSEBSEPrice

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

class Command(BaseCommand):
    help = "Download NSE BSE price and update to db"

    def handle(self, *args, **options):
        get_nse_price()
        get_bse_price()


def get_bse_price():
    date = datetime.now().date()
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    base_url = "http://www.bseindia.com/download/BhavCopy/Equity/" #2014/OCT/cm29OCT2014bhav.csv.zip"
    bse_file = "EQ"+str(date.day)+str(date.month)+date.strftime('%y')+'_CSV.ZIP'
    url = base_url+bse_file
    print url
    req = urllib2.Request(url, headers=hdr)

    page = urllib2.urlopen(req)

    f = open(bse_file, 'wb')
    meta = page.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (bse_file, file_size)

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

    f.close()
    zf = zipfile.ZipFile(bse_file, 'r')
    csv_file = zf.namelist()[0]
    zf.extract(csv_file, '.')
    f=open(csv_file, 'rb')
    g = csv.reader ((f), delimiter=",")
    r = -1
    latest_pr = None
    for rowi, row in enumerate(g):
        r = r + 1
        if r > 0:
            c=-1
            for coli, value in enumerate(row):
                c = c + 1
                if c == 0:
                    bse_code = value
                if c == 7:
                    close_price = value
                    try:
                        company = Company.objects.get(BSE_code = bse_code)
                        try:
                            try:
                                last = NSEBSEPrice.objects.get(company=company, last_review=True)
                                last.last_review = False;
                                last.save()
                            except:
                                pass
                            latest_pr = NSEBSEPrice.objects.get(company=company, latest=True)
                            latest_pr.latest = False
                            latest_pr.last_review = True
                            latest_pr.save()
                        except:
                            pass
                        price, created = NSEBSEPrice.objects.get_or_create(company=company, date=date)
                        price.BSE_price = close_price
                        price.latest = True
                        if latest_pr:
                            price.parent = latest_pr
                        price.save()
                    except Exception as ex:
                        print str(ex)
                        pass
    os.remove(bse_file)
    os.remove(csv_file)

def get_nse_price():
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    base_url = "http://www.nseindia.com/content/historical/EQUITIES/" #2014/OCT/cm29OCT2014bhav.csv.zip"
    date = datetime.now().date()
    directory = str(date.year)+"/"+month[str(date.month)]+"/"
    filename = "cm"+str(date.day)+month[str(date.month)]+str(date.year)+"bhav.csv.zip"
    url = base_url+directory+filename
    req = urllib2.Request(url, headers=hdr)
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

    f.close()
    zf = zipfile.ZipFile(filename, 'r')
    csv_file = zf.namelist()[0]
    zf.extract(csv_file, '.')
    f=open(csv_file, 'rb')
    g = csv.reader ((f), delimiter=",")
    r = -1
    latest_pr = None
    for rowi, row in enumerate(g):
        r = r + 1
        if r > 0:
            c=-1
            for coli, value in enumerate(row):
                c = c + 1
                if c == 5:
                    close_price = value
                if c == 12:
                    isin = value
                    try:
                        company = Company.objects.get(isin_code = isin)
                        try:
                            condition = NSEBSEPrice.objects.get(~Q(date=date), company=company, latest=True)
                            if condition:
                                last = latest_pr = NSEBSEPrice.objects.get(company=company, last_review=True)
                                last.last_review = False;
                                last.save()
                                latest_pr = NSEBSEPrice.objects.get(company=company, latest=True)
                                latest_pr.latest = False
                                latest_pr.last_review = True
                                latest_pr.save()
                        except:
                            pass
                        price, created = NSEBSEPrice.objects.get_or_create(company=company, date=date)
                        price.company = company
                        price.NSE_price = close_price
                        if latest_pr:
                            price.parent = latest_pr
                        price.latest = True
                        price.save()
                    except Exception as ex:
                        print str(ex)
                        pass
    os.remove(filename)
    os.remove(csv_file)