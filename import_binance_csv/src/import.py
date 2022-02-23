import csv
from operator import delitem

# csv file name
filename = "/media/binanceus_2020.csv"
 
# initializing the titles and rows list
fields = []
rows = []

with open(filename, newline='\n') as csvfile:
    reader = csv.reader(csvfile)

    # extracting field names through first row
    fields = next(reader)

     # extracting each data row one by one
    for row in reader:
        rows.append(row)

print('Field names are:' + ', '.join(field for field in fields))

#  printing first 5 rows
print('\nFirst 5 rows are:\n')
for row in rows[:5]:
    # parsing each column of a row
    for col in row:
        print("%10s"%col,end=" "),
    print('\n')