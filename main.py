import sys
import random
import sqlite3
import tempfile
import pathlib
import shutil

"""PyQt6"""
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidgetItem, QAbstractItemView, QFileDialog, \
    QListWidgetItem
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import *

"""Other packages"""
from py_ui_files.user_interface import Ui_MainWindow
from py_ui_files.choose import Ui_Form
from py_ui_files.author import Ui_Author_Form
from py_ui_files.genre import Ui_Genre_Form
from py_ui_files.song import Ui_Song_Form
from py_ui_files.delete import Ui_delete_form

"""Paths"""
temp_dir = pathlib.Path(__file__).parent.resolve() / "temp"
temp_dir.mkdir(parents=True, exist_ok=True)


class AudioTeka(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.data_from_base = None
        self.audio_output = None
        self.player = None
        self.pixmap = None
        self.setWindowTitle('Аудиотека')
        self.audio = []
        self.current = 0
        self.player_state = 0
        self.cur_position_of_audio = 0
        self.remote_btn_pause_icon = QPixmap('images/pause.png')
        self.remote_btn_play_icon = QPixmap('images/play-buttton.png')
        self.shuffle_icon = QPixmap('images/shuffle.png')
        self.next_icon = QPixmap('images/next.png')
        self.previous_icon = QPixmap('images/previous.png')
        self.con = sqlite3.connect("songs.sqlite")
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.pixmap = QPixmap('images/volume-up.png')
        self.add_audio.clicked.connect(self.update_result)
        self.image.setPixmap(self.pixmap)
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.volume.valueChanged.connect(self.set_volume)
        self.volume.setMaximum(100)
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.time_laps.sliderPressed.connect(self.disconnect_positionChanged)
        self.time_laps.sliderReleased.connect(self.connect_positionChanged)
        self.delete_audio.clicked.connect(self.delete)
        self.passed_time.setText("00:00")
        self.remain_time.setText("00:00")
        self.songs.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        for i in self.controllers.buttons():
            i.clicked.connect(self.run)
            i.setIconSize(QSize(48, 48))
        self.update_table.clicked.connect(self.update_songs)
        self.update_songs()
        self.remote_btn.setIcon(QIcon(self.remote_btn_pause_icon))
        self.next.setIcon(QIcon(self.next_icon))
        self.shuffle.setIcon(QIcon(self.shuffle_icon))
        self.previous.setIcon(QIcon(self.previous_icon))
        self.make_audios()

    def make_audios(self):
        con = sqlite3.connect("songs.sqlite")
        All_file_song = con.execute("select Name, file_song from song").fetchall()
        for i in All_file_song:
            self.audio.append(i)

    def update_result(self):
        self.up = Choose_What_To_Add(self)
        self.up.show()

    def delete(self):
        self.cur = Delete_Song(self)
        self.cur.show()

    def update_songs(self):
        self.songs.clearSpans()
        self.data_from_base = self.con.execute("""Select * from song""").fetchall()
        self.songs.setRowCount(0)
        self.songs.setColumnCount(3)
        for i, row in enumerate(self.data_from_base):
            self.songs.setRowCount(self.songs.rowCount() + 1)
            author = self.con.execute(f"""select name from author where id like {row[1]}""").fetchall()[0][0]
            genre = self.con.execute(f"""select name from genre where id like {row[3]}""").fetchall()[0][0]
            add_to_table = [author, row[2], genre]
            for j in range(3):
                self.songs.setItem(i, j, QTableWidgetItem(add_to_table[j]))

    def media_status_changed(self):
        if self.player.isPlaying():
            self.remote_btn.setIcon(QIcon(self.remote_btn_play_icon))
        if self.player.playbackState() is QMediaPlayer.PlaybackState.StoppedState:
            self.remote_btn.setIcon(QIcon(self.remote_btn_pause_icon))

    def positionChanged(self, position):
        self.time_laps.setValue(int(position / self.player.duration() * 100))
        dur = position // 1000
        mins = dur // 60
        sec = dur % 60
        self.passed_time.setText(f"{f'0{mins}' if mins < 10 else mins}:{f'0{sec}' if sec < 10 else sec}")

    def connect_positionChanged(self):
        if self.player.isSeekable():
            self.player.setPosition(int(self.time_laps.value() // 100 * self.player.duration()))
        self.player.positionChanged.connect(self.positionChanged)

    def disconnect_positionChanged(self):
        self.player.positionChanged.disconnect(self.positionChanged)

    def run(self):
        if self.sender() is self.remote_btn:
            if self.player_state == 0:
                self.play()
            else:
                self.pause()
        if self.sender() is self.shuffle:
            self.current = random.randint(0, len(self.audio) - 1)
            self.play(mode=1)
        if self.sender() is self.next:
            self.current = (self.current + 1 if self.current != len(self.audio) - 1 else 0)
            self.play(mode=1)
        if self.sender() is self.previous:
            self.current = (self.current - 1 if self.current != 0 else len(self.audio) - 1)
            self.play(mode=1)

    def play(self, mode=0):
        """
        :param mode:
        :0: pause
        :1: play
        """
        self.player_state = 1
        if mode == 0:
            self.player.setPosition(self.cur_position_of_audio)
        else:
            self.cur_position_of_audio = 0
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False, dir=str(temp_dir)) as temp_file:
                temp_file.write(self.audio[self.current][1])
                temp_file_path = temp_file.name
            self.player.setSource(QUrl.fromLocalFile(temp_file_path))
        dur = self.player.duration() // 1000
        mins = dur // 60
        sec = dur % 60
        self.remain_time.setText(f"{f'0{mins}' if mins < 10 else mins}:{f'0{sec}' if sec < 10 else sec}")
        self.player.play()

    def pause(self):
        self.remote_btn.setIcon(QIcon(self.remote_btn_pause_icon))
        self.player_state = 0
        self.player.pause()
        if self.player.playbackState() is QMediaPlayer.PlaybackState.StoppedState:
            self.cur_position_of_audio = 0
        elif self.player.playbackState() is QMediaPlayer.PlaybackState.PausedState:
            self.cur_position_of_audio = self.player.position()

    def set_volume(self):
        self.audio_output.setVolume(self.volume.value() * .01)


class Delete_Song(QWidget, Ui_delete_form):
    def __init__(self, other: AudioTeka):
        super().__init__()
        self.cur_main = other
        self.setupUi(self)
        self.unitUI()

    def unitUI(self):
        self.pushButton.clicked.connect(self.run)

    def run(self):
        song_name = self.lineEdit.text()
        con = sqlite3.connect('songs.sqlite')
        f = con.execute(f"""select Name from Song where name like '{song_name}'""").fetchone()
        if f is None:
            self.lineEdit.setText("Такой песни нет!")
        else:
            con.execute(f"""delete from Song where name like '{song_name}'""")
            con.commit()
        con.close()
        self.close()


class Choose_What_To_Add(QWidget, Ui_Form):
    def __init__(self, other: AudioTeka):
        super().__init__()
        self.cur = None
        self.main = other
        self.setupUi(self)
        self.unitUI()

    def unitUI(self):
        self.Author.clicked.connect(self.run)
        self.Genre.clicked.connect(self.run)
        self.Song.clicked.connect(self.run)

    def run(self):
        if self.sender() is self.Author:
            self.cur = Add_Author()
        elif self.sender() is self.Genre:
            self.cur = Add_Genre()
        else:
            self.cur = Add_Song(self.main)
        self.cur.show()


class Add_Author(QWidget, Ui_Author_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.unitUI()

    def unitUI(self):
        self.pushButton.clicked.connect(self.run)
        con = sqlite3.connect("songs.sqlite")
        names = con.execute("select Name from Author").fetchall()
        for i in names:
            self.all.addItem(QListWidgetItem(str(i[0])))


    def run(self):
        con = sqlite3.connect("songs.sqlite")
        author_name = self.lineEdit.text()
        if author_name is not None and author_name != '':
            con.execute(f"""insert into Author (name) values ('{author_name}')""")
            con.commit()
            con.close()
            self.close()
        else:
            self.lineEdit.setText("Введите настоящее имя автора")


class Add_Genre(QWidget, Ui_Genre_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.unitUI()

    def unitUI(self):
        self.pushButton.clicked.connect(self.run)
        con = sqlite3.connect("songs.sqlite")
        names = con.execute("select Name from Genre").fetchall()
        for i in names:
            self.all.addItem(QListWidgetItem(str(i[0])))

    def run(self):
        con = sqlite3.connect("songs.sqlite")
        genre_name = self.lineEdit.text()
        if genre_name is not None and genre_name != '':
            con.execute(f"""insert into Genre (name) values ('{genre_name}')""")
            con.commit()
            con.close()
            self.close()
        else:
            self.lineEdit.setText("Введите настоящее название жанра")


class Add_Song(QWidget, Ui_Song_Form):
    def __init__(self, other: AudioTeka):
        super().__init__()
        self.cur_main = other
        self.setupUi(self)
        self.unitUI()

    def unitUI(self):
        self.pushButton.clicked.connect(self.run)

    def run(self):
        try:
            fname = QFileDialog.getOpenFileName(
                self, 'Выбрать аудиодорожку', '',
                'Дорожка (*.mp3);;Все файлы (*)'
            )[0]
            con = sqlite3.connect("songs.sqlite")
            need_to_add = list(map(str.strip, self.lineEdit.text().split(',')))
            Author_id = con.execute("select id from author where Name = ?", (need_to_add[0],)).fetchone()[0]
            Genre_id = con.execute("select id from genre where Name = ?", (need_to_add[2],)).fetchone()[0]
            with open(fname, 'rb') as f:
                temp_array = f.read()
            con.execute("insert into Song (Author_id, Name, Genre_id, file_song) values (?, ?, ?, ?)",
                        (Author_id, need_to_add[1], Genre_id, temp_array))

            self.cur_main.audio.append((need_to_add[1], temp_array))
            con.commit()
            con.close()
        except Exception as e:
            print(e)
            self.lineEdit.setText("Неправильно введены Автор и/или Жанр. Файл может быть повреждён")
        self.close()


def cleanup():
    try:
        shutil.rmtree(temp_dir)
        print("Временная папка удалена.")
    except FileNotFoundError:
        print("Временная папка не найдена (возможно, уже удалена).")
    except OSError as e:
        print(f"Ошибка при удалении временной папки: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(cleanup)
    ex = AudioTeka()
    ex.show()
    sys.exit(app.exec())