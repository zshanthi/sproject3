from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.request import Request
from scrapy import signals
from urlparse import urlparse
import re
import scrapy
import os.path



class Quotes14spider(CrawlSpider):
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'BOT_NAME' : 'Chrome Browser',
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'DEPTH_LIMIT' : 3,
        'LOG_LEVEL' : 'INFO',
        'COOKIES_ENABLED' : False,
        'RETRY_ENABLED' : False,
        'DOWNLOAD_TIMEOUT' : 15,
        'REDIRECT_ENABLED' : True,
        'HTTPERROR_ALLOW_ALL' : True
      }
    name = "quotes14"
    urlsfilename = '/var/www/html/sprojects/tutorial/tutorial/spiders/urls.txt'
    alreadyfilename = '/var/www/html/sprojects/tutorial/tutorial/spiders/already.txt'
    newdomainsfilename = '/var/www/html/sprojects/tutorial/tutorial/spiders/newdomains.txt'
    emailfilename = '/var/www/html/sprojects/tutorial/tutorial/spiders/email.txt'
    emailfoundurls = '/var/www/html/sprojects/tutorial/tutorial/spiders/emailfoundurls.txt'
    progressfilename = '/var/www/html/sprojects/tutorial/tutorial/spiders/progress.txt'
    totalpagesperdomain = 100
    counter = {}
    emailfound = {}
    start_urls = []
    allowed_domains = []
    already_urls = []
    hostnamesofstarturls = {}
    newdomains = []
    hahaemails = []
    emailurls = []
   
 
    #start_urls = ['http://www.101cgi.com','https://www.washingtonpost.com/'];
    #start_url = 'http://www.yahoo.com'


    rules = (
        Rule(
            SgmlLinkExtractor(allow_domains=()),
            callback='parse_page', process_request='cprocess_request', follow=True
        ),
    )
 
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Quotes14spider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider



    def spider_closed(self, spider):
        
       self.cfilewrite(self.alreadyfilename,self.already_urls)
       self.cfilewrite(self.newdomainsfilename,self.newdomains)
       self.cfilewrite(self.emailfilename,self.hahaemails)
       self.cfilewrite(self.emailfoundurls,self.emailurls)
       spider.logger.info('Spider closed: %s', spider.name)
  
    def spider_opened(self, spider):
     with open(self.urlsfilename) as f:
      self.start_urls = f.read().splitlines()
     self.start_urls = list(set(self.start_urls))
     if os.path.isfile(self.alreadyfilename):
      with open(self.alreadyfilename) as f:
       self.already_urls = f.read().splitlines()
     if os.path.isfile(self.newdomainsfilename):
      with open(self.newdomainsfilename) as f:
       self.newdomains = f.read().splitlines() 
     if os.path.isfile(self.emailfoundurls):
      with open(self.emailfoundurls) as f:
       self.emailurls = f.read().splitlines()
     self.start_urls = list(set(self.start_urls) - set(self.already_urls)-set(self.newdomains)-set(self.emailurls))
     for r in self.start_urls:
          #print r
          self.hostnamesofstarturls[urlparse(r).hostname] = r
          self.counter[urlparse(r).hostname] = 0
          self.allowed_domains.append(urlparse(r).hostname)
     
     if os.path.isfile(self.emailfilename):
      with open(self.emailfilename) as f:
       self.hahaemails = f.read().splitlines()
     
     spider.logger.info('Spider opened: %s', spider.name)
 
    def __init__(self, category=None, *args, **kwargs):
         super(Quotes14spider, self).__init__(*args, **kwargs)
         #self.start_urls.append('http://www.101cgi.com/')
         
    
    def parse_start_url(self, response):
        
        return self.parse_page(response)
  
    def cprocess_request(self,request):
      upp = urlparse(request.url)
      hh = upp.hostname
      if (hh in self.counter):
       self.counter[hh]= self.counter[hh] + 1
      else:
       self.counter[hh] = 1
      newdomain = '{uri.scheme}://{uri.netloc}/'.format(uri=upp)
      soli = 0
      for fg in self.counter:
       if self.counter[fg] > 0:
        soli=soli+1
      if (soli % 100 == 0):
       thefile = open(self.progressfilename, 'w')
       for fg in self.counter:
        if self.counter[fg] > 0:
         if fg in self.hostnamesofstarturls:
          fg = self.hostnamesofstarturls[fg]
         thefile.write("%s\n" % fg)
       self.cfilewrite(self.alreadyfilename,self.already_urls)
       self.cfilewrite(self.newdomainsfilename,self.newdomains)
       self.cfilewrite(self.emailfilename,self.hahaemails)
       self.cfilewrite(self.emailfoundurls,self.emailurls)
   
    
      if (hh not in self.hostnamesofstarturls):
       if (newdomain not in self.newdomains):
         self.newdomains.append(newdomain)
      else:
       if (self.hostnamesofstarturls[hh] not in self.already_urls):
        self.already_urls.append(self.hostnamesofstarturls[hh])
    
      if (hh not in self.counter or (self.counter[hh] > self.totalpagesperdomain) or hh in self.emailfound):
       return None
      else:
      
   
       return request
 
    def start_requests(self):
     for r in self.start_urls:
         request = Request(r)
         
         yield request
  
    def parse_page(self, response):
     hh = urlparse(response.url).hostname
        # with open(self.urlsfilename, 'ab') as f:
                # f.write(response.url + '\n')
     # if (hh in self.counter):
      # self.counter[hh]= self.counter[hh] + 1
     # else:
      # self.counter[hh] = 1
     if (self.extractemail(response)):
       self.emailfound[hh] = 1
    
   

    def extractemail(self,response):
     upp = urlparse(response.request.url)
     hh = upp.hostname
     newdomain = '{uri.scheme}://{uri.netloc}/'.format(uri=upp)
     #emails = re.findall(r'[A-Za-z0-9_\-\.]+@[A-Za-z0-9_\-]+\.([A-Za-z0-9_\-][A-Za-z0-9_\.]+)', response.body)
     #emails = re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", response.body)
     # GOOD ONE but not for capitals emails = re.findall(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",response.body)
     emails = re.findall(r"(?:[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[A-Za-z0-9-]*[A-Za-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",response.body)
     #"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
   
     if len(emails) > 0:
      if (emails[0] not in self.hahaemails):
         self.hahaemails.append(emails[0])
      if (hh in self.hostnamesofstarturls):
        if (self.hostnamesofstarturls[hh] not in self.emailurls):
           self.emailurls.append(self.hostnamesofstarturls[hh])
      else:
        if (newdomain not in self.emailurls):
          self.emailurls.append(newdomain)
      return True
     else:
      return False
    
    def cfilewrite(self,file,contentarray):
     thefile = open(file, 'w')
     for item in contentarray:
      thefile.write("%s\n" % item)
 # https://stackoverflow.com/questions/35748061/how-to-stop-scrapy-spider-after-certain-number-of-requests
  