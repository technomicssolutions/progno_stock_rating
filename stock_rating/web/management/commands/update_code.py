
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
    help = "Download NSE BSE price and update to db"

    def handle(self, *args, **options):
        sheets = []
        workbook = xlrd.open_workbook('ListOfScrips_BSE.xlsx')
        worksheets = workbook.sheet_names()
        
        for worksheet_name in worksheets:
            
            worksheet = workbook.sheet_by_name(worksheet_name)
            num_rows = worksheet.nrows - 1
            num_cells = worksheet.ncols - 1
            curr_row = -1            
            curr_cell = -1
            while curr_row < num_rows:
                curr_row += 1                
                curr_cell = -1
                if curr_row != 0: 
                    while curr_cell < num_cells:
                        curr_cell += 1
                        cell_value = worksheet.cell_value(curr_row, curr_cell)
                        field_name = worksheet.cell_value(0, curr_cell)
                        if field_name == 'Scrip Code':
                            bse_code = int(cell_value)
                        if field_name == 'Status':
                            status = cell_value
                        if field_name == 'Group':
                            group = cell_value
                        if field_name == 'ISIN No':
                            isin_code = cell_value
                            
                            try:
                                company = Company.objects.get(isin_code = isin_code)
                                company.BSE_code = str(bse_code)
                                company.bse_status = status
                                company.bse_group = group
                                company.save()
                                print "company", company
                            except Exception as ex:
                                print str(ex)
                                pass
                    
                        
                
            