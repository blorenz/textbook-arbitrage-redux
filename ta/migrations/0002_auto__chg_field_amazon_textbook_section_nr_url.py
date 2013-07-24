# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Amazon_Textbook_Section_NR.url'
        db.alter_column(u'ta_amazon_textbook_section_nr', 'url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500))

    def backwards(self, orm):

        # Changing field 'Amazon_Textbook_Section_NR.url'
        db.alter_column(u'ta_amazon_textbook_section_nr', 'url', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True))

    models = {
        u'ta.amazon_nr': {
            'Meta': {'object_name': 'Amazon_NR'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ta.Book_NR']"}),
            'productcode': ('django.db.models.fields.CharField', [], {'max_length': '250', 'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ta.amazon_textbook_section_nr': {
            'Meta': {'object_name': 'Amazon_Textbook_Section_NR'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'})
        },
        u'ta.amazonmongotradein': {
            'Meta': {'object_name': 'AmazonMongoTradeIn'},
            'amazon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ta.Amazon_NR']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_price': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lp'", 'to': u"orm['ta.Price_NR']"}),
            'prices': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pr'", 'symmetrical': 'False', 'to': u"orm['ta.Price_NR']"}),
            'profitable': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'ta.amazonrank_nr': {
            'Meta': {'object_name': 'AmazonRank_NR'},
            'amazon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ta.Amazon_NR']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ta.AmazonRankCategory_NR']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ta.amazonrankcategory_nr': {
            'Meta': {'object_name': 'AmazonRankCategory_NR'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ta.ats_middle_nr': {
            'Meta': {'object_name': 'ATS_Middle_NR'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.IntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ta.Amazon_Textbook_Section_NR']"})
        },
        u'ta.book_nr': {
            'Meta': {'object_name': 'Book_NR'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'isbn10': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'pckey': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'ta.metatable_nr': {
            'Meta': {'object_name': 'MetaTable_NR'},
            'float_field': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'int_field': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'metakey': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'metatype': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'string_field': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'ta.price_nr': {
            'Meta': {'object_name': 'Price_NR'},
            'buy': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sell': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'ta.profitablebooks_nr': {
            'Meta': {'object_name': 'ProfitableBooks_NR'},
            'amazon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ta.Amazon_NR']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ta.Price_NR']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'ta.proxy_nr': {
            'Meta': {'object_name': 'Proxy_NR'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_and_port': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'proxy_type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'ta.seller_nr': {
            'Meta': {'object_name': 'Seller_NR'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ta.Book_NR']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ta.Unique_Seller_NR']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ta.unique_seller_nr': {
            'Meta': {'object_name': 'Unique_Seller_NR'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['ta']