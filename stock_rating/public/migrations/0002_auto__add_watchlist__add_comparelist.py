# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WatchList'
        db.create_table(u'public_watchlist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['public.PublicUser'])),
        ))
        db.send_create_signal(u'public', ['WatchList'])

        # Adding M2M table for field companies on 'WatchList'
        db.create_table(u'public_watchlist_companies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('watchlist', models.ForeignKey(orm[u'public.watchlist'], null=False)),
            ('company', models.ForeignKey(orm[u'web.company'], null=False))
        ))
        db.create_unique(u'public_watchlist_companies', ['watchlist_id', 'company_id'])

        # Adding model 'CompareList'
        db.create_table(u'public_comparelist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['public.PublicUser'])),
        ))
        db.send_create_signal(u'public', ['CompareList'])

        # Adding M2M table for field companies on 'CompareList'
        db.create_table(u'public_comparelist_companies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comparelist', models.ForeignKey(orm[u'public.comparelist'], null=False)),
            ('company', models.ForeignKey(orm[u'web.company'], null=False))
        ))
        db.create_unique(u'public_comparelist_companies', ['comparelist_id', 'company_id'])

    def backwards(self, orm):
        # Deleting model 'WatchList'
        db.delete_table(u'public_watchlist')

        # Removing M2M table for field companies on 'WatchList'
        db.delete_table('public_watchlist_companies')

        # Deleting model 'CompareList'
        db.delete_table(u'public_comparelist')

        # Removing M2M table for field companies on 'CompareList'
        db.delete_table('public_comparelist_companies')

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'public.comparelist': {
            'Meta': {'object_name': 'CompareList'},
            'companies': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web.Company']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public.PublicUser']"})
        },
        u'public.publicuser': {
            'Meta': {'object_name': 'PublicUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'public.watchlist': {
            'Meta': {'object_name': 'WatchList'},
            'companies': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web.Company']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public.PublicUser']"})
        },
        u'web.company': {
            'Meta': {'object_name': 'Company', '_ormbases': [u'web.Date']},
            'company_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            u'date_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['web.Date']", 'unique': 'True', 'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Industry']", 'null': 'True', 'blank': 'True'}),
            'is_all_data_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'isin_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'web.date': {
            'Meta': {'object_name': 'Date'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'web.industry': {
            'Meta': {'object_name': 'Industry'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['public']