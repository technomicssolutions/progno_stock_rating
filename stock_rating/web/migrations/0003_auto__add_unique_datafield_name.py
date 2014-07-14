# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'DataField', fields ['name']
        db.create_unique(u'web_datafield', ['name'])

    def backwards(self, orm):
        # Removing unique constraint on 'DataField', fields ['name']
        db.delete_unique(u'web_datafield', ['name'])

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
        u'web.analysismodel': {
            'Meta': {'object_name': 'AnalysisModel', '_ormbases': [u'web.Date']},
            'analytical_heads': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web.AnalyticalHead']", 'symmetrical': 'False'}),
            u'date_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['web.Date']", 'unique': 'True', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'insdustries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web.Industry']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'web.analyticalhead': {
            'Meta': {'object_name': 'AnalyticalHead', '_ormbases': [u'web.Date']},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'date_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['web.Date']", 'unique': 'True', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'web.company': {
            'Meta': {'object_name': 'Company'},
            'company_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Industry']"}),
            'isin_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'web.companyfunctionscore': {
            'Meta': {'object_name': 'CompanyFunctionScore'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Company']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Function']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {'max_length': '5'})
        },
        u'web.companymodelscore': {
            'Meta': {'object_name': 'CompanyModelScore'},
            'analysis_model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.AnalysisModel']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'star_rating': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.StarRating']"})
        },
        u'web.consistencyfunction': {
            'Meta': {'object_name': 'ConsistencyFunction', '_ormbases': [u'web.Function']},
            u'function_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['web.Function']", 'unique': 'True', 'primary_key': 'True'}),
            'mean': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'minimum_value': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'number_of_periods': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'period_1': ('django.db.models.fields.IntegerField', [], {'max_length': '5'})
        },
        u'web.continuityfunction': {
            'Meta': {'object_name': 'ContinuityFunction', '_ormbases': [u'web.Function']},
            u'function_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['web.Function']", 'unique': 'True', 'primary_key': 'True'}),
            'minimum_value': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'number_of_periods': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'period_1': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'period_2': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'period_3': ('django.db.models.fields.IntegerField', [], {'max_length': '5'})
        },
        u'web.datafield': {
            'Meta': {'object_name': 'DataField', '_ormbases': [u'web.Date']},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'date_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['web.Date']", 'unique': 'True', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'web.datafile': {
            'Meta': {'object_name': 'DataFile', '_ormbases': [u'web.Date']},
            u'date_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['web.Date']", 'unique': 'True', 'primary_key': 'True'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'uploaded_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'web.date': {
            'Meta': {'object_name': 'Date'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'web.fieldmap': {
            'Meta': {'object_name': 'FieldMap'},
            'data_field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.DataField']"}),
            'data_file': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.DataFile']"}),
            'file_field': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'web.formula': {
            'Meta': {'object_name': 'Formula'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operands': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web.DataField']", 'symmetrical': 'False'}),
            'operators': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web.Operator']", 'symmetrical': 'False'})
        },
        u'web.function': {
            'Meta': {'object_name': 'Function', '_ormbases': [u'web.Date']},
            'analytical_head': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.AnalyticalHead']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.FunctionCategory']"}),
            u'date_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['web.Date']", 'unique': 'True', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'formula': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Formula']", 'null': 'True', 'blank': 'True'}),
            'function_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'function_type': ('django.db.models.fields.CharField', [], {'max_length': '11'})
        },
        u'web.functioncategory': {
            'Meta': {'object_name': 'FunctionCategory'},
            'category_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'web.hardcodedformula': {
            'Meta': {'object_name': 'HardcodedFormula'},
            'consistency_formula': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'continuity_formula': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'web.industry': {
            'Meta': {'object_name': 'Industry'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'web.operator': {
            'Meta': {'object_name': 'Operator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'web.parameterlimit': {
            'Meta': {'object_name': 'ParameterLimit'},
            'analysis_model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.AnalysisModel']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Function']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'neutral_comment': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'neutral_max': ('django.db.models.fields.FloatField', [], {'max_length': '5'}),
            'neutral_min': ('django.db.models.fields.FloatField', [], {'max_length': '5'}),
            'strong_comment': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'strong_max': ('django.db.models.fields.FloatField', [], {'max_length': '5'}),
            'strong_min': ('django.db.models.fields.FloatField', [], {'max_length': '5'}),
            'week_comment': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'week_max': ('django.db.models.fields.FloatField', [], {'max_length': '5'}),
            'week_min': ('django.db.models.fields.FloatField', [], {'max_length': '5'})
        },
        u'web.scorerating': {
            'Meta': {'object_name': 'ScoreRating', '_ormbases': [u'web.Date']},
            u'date_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['web.Date']", 'unique': 'True', 'primary_key': 'True'}),
            'neutral_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'strong_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'week_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'})
        },
        u'web.starrating': {
            'Meta': {'object_name': 'StarRating'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.FloatField', [], {'max_length': '5'}),
            'min_score': ('django.db.models.fields.FloatField', [], {'max_length': '5'}),
            'star_count': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        },
        u'web.userpermission': {
            'Meta': {'object_name': 'UserPermission', '_ormbases': [u'web.Date']},
            'analytical_heads': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'data_upload': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'date_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['web.Date']", 'unique': 'True', 'primary_key': 'True'}),
            'field_settings': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'function_settings': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'score_settings': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['web']