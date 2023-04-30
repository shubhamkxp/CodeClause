from tkinter import *
import pygame
from tkinter import filedialog
from PIL import Image, ImageTk
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('Music Player')
root.iconbitmap("C:/Users/shubh/Desktop/MusicPlayer/Images/Musicplayer_Icon.png")
root.geometry("500x400")

# Initializing Pygame Mixer
pygame.mixer.init()


# Add Song Function
def add_song():
    song = filedialog.askopenfilename(initialdir="C:/Users/shubh/Desktop/MusicPlayer/Music/", title="Pick a song",
                                      filetypes=(("mp3 Files", "*.mp3"), ("wav Files", '*.wav'), ("All Files", '*.*')))

    # Filtering Name
    song = song.replace("C:/Users/shubh/Desktop/MusicPlayer/Music/", "")
    song = song.replace(".mp3", "")

    # Add song to listbox
    song_box.insert(END, song)


def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="C:/Users/shubh/Desktop/MusicPlayer/Music/",
                                        title="Pick all the songs",
                                        filetypes=(("mp3 Files", "*.mp3"), ("wav Files", '*.wav'), ("All Files", '*.*')))

    # Filtering Names
    for song in songs:
        song = song.replace("C:/Users/shubh/Desktop/MusicPlayer/Music/", "")
        song = song.replace(".mp3", "")

        # Add song to listbox
        song_box.insert(END, song)


# Play Selected Song
def play():

    # Set Stopped variable to false so song can play
    global stopped
    stopped = False

    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)

    song = song_box.get(ACTIVE)
    song = f'C:/Users/shubh/Desktop/MusicPlayer/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Call the play_time fn to get song length
    play_time()

    # Update Slider position
    # slider_position = int(song_length)
    # my_slider.config(to=slider_position, value=0)


# Stop playing the current song
global stopped
stopped = False


def stop():
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # Stop playing the song
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    # Clear the Status Bar
    status_bar.config(text="")

    # Set Stop Variable to True
    global stopped
    stopped = True


global paused
paused = False


# Pause and Unpause the current Song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True


def forward():
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # Get the current song number
    next_song = song_box.curselection()
    # Add one to the current one to skip to next
    next_song = next_song[0] + 1
    song = song_box.get(next_song)

    song = f'C:/Users/shubh/Desktop/MusicPlayer/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bar in the player
    song_box.selection_clear(0, END)

    # Activate new song bar
    song_box.activate(next_song)

    # Set Active Bar to Next Song
    song_box.selection_set(next_song, last=None)


def backward():
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # Get the current song number
    last_song = song_box.curselection()
    # Add one to the current one to skip to next
    last_song = last_song[0] - 1
    song = song_box.get(last_song)

    song = f'C:/Users/shubh/Desktop/MusicPlayer/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bar in the player
    song_box.selection_clear(0, END)

    # Activate new song bar
    song_box.activate(last_song)

    # Set Active Bar to Next Song
    song_box.selection_set(last_song, last=None)


# Remove a song
def remove_song():
    stop()
    # Delete Currently Selected Song
    song_box.delete(ANCHOR)
    # Stop Music
    pygame.mixer.music.stop()


# Clear the playlist
def clear_playlist():
    stop()
    # Delete all songs
    song_box.delete(0, END)
    # Stops music
    pygame.mixer.music.stop()


global song_length
song_length = False


# Grab Song Time Info
def play_time():
    # Check for double speed of timing
    if stopped:
        return

    # Grab Current time of Ongoing Song
    current_time = pygame.mixer.music.get_pos() / 1000

    # Converting to Time Format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    song = song_box.get(ACTIVE)
    # Add directory structure
    song = f'C:/Users/shubh/Desktop/MusicPlayer/Music/{song}.mp3'

    # Load song with Mutagen
    song_mut = MP3(song)
    # Get song length
    global song_length
    song_length = song_mut.info.length

    # Convert to Time Format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # Increase current time by 1 sec
    current_time += 1

    if int(my_slider.get()) == int(song_length):
        # Output Time to Status Bar
        status_bar.config(text=f'Time Elapsed: {converted_song_length}  of  {converted_song_length}  ')
    elif paused:
        pass

    elif int(my_slider.get()) == int(current_time):
        # Update Slider position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        # Update Slider position According to Time

        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        # convert to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        # Output time to status bar
        status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

        # Move this thing along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    # Update Time
    status_bar.after(1000, play_time)


