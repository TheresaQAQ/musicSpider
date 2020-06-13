from PySide2.QtWidgets import QApplication,QWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QUrl
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from spider import Search, Music,find_id_in_playlist
from GUI_DEMO_2 import Ui_Form
from threading import Thread
import re,sys

class MainWindows(QWidget):
    def __init__(self):
        super().__init__()

        self.gui = Ui_Form()
        self.gui.setupUi(self)



        self.player = QMediaPlayer()

        # 事件绑定
        self.gui.search_button.clicked.connect(self.thread_search) # 搜索
        self.gui.play_button.clicked.connect(self.thread_playmusic) # 播放
        self.gui.list.doubleClicked.connect(self.thread_open_playlist) # 打开歌单
        self.player.durationChanged.connect(self.set_time) # 初始化进度条
        self.player.positionChanged.connect(self.play_slide) # 更新进度条
        # self.gui.Slider.valueChanged.connect(self.set_position)

    # 更改进度
    def set_position(self):
        self.player.setPosition(self.gui.Slider.value())
    # 更新进度条
    def play_slide(self, val):
        self.gui.Slider.setValue(int(val / 1000))

    # 初始化进度条
    def set_time(self):
        self.gui.Slider.setValue(0)
        self.music_time = self.player.duration() / 1000
        self.gui.Slider.setRange(0, int(self.music_time))
    # 搜索
    def search(self):
        self.type = self.gui.search_type.currentText()

        search_input = self.gui.search_input.text()
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
        music = self.gui.list.currentItem().text()
        name = re.search(r'(^.*?)(-)(.*?)$', music).group(0)
        if music != None:
            if self.gui.play_button.text() == '开始':
                self.gui.label.setText('正在播放：' + music)
                for i in self.search_return:
                    if i['name'] == music.split('-')[0]:
                        id = i['id']
                        break
                music = Music(id=str(id))
                music.download()
                path = r'cache\{0}.zqj'.format(name)
                url = QUrl.fromLocalFile(path)
                content = QMediaContent(url)
                self.player.setMedia(content)
                self.player.play()
                self.gui.play_button.setText('暂停')
            else:
                self.player.stop()
                self.gui.play_button.setText('开始')

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

            musics = find_id_in_playlist(id=id)
            self.gui.list.clear()
            for i in musics:
                music = Music(id=i)
                name = '{name}-{singer}'.format(name=music.name,singer=music.singer)
                self.gui.list.addItem(name)

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