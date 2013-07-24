# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Amazon_Textbook_Section_NR'
        db.create_table(u'ta_amazon_textbook_section_nr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'ta', ['Amazon_Textbook_Section_NR'])

        # Adding model 'Book_NR'
        db.create_table(u'ta_book_nr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pckey', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
            ('isbn10', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
        ))
        db.send_create_signal(u'ta', ['Book_NR'])

        # Adding model 'ATS_Middle_NR'
        db.create_table(u'ta_ats_middle_nr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ta.Amazon_Textbook_Section_NR'])),
            ('page', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'ta', ['ATS_Middle_NR'])

        # Adding model 'Unique_Seller_NR'
        db.create_table(u'ta_unique_seller_nr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'ta', ['Unique_Seller_NR'])

        # Adding model 'Seller_NR'
        db.create_table(u'ta_seller_nr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ta.Book_NR'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ta.Unique_Seller_NR'])),
        ))
        db.send_create_signal(u'ta', ['Seller_NR'])

        # Adding model 'AmazonRankCategory_NR'
        db.create_table(u'ta_amazonrankcategory_nr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'ta', ['AmazonRankCategory_NR'])

        # Adding model 'Amazon_NR'
        db.create_table(u'ta_amazon_nr', (
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ta.Book_NR'])),
            ('productcode', self.gf('django.db.models.fields.CharField')(max_length=250, primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'ta', ['Amazon_NR'])

        # Adding model 'AmazonRank_NR'
        db.create_table(u'ta_amazonrank_nr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amazon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ta.Amazon_NR'])),
            ('rank', self.gf('django.db.models.fields.IntegerField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ta.AmazonRankCategory_NR'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'ta', ['AmazonRank_NR'])

        # Adding model 'Price_NR'
        db.create_table(u'ta_price_nr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buy', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('sell', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'ta', ['Price_NR'])

        # Adding model 'Proxy_NR'
        db.create_table(u'ta_proxy_nr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proxy_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('ip_and_port', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'ta', ['Proxy_NR'])

        # Adding model 'MetaTable_NR'
        db.create_table(u'ta_metatable_nr', (
            ('metakey', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('metatype', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('string_field', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('int_field', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('float_field', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal(u'ta', ['MetaTable_NR'])

        # Adding model 'ProfitableBooks_NR'
        db.create_table(u'ta_profitablebooks_nr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amazon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ta.Amazon_NR'])),
            ('price', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ta.Price_NR'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'ta', ['ProfitableBooks_NR'])

        # Adding model 'AmazonMongoTradeIn'
        db.create_table(u'ta_amazonmongotradein', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amazon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ta.Amazon_NR'])),
            ('latest_price', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lp', to=orm['ta.Price_NR'])),
            ('profitable', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'ta', ['AmazonMongoTradeIn'])

        # Adding M2M table for field prices on 'AmazonMongoTradeIn'
        m2m_table_name = db.shorten_name(u'ta_amazonmongotradein_prices')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('amazonmongotradein', models.ForeignKey(orm[u'ta.amazonmongotradein'], null=False)),
            ('price_nr', models.ForeignKey(orm[u'ta.price_nr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['amazonmongotradein_id', 'price_nr_id'])


    def backwards(self, orm):
        # Deleting model 'Amazon_Textbook_Section_NR'
        db.delete_table(u'ta_amazon_textbook_section_nr')

        # Deleting model 'Book_NR'
        db.delete_table(u'ta_book_nr')

        # Deleting model 'ATS_Middle_NR'
        db.delete_table(u'ta_ats_middle_nr')

        # Deleting model 'Unique_Seller_NR'
        db.delete_table(u'ta_unique_seller_nr')

        # Deleting model 'Seller_NR'
        db.delete_table(u'ta_seller_nr')

        # Deleting model 'AmazonRankCategory_NR'
        db.delete_table(u'ta_amazonrankcategory_nr')

        # Deleting model 'Amazon_NR'
        db.delete_table(u'ta_amazon_nr')

        # Deleting model 'AmazonRank_NR'
        db.delete_table(u'ta_amazonrank_nr')

        # Deleting model 'Price_NR'
        db.delete_table(u'ta_price_nr')

        # Deleting model 'Proxy_NR'
        db.delete_table(u'ta_proxy_nr')

        # Deleting model 'MetaTable_NR'
        db.delete_table(u'ta_metatable_nr')

        # Deleting model 'ProfitableBooks_NR'
        db.delete_table(u'ta_profitablebooks_nr')

        # Deleting model 'AmazonMongoTradeIn'
        db.delete_table(u'ta_amazonmongotradein')

        # Removing M2M table for field prices on 'AmazonMongoTradeIn'
        db.delete_table(db.shorten_name(u'ta_amazonmongotradein_prices'))


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
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
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