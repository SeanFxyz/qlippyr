import sys, random, clippyr, re
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt, QCoreApplication, QFile, QObject
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QProgressBar
from PySide2.QtUiTools import QUiLoader

class ClippyrWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Load main window UI file.
        ui_file = QFile('mainwindow.ui')
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        self.sourceLineEdit = (
                self.window.findChild(QLineEdit, 'sourceLineEdit'))
        self.sourceListWidget = (
                self.window.findChild(QListWidget, 'sourceListWidget'))
        self.specLineEdit = (
                self.window.findChild(QLineEdit, 'specLineEdit'))
        self.specListWidget = (
                self.window.findChild(QListWidget, 'specListWidget'))
        self.clippyrProgressBar = (
                self.window.findChild(QProgressBar, 'clippyrProgressBar'))

        (self.sourceListWidget
                .currentItemChanged.connect(self.source_selected))
        (self.specListWidget
                .currentItemChanged.connect(self.spec_selected))

        (self.window.findChild(QPushButton, 'addSourcePushButton')
                .clicked.connect(self.add_source))
        (self.window.findChild(QPushButton, 'rmSourcePushButton')
                .clicked.connect(self.rm_source))
        (self.window.findChild(QPushButton, 'addSpecPushButton')
                .clicked.connect(self.add_spec))
        (self.window.findChild(QPushButton, 'rmSpecPushButton')
                .clicked.connect(self.rm_spec))
        (self.window.findChild(QPushButton, 'runPushButton')
                .clicked.connect(self.run_clippyr))

        self.spec_data = {}

        self.current_source = ''

    def source_selected(self, current, previous):
        self.current_source = current.text()
        self.specListWidget.clear()
        for spec in self.spec_data[self.current_source]:
            specItem = QListWidgetItem()
            specItem.setText(spec)
            self.specListWidget.addItem(specItem)

    def spec_selected(self, current, previous):
        pass

    def add_source(self):
        source = self.sourceLineEdit.text()

        # TODO: Verify validity of source text.
        self.spec_data[source] = []

        sourceItem = QListWidgetItem()
        sourceItem.setText(source)
        # TODO: Set icon for web/local source.
        # TODO: For web source, change text to video title.
        self.sourceListWidget.addItem(sourceItem)

        self.sourceLineEdit.setText('')

    def rm_source(self):
        source = (self.sourceListWidget
                .takeItem(self.sourceListWidget.currentRow()))
        self.spec_data[source.text()] = []
        del source

    def add_spec(self):
        spec = self.specLineEdit.text()

        # TODO: Verify validity of spec.
        self.spec_data[self.current_source].append(spec)

        specItem = QListWidgetItem()
        specItem.setText(spec)
        self.specListWidget.addItem(specItem)

        self.specLineEdit.setText('')

    def rm_spec(self):
        row = self.specListWidget.currentRow()
        spec = self.specListWidget.takeItem(row)
        spec_data[self.currentSource][row] = ''
        del spec

    def run_clippyr(self):
        source_count = self.sourceListWidget.count()
        self.clippyrProgressBar.setValue(0)
        for row in range(source_count):
            source = self.sourceListWidget.item(row).text()
            clips = ','.join(self.spec_data[source])
            clippyr.clippyr(url=source, in_file='', clip=clips, output='')
            self.clippyrProgressBar.setValue((row + 1) / source_count * 100)


    def check_specs(self):
        clips = self.clipTextEdit.toPlainText().split('\n')
        bad_specs = clippyr.check_time_specs(clips)
        for spec in bad_specs():
            print('Bad clip specifier "' + spec + '"')


def main():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    app = QtWidgets.QApplication(sys.argv)

    widget = ClippyrWidget()
    widget.window.show()

    sys.exit(app.exec_())

