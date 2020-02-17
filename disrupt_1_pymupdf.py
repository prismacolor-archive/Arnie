# import pandas for dataframe storage TR
import pandas

# import PyMuPDF TR
import fitz

# additional processing tools TR
from operator import itemgetter
from itertools import groupby
import csv


# set up lists to store rectangle and employee info later TR
my_file = "U:\\PC NAC\\Data Team\\Work in Progress\\Taylor_R\\Disrupt2020\\Phase1\\SampleDocs_HaveKeyValuePair\\Heartland_Redacted.pdf"
mydoc = fitz.Document(my_file)
startcoordinates = []
endcoordinates = []
datatable = []
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

    datatable.append(words)

    # set up the start and end of each rectangle
    point1 = page.searchFor(starting_point, hit_max=1)
    point2 = page.searchFor(end_point, hit_max=1)

    # if a rectangle is found, append the start and stop points to a list
    # if point1 and point2:
    #     startcoordinates.append(point1)
    #     endcoordinates.append(point2)

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
            print(ee_text)
            master_ee_info.append(ee_text)

        # need to figure out what rectangle values mean
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

# now loop through the rectangle coordinates and the text to extract the text inside each rectangle TR
'''for x, y, z in zip(startcoordinates, endcoordinates, datatable):
    rectangle = x[0] | y[0]
    try:
        eeprofile = [w for w in z if fitz.Rect(w[:4]).intersects(rectangle)]
        # eeprofile = [w for w in z if fitz.Rect(w[:4]) in rectangle]
    except Exception as e:
        print(e)
        continue
    eeprofile.sort(key=itemgetter(3, 0))
    stats = groupby(eeprofile, key=itemgetter(3))
    for y1, gwords in stats:
        ee_text = " ".join(w[4] for w in gwords)
        # print(ee_text)
        master_ee_info.append(ee_text)
    # need to figure out what rectangle values mean
    for item in z:
        data_dict = {}
        data_dict['X1'] = item[0]
        data_dict['Y1'] = item[1]
        data_dict['X2'] = item[2]
        data_dict['Y2'] = item[3]
        data_dict['Text'] = item[4]
        data_dict['Block Number'] = item[5]
        data_dict['Line Number'] = item[6]
        data_dict['Word Number'] = item[7]
        storage.append(data_dict)'''

ee_dataframe = pandas.DataFrame(master_ee_info)
# print(ee_dataframe)

# this will store the coordinate info for later
masterlist = zip(startcoordinates, endcoordinates, datatable)
my_dataframe = pandas.DataFrame(list(masterlist))

fitz.Document.close(mydoc)

# with open('sample_data14.csv', 'w+', newline='') as f:
with open('sample_data_16.csv', 'w+', newline='') as f:
    writer = csv.DictWriter(f, ['X1', 'Y1', 'X2', 'Y2', 'Text', 'Block Number', 'Line Number', 'Word Number'])
    writer.writeheader()

    for item in storage:
        writer.writerow(item)
print(storage)
