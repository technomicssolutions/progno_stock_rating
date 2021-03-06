
from jsonfield import JSONField
from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponse


class Date(models.Model):
    created_by = models.ForeignKey(User, null=True, blank=True)
    created_date = models.DateTimeField('Created Date', auto_now_add=True)
    updated_date = models.DateTimeField('Updated Date', auto_now=True)

class UserPermission(Date):

    user = models.ForeignKey(User)
    data_upload = models.BooleanField('Data Upload', default=False)
    field_settings = models.BooleanField('Field Settings', default=False)
    score_settings = models.BooleanField('Score Settings', default=False)
    function_settings = models.BooleanField('Function Settings', default=False)
    analytical_heads = models.BooleanField('Analytical heads', default=False)

    def __unicode__(self):
        return self.user.first_name

class AnalyticalHead(Date):

    title = models.CharField('Title', max_length=200, unique=True)
    description = models.TextField('Description', null=True, blank=True)

    def __unicode__(self):
        return self.title

class DataField(Date):
    name = models.CharField('Name', max_length=200, unique=True)
    description = models.TextField('Description', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Field'
        verbose_name_plural = 'Fields'

class DataFile(Date):

    uploaded_by = models.ForeignKey(User)
    uploaded_file = models.FileField(upload_to='uploads/data_file/')
    number_of_sheets = models.IntegerField('Number of sheets', null=True, blank=True)
    sheets = JSONField('sheets', null=True, blank=True)
    processing_completed = models.BooleanField('Processing Completed', default = False)


    def __unicode__(self):
        return self.uploaded_by.first_name + ' - ' + self.uploaded_file.name

class FieldMap(Date):

    data_field = models.ForeignKey(DataField, null=True, blank=True)
    file_field = models.CharField('File Field', max_length=200, unique=False, null=True, blank=True)

    def __unicode__(self):
        return str(self.data_field) + ' - ' + self.file_field

class Operator(Date):
    symbol = models.CharField('Symbol', max_length=5)

    def __unicode__(self):
        return self.symbol

class Formula(Date):
    operands = models.ManyToManyField(DataField)
    operators = models.ManyToManyField(Operator)
    formula_string = models.CharField('Formula', max_length=500)

    def __unicode__(self):
        return self.formula_string

FUNCTION_TYPES = (
    ('general', 'General'),
    ('continuity', 'Continuity'),
    ('consistency', 'Consistency'),
)

class Function(Date):

    analytical_head = models.ForeignKey(AnalyticalHead)
    function_name = models.CharField('Name', max_length=200, unique=True)
    description = models.TextField('Description', null=True, blank=True)
    function_type = models.CharField('Type', choices=FUNCTION_TYPES, max_length=11)
    formula = models.ForeignKey(Formula, null=True, blank=True)
    order = models.IntegerField('Order', null=True, blank=True)

    def __unicode__(self):
        return self.function_name

class HardcodedFormula(Date):
    continuity_formula = models.CharField('Continuity Formula', max_length=200)
    consistency_formula = models.CharField('Consistency Formula', max_length=200)

class ContinuityFunction(Function):
    number_of_fields = models.IntegerField('Number of Periods', max_length=3)
    number_of_functions = models.IntegerField('Number of Functions', max_length=3)
    fields = models.ManyToManyField(DataField, related_name="fields_in_continuity")
    functions = models.ManyToManyField(Function, related_name="functions_in_continuity")

class ConsistencyFunction(Function):
    number_of_fields = models.IntegerField('Number of Periods', max_length=3)
    number_of_functions = models.IntegerField('Number of Functions', max_length=3)
    fields = models.ManyToManyField(DataField, related_name="fields_in_consistency")
    functions = models.ManyToManyField(Function, related_name="functions_in_consistency")

class Industry(models.Model):
    industry_name = models.CharField('Industry', max_length=200, unique=True)
    created_by = models.ForeignKey(User, null=True, blank=True)
    def __unicode__(self):
        return self.industry_name

class CompanyFile(Date):
    uploaded_by = models.ForeignKey(User)
    uploaded_file = models.FileField(upload_to='uploads/data_file/')
    number_of_sheets = models.IntegerField('Number of sheets', null=True, blank=True)
    processing_completed = models.BooleanField('Processing Completed', default = False)

    def __unicode__(self):
        return self.uploaded_by.first_name + ' - ' + self.uploaded_file.name

class Company(Date):
    company_name = models.CharField('company_name', max_length=200, unique=True)
    isin_code = models.CharField('ISIN Code', max_length=200, unique=True)
    NSE_code = models.CharField('NSE Code', max_length=200, null=True, blank=True)
    BSE_code = models.CharField('BSE Code', max_length=200, null=True, blank=True)
    industry = models.ForeignKey(Industry, null=True, blank=True)
    bse_status = models.CharField('BSE Status', max_length=50, null=True, blank=True)
    bse_group = models.CharField('BSE Group', max_length=50, null=True, blank=True)
    is_all_data_available = models.BooleanField('Is all data avaialble', default=True)
    bse_scrip_id = models.CharField('Scrip Id', max_length=50, null=True, blank=True)
    unavailable_data = JSONField('Unavailable Data', null=True, blank=True)
    
    def __unicode__(self):
        return self.company_name + ' - ' + self.isin_code


class AnalysisModel(Date):

    name = models.CharField('Model name', max_length=200, unique=True, null=True)
    description = models.TextField('Description')
    industries = models.ManyToManyField(Industry)
    analytical_heads = models.ManyToManyField(AnalyticalHead)
    max_points = models.FloatField('Total points', default=0)

    def __unicode__(self):
        return self.name

class ParameterLimit(Date):

    analysis_model = models.ForeignKey('AnalysisModel')
    function = models.ForeignKey(Function)
    strong_min = models.FloatField('Strong Min', max_length=5)
    strong_max = models.CharField('Strong Max', max_length=30)
    strong_points = models.FloatField('Strong Points', max_length=5, default=0)
    neutral_min = models.FloatField('Neutral Min', max_length=5)
    neutral_max = models.FloatField('Neutral Max', max_length=5)
    neutral_points = models.FloatField('Neutral Points', max_length=5, default=0)
    weak_min = models.CharField('weak Min', max_length=30, default=0)
    weak_min_1 = models.CharField('weak Min 1', max_length=30, null=True, blank = True)
    weak_max = models.CharField('weak Max', max_length=30, default=0)
    weak_max_1 = models.CharField('weak Max 1', max_length=30, null=True, blank=True)
    weak_points = models.FloatField('weak Points', max_length=5, default=0)
    strong_comment = models.CharField('Strong Comment', max_length=200)
    neutral_comment = models.CharField('Neutral Comment', max_length=200)
    weak_comment = models.CharField('weak Comment', max_length=200, null=True)

    def __unicode__(self):
        return self.analysis_model.name + ' - '+ self.function.function_name
        
class StarRating(Date):
    model = models.ForeignKey(AnalysisModel)
    star_count = models.IntegerField('StarCount', max_length=1)
    min_score = models.FloatField('Min Score', max_length=5)
    max_score = models.FloatField('Max Score', max_length=5, null=True, blank=True)
    comment = models.CharField('Comment', max_length=200)

    def __unicode__(self):
        return str(self.star_count) + ' star'

class CompanyFunctionScore(Date):
    company = models.ForeignKey(Company)
    function = models.ForeignKey(Function)
    score = models.FloatField('Function Score', max_length=5, null=True, blank=True)

    def __unicode__(self):
        return self.company.company_name + " - " + self.function.function_name + " - " + str(self.score)

class CompanyModelFunctionPoint(Date):
    company = models.ForeignKey(Company)
    parameter_limit = models.ForeignKey(ParameterLimit, null=True, blank=True)
    points = models.FloatField('Function Point', max_length=5, null=True, blank=True)

    def __unicode__(self):
        return self.company.company_name + " - " + (self.parameter_limit.function.function_name if self.parameter_limit else '') + " - " + str(self.points)

class CompanyModelScore(Date):
    company = models.ForeignKey(Company)
    analysis_model = models.ForeignKey(AnalysisModel)
    score = models.FloatField('Model Score', max_length=5, null=True, blank=True)
    points = models.IntegerField('Model Points in percentage terms', default=0)
    star_rating = models.ForeignKey(StarRating, null=True, blank=True)
    star_rating_change = models.IntegerField('Change in Star Rating', null=True, blank=True)


    def __unicode__(self):
        return self.company.company_name

class CompanyStockData(Date):
    company = models.ForeignKey(Company)
    stock_data = JSONField('Stock Data', null=True, blank=True)

    def __unicode__(self):
        return self.company.company_name


# class NSEBSEPrice(models.Model):
#     company = models.ForeignKey(Company)
#     date = models.DateField('Date')
#     NSE_price = models.DecimalField('NSE Price', max_digits=10, decimal_places=5, null=True, blank=True)
#     BSE_price = models.DecimalField('BSE Price', max_digits=10, decimal_places=5, null=True, blank=True)
#     latest = models.BooleanField('Is Latest', default=True)
#     last_review = models.BooleanField('Is last review', default=False)
#     parent = models.ForeignKey('self', null=True, blank=True)

#     def __unicode__(self):
#         return self.company.company_name + '-' + str(self.date)

class NSEPrice(models.Model):
    company = models.ForeignKey(Company)
    date = models.DateField('Date')
    NSE_price = models.DecimalField('NSE Price', max_digits=10, decimal_places=5, null=True, blank=True)

    def __unicode__(self):
        return self.company.company_name + '-' + str(self.date)

class BSEPrice(models.Model):
    company = models.ForeignKey(Company)
    date = models.DateField('Date')
    BSE_price = models.DecimalField('BSE Price', max_digits=10, decimal_places=5, null=True, blank=True)

    def __unicode__(self):
        return self.company.company_name + '-' + str(self.date)