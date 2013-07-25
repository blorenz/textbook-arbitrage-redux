from celery.task import TaskSet, task
import amazon
from .models import *

from itertools import islice


@task(name='ta.tasks.add')
def add(x, y):
	return x + y


def chunks(it, n):
    for first in it:
        yield [first] + list(islice(it, n - 1))


@task(name='ta.tasks.process_chunk')
def process_chunk(pks, ignore_result=True):
    #objs = Amazon_NR.objects.filter(pk__in=pks)
    print 'Gonna process a chunk of ' + str(len(pks))
    for p in pks:
        print p
        objs = AmazonMongoTradeIn_NJ.objects.filter(productcode=p)
        for obj in objs:
            amazon.parseUsedPage(obj)


@task(name='ta.tasks.process_lots_of_items')
def process_lots_of_items(ids_to_process):
    return TaskSet(process_chunk.subtask((chunk, ))
                       for chunk in chunks(iter(ids_to_process),
                                           25))#.apply_async()


@task(name='ta.tasks.process_chunk_extra')
def process_chunk_extra(pks, ignore_result=True):
    objs = Amazon_NR.objects.filter(pk__in=pks)
    amazon.deleteExtraneousPricesWorker(objs)


@task(name='ta.tasks.process_lots_of_items_extra')
def process_lots_of_items_extra(ids_to_process):
    return TaskSet(process_chunk_extra.subtask((chunk, ))
                       for chunk in chunks(iter(ids_to_process),
                                           25)).apply_async()


@task(name='ta.tasks.task_addFacetToScan')
def task_addFacetToScan(url):
    print 'adding facet'
    amazon.addFacetToScan(url)


@task(name='ta.tasks.task_scanCategoryAndAddBooks')
def task_scanCategoryAndAddBooks(obj):
    amazon.scanCategoryAndAddBooks(obj)


@task(name='ta.tasks.addCat', ignore_result=True)
def addCat(x):
    amazon.addCategory(x)


@task(name='ta.tasks.scanTradeInPage', ignore_result=True)
def scanTradeInPage(x, i):
    amazon.getAmazonBooksOnTradeinPage(x, i)


@task(name='ta.tasks.detailTheBook', ignore_result=True)
def detailTheBook(am):
    amazon.parseUsedPage(am)


@task(name='ta.tasks.findNewBooks', ignore_result=True)
def findNewBooks():
    amazon.detailAllBooks()


@task(name='ta.tasks.updateProfitable', ignore_result=True)
def updateProfitable():
    ProfitableBooks_NR.objects.values_list("price__amazon")


@task(name='ta.tasks.lookForNewBooks', ignore_result=True)
def lookForNewBooks():
    amazon.lookForBooks()


@task(name='ta.tasks.deleteExtraneousPrices', ignore_result=True)
def deleteExtraneousPrices():
    objs = Amazon_NR.objects.all()
    for obj in objs:
        amz = Price_NR.objects.filter(amazon=obj).order_by("-timestamp")
        count = len(amz)
        #print "Trying! " + str(count)
        if count > 1:
            for i in xrange(count-1, 1, -1):
                #print i
                if (amz[i-1].buy == amz[i-2].buy) and (amz[i-1].sell == amz[i-2].sell):
                    amz[i-1].delete()


@task(name='ta.tasks.doTheBooks', ignore_result=True)
def doTheBooks(objs):
    for obj in objs:
        detailTheBook.delay(obj)


@task(name='ta.tasks.updateBCs', ignore_result=True)
def updateBCs():
    amazon.updateBookCounts()
    amazon.getProfitableBooks()
