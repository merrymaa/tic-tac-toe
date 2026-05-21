import datetime as dt

d = dt.datetime.now()

for i in d.timetuple():
    print(i)

