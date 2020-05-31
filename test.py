from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QUrl
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from spider import Search, Music
import sys,re

class MainWindows:
    def __init__(self):
        #读取文件
        gui_file = QFile('GUI.ui')
        gui_file.open(QFile.ReadOnly)
        gui_file.close()

        self.gui = QUiLoader().load(gui_file)

        self.player = QMediaPlayer()

        #事件绑定
        self.gui.search_button.clicked.connect(self.search)
        self.gui.start_button.clicked.connect(self.playmusic)



    def search(self):
        search_input = self.gui.search_input.text()
        search_type = self.gui.search_type.currentText()
        search = Search(type=search_type, keyword=search_input)
        self.search_return = search.run()
        self.gui.list.clear()
        for i in self.search_return:
            name = '{name}-{singer}'.format(name=i['name'], singer=i['singer'])
            self.gui.list.addItem(name)

    def playmusic(self):
        try:
            music = self.gui.list.currentItem().text()
            if music != None:
                if self.gui.start_button.text() == '开始':
                    self.gui.label.setText('正在播放：' + music)
                    name = re.search(r'(^.*?)(-)(.*?)$',music).group(0)
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
                    self.gui.start_button.setText('暂停')
                else:
                    self.player.stop()
                    self.gui.start_button.setText('开始')
        except AttributeError:
            print('未选中')

def main():
    app = QApplication()
    windows = MainWindows()
    windows.gui.show()
    app.exec_()
if __name__ == '__main__':
    main()