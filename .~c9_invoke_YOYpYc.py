import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib2
import urllib;
import re
import bs4;
import urlparse
from Queue import Queue
from pageRank import AlexaTrafficRank
from test import DataBase
from craw_phan import css_prop
from color import catColor
"""
header={
    "Host": "www.xtnote.com",
    "Proxy-Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Save-Data": "on",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":" gzip, deflate, sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "Chrome-Proxy": "s=CjUKEwjNkJKzzonQAhULrmgKHdO5DH8SDAi23-vABRCFlIebAhoQCg5zdGFibGVfZGVmYXVsdBJIMEYCIQC66avOkF48BbVSysFSWa6tc-v2FbwRuQ1d2gJ9xl3ANAIhAKtdeEhTPwAViHL56tY3R78XjXwWsHehWXZUkBLJABRZ, c=linux, b=2840, p=59"
}
header = {
    "Host":"www.xtnote.com",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"en-US,en;q=0.8",
    "Cache-Control":"max-age=0",
    "Save-Data":"off",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
};


            pdata = urllib.urlencode(header)
            print pdata
            req = urllib2.Request(link, pdata)
            print req
"""

list_of_domain = set();
list_dom = ["twitter.com","facebook.com","t.com","f.com","google.com"]
for i in list_dom:
    list_of_domain.add(i);
list_of_sites = set();
dynamic = Queue();


class crawler:
    
    #DATA
    Alexa = {};
    db = {};
    color = {};
    
    def __init__(self):
        self.Alexa = AlexaTrafficRank();
        self.db = DataBase();
        self.cato = catColor(setLevel = 8, levelDiv = 32);
        self.html = {};
        
    def cleanDomain(self, x):
        if(x==None):
            return "google.com"
        y = x.split('.')
        domain = y[-2]+ '.' + y[-1]
        return domain
        
    #------------------ REQUEST PAGE -------------------------
    def getPage(self,link):
        html = "";
        try:
            try:
                domain = self.cleanDomain(urlparse.urlparse(link).hostname);
            except Error,e:
                print link,e.info()
            rank = self.Alexa.get_rank(link)
            
            print ( domain , link , rank)
            #print list_of_domain
            if domain not in list_of_domain:
                list_of_domain.add(domain)
                row={}
                row["url"]=link;
                row["domain"]=domain;
                row["color_data"]=self.PhanOut(link);
                row["ranks"]= -1 if rank == None else rank;
                if(lrow["color_data"]>1):
                    self.db.insert(row);
                html = self.html;
            
        except urllib2.HTTPError, e:
            print e.code,e.info()
            return "";
            
        return html;
    
    #------------------ EXTRACT LINK FROM PAGE -------------------------
    def getLink(self,page):
        count = 0;
        
        soup = bs4.BeautifulSoup(page,'lxml');
        link = soup.find_all('a',{'href' : re.compile('http')});
        
        for i in link:
            newLink=i.attrs['href'];
            domain = urlparse.urlparse(newLink).hostname
        
            if newLink not in list_of_sites:
                list_of_sites.add(newLink)
                dynamic.put(newLink);
                
                    
    def crawl(self,link='http://www.w3school.com/'):
        k=0;
        
        dynamic.put(link);
        
        while not dynamic.empty():
            
            front = dynamic.get();
            try:
                
                k+=1;
                page = self.getPage(front);
                
            except urllib2.HTTPError, e:
                print "HTML Error ",link
                continue
            
            print "K = ",k;
            self.getLink(page);
            
    
    def PhanOut(self,link):
        sets = {}
        try:
            self.color = css_prop(link,"colorOnly");
            self.html = self.color.getPage();
            sets = self.color.collect();
            print sets;
            color = list(sets);
            color_set = set();
            for i in color:
                print i, '==>', self.cato.cat(i)
                color_set.add(self.cato.cat(i));
        except selenium.common.exceptions.WebDriverException,e:
            print e;
            return [];
        return Lcolor_set;
        
        
c = crawler();
c.crawl("http://xtnote.com/*");