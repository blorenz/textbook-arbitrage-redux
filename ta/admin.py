from .models import *
from django.contrib import admin




class AmazonAdmin(admin.ModelAdmin):
    list_filter = ('is_profitable',)
    exclude = ()



admin.site.register(Amazon_NR)
admin.site.register(Amazon_Textbook_Section_NR)
admin.site.register(AmazonMongoTradeIn)
admin.site.register(AmazonTradeIn, AmazonAdmin)
admin.site.register(AmazonRank_NR)
admin.site.register(AmazonRankCategory_NR)
admin.site.register(ATS_Middle_NR)
admin.site.register(Price_NR)
admin.site.register(ProfitableBooks_NR)
admin.site.register(Proxy_NR)
admin.site.register(MetaTable_NR)
admin.site.register(Seller_NR)
admin.site.register(Unique_Seller_NR)
admin.site.register(Book_NR)
