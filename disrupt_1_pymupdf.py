# import pandas for dataframe storage TR
import pandas

# import PyMuPDF TR
import fitz

# additional processing tools TR
import datetime
from operator import itemgetter
from itertools import groupby
import csv

# create and clean a timestamp for data outputs
timestamp = str(datetime.datetime.now())
timestamp = timestamp.split('.')[0].replace('-', '_')
timestamp = timestamp.replace(' ', '_')
timestamp = timestamp.replace(':', '')

# set up lists to store rectangle and employee info later TR
my_file = "U:\\PC NAC\\Data Team\\Work in Progress\\Taylor_R\\Disrupt2020\\Phase1\\SampleDocs_HaveKeyValuePair\\Heartland_Redacted.pdf"
mydoc = fitz.Document(my_file)

# this is to store the data for possible manipulation, unsure if this is final solution TR
master_ee_info = []

# this will be for storing things in a database to train our model TR
storage = []

# on this particular document, starting_point should be 'Name:' and end should be 'Miscellaneous Fields' TR
# ideally we would need an example of this, maybe there's a short tutorial video the client can watch to get help with this
starting_point = input('Please type the first word in the employee profile. (e.g. Name:, Employee:): ')
end_point = input('Please type the last word in the employee profile. (e.g. Taxes:, Miscellaneous:): ')

# loop through the pages in the pdf and gather the text TR
for n in range(mydoc.pageCount):
    page = mydoc.loadPage(n)
    text = page.getText("text")
    words = page.getTextWords()

    # set up the start and end of each rectangle
    point1 = page.searchFor(starting_point, hit_max=1)
    point2 = page.searchFor(end_point, hit_max=1)

    # if a rectangle is found, retrieve the text from within the rectangle TR
    # note that this currently only works if the rectangle is all on one page
    if point1 and point2:
        rectangle = point1[0] | point2[0]
        try:
            eeprofile = [w for w in words if fitz.Rect(w[:4]).intersects(rectangle)]
        except Exception as e:
            print(e)
            continue
        eeprofile.sort(key=itemgetter(3, 0))
        stats = groupby(eeprofile, key=itemgetter(3))
        for y1, gwords in stats:
            ee_text = " ".join(w[4] for w in gwords)

        # need to figure out what rectangle values exactly mean
        for item in eeprofile:
            data_dict = {}
            data_dict['X1'] = item[0]
            data_dict['Y1'] = item[1]
            data_dict['X2'] = item[2]
            data_dict['Y2'] = item[3]
            data_dict['Text'] = item[4]
            data_dict['Block Number'] = item[5]
            data_dict['Line Number'] = item[6]
            data_dict['Word Number'] = item[7]
            storage.append(data_dict)
            master_ee_info.append(item[4])

# close the document TR
fitz.Document.close(mydoc)

# Create a dataframe with all of the info TR
ee_dataframe = pandas.DataFrame(master_ee_info)
dataframe_output = 'test_outputs\\dataframe_' + timestamp + '.xlsx'
ee_dataframe.to_excel(dataframe_output)

# write the data to a csv file for review TR
output_file = 'test_outputs\\sample_data_' + timestamp + '.csv'
with open(output_file, 'w+', newline='') as f:
    writer = csv.DictWriter(f, ['X1', 'Y1', 'X2', 'Y2', 'Text', 'Block Number', 'Line Number', 'Word Number'])
    writer.writeheader()

    for item in storage:
        writer.writerow(item)

x = 5



