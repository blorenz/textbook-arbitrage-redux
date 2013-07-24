from lxml import html as lhtml
from pyquery import PyQuery as pq
from lxml import etree
import requests
from models import AmazonMongoTradeIn, Amazon_Textbook_Section_NR, Amazon_NR, Price_NR, Book_NR, ProfitableBooks_NR, MetaTable_NR
import re
import tasks


def getROI(theBuy, theSell):
    theBuy = float(theBuy)
    theSell = float(theSell)
    actb = (theBuy - (theSell + 3.99)) / (theSell + 3.99)
    actb = round(actb * 100, 2)
    return actb


def isGoodProfit(obj):
    theBuy = float(obj.latest_price.buy)
    theSell = float(obj.latest_price.sell)
    actb = (theBuy - (theSell + 3.99)) / (theSell + 3.99)
    actb = round(actb * 100, 2)
    if actb >= 50.0:
        return True
    return False


def retrievePage(url, proxy=None):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11", }

    '''if (proxy):
        theProxy = Proxy.objects.order_by('?')[0]
        proxy = {theProxy.proxy_type:theProxy.ip_and_port}
        r = requests.get(url,proxies=proxy,headers=headers)
    else:'''
    r = requests.get(url, headers=headers)
    return r.content


def toAscii(content):
    return unicode(content).encode('ascii', 'ignore')


def createOrUpdateMetaField(keyvalue, value1):
    try:
        obj = MetaTable_NR.objects.get(metakey=keyvalue)
    except MetaTable_NR.DoesNotExist:
        obj = MetaTable_NR(metakey=keyvalue, metatype="INTEGER")
    obj.int_field = value1
    obj.save()


def updateBookCounts():
    createOrUpdateMetaField("totalIndexed", AmazonMongoTradeIn.objects.count())
    createOrUpdateMetaField("totalBooks", AmazonMongoTradeIn.objects.count())
    createOrUpdateMetaField("totalProfitable", ProfitableBooks_NR.objects.all().count())


'''def addProxy(type, proxy):
    p = Proxy(proxy_type=type, ip_and_port=proxy)
    p.save()'''

# thread = ta.models.AmazonMongo.objects.get().fields(slice__prices=-1)


def checkProfitable(a):
    # print a
    price = a.prices[-1]
    if price.buy:
        if price.buy > price.sell:
            b = ProfitableBooks_NR()
            b.amazon = a.amazon
            b.price = price
            b.timestamp = price.timestamp
            b.save()


def getProfitableBooks():
    AmazonMongoTradeIn.objects.all().delete()
    objs = AmazonMongoTradeIn.objects.values_list('id', flat=True)
    tasks.process_lots_of_items_profitable.delay(objs)


def detailAllBooks():
    objs = AmazonMongoTradeIn.objects.values_list('id', flat=True)
    # print 'Objs len is %d' % (len(objs),)
    # print 'ok done with that'
    tasks.process_lots_of_items(objs)


'''
   New Detail book:

   if div#more-buying-choice-content-div
   if children divs == 3
     parse first-child with span.price
     parse third-child with div 2 span
'''
#//div[contains(concat(' ',normalize-space(@class),' '),' result')]


def countBooksInCategory(url):
    '''Counts how may books are in each category, to intelligently scrape the correct number of pages.'''
    print 'counting book in %s' % (url,)
    content = retrievePage(url)
    d = pq(content)

    s = d("#resultCount")
    resultsNoComma = 0

    if len(s):
        txt = s[0].text_content().strip()
        #print txt
        matches = re.search(r'of\s+([,\d]+) Results', txt)

        if matches != None:
            resultsNoComma = re.sub(",", "", matches.group(1))

    return resultsNoComma


# Edited on Apr27
def getAmazonBooksOnTradeinPage(url, page):
    '''Gets all the books on the tradein page'''
    print ('Getting books for ' + url + '&page=' + str(page))
    content = retrievePage("http://amazon.com" + url + "&page=" + str(page))
    d = pq(content)

    s = d('.list.results > div')
    for result in s:
        aa = d('.image a',result)
        title = d('span.lrg.bold',result).text()
        re_product_code = re.compile(r'/dp/(.*?)/')
        pc = re.findall(re_product_code, aa[0].get('href'))

        # print aa
        # print title
        # print pc

        am = AmazonMongoTradeIn()

        book = Book_NR()
        book.pckey = pc[0]
        book.title = title
        book.save()

        amazon = Amazon_NR()
        amazon.book = book
        amazon.productcode = pc[0]
        amazon.save()
        am.amazon = amazon

        price = Price_NR()
        price.save()
        am.latest_price = price
        am.profitable = 0

        am.save()


