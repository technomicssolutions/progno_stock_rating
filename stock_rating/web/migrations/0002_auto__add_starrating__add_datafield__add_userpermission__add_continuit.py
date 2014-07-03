# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StarRating'
        db.create_table(u'web_starrating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('star_count', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('min_score', self.gf('django.db.models.fields.FloatField')(max_length=5)),
            ('max_score', self.gf('django.db.models.fields.FloatField')(max_length=5)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'web', ['StarRating'])

        # Adding model 'DataField'
        db.create_table(u'web_datafield', (
            (u'date_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['web.Date'], unique=True, primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['DataField'])

        # Adding model 'UserPermission'
        db.create_table(u'web_userpermission', (
            (u'date_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['web.Date'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('data_upload', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('field_settings', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('score_settings', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('function_settings', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('analytical_heads', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'web', ['UserPermission'])

        # Adding model 'ContinuityFunction'
        db.create_table(u'web_continuityfunction', (
            (u'function_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['web.Function'], unique=True, primary_key=True)),
            ('number_of_periods', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('minimum_value', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('period_1', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('period_2', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('period_3', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
        ))
        db.send_create_signal(u'web', ['ContinuityFunction'])

        # Adding model 'FunctionCategory'
        db.create_table(u'web_functioncategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['FunctionCategory'])

        # Adding model 'HardcodedFormula'
        db.create_table(u'web_hardcodedformula', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('continuity_formula', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('consistency_formula', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'web', ['HardcodedFormula'])

        # Adding model 'CompanyModelScore'
        db.create_table(u'web_companymodelscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Company'])),
            ('analysis_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.AnalysisModel'])),
            ('score', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('star_rating', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.StarRating'])),
        ))
        db.send_create_signal(u'web', ['CompanyModelScore'])

        # Adding model 'AnalysisModel'
        db.create_table(u'web_analysismodel', (
            (u'date_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['web.Date'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'web', ['AnalysisModel'])

        # Adding M2M table for field insdustries on 'AnalysisModel'
        db.create_table(u'web_analysismodel_insdustries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('analysismodel', models.ForeignKey(orm[u'web.analysismodel'], null=False)),
            ('industry', models.ForeignKey(orm[u'web.industry'], null=False))
        ))
        db.create_unique(u'web_analysismodel_insdustries', ['analysismodel_id', 'industry_id'])

        # Adding M2M table for field analytical_heads on 'AnalysisModel'
        db.create_table(u'web_analysismodel_analytical_heads', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('analysismodel', models.ForeignKey(orm[u'web.analysismodel'], null=False)),
            ('analyticalhead', models.ForeignKey(orm[u'web.analyticalhead'], null=False))
        ))
        db.create_unique(u'web_analysismodel_analytical_heads', ['analysismodel_id', 'analyticalhead_id'])

        # Adding model 'Formula'
        db.create_table(u'web_formula', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'web', ['Formula'])

        # Adding M2M table for field operands on 'Formula'
        db.create_table(u'web_formula_operands', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('formula', models.ForeignKey(orm[u'web.formula'], null=False)),
            ('datafield', models.ForeignKey(orm[u'web.datafield'], null=False))
        ))
        db.create_unique(u'web_formula_operands', ['formula_id', 'datafield_id'])

        # Adding M2M table for field operators on 'Formula'
        db.create_table(u'web_formula_operators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('formula', models.ForeignKey(orm[u'web.formula'], null=False)),
            ('operator', models.ForeignKey(orm[u'web.operator'], null=False))
        ))
        db.create_unique(u'web_formula_operators', ['formula_id', 'operator_id'])

        # Adding model 'Company'
        db.create_table(u'web_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('isin_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('industry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Industry'])),
        ))
        db.send_create_signal(u'web', ['Company'])

        # Adding model 'Date'
        db.create_table(u'web_date', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Date'])

        # Adding model 'FieldMap'
        db.create_table(u'web_fieldmap', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_file', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.DataFile'])),
            ('data_field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.DataField'])),
            ('file_field', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'web', ['FieldMap'])

        # Adding model 'Operator'
        db.create_table(u'web_operator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'web', ['Operator'])

        # Adding model 'DataFile'
        db.create_table(u'web_datafile', (
            (u'date_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['web.Date'], unique=True, primary_key=True)),
            ('uploaded_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('uploaded_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'web', ['DataFile'])

        # Adding model 'Industry'
        db.create_table(u'web_industry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('industry_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'web', ['Industry'])

        # Adding model 'CompanyFunctionScore'
        db.create_table(u'web_companyfunctionscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Company'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Function'])),
            ('score', self.gf('django.db.models.fields.FloatField')(max_length=5)),
        ))
        db.send_create_signal(u'web', ['CompanyFunctionScore'])

        # Adding model 'ParameterLimit'
        db.create_table(u'web_parameterlimit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('analysis_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.AnalysisModel'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Function'])),
            ('strong_min', self.gf('django.db.models.fields.FloatField')(max_length=5)),
            ('strong_max', self.gf('django.db.models.fields.FloatField')(max_length=5)),
            ('neutral_min', self.gf('django.db.models.fields.FloatField')(max_length=5)),
            ('neutral_max', self.gf('django.db.models.fields.FloatField')(max_length=5)),
            ('week_min', self.gf('django.db.models.fields.FloatField')(max_length=5)),
            ('week_max', self.gf('django.db.models.fields.FloatField')(max_length=5)),
            ('strong_comment', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('neutral_comment', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('week_comment', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'web', ['ParameterLimit'])

        # Adding model 'ConsistencyFunction'
        db.create_table(u'web_consistencyfunction', (
            (u'function_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['web.Function'], unique=True, primary_key=True)),
            ('number_of_periods', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('minimum_value', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('period_1', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('mean', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
        ))
        db.send_create_signal(u'web', ['ConsistencyFunction'])

        # Adding model 'Function'
        db.create_table(u'web_function', (
            (u'date_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['web.Date'], unique=True, primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.FunctionCategory'])),
            ('analytical_head', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.AnalyticalHead'])),
            ('function_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('function_type', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('formula', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Formula'], null=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Function'])

        # Adding model 'AnalyticalHead'
        db.create_table(u'web_analyticalhead', (
            (u'date_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['web.Date'], unique=True, primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['AnalyticalHead'])

        # Adding model 'ScoreRating'
        db.create_table(u'web_scorerating', (
            (u'date_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['web.Date'], unique=True, primary_key=True)),
            ('strong_score', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('neutral_score', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('week_score', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
        ))
        db.send_create_signal(u'web', ['ScoreRating'])

    def backwards(self, orm):
        # Deleting model 'StarRating'
        db.delete_table(u'web_starrating')

        # Deleting model 'DataField'
        db.delete_table(u'web_datafield')

        # Deleting model 'UserPermission'
        db.delete_table(u'web_userpermission')

        # Deleting model 'ContinuityFunction'
        db.delete_table(u'web_continuityfunction')

        # Deleting model 'FunctionCategory'
        db.delete_table(u'web_functioncategory')

        # Deleting model 'HardcodedFormula'
        db.delete_table(u'web_hardcodedformula')

        # Deleting model 'CompanyModelScore'
        db.delete_table(u'web_companymodelscore')

        # Deleting model 'AnalysisModel'
        db.delete_table(u'web_analysismodel')

        # Removing M2M table for field insdustries on 'AnalysisModel'
        db.delete_table('web_analysismodel_insdustries')

        # Removing M2M table for field analytical_heads on 'AnalysisModel'
        db.delete_table('web_analysismodel_analytical_heads')

        # Deleting model 'Formula'
        db.delete_table(u'web_formula')

        # Removing M2M table for field operands on 'Formula'
        db.delete_table('web_formula_operands')

        # Removing M2M table for field operators on 'Formula'
        db.delete_table('web_formula_operators')

        # Deleting model 'Company'
        db.delete_table(u'web_company')

        # Deleting model 'Date'
        db.delete_table(u'web_date')

        # Deleting model 'FieldMap'
        db.delete_table(u'web_fieldmap')

        # Deleting model 'Operator'
        db.delete_table(u'web_operator')

        # Deleting model 'DataFile'
        db.delete_table(u'web_datafile')

        # Deleting model 'Industry'
        db.delete_table(u'web_industry')

        # Deleting model 'CompanyFunctionScore'
        db.delete_table(u'web_companyfunctionscore')

        # Deleting model 'ParameterLimit'
        db.delete_table(u'web_parameterlimit')

        # Deleting model 'ConsistencyFunction'
        db.delete_table(u'web_consistencyfunction')

        # Deleting model 'Function'
        db.delete_table(u'web_function')

        # Deleting model 'AnalyticalHead'
        db.delete_table(u'web_analyticalhead')

        # Deleting model 'ScoreRating'
        db.delete_table(u'web_scorerating')

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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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