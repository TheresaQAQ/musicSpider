from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QUrl
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from spider import Search, Music



path = r'C;\Users\zhouq\PycharmProjects\音乐爬虫\凉凉-张碧晨.mp3'
url = QUrl.fromLocalFile(path)
content = QMediaContent(url)
player = QMediaPlayer()
player.setMedia(content)
player.setVolume(100)
player.play()