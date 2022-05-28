from pytube import YouTube
import PySimpleGUI as sg
from pathlib import Path
import socket
import calendar as cal
from tkinter import *
from sys import exit
import os
from PIL import ImageTk,Image
import tkinter as tk
import random
from threading import Lock

startasdef = False
sdefdef = True
start = False

credit = "All the code belong to me :D"
instruction = "After you open the 'main.py', type '/start.def',\nand then '/start.func', and you will be good to go! :D\n"

sayIt = ""

#def func
def Ytconv():
    def progress_check(stream, chunk, bytes_remaining):
        window['-DOWNLOADPROGRESS-'].update(100 - round(bytes_remaining / stream.filesize * 100))

    def on_complete(stream, file_path):
        window['-DOWNLOADPROGRESS-'].update(0)

    sg.theme('Darkred1')
    start_layout = [
        [sg.Input(key='-INPUT-'), sg.Button('submit')],
    ]

    info_tab = [
        [sg.Text('Title:'), sg.Text('', key='-TITLE-')],
        [sg.Text('Length:'), sg.Text('', key='-LENGTH-')],
        [sg.Text('Views:'), sg.Text('', key='-VIEWS-')],
        [sg.Text('Author:'), sg.Text('', key='-AUTHOR-')],
        [sg.Text('Description:'),
         sg.Multiline('', key='-DESCRIPTION-', size=(40, 20), no_scrollbar=True, disabled=True)]
    ]

    download_tab = [
        [sg.Frame('Best Quality', [[sg.Button('Download', key='-BEST-'), sg.Text('', key='-BESTRES-'),
                                    sg.Text('', key='-BESTSIZE-')]])],
        [sg.Frame('Worst Quality', [[sg.Button('Download', key='-WORST-'), sg.Text('', key='-WORSTRES-'),
                                     sg.Text('', key='-WORSTSIZE-')]])],
        [sg.Frame('Audio', [[sg.Button('Download', key='-AUDIO-'), sg.Text('', key='-AUDIOSIZE-')]])],
        [sg.VPush()],
        [sg.Progress(100, orientation='h', size=(20, 20), key='-DOWNLOADPROGRESS-', expand_x=True)]
    ]

    main_layout = [
        [sg.TabGroup([
            [sg.Tab('info', info_tab), sg.Tab('download', download_tab)]])]
    ]

    window = sg.Window('Youtube Downloader', start_layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'submit':
            video_object = YouTube(values['-INPUT-'], on_progress_callback=progress_check,
                                   on_complete_callback=on_complete)
            window.close()

            # main window info setup
            window = sg.Window('Converter', main_layout, finalize=True)
            window['-TITLE-'].update(video_object.title)
            window['-LENGTH-'].update(f'{round(video_object.length / 60, 2)} minutes')
            window['-VIEWS-'].update(video_object.views)
            window['-AUTHOR-'].update(video_object.author)
            window['-DESCRIPTION-'].update(video_object.description)

            # main window download setup
            window['-BESTSIZE-'].update(
                f'{round(video_object.streams.get_highest_resolution().filesize / 1048576, 1)} MB')
            window['-BESTRES-'].update(video_object.streams.get_highest_resolution().resolution)

            window['-WORSTSIZE-'].update(
                f'{round(video_object.streams.get_lowest_resolution().filesize / 1048576, 1)} MB')
            window['-WORSTRES-'].update(video_object.streams.get_lowest_resolution().resolution)

            window['-AUDIOSIZE-'].update(
                f'{round(video_object.streams.get_audio_only().filesize / 1048576, 1)} MB')

        if event == '-BEST-':
            video_object.streams.get_highest_resolution().download()

        if event == '-WORST-':
            video_object.streams.get_lowest_resolution().download()

        if event == '-AUDIO-':
            video_object.streams.get_audio_only().download()

    window.close()
def custometextsay():
    sayIt = input("What do you want me to say?")
    sayItAv = True
    print("If you want to say it, type '/saynow'")
def txteditor():
    smileys = [
        'happy', [':)', 'xD', ':D', '<3'],
        'sad', [':(', 'T_T'],
        'other', [':3', 'UwU']
    ]
    smiley_events = smileys[1] + smileys[3] + smileys[5]

    menu_layout = [
        ['File', ['Open', 'Save', '---', 'Exit']],
        ['Tools', ['Word Count']],
        ['Add', smileys]
    ]

    sg.theme('GrayGrayGray')
    layout = [
        [sg.Menu(menu_layout)],
        [sg.Text('Untitled', key='-DOCNAME-')],
        [sg.Multiline(no_scrollbar=True, size=(40, 30), key='-TEXTBOX-')]
    ]

    window = sg.Window('Text Editor', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == 'Open':
            file_path = sg.popup_get_file('open', no_window=True)
            if file_path:
                file = Path(file_path)
                window['-TEXTBOX-'].update(file.read_text())
                window['-DOCNAME-'].update(file_path.split('/')[-1])

        if event == 'Save':
            file_path = sg.popup_get_file('Save as', no_window=True, save_as=True) + '.txt'
            file = Path(file_path)
            file.write_text(values['-TEXTBOX-'])
            window['-DOCNAME-'].update(file_path.split('/')[-1])

        if event == 'Word Count':
            full_text = values['-TEXTBOX-']
            clean_text = full_text.replace('\n', ' ').split(' ')
            word_count = len(clean_text)
            char_count = len(''.join(clean_text))
            sg.popup(f'words {word_count}\ncharacters: {char_count}')

        if event in smiley_events:
            current_text = values['-TEXTBOX-']
            new_text = current_text + ' ' + event
            window['-TEXTBOX-'].update(new_text)

    window.close()
def chatingsystem():
    chatinput = input("Do you want to be the sender?\nIf yes type 'yes' if no, type 'no'")
    if chatinput == "yes":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect(('localhost', 9999))

        done = False

        while not done:
            client.send(input("Messege: ").encode('utf-8'))
            msg = client.recv(1024).decode('utf-8')
            if msg == "quit":
                done = True
            else:
                print(msg)
    if chatinput == "no":
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 9999))

        server.listen()

        client, addr = server.accept()

        done = False

        while not done:
            msg = (client.recv(1024).decode('utf-8'))
            if msg == 'quit':
                done = True
            else:
                print(msg)
            client.send(input("Messege: ").encode('utf-8'))
