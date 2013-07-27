# Create your views here.
from django.shortcuts import render_to_response
from .models import *
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpRequest, HttpResponse
from celery.task.sets import TaskSet
from django.db.models import F
import tasks
from amazon import isGoodProfit
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json


def loginThing(request):
    if request.method == 'POST':
     username = request.POST['l']
     password = request.POST['p']
     user = authenticate(username=username, password=password)
     if (user is not None):
         if user.is_active:
           login(request,user)
           return HttpResponse("Logged in!!")
         else:
            return HttpResponse("Disabled account!")
     else:
            
            return HttpResponse("No Account! ")
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html',c)
	
    
def known(request):
    tasks.findNewBooks.delay()
    return HttpResponse('done!')
  
def lazy(request):
    objs = Amazon_NR.objects.values_list('productcode', flat=True).filter(productcode=request.GET['product'])
    tasks.process_lots_of_items(objs)
    return HttpResponse(request.GET['product'] + " : " + str(objs))
    
    
def getHistoricalPrices(request):
    amz_code = request.GET['amazoncode']
    return
    #Not implemented
    foo = Price_NR.objects.raw("SELECT id,buy,sell,timestamp from ta_price a WHERE a.amazon_id = '" + amz_code + "' ORDER BY a.timestamp ASC")
    output = []
    lastprice = -1
    
    if request.GET['type'] == 'buy':
        for s in foo:
            if not s.buy:
                s.buy = 0.0
            
            if s.buy != lastprice:   
                output.append((s.timestamp.isoformat(' '), float(s.buy)))
            lastprice = s.buy
    else:
        for s in foo:
            if not s.sell:
                s.sell = 0.0
            if s.sell != lastprice:
                output.append((s.timestamp.isoformat(' '), float(s.sell)))
            lastprice = s.sell
    
    
    return HttpResponse(json.dumps(output))
    

@login_required(login_url='/login/')
def getDeals(request):
    dictItems = {}
    
    if request.user.username == 'brandon':
      referer = 'http://www.amazon.com/gp/product/%s/ref=as_li_ss_tl?ie=UTF8&tag=deafordea-20&linkCode=as2&camp=217145&creative=399373&creativeASIN=%s'
    else:
      referer = 'http://www.amazon.com/gp/product/%s/ref=as_li_ss_tl?ie=UTF8&tag=ngre-20&linkCode=as2&camp=217145&creative=399373&creativeASIN=%s'



    objs2 = AmazonTradeIn.objects.filter(profitable__gte=10)
    totalProfitable = objs2.count()

    totalBooks = totalIndexed = AmazonTradeIn.objects.all().count()
    for obj in iter(objs2):
        ctb = 0
        actb = 0

        try:
            theBuy = float(obj.buy)
            theSell = float(obj.sell)
        except:
            continue
        
        if (theSell != 0):
            ctb = (theBuy-theSell) / theSell
            actb = (theBuy-(theSell+3.99)) / (theSell+3.99) 
            ctb = round(ctb * 100,2)
            actb = round(actb * 100,2)
            
            productCode = obj.productcode
            dictItems[productCode] = (referer % (productCode, productCode),
                                 obj.title,
                                theBuy,
                                theSell,
                                theBuy - theSell,
            	    ctb, actb, obj.timestamp, productCode,
		    'http://www.amazon.com/gp/offer-listing/%s/ref=dp_olp_used?ie=UTF8&condition=used' % (productCode))
    c = RequestContext(request)
    return render_to_response('deals.html', {'dictItems': dictItems, 
                                             'totalIndexed': totalIndexed,
                                             'totalProfitable': totalProfitable,
                                             'totalBooks': totalBooks,
                                             'username': request.user.username,
					     },
					     context_instance = c,
					     )

def logout_user(request):
	logout(request)
	return HttpResponse("Logged out!")
	
def launch(request):   
    objs = ATS_Middle_NR.objects.values_list('id', flat=True)
    tasks.process_lots_of_items_cats(objs) 
    return HttpResponse("Created " + str(len(objs)) + " tasks (but didn't execute)")

def defineCategories(request):
    if request.method == 'POST':
        if (request.POST.get('categories')):
            urls = request.POST.get('categories').strip().split()
            for url in urls:
                tasks.addCat.delay(url)
            return HttpResponse("Added all urls!")
        return HttpResponse("Nothing to do.")
    else:
        c = {}
        c.update(csrf(request))
       # latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
        return render_to_response('defineCategories.html',c)
