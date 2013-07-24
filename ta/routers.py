import ta

def whichDB(model):
    sqlList = [ta.models.Amazon_Textbook_Section,
    ta.models.ATS_Middle,
     ta.models.Book, 
     ta.models.Unique_Seller,  
     ta.models.Seller,
     ta.models.AmazonRankCategory,
    ta.models.Amazon,
    ta.models.AmazonRank, 
     ta.models.Price, 
     ta.models.Proxy,  
     ta.models.MetaTable,  
     ta.models.ProfitableBooks,]
 

# Mongo-izing it!

    mongoList = [ta.models.Amazon_Textbook_Section_NR,
    ta.models.Book_NR,
   ta.models.ATS_Middle_NR,
     ta.models.Unique_Seller_NR,
    ta.models.Seller_NR,
    ta.models.AmazonRankCategory_NR,
     ta.models.Amazon_NR,
    ta.models.AmazonRank_NR,
     ta.models.Price_NR,
     ta.models.Proxy_NR,
     ta.models.MetaTable_NR,
     ta.models.ProfitableBooks_NR,]
    
    if model in sqlList:
        return 'default'
    else:
        return 'mongo'

    
class MyAppRouter(object):
    """A router to control all database operations on models in
    the myapp application"""

    def db_for_read(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        return whichDB(model)

    def db_for_write(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        return whichDB(model)


    def allow_syncdb(self, db, model):
        "Make sure the myapp app only appears on the 'other' db"
        return whichDB(model) == db
    
class MyAppRouter2(object):
    """A router to control all database operations on models in
    the myapp application"""

    def db_for_read(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        if model._meta.app_label == 'myapp':
            return 'mongo'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        if model._meta.app_label == 'myapp':
            return 'mongo'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in myapp is involved"
        if obj1._meta.app_label == 'myapp' or obj2._meta.app_label == 'myapp':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the myapp app only appears on the 'other' db"
        if db == 'mongo':
            return model._meta.app_label == 'myapp'
        elif model._meta.app_label == 'myapp':
            return False
        return None