def getDepartmentContainer(containers):
    for container in containers:
# Selects [New Releases, Departments, ...]
        h2s = container.cssselect("h2")
        for s in h2s:
        #s = container.cssselect("h2")
            print s.text_content()
        #s = container.cssselect("div.narrowItemHeading")
            matches = re.search(r'Department', s.text_content())
            if matches:
                return container
    return None


def getFormatContainer(containers):
    for container in containers:
        s = container.cssselect("div.narrowItemHeading")
        matches = re.search(r'Format', s[0].text_content())
        if matches:
            return container
    return None


# Works on Apr 27
def addFacetToScan(url):
    content = retrievePage(url)

    d = pq(content)

    thecontainer = d('.expand')
    if thecontainer is None:
        return

    currentHeading = d('li strong')
    currentHeading = currentHeading.parent()
    lst = currentHeading.parent()
    children = lst.children('li')
    index = children.index(currentHeading[0])
    s = children[index:]
    s = s[1:]

    #Get all navigable directories
    # s = thecontainer[0].xpath("./li/a/span[@class='refinementLink']")
    # No more to get -- this is a leaf node so add it to scan
    if not len(s):
        # print 'Adding finally!'
        addCategoryToScan(url)

    for cat in s:
    # Get to the anchor tag
        p1 = pq(cat)
        el = p1('a')
        if el:
            tasks.task_addFacetToScan.delay("http://www.amazon.com" + el[0].get('href'))
            # print 'Adding facet %s' % ("http://www.amazon.com" + el[0].get('href'),)
            # addFacetToScan("http://www.amazon.com" + el[0].get('href'))
    # print 'Made it thru!'


# Works on Apr 27
def addCategoryToScan(url):
    content = retrievePage(url)
    html = lhtml.fromstring(content)
    d = pq(content)
    s = d('h1#breadCrumb')
    # s = html.xpath("//h1[@id='breadCrumb']")
    breadcrumb = toAscii(s[0].text_content())

    # print breadcrumb
    # containers = html.xpath(".//*[@id='bestRefinement']")
    containers = d('#bestRefinement > a')
    # thecontainer = getFormatContainer(containers)

    #currently always going here - Apr27
    if containers is None:
        ats = Amazon_Textbook_Section_NR(title=breadcrumb, url=url)
        try:
            ats.save()
        except:
            pass
        return

    # s = thecontainer.xpath(".//div[@class='refinement']")
    for cat in containers:
        el = cat
        if len(el):
            ats = Amazon_Textbook_Section_NR(title=breadcrumb + " " + el.text_content(), url=el.get('href'))
            ats.save()


def scanCategories():
    objs = Amazon_Textbook_Section_NR.objects.all()
    for obj in iter(objs):
        # scanCategoryAndAddBooks(obj)
        tasks.task_scanCategoryAndAddBooks.delay(obj)


def scanCategoryAndAddBooks(cat):
    books = countBooksInCategory(cat.url)
    #print "Counted " + str(books)
    pages = int(books) / 12 + 1
    for i in range(1, pages + 1):
        tasks.scanTradeInPage.delay(cat.url, i)
        # tasks.scanTradeInPage(cat.url,i)


def parseUsedPage(am):
    if not am.latest_price:
        am.price = Price_NR()
    url = 'http://www.amazon.com/gp/offer-listing/%s/ref=dp_olp_used?ie=UTF8&condition=used' % (am.amazon.productcode)
    try:
        content = retrievePage(url)
    except:
        return
    html = lhtml.fromstring(content)
    matches = re.search(r'a \$?(\d*\.\d{2}) Amazon.com Gift Card', html.text_content())
    buyprice = None
    if matches != None:
        buyprice = matches.group(1)

    results = html.xpath("//tbody[@class='result']")

    for result in results:
        if re.search('Acceptable', result.cssselect('.condition')[0].text_content()):
            continue
        if re.search('nternational', result.cssselect('.comments')[0].text_content()):
            continue

        sellprice = re.match('\$?(\d*\.\d{2})', result.cssselect('.price')[0].text_content())
        if sellprice != None and buyprice != None:
            sellprice = sellprice.group(1)

            price = Price_NR(buy=buyprice, sell=sellprice)
        else:
            price = Price_NR()

        #am.prices.append(price)
        am.latest_price = price

        if price.buy and price.sell:
            roi = getROI(price.buy, price.sell)
            if roi:
                am.profitable = roi
            else:
                am.profitable = 0
        am.save()
        #print result.cssselect('.condition')[0].text_content()
        break


def fetchPage(url, add):
    content = retrievePage(url)
    # f = open('/home/seocortex/dropbox/web/static/testing-' + add + '.html', 'w')
    # f.write(content)
    # f.close()
