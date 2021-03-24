import subprocess
import sys
import PySimpleGUI as sg
import time

'''Add findImages script for popup icons and images'''


class UI():

    def __init__(self, run):
        self.appName = 'OMEGA-DMCA-LUL'
        self.windowColor = sg.theme('DefaultNoMoreNagging')
        self.layout = [[sg.Image(r'D:\pyPlaylist\assets\FMAsymbole.png'), sg.T('Chose song/playlist URL', key='input')],
                       [sg.In('', key='url',),
                        sg.Image(r'D:\pyPlaylist\assets\addURL.png',
                                 key='Confirm URL', enable_events=True),
                        sg.Image(r'D:\pyPlaylist\assets\reset.png',
                                 key='Clear URL', enable_events=True, size=(125, 38)),
                        sg.Button('Cancel')],
                       [sg.Output(size=(88, 20), key='output')],
                       [sg.Image(r'D:\pyPlaylist\assets\firstButton.png', key='URL Playlist', enable_events=True),
                        sg.Button('File of URLS'),
                        sg.Button('Version checker'), sg.Button('help')]]
        self.operationsComplete = 0
        self.event = ''
        self.values = ''
        self.startDownload = None
        self.version = ''
        self.helpText = ''

        self.run = run
        self.activeWindow = ()

        self.command = 'youtube-dl'

        self.userConfig = []
        self.configOptions = {'-i': 'errors dont halt download',
                              '--yes-playlist': 'if url is a playlist download each entry',
                              '-a': 'File containing URLs to download', }
        self.link = ''

    def Run(self):
        self.loopCount = 0
        if self.run:

            self.activeWindow = sg.Window(self.appName, self.layout)
            sg.PopupOK('Launched successfully!',
                       image=r'D:\melee-custom-files\Shared animations\EfCoData.dat_0x4CDA0_9.png')

            while self.run:
                
                self.event, self.values = self.activeWindow.read()
                self.staticButtons(self.event)
                self.activeButtons(self.event)

                self.loopCount += 1

                if len(self.userConfig) > 5:
                    sg.popup_error('arguments over 3 double check command', self.userConfig,
                                   title='Slowdown Warning', image=r'D:\melee-custom-files\luigi\EfMrData.dat_0x7A0_9.png')

                elif self.operationsComplete !=0 and self.loopCount < self.operationsComplete:
                    sg.popup_error('BIG PROBLEM BECAUSE YOUR CODE IS BAD', self.link, self.event, self.values, self.userConfig,
                                   image=r'D:\melee-custom-files\luigi\EfMrData.dat_0x17A0_9.png', title='Fatal Error!!!!!!')
                    sys.exit()
                
    """Create an array for button names to futher remove hard coding'"""

    def activeButtons(self, arg1):
        '''This has to get broken down into managable piceaces
            1. turn subprocess.Popen into a static method - after button event ary 
            2. we need a better way to manage event names - STATIC AND NORM BUTTONS NOW!
            3. MAYBE turn all the button events into there own functions. - STARTED
        '''
        if arg1 == 'Confirm URL':
            key = self.configOptions.keys()
            self.link = self.activeWindow.ReturnValuesList[0]
            
            for i in key:
                if i == '-i':
                    self.userConfig += [self.command, i, self.link]
                    print(self.link)
                break

        elif arg1 == 'URL Playlist':
            """stop using Hardcodded arguments for CLI- NEVERMIND NOT FIXED"""

            if len(self.userConfig) > 0:
                self.userConfig.insert(2, '--yes-playlist')
            else:
                self.userConfig *= 0

            print('Starting Download')
            if self.link != '':
                self.startDownload = subprocess.Popen(self.userConfig, stdout=subprocess.PIPE,
                                                      stderr=subprocess.STDOUT)
                for line in iter(self.startDownload.stdout.readline, b''):
                    self.operationsComplete += 1
                    print(self.operationsComplete)
                    print(">>> " + str(line).rstrip())
                    time.sleep(0.01)
                    self.loopCount += 1
                self.userConfig *= 0
                print('Done, cleared URL config: ', self.userConfig)
        else:
            print('Recursive start#: ', self.loopCount)

    def staticButtons(self, pressedButton):
        if pressedButton == 'Cancel' or sg.WIN_CLOSED:
            self.activeWindow.close()
            self.run = False
        try:
            if self.event == sg.WIN_CLOSED:
                self.activeWindow.close()
                self.helpText.kill
                self.version.kill
                self.startDownload.kill
        except AttributeError or ValueError:
            sys.exit

        if pressedButton == 'help':
            self.helpText = subprocess.Popen([self.command, '-h'], stdout=subprocess.PIPE,
                                             stderr=subprocess.STDOUT)

            for helpLine in iter(self.helpText.stdout.readline, b''):
                print('>>> ' + str(helpLine).rstrip())
                self.userConfig *= 0

        elif pressedButton == 'Clear URL':

            self.activeWindow['url'].update('')
            sg.Popup('url cleared of chache',
                     image=r'D:\melee-custom-files\Shared animations\EfCoData.dat_0x4CDA0_92.png')
            self.userConfig *= 0

        elif pressedButton == 'Version checker':

            self.version = subprocess.Popen([self.command, '--version'], stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT)
            for line0 in iter(self.version.stdout.readline, b''):
                print('>>> ' + str(line0).rstrip())

    def runCLI(self, pressedButton, buttonNames):
        for name, modifier in buttonNames:
            if pressedButton == name:
                 self.userConfig


on = True
program = UI(on).Run()
