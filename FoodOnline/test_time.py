from datetime import time,datetime,date

today_date=date.today()
today=today_date.isoweekday()
print(today_date,today)
now=datetime.now()
print(now)
current_time=now.strftime("%I:%M:%p")
print(current_time)