from random import random, randint
from datetime import datetime
import PySimpleGUI as sg
from os import system
import time

ui_back, ui_mid, ui_front, ui_text = '#373737', '#404040', '#505050', '#A4A4A4'
sg.theme_background_color(ui_mid)
sg.theme_button_color((ui_text, ui_back))
sg.theme_element_background_color(ui_mid)
sg.theme_input_background_color(ui_back)
sg.theme_text_element_background_color(ui_mid)
sg.theme_element_text_color('white')
sg.theme_input_text_color('white')
sg.theme_text_color(ui_text)
sg.theme_element_text_color(ui_text)
sg.theme_input_text_color(ui_text)
# sg.theme('SystemDefaultForReal')

frame1 = [[sg.Text('Key:         '), sg.Input(size=(12,1))],
          [sg.Text('Epochs:     '), sg.Spin([i for i in range(1, 501)], 5, size=(10,1))],
          [sg.Text('Batch Size:'), sg.Spin([i for i in range(1, 65)], 1, size=(10,1))],
          [sg.Radio('CPU', 1), sg.Radio('GPU', 1, True)]]

frame2 = [[sg.ProgressBar(100, size=(52,8), bar_color=(ui_front, ui_back), key='prog')],
          [sg.Output((80,7))]]

# frame2 = [[sg.ProgressBar(100, size=(52,8), bar_color=(ui_front, ui_back), key='prog')]]    # debug layout

layout = [[sg.Column([[sg.Frame('Setup', frame1)],
                      [sg.Button('Start', size=(8,1)),
                       sg.Button('Stop', size=(6,1), disabled=True),
                       sg.Button('Exit', size=(4,1))]]),
           sg.Frame('Status', frame2)],
          [sg.StatusBar('Start Time:         '+('    '*5)+'Elapsed Time:         ', size=(100,1), key='timer')]]

window = sg.Window('LILLIAN', layout, icon='./icons/logo-flat.ico')

def errorcheck():
    if value[0] == '':
        print('Error: missing key')
        return ValueError
    if int(value[1]) <= 0:
        print('Error: epochs must be >0')
        return ValueError
    if int(value[2]) <= 0:
        print('Error: batch size must be >0')
        return ValueError

start = time.time()
def timer():
    elap = time.time() - start
    startlist = time.localtime(start)
    elaplist = time.localtime(elap)
    window['timer'].Update(f'Start Time: {startlist[3]}:{startlist[4]}:{startlist[5]}'+('    '*5)+
                           f'Elapsed Time: {elaplist[3]}:{elaplist[4]}:{elaplist[5]}')
    time.sleep(.5)

def progress():
    percent = 0
    print('Started')

    while True:
        timer()
        event, value = window.read(timeout=100)
        if event == 'Stop':
            window['prog'].UpdateBar(0)
            window['Start'].Update(disabled=False)
            window['Stop'].Update(disabled=True)
            print(f'Stopped at {percent}%')
            break
        if percent > 100:
            print('Finished')
            window['Start'].Update(disabled=False)
            window['Stop'].Update(disabled=True)
            break
        step = randint(1, 10)
        percent = percent + step
        window['prog'].UpdateBar(percent)
        time.sleep(random())

while True:
    event, value = window.read()
    if event == 'Start':
        if errorcheck() == ValueError: continue
        window['Start'].Update(disabled=True)
        window['Stop'].Update(disabled=False)
        print(f'Key: {value[0]}\nEpochs: {value[1]}\nBatch Size: {value[2]}')
        progress()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
window.close()
