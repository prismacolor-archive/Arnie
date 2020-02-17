import PySimpleGUI as Sg
import tkinter
from multiprocessing import freeze_support
import datetime

my_file = "U:\\PC NAC\\Data Team\\Work in Progress\\Taylor_R\\Disrupt2020\\Phase1\\SampleDocs_HaveKeyValuePair\\Heartland_Redacted.pdf"


def main():
    freeze_support()
    # set up initial GUI layout
    Sg.change_look_and_feel('BlueMono')

    # layout mapping
    # values[0] == client id
    # values[1] == prior provider
    # values[2] == name of document
    # values[3] == document path

    layout = [Sg.Text('Please enter your client ID:')], \
             [Sg.InputText('')], \
             [Sg.Text('Select Prior Provider')], \
             [Sg.InputCombo(('ADP', 'ADP Run', 'Paychex', 'Paychex Flex',
                                'Paycom', 'Paylocity', 'Other'), size=(45, 3))], \
             [Sg.Text('If you selected "other" in the previous section, please include the name of your prior provider below.')], \
             [Sg.Text('Please enter the name of your document:')], \
             [Sg.InputText('')], \
             [Sg.In('Upload a PDF file'), Sg.FileBrowse(file_types=(("Text Files", "*"),))], \
             [Sg.Button('Run'), Sg.Button('Cancel')]

    window = Sg.Window('Parallel Script Testing Tool', layout)
    event, values = window.read()
    wrong_file_type = False
    ees_can_be_mapped = False

    ClientID = values[0]
    current_timestamp = datetime.datetime.now
    tracking_file = open(r"dist\TF2_tracking.txt", 'a')

    # if prior provider = 'other' then name of doc is values 2, if not it's value 1 + value 2

    if event in (None, 'Cancel'):
        # if user closes window or clicks cancel, terminate process TR
        window.close()
        exit()
    elif event == 'Run':
        try:
            # did the user upload the correct type of document? TR
            if not values[3].endswith('.pdf'):
                Sg.popup('You have entered an invalid file type.')
                wrong_file_type = True
            else:
                ees_can_be_mapped = True
                while ees_can_be_mapped:
                    Sg.popup(values[3])
                    layout2 = [Sg.Text('Please enter the first item of text for your employee:')], \
                             [Sg.InputText('')], \
                             [Sg.Text('Please enter the last item of text for this employee:')], \
                             [Sg.InputText('')], \
                             [Sg.Button('Map'), Sg.Button('Cancel')]
                    window2 = Sg.Window('Parallel Script Testing Tool', layout)
                    event, values = window.read()

                    # ask the client if they are done or have more? if so continue
                    # if not ees_can_be_mapped becomes false and we break

            if ClientID == '123456':
                tracking_file.write('TEST  ')
            tracking_file.write(ClientID + ' ')
            if wrong_file_type:
                tracking_file.write(values[2] + str(current_timestamp) + ' ' + 'User uploaded wrong file type.' + '\n')
            elif values[1] == 'Other':
                tracking_file.write(values[2] + str(current_timestamp) + ' ' + 'Completed' + '\n')
            else:
                tracking_file.write(ClientID + ' ' + values[1] + ' ' + values[2] + ' ' + str(current_timestamp) + ' ' + 'Completed' + '\n')
            tracking_file.close()
            window.close()
            Sg.Popup('Mapping process completed.')

        except Exception as e:
            if ClientID == '123456':
                tracking_file.write('TEST  ')
            tracking_file.write(ClientID + ' ' + values[1] + ' ' + str(current_timestamp) + ' ' + str(e) + '\n')
            tracking_file.close()
            Sg.Popup('Mapping failed. Please contact your consultant.')


if __name__ == '__main__':
    main()