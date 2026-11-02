import os
import tkinter as tk
from tkinter import filedialog
import pygame

#audio
pygame.mixer.init()

#playlist
playlist = []

#functions
def openAndPlay():
    path = playlist[0] if playlist else None
    if path:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

def addSong():
    path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
    if path:
        playlist.append(path)
        listbox.insert(tk.END, os.path.basename(path))
def nextSong():
    if playlist:
        current_index = playlist.index(pygame.mixer.music.get_pos())
        next_index = (current_index + 1) % len(playlist)
        pygame.mixer.music.load(playlist[next_index])
        pygame.mixer.music.play()
def previousSong():
    if playlist:
        current_index = playlist.index(pygame.mixer.music.get_pos())
        previous_index = (current_index - 1) % len(playlist)
        pygame.mixer.music.load(playlist[previous_index])
        pygame.mixer.music.play()
def pauseSong():
    pygame.mixer.music.pause()
# main loop

root = tk.Tk()
root.title("Music Player")
root.geometry("800x600")
root.configure(bg="gray12")

#widgets

listbox = tk.Listbox(root,highlightbackground="white",  bg="gray7", fg="white", width=60, height=15)
listbox.place(rely=0.3, relx=0.5, anchor=tk.CENTER)


tk.Button(root, text="Play",          command=openAndPlay,highlightbackground="white", bg="gray7", fg="white").place(relx=0.5, rely=0.75, anchor=tk.CENTER)
tk.Button(root, text="Next Song",     command=nextSong,highlightbackground="white", bg="gray7", fg="white").place(relx=0.60, rely=0.75, anchor=tk.CENTER)
tk.Button(root, text="Previous Song", command=previousSong,highlightbackground="white", bg="gray7", fg="white").place(relx=0.40, rely=0.75, anchor=tk.CENTER)
tk.Button(root, text="Pause Song",    command=pauseSong,highlightbackground="white", bg="gray7", fg="white").place(relx=0.5, rely=0.8, anchor=tk.CENTER)
tk.Button(root, text="Add Song",      command=addSong,highlightbackground="white", bg="gray7", fg="white").place(relx=0.1, rely=0.8, anchor=tk.CENTER)

root.mainloop()




