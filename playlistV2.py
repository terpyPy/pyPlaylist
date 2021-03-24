import subprocess
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import WIN_CLOSED, Window


class UI():
    
    sg.LOOK_AND_FEEL_TABLE['my_new_theme'] = {'BACKGROUND': '#00003a',
                                            'TEXT': '#ffffff',
                                            'INPUT': '#778899',
                                            'TEXT_INPUT': '#000000',
                                            'SCROLL': '#c7e78b',
                                            'BUTTON': ('white', '#3e0000'),
                                            'PROGRESS': ('#01826B', '#D0D0D0'),
                                            'BORDER': 1,
                                            'SLIDER_DEPTH': 0,
                                            'PROGRESS_DEPTH': 0}

    def __init__(self):
        # the app window
        self.appName = 'OMEGA-DMCA-LUL'
        self.windowColor = sg.theme('my_new_theme')
        self.layout = [
            [sg.Image(r'assets\FMAsymbole.png'),
             sg.T('Chose song/playlist URL', key='input')],
            [sg.In('', key='url',)],
            [sg.Button('Confirm URL',image_filename=r'assets\addURL.png',
                       key='Confirm URL'),
             sg.Button('Clear URL', image_filename=r'assets\addURL.png',
                       key='Clear URL', size=(125, 38)),
             sg.Button('Cancel',image_filename=r'assets\addURL.png'),
             ],

            [sg.Output(size=(88, 22), key='output')],
            [sg.Button('download', image_filename=r'assets\addURL.png',
                       key='download'),
             sg.Button('auto Gen subtitles', image_filename=r'assets\addURL.png'),
             sg.Button('Version checker', image_filename=r'assets\addURL.png'),
             sg.Button('help', image_filename=r'assets\addURL.png'),
             ],
        ]
        self.event = ''
        self.values = ''
        self.startDownload = None
        self.link = None
        self.activeWindow = sg.Window(self.appName, self.layout)
    # app state and events handler

    def loadargs(self):
        self.currentData = []
        if not self.event == 'Cancel' or sg.WIN_CLOSED:
            self.event, self.values = self.activeWindow.read()
            self.currentData = self.buttonFunction(self.event)
            if self.currentData:
                print('current command: ', ' '.join(self.currentData))
        elif self.event == WIN_CLOSED:
                self.activeWindow.close()    
    # button functions

    def buttonFunction(self, button):
        if button:
            argList = ['youtube-dl', '-i', '-h', '--yes-playlist',
                    self.values['url'], self.event, self.currentData,
                    '--version', '--write-auto-sub', '--skip-download', '--sub-format best']
            eventButtons = {'Confirm URL': [argList[0], argList[1], argList[3], argList[4]],
                        'Clear URL': '',
                        'download': argList[6],
                        'help': [argList[0], argList[2]],
                        'Cancel': argList[5],
                        'Version checker': [argList[0], argList[7]],
                        'auto Gen subtitles': [argList[0], argList[8], argList[4], argList[9]],
                        }

            if button == 'download':
                self.currentData = eventButtons[button]
                self.download()
        
            else:
                if button:
                    return eventButtons[button]

    # the download handler
    def download(self):

        layout = [[sg.Text('download')],
                  [sg.ProgressBar(1, orientation='h', size=(
                      20, 20), key='progress')],
                  [sg.Cancel()]]
        i = 0
        # create the form`
        with subprocess.Popen(self.currentData, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as run:
            window = sg.Window('Custom Progress Meter', layout)
            progress_bar = window['progress']
            
            # loop that would normally do something useful
            
            for line0 in iter(run.stdout.readline, b''):
                i+=1
                # check to see if the cancel button was clicked and exit loop if clicked
                event, values = window.read(timeout=0)
                if event == 'Cancel' or event == None:
                    break
                    # update bar with loop value +1 so that bar eventually reaches the maximum
                print('>>> ' + str(line0, 'utf-8'))
                progress_bar.update_bar(i, 6)

                # done with loop... need to destroy the window as it's still open
        window.close()


UI().loadargs()
