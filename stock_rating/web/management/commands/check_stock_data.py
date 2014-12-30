
import xlrd

from web.models import Company

from datetime import datetime
from django.core.management.base import BaseCommand


month = {
    '01': 'JAN',
    '02': 'FEB',
    '03': 'MAR',
    '04': 'APR',
    '05': 'MAY',
    '06': 'JUN',
    '07': 'JUL',
    '08': 'AUG',
    '09': 'SEP',
    '10': 'OCT',
    '11': 'NOV',
    '12': 'DEC'
}

class Command(BaseCommand):
    help = "Check if all data is available"

    def handle(self, *args, **options):
        companies = Company.objects.all()
        for company in companies:
            unavailable_data = []
            if(company.companystockdata_set.all().count() > 0):
                stock_data = company.companystockdata_set.all()[0].stock_data
                for k in stock_data:
                    if stock_data[k] == "":
                        unavailable_data.append(k)
                company.unavailable_data = unavailable_data
            else:
                company.unavailable_data = ['No data available']
                company.is_all_data_available = False
            if len(unavailable_data) == 0:
                company.is_all_data_available = True
            else:
                company.is_all_data_available = False
                company.companyfunctionscore_set.all().delete()
                company.companymodelfunctionpoint_set.all().delete()
                company.companymodelscore_set.all().delete()
            company.save()

                        
                    
                        
                
            