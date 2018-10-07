from datetime import datetime
from datetime import timedelta

today = datetime.now().date()
expiration = 10

expiration_date = (today + timedelta(expiration)).strftime("%Y%m%d")

# dat = dat.strftime("%Y%m%d")
#
# print(datez)
print(expiration_date)