def caldussystem():
    for i in range(1, 13):
        print(cal.month(2022, i))
def tetrissystem():
    COLORS = ['gray', 'lightgreen', 'pink', 'blue', 'orange', 'purple']

    class Tetris():
        FIELD_HEIGHT = 20
        FIELD_WIDTH = 10
        SCORE_PER_ELIMINATED_LINES = (0, 40, 100, 300, 1200)
        TETROMINOS = [
            [(0, 0), (0, 1), (1, 0), (1, 1)],  # O
            [(0, 0), (0, 1), (1, 1), (2, 1)],  # L
            [(0, 1), (1, 1), (2, 1), (2, 0)],  # J
            [(0, 1), (1, 0), (1, 1), (2, 0)],  # Z
            [(0, 1), (1, 0), (1, 1), (2, 1)],  # T
            [(0, 0), (1, 0), (1, 1), (2, 1)],  # S
            [(0, 1), (1, 1), (2, 1), (3, 1)],  # I
        ]

        def __init__(self):
            self.field = [[0 for c in range(Tetris.FIELD_WIDTH)] for r in range(Tetris.FIELD_HEIGHT)]
            self.score = 0
            self.level = 0
            self.total_lines_eliminated = 0
            self.game_over = False
            self.move_lock = Lock()
            self.reset_tetromino()

        def reset_tetromino(self):
            self.tetromino = random.choice(Tetris.TETROMINOS)[:]
            self.tetromino_color = random.randint(1, len(COLORS) - 1)
            self.tetromino_offset = [-2, Tetris.FIELD_WIDTH // 2]
            self.game_over = any(not self.is_cell_free(r, c) for (r, c) in self.get_tetromino_coords())

        def get_tetromino_coords(self):
            return [(r + self.tetromino_offset[0], c + self.tetromino_offset[1]) for (r, c) in self.tetromino]

        def apply_tetromino(self):
            for (r, c) in self.get_tetromino_coords():
                self.field[r][c] = self.tetromino_color

            new_field = [row for row in self.field if any(tile == 0 for tile in row)]
            lines_eliminated = len(self.field) - len(new_field)
            self.total_lines_eliminated += lines_eliminated
            self.field = [[0] * Tetris.FIELD_WIDTH for x in range(lines_eliminated)] + new_field
            self.score += Tetris.SCORE_PER_ELIMINATED_LINES[lines_eliminated] * (self.level + 1)
            self.level = self.total_lines_eliminated // 10
            self.reset_tetromino()

        def get_color(self, r, c):
            return self.tetromino_color if (r, c) in self.get_tetromino_coords() else self.field[r][c]

        def is_cell_free(self, r, c):
            return r < Tetris.FIELD_HEIGHT and 0 <= c < Tetris.FIELD_WIDTH and (r < 0 or self.field[r][c] == 0)

        def move(self, dr, dc):
            with self.move_lock:
                if self.game_over:
                    return

                if all(self.is_cell_free(r + dr, c + dc) for (r, c) in self.get_tetromino_coords()):
                    self.tetromino_offset = [self.tetromino_offset[0] + dr, self.tetromino_offset[1] + dc]
                elif dr == 1 and dc == 0:
                    self.game_over = any(r < 0 for (r, c) in self.get_tetromino_coords())
                    if not self.game_over:
                        self.apply_tetromino()

        def rotate(self):
            with self.move_lock:
                if self.game_over:
                    self.__init__()
                    return

                ys = [r for (r, c) in self.tetromino]
                xs = [c for (r, c) in self.tetromino]
                size = max(max(ys) - min(ys), max(xs) - min(xs))
                rotated_tetromino = [(c, size - r) for (r, c) in self.tetromino]
                wallkick_offset = self.tetromino_offset[:]
                tetromino_coord = [(r + wallkick_offset[0], c + wallkick_offset[1]) for (r, c) in
                                   rotated_tetromino]
                min_x = min(c for r, c in tetromino_coord)
                max_x = max(c for r, c in tetromino_coord)
                max_y = max(r for r, c in tetromino_coord)
                wallkick_offset[1] -= min(0, min_x)
                wallkick_offset[1] += min(0, Tetris.FIELD_WIDTH - (1 + max_x))
                wallkick_offset[0] += min(0, Tetris.FIELD_HEIGHT - (1 + max_y))

                tetromino_coord = [(r + wallkick_offset[0], c + wallkick_offset[1]) for (r, c) in
                                   rotated_tetromino]
                if all(self.is_cell_free(r, c) for (r, c) in tetromino_coord):
                    self.tetromino, self.tetromino_offset = rotated_tetromino, wallkick_offset

    class Application(tk.Frame):
        def __init__(self, master=None):
            super().__init__(master)
            self.tetris = Tetris()
            self.pack()
            self.create_widgets()
            self.update_clock()

        def update_clock(self):
            self.tetris.move(1, 0)
            self.update()
            self.master.after(int(1000 * (0.66 ** self.tetris.level)), self.update_clock)

        def create_widgets(self):
            PIECE_SIZE = 30
            self.canvas = tk.Canvas(self, height=PIECE_SIZE * self.tetris.FIELD_HEIGHT,
                                    width=PIECE_SIZE * self.tetris.FIELD_WIDTH, bg="black", bd=0)
            self.canvas.bind('<Left>', lambda _: (self.tetris.move(0, -1), self.update()))
            self.canvas.bind('<Right>', lambda _: (self.tetris.move(0, 1), self.update()))
            self.canvas.bind('<Down>', lambda _: (self.tetris.move(1, 0), self.update()))
            self.canvas.bind('<Up>', lambda _: (self.tetris.rotate(), self.update()))
            self.canvas.focus_set()
            self.rectangles = [
                self.canvas.create_rectangle(c * PIECE_SIZE, r * PIECE_SIZE, (c + 1) * PIECE_SIZE,
                                             (r + 1) * PIECE_SIZE)
                for r in range(self.tetris.FIELD_HEIGHT) for c in range(self.tetris.FIELD_WIDTH)
            ]
            self.canvas.pack(side="left")
            self.status_msg = tk.Label(self, anchor='w', width=11, font=("Courier", 24))
            self.status_msg.pack(side="top")
            self.game_over_msg = tk.Label(self, anchor='w', width=11, font=("Courier", 24), fg='red')
            self.game_over_msg.pack(side="top")

        def update(self):
            for i, _id in enumerate(self.rectangles):
                color_num = self.tetris.get_color(i // self.tetris.FIELD_WIDTH, i % self.tetris.FIELD_WIDTH)
                self.canvas.itemconfig(_id, fill=COLORS[color_num])

            self.status_msg['text'] = "Score: {}\nLevel: {}".format(self.tetris.score, self.tetris.level)
            self.game_over_msg['text'] = "GAME OVER.\nPress UP\nto reset" if self.tetris.game_over else ""

    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
def instructionlist():
    print(instruction)
    print("\n")
def creditlist():
    print(credit)
    print("...and some tutorial...")
def picture_of_a_cat():
    ccaatt = Tk()
    ccaatt.title('Cat')

    my_image = ImageTk.PhotoImage(Image.open("cat.png"))
    my_label = Label(image=my_image)
    my_label.pack()

    ccaatt.mainloop()
def helpsystem():
    problem = input("Whats the problem " + username + "?\n")
    print("Thanks for the problem/bug submition!\n")
def clearingConsole():
    os.system('cls')
    print("command has been cleared")
def showlist():
    print("/clearC\n/help\n/open.picc\n/credit\n/inst\n/calcus\n/tetris.play\n/cald\n/chat\n/text_editor.open\n/ytConv.conv")
    print("\n\n")

#main loop
while True:

    command = input()
    cprom = command

    if command == "/quit":
        exit()

    elif command == "":
        print("☻You Are An Idiot HaHaHaHa☻")

    #/start
    if sdefdef == True:
        if command == "/start.def":
            startasdef = True
            print("the system has been started\nloding...")
            username = input("Enter Username: ")

            print("Welcome back, " + username  + "!")
            sdefdef = False

    #/startfunc
    if startasdef == True:
        if command == "/start.func":
            start = True
            print("System has been started.\n")
            startasdef = False

    if start == True:
        if command == "/showC":
            showlist()
        if command == "/clearC":
            clearingConsole()
        if command == "/help":
           helpsystem()
        if command == "/open.picc":
           picture_of_a_cat()
        if command == "/credit":
            creditlist()
        if command == "/inst":
            instructionlist()
        if command == "/calcus":
            def button_press(num):

                global equation_text

                equation_text = equation_text + str(num)

                equation_label.set(equation_text)


            def equals():

                global equation_text

                try:

                    total = str(eval(equation_text))

                    equation_label.set(total)

                    equation_text = total

                except SyntaxError:

                    equation_label.set("syntax error")

                    equation_text = ""

                except ZeroDivisionError:

                    equation_label.set("arithmetic error")

                    equation_text = ""


            def clear():

                global equation_text

                equation_label.set("")

                equation_text = ""


            window = Tk()
            window.title("Calculator program")
            window.geometry("500x500")

            equation_text = ""

            equation_label = StringVar()

            label = Label(window, textvariable=equation_label, font=('consolas', 20), bg="white", width=24, height=2)
            label.pack()

            frame = Frame(window)
            frame.pack()

            button1 = Button(frame, text=1, height=4, width=9, font=35,
                             command=lambda: button_press(1))
            button1.grid(row=0, column=0)

            button2 = Button(frame, text=2, height=4, width=9, font=35,
                             command=lambda: button_press(2))
            button2.grid(row=0, column=1)

            button3 = Button(frame, text=3, height=4, width=9, font=35,
                             command=lambda: button_press(3))
            button3.grid(row=0, column=2)

            button4 = Button(frame, text=4, height=4, width=9, font=35,
                             command=lambda: button_press(4))
            button4.grid(row=1, column=0)

            button5 = Button(frame, text=5, height=4, width=9, font=35,
                             command=lambda: button_press(5))
            button5.grid(row=1, column=1)

            button6 = Button(frame, text=6, height=4, width=9, font=35,
                             command=lambda: button_press(6))
            button6.grid(row=1, column=2)

            button7 = Button(frame, text=7, height=4, width=9, font=35,
                             command=lambda: button_press(7))
            button7.grid(row=2, column=0)

            button8 = Button(frame, text=8, height=4, width=9, font=35,
                             command=lambda: button_press(8))
            button8.grid(row=2, column=1)

            button9 = Button(frame, text=9, height=4, width=9, font=35,
                             command=lambda: button_press(9))
            button9.grid(row=2, column=2)

            button0 = Button(frame, text=0, height=4, width=9, font=35,
                             command=lambda: button_press(0))
            button0.grid(row=3, column=0)

            plus = Button(frame, text='+', height=4, width=9, font=35,
                          command=lambda: button_press('+'))
            plus.grid(row=0, column=3)

            minus = Button(frame, text='-', height=4, width=9, font=35,
                           command=lambda: button_press('-'))
            minus.grid(row=1, column=3)

            multiply = Button(frame, text='*', height=4, width=9, font=35,
                              command=lambda: button_press('*'))
            multiply.grid(row=2, column=3)

            divide = Button(frame, text='/', height=4, width=9, font=35,
                            command=lambda: button_press('/'))
            divide.grid(row=3, column=3)

            equal = Button(frame, text='=', height=4, width=9, font=35,
                           command=equals)
            equal.grid(row=3, column=2)

            decimal = Button(frame, text='.', height=4, width=9, font=35,
                             command=lambda: button_press('.'))
            decimal.grid(row=3, column=1)

            clear = Button(window, text='clear', height=4, width=12, font=35,
                           command=clear)

            window.mainloop()
        if command == "/tetris.play":
            tetrissystem()
        if command == "/cald":
            caldussystem()
        if command == "/chat":
            chatingsystem()
        if command == "/text_editor.open":
            txteditor()
        if command == "/ytConv.conv":
            Ytconv()