def slide(x):
    # Converting Current Time to Time Format
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    # Convert to Time Format
    #converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    #my_slider.config(text=f'{converted_current_time}  of  {converted_song_length}  ')

    song = song_box.get(ACTIVE)
    song = f'C:/Users/shubh/Desktop/MusicPlayer/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


# Create Volume Function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    #current_volume = pygame.mixer.music.get_volume()
    #slider_label.config(text=current_volume * 100)


# Create Master Frame
master_frame = Frame(root)
master_frame.pack(pady=20)

# Creating Playlist Box
song_box = Listbox(master_frame, bg='white', fg='green', width=60, selectbackground="yellow", selectforeground="black")
song_box.grid(row=0, column=0)

# Defining Player Control Button
back_butt_img = Image.open("C:/Users/shubh/Desktop/MusicPlayer/Images/Musicplayer_backward.png")
forward_butt_img = Image.open("C:/Users/shubh/Desktop/MusicPlayer/Images/Musicplayer_forward.png")
play_butt_img = Image.open("C:/Users/shubh/Desktop/MusicPlayer/Images/Musicplayer_play.png")
pause_butt_img = Image.open("C:/Users/shubh/Desktop/MusicPlayer/Images/Musicplayer_pause.png")
stop_butt_img = Image.open("C:/Users/shubh/Desktop/MusicPlayer/Images/Musicplayer_stop.png")

# Resizing Icons
back_butt_img = back_butt_img.resize((45, 45), Image.ANTIALIAS)
forward_butt_img = forward_butt_img.resize((45, 45), Image.ANTIALIAS)
play_butt_img = play_butt_img.resize((45, 45), Image.ANTIALIAS)
pause_butt_img = pause_butt_img.resize((45, 45), Image.ANTIALIAS)
stop_butt_img = stop_butt_img.resize((45, 45), Image.ANTIALIAS)

# Initializing Icons
back_butt_img = ImageTk.PhotoImage(back_butt_img)
forward_butt_img = ImageTk.PhotoImage(forward_butt_img)
play_butt_img = ImageTk.PhotoImage(play_butt_img)
pause_butt_img = ImageTk.PhotoImage(pause_butt_img)
stop_butt_img = ImageTk.PhotoImage(stop_butt_img)

# Creating Player Control Frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

# Creating Volume Label frame
volume_frame = LabelFrame(master_frame, text='Volume')
volume_frame.grid(row=0, column=1, padx=20)

# Creating Player Control Button
back_butt = Button(controls_frame, image=back_butt_img, borderwidth=0, command=backward)
forward_butt = Button(controls_frame, image=forward_butt_img, borderwidth=0, command=forward)
play_butt = Button(controls_frame, image=play_butt_img, borderwidth=0, command=play)
pause_butt = Button(controls_frame, image=pause_butt_img, borderwidth=0, command=lambda: pause(paused))
stop_butt = Button(controls_frame, image=stop_butt_img, borderwidth=0, command=stop)


back_butt.grid(row=0, column=0, padx=10)
play_butt.grid(row=0, column=2, padx=10)
pause_butt.grid(row=0, column=1, padx=10)
stop_butt.grid(row=0, column=3, padx=10)
forward_butt.grid(row=0, column=4, padx=10)

# Creating Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add Add Song Menu
add_song_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add Song To Playlist", command=add_song)
add_song_menu.add_command(label="Bulk Add Songs To Playlist", command=add_many_songs)

# Removing Song From Playlist
manage_playlist = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Remove Songs", menu=manage_playlist)
manage_playlist.add_command(label="Delete selected Song from Playlist", command=remove_song)
manage_playlist.add_command(label="Clear Playlist", command=clear_playlist)

# Exit Menu
exit_menu = Menu(my_menu, tearoff=False)
my_menu.add_command(label="Exit", command=quit)

# Creating Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Creating Music Position Slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)

# Create Volume Slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

# Creating Temporary Slider Label (For Testing)
#slider_label = Label(root, text='0')
#slider_label.pack(pady=10)

root.mainloop()
