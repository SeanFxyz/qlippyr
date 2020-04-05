import sys, random, clippyr
from PySide2 import QtCore, QtWidgets, QtGui

class ClippyrWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        self.layout = QtWidgets.QVBoxLayout()



        ## Two-Panel layout
        self.panelLayout = QtWidgets.QHBoxLayout()

        ### Left panel layout
        self.leftLayout = QtWidgets.QVBoxLayout()

        self.sourceLabel = QtWidgets.QLabel()
        self.sourceLabel.setText('URL or filename of source video:')
        self.leftLayout.addWidget(self.sourceLabel)



        #### Left panel source input sub-layout
        self.sourceInputLayout = QtWidgets.QHBoxLayout()

        self.sourceLineEdit = QtWidgets.QLineEdit()
        self.sourceLineEdit.setAlignment(QtCore.Qt.AlignLeft)
        self.sourceInputLayout.addWidget(self.sourceLineEdit)

        self.sourceAddButton = QtWidgets.QPushButton('Add source')
        self.sourceAddButton.clicked.connect(self.add_source)
        self.sourceInputLayout.addWidget(self.sourceAddButton)
        self.leftLayout.addLayout(self.sourceInputLayout)

        self.sourceList = QtWidgets.QListWidget()
        self.leftLayout.addWidget(self.sourceList)

        self.sourceRmButton = QtWidgets.QPushButton('Remove')
        self.sourceRmButton.clicked.connect(self.remove_source)
        self.leftLayout.addWidget(self.sourceRmButton)

        self.panelLayout.addLayout(self.leftLayout)



        ### Right panel layout
        self.rightLayout = QtWidgets.QVBoxLayout()

        self.clipLabel = QtWidgets.QLabel()
        self.rightLayout.addWidget(self.clipLabel)

        self.clipTextEdit = QtWidgets.QTextEdit()
        self.clipTextEdit.textChanged.connect(self.check_specs)
        self.rightLayout.addWidget(self.clipTextEdit)

        self.runButton = QtWidgets.QPushButton()
        self.runButton.clicked.connect(self.clippyr_run)
        self.rightLayout.addWidget(self.runButton)

        self.panelLayout.addLayout(self.rightLayout)



        ## Command output view

        self.cmdOutput = ''



        self.layout.addLayout(self.panelLayout)
        self.setLayout(self.layout)




    def clippyr_run(self):
        pass

    def add_source(self):
        source = self.sourceLineEdit.text()

    def remove_source(self):
        source = self.sourceList.takeItem(self.sourceList.currentRow)
        del source

    def check_specs(self):
        clips = self.clipTextEdit.toPlainText().split('\n')
        bad_specs = clippyr.check_time_specs(clips)
        for spec in bad_specs():
            print('Bad clip specifier "' + spec + '"')


if __name__=="__main__":
    app = QtWidgets.QApplication([])

    widget = ClippyrWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
