import random
import os, sys, mutagen
import tkinter as tk
from tkinter import filedialog
import pygame
from PIL import Image, ImageTk

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
shuffled = False




musicFolder = "Songs"
playlist = [
    os.path.join(musicFolder, file)
    for file in os.listdir(musicFolder)
    if file.lower().endswith(".mp3")
]
current = 0


# Joy
pictureFolder = "images"

pictures = [
    file for file in os.listdir(pictureFolder)
    if file.lower().endswith((".png", ".gif"))
]

random_picture = random.choice(pictures)

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
        changeImage()
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
    global paused

    if not paused:
        pygame.mixer.music.pause()
        paused = True
    else:
        pygame.mixer.music.unpause()
        paused = False
def toggleShuffle():
    global playlist, current, shuffled
    shuffled = not shuffled

    if shuffled and len(playlist) > 1:
        current_song = playlist[current]
        random.shuffle(playlist)
        current = playlist.index(current_song)

def setVolume(value):
    pygame.mixer.music.set_volume(float(value) / 100)
def checkSongEnd():
    if started and not paused and not shuffled and not pygame.mixer.music.get_busy():
        nextSong()
    elif started and not paused and shuffled and not pygame.mixer.music.get_busy():
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
def changeImage():
    global img

    random_picture = random.choice(pictures)

    img = Image.open(os.path.join(pictureFolder, random_picture))
    img.thumbnail((200, 200))
    img = ImageTk.PhotoImage(img)

    image_label.config(image=img)

def chooseFolder():
    global current, started, paused
    folder = filedialog.askdirectory(
        initialdir=os.path.expanduser("~/Music"),
        title="Choose your music folder"
    )
    if not folder:
        return  # user cancelled the dialog

    songs = sorted(
        os.path.join(folder, file)
        for file in os.listdir(folder)
        if file.lower().endswith(".mp3")
    )
    if not songs:
        status.config(text="No .mp3 files in that folder")
        return

    # stop the old song and reset the flags, otherwise checkSongEnd
    # sees the stopped music and starts playing the next song by itself
    pygame.mixer.music.stop()
    started = False
    paused = False

    playlist[:] = songs   # replace the contents in place so every function sees the new list
    current = 0

    listbox.delete(1, tk.END)  # keep the "Songs:" label at index 0
    for song in playlist:
        listbox.insert(tk.END, os.path.basename(song))

    status.config(text="No song playing")
    progress.set(0)


# main loop

root = tk.Tk()
root.title("Music Player")
root.geometry("800x600")
root.configure(bg="gray12")

#widgets
img = Image.open(os.path.join(pictureFolder, random_picture))
img.thumbnail((150, 150))
img = ImageTk.PhotoImage(img)
image_label = tk.Label(root, image=img, bg="gray12")
image_label.place(relx=0.1, rely=0.15, anchor=tk.CENTER)

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

tk
tk.Button(root, text="Play",          command=play,highlightbackground="white", bg="gray7", fg="white").place(relx=0.5, rely=0.75, anchor=tk.CENTER)
tk.Button(root, text="Next Song",     command=nextSong,highlightbackground="white", bg="gray7", fg="white").place(relx=0.60, rely=0.75, anchor=tk.CENTER)
tk.Button(root, text="Previous Song", command=previousSong,highlightbackground="white", bg="gray7", fg="white").place(relx=0.40, rely=0.75, anchor=tk.CENTER)
tk.Button(root, text="Toggle Pause",  command=togglePause,highlightbackground="white", bg="gray7", fg="white").place(relx=0.5, rely=0.8, anchor=tk.CENTER)
tk.Button(root, text="Add Song",      command=addSong,highlightbackground="white", bg="gray7", fg="white").place(relx=0.1, rely=0.8, anchor=tk.CENTER)
tk.Button(root, text="Choose Folder", command=chooseFolder,highlightbackground="white", bg="gray7", fg="white").place(relx=0.1, rely=0.87, anchor=tk.CENTER)
tk.Button(root, text="Toggle Shuffle", command=toggleShuffle,highlightbackground="white", bg="gray7", fg="white").place(relx=0.1, rely=0.94, anchor=tk.CENTER)
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




