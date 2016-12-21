import urllib2;
import re
import bs4;
import urlparse
from Queue import Queue
from pageRank import AlexaTrafficRank


list_of_sites= set();
dynamic = Queue();


class crawler:
    Alexa = {};
    def __init__(self):
        self.Alexa = AlexaTrafficRank();
    def getPage(self,link):
        
        try:
            domain = urlparse.urlparse(link).hostname
            rank = str(self.Alexa.get_rank(link))
            
            print ( domain , link , rank)
            
        except UnicodeEncodeError,UnicodeDecodeError:
            print 'can not encode'
        
        html = urllib2.urlopen(link).read()
        soup = bs4.BeautifulSoup(html,'lxml')
        
        return html;
    
    def getLink(self,page):
        soup = bs4.BeautifulSoup(page,'lxml');
        soup = bs4.BeautifulSoup(page,'lxml');
        link = soup.find_all('a',{'href' : re.compile('http')});
        for i in link:
            newLink=i.attrs['href'];
            if newLink not in list_of_siteslist_of_sites.add(urlparse.urlparse(newLink).hostname)
                dynamic.put(newLink);
                
                    
    def crawl(self,page='http://www.xtnote.com/*'):
        k=0;
        dynamic.put(page);
        print not dynamic.empty()
        while not dynamic.empty():
            front = dynamic.get();
            k+=1;
            #try:
            page = self.getPage(front);
            #except MySQLdb.Error, e:
            #print "MySQL Error ",e
            #continue
            print "K = ",k;
            self.getLink(page);
c = crawler();
c.crawl('http://www.politico.com/tipsheets/morning-money/2016/05/pro-morning-money-214471');