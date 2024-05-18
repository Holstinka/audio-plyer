import os
import tkinter as tk
import threading
import time
from tkinter.ttk import Progressbar, Scale
from tkinter import filedialog
from pygame import mixer


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x500')
        self.resizable(False, False)
        self.title('love music')
        self.config(bg='#beedd3')
        self.select_song_index = 0        
        self.check_directory()
        self.plalylists_flag = False
        
    #проверка наличиия директории
    def check_directory(self):
        if os.path.isfile('path.txt'):
            self.music_window()
        else:            
            self.lab_path = tk.Label(self, text='Здравствуйте, выберете папку с музыкой', font=('Arial,bold', 18), bg='#beedd3')
            self.lab_path.place(x=80, y=100)

            self.start_btn = tk.Button(text='Выбрать', width=25, height=3, command=self.path_to_mus)
            self.start_btn.place(x=200, y=200)              

    # запрос директории 
    def path_to_mus(self):
        self.path = filedialog.askdirectory()
        with open(f'path.txt', 'w') as file:
            file.write(self.path)
            print('файл записан')
        self.music_window()   
            
    def music_window(self):        
        #фрэймы
        self.f_top_menu = tk.Frame(self, width=600, height=100, bg='#a9d6bd')
        self.f_player = tk.Frame(self, width=600, height=350, bg='#8cc2a4')
        self.f_playlist = tk.Frame(self, width=400, height=150, bg='#ebfaf2')

        self.f_top_menu.pack(anchor='nw')
        self.f_player.pack(anchor='w')
        self.f_playlist.pack(anchor='sw')

        self.pack_frame = tk.Frame(self, width=300, height=500, bg='#ebfaf2')

        #название
        btn_path = tk.Button(self.f_top_menu, text='Сменить папку', command=self.next_path).pack()
        l_title = tk.Label(self.f_top_menu, text="Love Music")
        l_title.pack()        

        #плэйлист
        self.scroll = tk.Scrollbar(self.f_playlist)
        self.playlist = tk.Listbox(self.f_playlist, selectmode=tk.SINGLE, width=380, height=50, font=('Arial,bold', 13), bg='#ebfaf2', fg='#153642', selectbackground="lightblue", cursor="hand2", bd=0, yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.playlist.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.playlist.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.playlist.bind('<<ListboxSelect>>', self.set_active_song)
      
        self.addMusic()
        self.player()   

    def addMusic(self):
        with open('path.txt', 'r') as file:
            self.path = file.readline()
        os.chdir(self.path)
        self.files = os.listdir(self.path)
        self.songs = []
        self.len_playlist = 0
        for file in self.files:
            if file.endswith('.mp3'):
                self.songs.append(file)
                self.len_playlist += 1
                self.playlist.insert(tk.END, file) 

    def next_path(self):
        os.remove("../path.txt")
        os.chdir('../C')
        self.f_top_menu.pack_forget()
        self.f_player.pack_forget()
        self.f_playlist.pack_forget()
        self.lab_path = tk.Label(self, text='Здравствуйте, выберете папку с музыкой', font=('Arial,bold', 18), bg='#beedd3')
        self.lab_path.place(x=80, y=100)

        self.start_btn = tk.Button(text='Выбрать', width=25, height=3, command=self.path_to_mus)
        self.start_btn.place(x=200, y=200)
    
    #--------------------------------------DONE-----------------------------------------------------------
    def play_mus(self):
        self.songname = tk.Label(self.f_player, text=self.songs[self.select_song_index][0:-4]).place(x=250, y=300)
        mixer.music.load(self.songs[self.select_song_index])
        mixer.music.play()          

    # выбор песни
    def set_active_song(self, a):
        mixer.music.stop()
        currsell = self.playlist.curselection()
        self.select_song_index = currsell[0]
        self.play_mus()

    # start
    def start_music(self):        
        self.play_mus()
        self.btn_control = tk.Button(self.f_player, image=self.im_play,  height=50, width=50, command=self.pause_music).place(x=270, y=100)

    # pause
    def pause_music(self):       
        mixer.music.pause()
        self.btn_control = tk.Button(self.f_player, image=self.im_pause,  height=50, width=50, command=self.unpause_music).place(x=270, y=100)

    # unpause
    def unpause_music(self):
        mixer.music.unpause()
        self.btn_control = tk.Button(self.f_player, image=self.im_play,  height=50, width=50, command=self.pause_music).place(x=270, y=100)        

    # предыдущая песня
    def left(self):
        if 0 < self.select_song_index <= self.len_playlist-1:
            self.select_song_index -= 1
            self.play_mus()
    # следующая песня
    def rigth(self):
        if 0 <= self.select_song_index < self.len_playlist-1:
            self.select_song_index += 1
            self.play_mus()        
    #---------------------------------DONE---------------------------------------------------------------      

    def player(self):

        self.im_pause = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), './png/pause.png'))
        self.im_play = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), './png/play.png'))
        self.btn_control = tk.Button(self.f_player, image=self.im_play,  height=50, width=50, command=self.start_music).place(x=270, y=100)
        
        self.lefti = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), './png/лево.png'))
        self.rigthi = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), './png/право.png'))

        self.btn_left = tk.Button(self.f_player, image=self.lefti, height=200, width=50, command=self.left).place(x=5, y=50)
        self.btn_rigth = tk.Button(self.f_player, image=self.rigthi, height=200, width=50, command=self.rigth).place(x=540, y=50)

        self.songname = tk.Label(self.f_player, text=self.songs[self.select_song_index][0:-4]).place(x=250, y=300)

mixer.init()
root = Window()


root.mainloop() 