import sys, random, clippyr, re
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt, QCoreApplication, QFile, QObject
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QProgressBar
from PySide2.QtUiTools import QUiLoader

RUN_BUTTON_TEXT = 'Run Clippyr'

class ClippyrWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # Load main window UI file.
        ui_file = QFile('mainwindow.ui')
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        # Assign UI elements that need to be directly accessed to variables.
        self.sourceLineEdit = (
                self.window.findChild(QLineEdit, 'sourceLineEdit'))
        self.sourceListWidget = (
                self.window.findChild(QListWidget, 'sourceListWidget'))
        self.specLineEdit = (
                self.window.findChild(QLineEdit, 'specLineEdit'))
        self.specListWidget = (
                self.window.findChild(QListWidget, 'specListWidget'))
        self.runPushButton = (
                self.window.findChild(QPushButton, 'runPushButton'))
        self.clippyrProgressBar = (
                self.window.findChild(QProgressBar, 'clippyrProgressBar'))

        # Set initial text for UI elements as necessary.
        self.runPushButton.setText(RUN_BUTTON_TEXT)

        # Connect signals for variable-assigned UI elements.
        self.sourceLineEdit.returnPressed.connect(self.add_source)
        self.sourceListWidget.currentItemChanged.connect(self.source_selected)
        self.specLineEdit.returnPressed.connect(self.add_spec)
        self.specListWidget.currentItemChanged.connect(self.spec_selected)
        self.runPushButton.clicked.connect(self.run_clippyr)

        # Connect signals for other UI elements.
        (self.window.findChild(QPushButton, 'addSourcePushButton')
                .clicked.connect(self.add_source))
        (self.window.findChild(QPushButton, 'rmSourcePushButton')
                .clicked.connect(self.rm_source))
        (self.window.findChild(QPushButton, 'addSpecPushButton')
                .clicked.connect(self.add_spec))
        (self.window.findChild(QPushButton, 'rmSpecPushButton')
                .clicked.connect(self.rm_spec))

        # Initialize dictionary to store user input.
        self.spec_data = {}

        # Will store currently selected source name.
        self.current_source = ''

    def source_selected(self, current, previous):
        if current is None:
            return
        self.current_source = current.text()
        self.specListWidget.clear()
        for spec in self.spec_data[self.current_source]:
            if spec:
                specItem = QListWidgetItem()
                specItem.setText(spec)
                self.specListWidget.addItem(specItem)

    def spec_selected(self, current, previous):
        pass

    def add_source(self):
        source = self.sourceLineEdit.text()
        if source == '':
            return
        # TODO: For web source, change text to video title.

        # TODO: Verify validity of source text.
        self.spec_data[source] = []

        sourceItem = QListWidgetItem()
        sourceItem.setText(source)
        # TODO: Set icon for web/local source.
        self.sourceListWidget.addItem(sourceItem)

        # Select the newly added item.
        self.sourceListWidget.setCurrentItem(sourceItem)

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

        # Select the newly added item.
        self.specListWidget.addItem(specItem)

        self.specLineEdit.setText('')

    def rm_spec(self):
        row = self.specListWidget.currentRow()
        specItem = self.specListWidget.takeItem(row)
        spec = specItem.text()
        self.spec_data[self.current_source].remove(spec)
        del specItem

    def run_clippyr(self):
        self.runPushButton.clicked.disconnect()
        source_count = self.sourceListWidget.count()
        self.clippyrProgressBar.setValue(0)
        for row in range(source_count):
            self.runPushButton.setText(
                    'Processing ' + str(row + 1) + '/' + str(source_count))

            source = self.sourceListWidget.item(row).text()
            clips = ','.join(self.spec_data[source])
            if re.match('^http', source):
                clippyr.main(url=source, in_file='', clip=clips, output='')
            else:
                clippyr.main(url='', in_file=source, clip=clips, output='')

            self.clippyrProgressBar.setValue((row + 1) / source_count * 100)

        self.sourceListWidget.clear()
        self.specListWidget.clear()
        self.runPushButton.setText(RUN_BUTTON_TEXT)
        self.runPushButton.clicked.connect(self.run_clippyr)


def main():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    app = QtWidgets.QApplication(sys.argv)

    widget = ClippyrWidget()
    widget.window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
