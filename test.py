from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from spider import Search

class MainWindows:
    def __init__(self):
        #读取文件
        gui_file = QFile('GUI.ui')
        gui_file.open(QFile.ReadOnly)
        gui_file.close()

        self.gui = QUiLoader().load(gui_file)

        #设置属性

        #事件绑定

        self.gui.search_button.clicked.connect(self.search)


    def search(self):
        search_input = self.gui.search_input.text()
        search_type = self.gui.search_type.currentText()
        search = Search(type=search_type, keyword=search_input)
        re = search.run()
        for i in re:
            name = '{name}-{singer}-{id}'.format(name=i['name'], singer=i['singer'], id=str(i['id']))
            self.gui.list.addItem(name)

def main():
    app = QApplication()

    windows = MainWindows()

    windows.gui.show()
    app.exec_()
if __name__ == '__main__':
    main()