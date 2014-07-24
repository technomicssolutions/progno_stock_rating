from django.db import models
from django.contrib.auth.models import User


class Date(models.Model):

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

    created_by = models.ForeignKey(User)
    title = models.CharField('Title', max_length=200)
    description = models.TextField('Description', null=True, blank=True)

    def __unicode__(self):
        return self.title

class DataField(Date):
    created_by = models.ForeignKey(User)
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

    def __unicode__(self):
        return self.user.first_name + ' - ' + self.uploaded_file.name

class FieldMap(models.Model):

    data_file = models.ForeignKey(DataFile)
    data_field = models.ForeignKey(DataField)
    file_field = models.CharField('File Field', max_length=200, unique=True)

    def __unicode__(self):
        return str(self.data_file) + ' - ' + self.file_field

class FunctionCategory(models.Model):

    category_name = models.CharField('Category Name', max_length=200, unique=True)
    description = models.TextField('Description', null=True, blank=True)

    def __unicode__(self):
        return self.category_name

class Operator(models.Model):
    symbol = models.CharField('Symbol', max_length=1)

class Formula(models.Model):
    operands = models.ManyToManyField(DataField)
    operators = models.ManyToManyField(Operator)

    def display(self):
        pass
    def __unicode__(self):
        return self.display()

FUNCTION_TYPES = (
    ('general', 'General'),
    ('continuity', 'Continuity'),
    ('consistency', 'Consistency'),
)

class Function(Date):

    category = models.ForeignKey(FunctionCategory)
    analytical_head = models.ForeignKey(AnalyticalHead)
    function_name = models.CharField('Name', max_length=200, unique=True)
    description = models.TextField('Description', null=True, blank=True)
    function_type = models.CharField('Type', choices=FUNCTION_TYPES, max_length=11)
    formula = models.ForeignKey(Formula, null=True, blank=True)

    def __unicode__(self):
        return self.function_name

class HardcodedFormula(models.Model):
    continuity_formula = models.CharField('Continuity Formula', max_length=200)
    consistency_formula = models.CharField('Consistency Formula', max_length=200)

class ContinuityFunction(Function):
    number_of_periods = models.IntegerField('Number of Periods', max_length=3)
    minimum_value = models.IntegerField('Minimum Value', max_length=3)
    period_1 = models.IntegerField('Period 1', max_length=5)
    period_2 = models.IntegerField('Period 2', max_length=5)
    period_3 = models.IntegerField('Period 3', max_length=5)

class ConsistencyFunction(Function):
    number_of_periods = models.IntegerField('Number of Periods', max_length=3)
    minimum_value = models.IntegerField('Minimum Value', max_length=3, default=0)
    period_1 = models.IntegerField('Period 1', max_length=5, default=0)
    period_2 = models.IntegerField('Period 2', max_length=5, default=0)
    mean = models.IntegerField('Mean', max_length=5)

class Industry(models.Model):
    industry_name = models.CharField('Industry', max_length=200, unique=True)

    def __unicode__(self):
        return self.industry_name

class Company(models.Model):
    company_name = models.CharField('company_name', max_length=200, unique=True)
    isin_code = models.CharField('ISIN Code', max_length=200, unique=True)
    industry = models.ForeignKey(Industry)

    def __unicode__(self):
        return self.company_name + ' - ' + self.isin_code

class ScoreRating(Date):
    strong_score = models.IntegerField('Strong', max_length=1, default=0)
    neutral_score = models.IntegerField('Neutral', max_length=1, default=0)
    weak_score = models.IntegerField('weak', max_length=1, default=0)


class AnalysisModel(Date):

    name = models.CharField('Model name', max_length=200, unique=True, null=True)
    description = models.TextField('Description')
    industries = models.ManyToManyField(Industry)
    analytical_heads = models.ManyToManyField(AnalyticalHead)

    def __unicode__(self):
        return self.name

class ParameterLimit(models.Model):

    analysis_model = models.ForeignKey('AnalysisModel')
    function = models.ForeignKey(Function)
    strong_min = models.FloatField('Strong Min', max_length=5)
    strong_max = models.FloatField('Strong Max', max_length=5)
    strong_points = models.FloatField('Strong Points', max_length=5, default=0)
    neutral_min = models.FloatField('Neutral Min', max_length=5)
    neutral_max = models.FloatField('Neutral Max', max_length=5)
    neutral_points = models.FloatField('Neutral Points', max_length=5, default=0)
    weak_min = models.FloatField('weak Min', max_length=5, default=0)
    weak_max = models.FloatField('weak Max', max_length=5, default=0)
    weak_points = models.FloatField('weak Points', max_length=5, default=0)
    strong_comment = models.CharField('Strong Comment', max_length=200)
    neutral_comment = models.CharField('Neutral Comment', max_length=200)
    weak_comment = models.CharField('weak Comment', max_length=200, null=True)
        
class StarRating(models.Model):

    star_count = models.IntegerField('StarCount', max_length=1)
    min_score = models.FloatField('Min Score', max_length=5)
    max_score = models.FloatField('Max Score', max_length=5)
    comment = models.CharField('Comment', max_length=200)

    def __unicode__(self):
        return str(self.star_count) + ' star'

class CompanyFunctionScore(models.Model):
    company = models.ForeignKey(Company)
    function = models.ForeignKey(Function)
    score = models.FloatField('Function Score', max_length=5)

class CompanyModelScore(models.Model):
    company = models.ForeignKey(Company)
    analysis_model = models.ForeignKey(AnalysisModel)
    score = models.IntegerField('Model Score', max_length=5)
    star_rating = models.ForeignKey(StarRating)

    def __unicode__(self):
        return self.company