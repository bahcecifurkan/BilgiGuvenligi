__author__ = 'furkanb'

from sgmllib import SGMLParser
import sys, urllib, httplib, re, urllib2, sets, socket

#LFI Acigi kodu
LFI = "../../../../../../../../../../../../etc/passwd"


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

#Uyumlu url'leri yazdir
for url in urls:
    print("Uyumlu URL",url)
