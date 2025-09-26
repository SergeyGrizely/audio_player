import os
from tkinter import *
from tkinter import filedialog
from pygame import mixer

# создаём основное окно
root = Tk()
root.geometry("516x670")
root.title("Altair")
root.config(bg='#262626')
root.resizable(False, False)

# инициализация микшера
mixer.init()

# переменные состояния
start = 0
is_paused = False
current_music = ""

# функция добавления музыки
def addMusic():
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)
        for song in songs:
            if song.endswith(".mp3"):
                Playlist.insert(END, song)

# функция переключения play/pause
def togglePlayPause():
    global start, current_music, is_paused

    if not Playlist.curselection():
        return  # ничего не выбрано — выходим

    selected_music = Playlist.get(ACTIVE)

    # Если музыка ещё не начиналась или выбран другой трек
    if start == 0 or selected_music != current_music:
        mixer.music.load(selected_music)
        mixer.music.play()
        current_music = selected_music
        is_paused = False
        start = 1
        btn_play_pause.config(image=btn_pause_icon)
        print(current_music[0:-4])

    # Если текущий трек на паузе — воспроизвести
    elif is_paused:
        mixer.music.unpause()
        is_paused = False
        btn_play_pause.config(image=btn_pause_icon)

    # Если трек играет — поставить на паузу
    else:
        mixer.music.pause()
        is_paused = True
        btn_play_pause.config(image=btn_play_icon)

def skipTrack():
    global current_music, is_paused, start

    if Playlist.size() == 0:
        return  # плейлист пуст

    current_index = Playlist.curselection()
    if not current_index:
        current_index = (0,)  # если ничего не выбрано, начнём с первого

    next_index = current_index[0] + 1

    if next_index >= Playlist.size():
        return  # следующий трек отсутствует

    # выбрать следующий элемент
    Playlist.select_clear(0, END)
    Playlist.activate(next_index)
    Playlist.selection_set(next_index)

    # загрузка и воспроизведение нового трека
    next_track = Playlist.get(next_index)
    mixer.music.load(next_track)
    mixer.music.play()

    # обновление состояния
    current_music = next_track
    is_paused = False
    start = 1
    btn_play_pause.config(image=btn_pause_icon)
    print(current_music[0:-4])

def backTrack():
    global current_music, is_paused, start

    if Playlist.size() == 0:
        return  # плейлист пуст

    current_index = Playlist.curselection()
    if not current_index:
        current_index = (0,)  # если ничего не выбрано, начнём с первого

    prev_index = current_index[0] - 1

    if prev_index < 0:
        return  # предыдущего трека нет

    # выбрать предыдущий трек
    Playlist.select_clear(0, END)
    Playlist.activate(prev_index)
    Playlist.selection_set(prev_index)

    prev_track = Playlist.get(prev_index)
    mixer.music.load(prev_track)
    mixer.music.play()

    # обновление состояния
    current_music = prev_track
    is_paused = False
    start = 1
    btn_play_pause.config(image=btn_pause_icon)
    print(current_music[0:-4])

def setVolume(val):
    volume = float(val) / 100  # Scale возвращает от 0 до 100, а mixer ожидает 0.0–1.0
    mixer.music.set_volume(volume)

# кадры анимации
frmcount = 32
frms = [PhotoImage(file=os.path.join(os.path.dirname(__file__), 'animation.gif'), format='gif -index %i' % i) for i in range(frmcount)]

def update(ind):
    frame = frms[ind]
    ind += 1
    if ind == frmcount:
        ind = 0
    lbl.config(image=frame)
    root.after(40, update, ind)

lbl = Label(root)
lbl.place(x=100, y=0)
root.after(0, update, 0)

volume_slider = Scale(root,
                      from_=100,
                      to=0,
                      orient=VERTICAL,
                      command=setVolume,
                      length=200,
                      troughcolor='#444444',
                      fg='#00ff00',
                      bg='#262626',
                      highlightthickness=0)

volume_slider.set(70)  # начальное значение громкости
volume_slider.place(x=440, y=125)

# иконки кнопок
btn_play_icon = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'play.png'))
btn_pause_icon = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'pause.png'))
btn_source = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'source.png'))

# фрейм под плейлист
frm_music = Frame(root, bd=2, relief=RIDGE, width=516, height=70)
frm_music.place(x=0, y=416)

#Кнопка бэк скип
btn_back_icon = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'back_skip.png'))
btn_back = Button(root, image=btn_back_icon, bg='#262626', cursor="hand2", height=60, width=60, command=backTrack)
btn_back.place(x=155, y=326)

# кнопка скип
btn_skip_icon = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'skip.png'))
btn_skip = Button(root, image=btn_skip_icon, bg='#262626', cursor="hand2", height=60, width=60, command=skipTrack)
btn_skip.place(x=295, y=326)

# кнопка play/pause
btn_play_pause = Button(root, image=btn_play_icon, bg='#262626', cursor="hand2", height=60, width=60, command=togglePlayPause)
btn_play_pause.place(x=225, y=326)

# кнопка выбора музыки
btn_browse = Button(root, image=btn_source, bg='#262626', cursor="hand2", width=60, height=60, command=addMusic)
btn_browse.place(x=10, y=10)

# прокрутка и список воспроизведения
Scroll = Scrollbar(frm_music)
Playlist = Listbox(frm_music, width=100, font=('Arial,bold', 15), bg='#0f0f0f', fg='#00ff00', selectbackground="lightblue", cursor="hand2", bd=0, yscrollcommand=Scroll.set)
Scroll.config(command=Playlist.yview)
Scroll.pack(side=RIGHT, fill=Y)
Playlist.pack(side=RIGHT, fill=BOTH)

# запуск главного окна
root.mainloop()
