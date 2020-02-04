# import pandas for dataframe storage TR
import pandas

# import PyMuPDF TR
import fitz

# additional processing tools TR
from operator import itemgetter
from itertools import groupby


# set up lists to store rectangle and employee info later TR
my_file = "U:\\PC NAC\\Data Team\\Work in Progress\\Taylor_R\\Disrupt2020\\Phase1\\SampleDocs_HaveKeyValuePair\\Heartland_Redacted.pdf"
mydoc = fitz.Document(my_file)
startcoordinates = []
endcoordinates = []
datatable = []
master_ee_info = []

# loop through the pages in the pdf and gather the text TR
for n in range(mydoc.pageCount):
    page = mydoc.loadPage(n)
    text = page.getText("text")
    words = page.getTextWords()

    datatable.append(words)

    # set up the start and end of each rectangle
    point1 = page.searchFor("Name", hit_max=1)
    point2 = page.searchFor("Miscellaneous Fields", hit_max=1)

    # if a rectangle is found, append the text to a master table
    if point1 and point2:
        startcoordinates.append(point1)
        # print(point1)
        datatable.append(text)
        endcoordinates.append(point2)
        # print(point2)

# now loop through the rectangle coordinates and the text to extract the text inside each rectangle TR
for x, y, z in zip(startcoordinates, endcoordinates, datatable):
    rectangle = x[0] | y[0]
    try:
        eeprofile = [w for w in z if fitz.Rect(w[:4]).intersects(rectangle)]
    except Exception as e:
        print(e)
    eeprofile.sort(key=itemgetter(3, 0))
    stats = groupby(eeprofile, key=itemgetter(3))
    for y1, gwords in stats:
        ee_text = " ".join(w[4] for w in gwords)
        master_ee_info.append(ee_text)

# print(master_ee_info)
ee_dataframe = pandas.DataFrame(master_ee_info)
# print(ee_dataframe)

for i, j in ee_dataframe.iterrows():
    # retrieve the text from inside the data frame TR
    if 'Name:' in j.values[0]:
        ee_start = str(j.values).split()
        lucy = "In the sky"

# this will store the coordinate info for later
masterlist = zip(startcoordinates, endcoordinates, datatable)
my_dataframe = pandas.DataFrame(list(masterlist))

fitz.Document.close(mydoc)
