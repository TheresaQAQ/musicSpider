from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from spider import Search, Music, find_id_in_playlist
from GUI import Ui_Form
from threading import Thread
import re
import sys


class MainWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.gui = Ui_Form()
        self.gui.setupUi(self)

        self.player = QMediaPlayer()

        self.gui.voiceSlider.setMinimum(0) # 最小值
        self.gui.voiceSlider.setMaximum(100) # 最大值
        self.gui.voiceSlider.setSingleStep(1) # 步长

        self.gui.voiceSlider.setValue(100) # 音量初始化

        # 事件绑定
        self.gui.search_button.clicked.connect(self.thread_search) # 搜索
        self.gui.play_button.clicked.connect(self.thread_playmusic) # 播放
        self.gui.list.doubleClicked.connect(self.thread_open_playlist) # 打开歌单
        self.player.durationChanged.connect(self.set_time) # 初始化进度条
        self.player.positionChanged.connect(self.play_slide) # 更新进度条
        self.gui.voiceSlider.valueChanged.connect(self.changed_voice)


    def changed_voice(self):
        try:
            self.player.setVolume(self.gui.voiceSlider.value())
        except:
            pass

    # 更新进度条
    def play_slide(self):
        val = self.player.position() / 1000
        self.gui.Slider.setValue(val)
        music_time = self.player.duration() / 1000 # 把毫秒转换为秒

        # 现在时间
        now_min = int(val // 60) # 分钟
        now_s = int(val - now_min * 60) # 秒

        # 总时间
        all_min = int(int(music_time) // 60) # 分钟
        all_s = int(music_time - all_min*60) # 秒

        self.gui.time_label.setText('{0}:{1}/{2}:{3}'.format(now_min,now_s,all_min,all_s))

    # 初始化进度条
    def set_time(self):
        self.gui.Slider.setValue(0)
        self.music_time = self.player.duration() / 1000
        self.gui.Slider.setRange(0, int(self.music_time))

    # 搜索
    def search(self):
        search_input = self.gui.search_input.text() # 获取输入
        search_type = self.gui.search_type.currentText()
        search = Search(type=search_type, keyword=search_input)
        self.search_return = search.run()
        self.gui.list.clear()
        if search_type == '单曲':
            for i in self.search_return:
                name = '{name}-{singer}'.format(name=i['name'], singer=i['singer'])
                self.gui.list.addItem(name)
        elif search_type == '歌单':
            for i in self.search_return:
                name = '{name}'.format(name=i['name'])
                self.gui.list.addItem(name)


    # 搜索线程
    def thread_search(self):
        thread = Thread(target=self.search)
        thread.start()

    # 播放音乐
    def playmusic(self):
        music_name = self.gui.list.currentItem().text()
        try:
            name = re.search(r'(^.*?)(-)(.*?)$', music_name).group(0)
        except AttributeError:
            pass

        if music_name != None:
            if self.gui.play_button.text() == '播放':
                if self.gui.search_type.currentText() == '单曲':
                    for i in self.search_return:
                        if i['name'] == music_name.split('-')[0]:
                            id = i['id']
                            break
                elif self.gui.search_type.currentText() == '歌单':
                    for i in self.musics_by_playlist:
                        if i['name'] == music_name.split('-')[0]:
                            id = i['id']
                            break

                music = Music(id=str(id))
                if music_name != self.gui.label.text()[5:]:
                    self.gui.label.setText('正在播放：' + music_name)
                    music.download()
                    path = r'cache\{0}.mp3'.format(name)
                    url = QUrl.fromLocalFile(path)
                    content = QMediaContent(url)
                    self.player.setMedia(content)
                    self.player.play()
                    self.gui.play_button.setText('暂停')
                else:
                    self.player.play()
                    self.gui.play_button.setText('暂停')
            else:
                self.player.pause()
                self.gui.play_button.setText('播放')

    # 播放音乐线程
    def thread_playmusic(self):
        thread = Thread(target=self.playmusic)
        thread.start()
        if self.gui.label.text() == '暂时还没有歌曲':
            self.gui.label.setText('正在加载，请稍等...')

    # 打开歌单
    def open_playlist(self):
        if self.gui.search_type.currentText() == '歌单':
            playlist = self.gui.list.currentItem().text()
            for i in self.search_return:
                if i['name'] == playlist:
                    id = i['id']
                    break
            self.musics_by_playlist,ids = find_id_in_playlist(id=id)

            self.gui.list.clear()
            for i in self.musics_by_playlist:
                name = '{name}-{singer}'.format(name=i['name'],singer=i['singer'])
                self.gui.list.addItem(name)

            for i in ids:
                music = Music(id=i)
                self.musics_by_playlist.append(music.detail)
                name = '{name}-{singer}'.format(name=music.name,singer=music.singer)
                self.gui.list.addItem(name)

    # 打开歌单进程
    def thread_open_playlist(self):
        thread = Thread(target=self.open_playlist)
        thread.start()


def main():
    app = QApplication(sys.argv)
    windows = MainWindows()
    windows.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()