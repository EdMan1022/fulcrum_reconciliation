from .bad_data_compiler import fulcrum_bad_data_compiler
import datetime

today = datetime.datetime.today()

this_month = today.date()
fulcrum_bad_data_compiler(month=this_month)
