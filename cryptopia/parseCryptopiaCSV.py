# Export cryptopia trades through website menu
# Run script:
#   python3 parseCryptopiaCSV.py trades.csv > myCSV.csv

import csv

def parseCSV(file):
  source = "cryptopia"

  with open(file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    index = 0
    for row in reader:
      index += 1
      if (index == 1):
        print("Date,Action,Source,Symbol,Volume,Price,Currency")
        continue

      # date
      date = row[6]
      dayMonthYear, time, amPm = date.split(' ')
      day, month, year = dayMonthYear.split('/')
      hour, minute, second = time.split(':')
      if (amPm == "PM"):
        hour = str((int(hour)+12)%24)
      date = ("%s-%s-%s %s:%s:%s") % (year, month, day, hour, minute, second)

      # coin
      symbol, currency = row[1].split('/')
      action = row[2]
      volume = row[4]
      price = row[3]

      print('%s,%s,%s,%s,%s,%s,%s' % (date, action, source, symbol, volume, price, currency))



fname = sys.argv[1]
parseCSV(fname)
