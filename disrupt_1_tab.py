import PyPDF4
import sqlite3
import io

pdf_file = open("U:\PC NAC\Data Team\Work in Progress\Taylor_R\Disrupt2020\Phase1\SampleDocs_HaveKeyValuePair\Heartland_Redacted.pdf", 'rb')
read_pdf = PyPDF4.PdfFileReader(pdf_file)
num_of_pgs = read_pdf.getNumPages()

conn = sqlite3.connect('experiment.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Employees
    ([employee_info] STRING)''')
conn.commit()


def pdf_to_db(some_cursor):
    for num in range(0, num_of_pgs):
        page = read_pdf.getPage(num)
        page_content = page.extractText().encode('utf-8')


        cursor.execute('''INSERT INTO Employees (employee_info)
            Values(page_line)''')


pdf_to_db(cursor)


conn.close()