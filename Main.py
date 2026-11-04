import os, sys, mutagen
import tkinter as tk
from tkinter import filedialog
import pygame

print(sys.executable)
#audio
pygame.mixer.init()
paused = False
started = False
pos = 0
songLength = 0
startOffset = 0
dragging = False
elapsed = startOffset + pygame.mixer.music.get_pos() / 1000
#playlist
playlist = ["Songs/ChennelRemix.mp3", "Songs/Drake-Gods-Plan.mp3"]
current = len(playlist) - 1

#functions
def addSong():
    path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
    if path:
        playlist.append(path)
        listbox.insert(tk.END, os.path.basename(path))

# moving through the playlist
def play():
    global paused, started, startOffset, songLength
    if not playlist:
        return
    path = playlist[0] if playlist else None
    if path:
        pygame.mixer.music.load(playlist[current])
        pygame.mixer.music.play()
        status.config(text=f"Playing: {os.path.basename(playlist[current])}")

        paused = False
        started = True

        startOffset = 0
        info = mutagen.File(playlist[current])
        songLength = info.info.length if info else 0
        progress.config(to=max(songLength, 1))
        progress.set(0)
def playSelected(event):
    global current
    selection = listbox.curselection()
    if not selection or selection[0] == 0:  # Ignore the "Songs:" label at index 0
        return
    elif selection:
        current = selection[0] - 1  # Adjust for the "Songs:" label at index 0
        path = playlist[current]
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
def nextSong():
    if playlist:
        global current
        if not playlist:
            return
        current = (current + 1) % len(playlist)
        play()
def previousSong():
    if playlist:
        global current
        if not playlist:
            return
        current = (current - 1) % len(playlist)
        play()

# song settings
def togglePause():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
def setVolume(value):
    pygame.mixer.music.set_volume(float(value) / 100)
def checkSongEnd():
    if started and not pygame.mixer.music.get_busy():
        nextSong()
    root.after(1000, checkSongEnd)


    # progress bar
def start_drag(event):
    global dragging
    dragging = True
def seek(event):
    global dragging, startOffset
    dragging = False
    if not started:
        return
    pos = progress.get()
    pygame.mixer.music.play(start=pos)
    startOffset = pos
    if paused:
        pygame.mixer.music.pause()
def update_progress():
    pos = pygame.mixer.music.get_pos()
    global paused, dragging, elapsed, startOffset
    if started and not dragging and not paused:
        pos = pygame.mixer.music.get_pos() 
        if pos >= 0:
            progress.set(startOffset + pos / 1000)

    elapsed = progress.get()
    time_label.config(text=f"{int(elapsed // 60)}:{int(elapsed % 60):02d}")
    root.after(500, update_progress)

# main loop

root = tk.Tk()
root.title("Music Player")
root.geometry("800x600")
root.configure(bg="gray12")

#widgets
status = tk.Label(root, text="No song playing", bg="gray7", fg="white")
status.place(relx=0.5, rely=0.65, anchor=tk.CENTER)


listbox = tk.Listbox(root,highlightbackground="white",  bg="gray7", fg="white", width=60, height=15)
listbox.place(rely=0.3, relx=0.5, anchor=tk.CENTER)
listbox.bind("<Double-1>",playSelected)
listbox.insert(0, "Songs:")

volume = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=setVolume,highlightbackground="white", bg="gray7", fg="white", length=200)
volume_label = tk.Label(root, text="Volume", bg="gray12", fg="white")
volume_label.place(relx=0.5, rely=0.84, anchor=tk.CENTER)
volume.set(20)
volume.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

tk.Button(root, text="Play",          command=play,highlightbackground="white", bg="gray7", fg="white").place(relx=0.5, rely=0.75, anchor=tk.CENTER)
tk.Button(root, text="Next Song",     command=nextSong,highlightbackground="white", bg="gray7", fg="white").place(relx=0.60, rely=0.75, anchor=tk.CENTER)
tk.Button(root, text="Previous Song", command=previousSong,highlightbackground="white", bg="gray7", fg="white").place(relx=0.40, rely=0.75, anchor=tk.CENTER)
tk.Button(root, text="Toggle Pause",  command=togglePause,highlightbackground="white", bg="gray7", fg="white").place(relx=0.5, rely=0.8, anchor=tk.CENTER)
tk.Button(root, text="Add Song",      command=addSong,highlightbackground="white", bg="gray7", fg="white").place(relx=0.1, rely=0.8, anchor=tk.CENTER)


progress = tk.Scale(root, from_=0, to=100, orient="horizontal",
                    showvalue=False, length=400,
                    bg="gray12", troughcolor="gray20", highlightthickness=0)
progress.bind("<Button-1>", start_drag)
progress.bind("<ButtonRelease-1>", seek)
progress.place(relx=0.5, rely=0.52, anchor=tk.CENTER)

time_label = tk.Label(root, text="0:00", bg="gray12", fg="white")
time_label.place(relx=0.5, rely=0.57, anchor=tk.CENTER)

if len(playlist) > 0:
    for song in playlist:
        listbox.insert(tk.END, os.path.basename(song))

update_progress()
checkSongEnd()
root.mainloop()




