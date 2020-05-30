from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from spider import Search,Music
import playsound

class MainWindows:
    def __init__(self):
        #读取文件
        gui_file = QFile('GUI.ui')
        gui_file.open(QFile.ReadOnly)
        gui_file.close()

        self.gui = QUiLoader().load(gui_file)


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
        music = self.gui.list.currentItem().text()
        if music != None:
            name = music.split('-')[0]
            print(name)
            for i in self.search_return:
                if i['name'] == name:
                    id = i['id']
                    print(id)
                    break
        music = Music(id=str(id))
        music.download()
        print(music.file_name)
        playsound.playsound(sound=music.file_name)

def main():
    app = QApplication()

    windows = MainWindows()

    windows.gui.show()
    app.exec_()

if __name__ == '__main__':
    main()