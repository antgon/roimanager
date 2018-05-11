# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1051, 744)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/roimanager.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(1050, 640))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabImage = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tabImage.setFont(font)
        self.tabImage.setObjectName("tabImage")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabImage)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.listChan = QtWidgets.QListWidget(self.tabImage)
        self.listChan.setObjectName("listChan")
        self.gridLayout_2.addWidget(self.listChan, 0, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.tabImage)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 2)
        self.labelMin = QtWidgets.QLabel(self.tabImage)
        self.labelMin.setObjectName("labelMin")
        self.gridLayout_2.addWidget(self.labelMin, 2, 0, 1, 1)
        self.sliderMin = QtWidgets.QSlider(self.tabImage)
        self.sliderMin.setOrientation(QtCore.Qt.Horizontal)
        self.sliderMin.setObjectName("sliderMin")
        self.gridLayout_2.addWidget(self.sliderMin, 2, 1, 1, 1)
        self.labelMax = QtWidgets.QLabel(self.tabImage)
        self.labelMax.setObjectName("labelMax")
        self.gridLayout_2.addWidget(self.labelMax, 3, 0, 1, 1)
        self.sliderMax = QtWidgets.QSlider(self.tabImage)
        self.sliderMax.setOrientation(QtCore.Qt.Horizontal)
        self.sliderMax.setObjectName("sliderMax")
        self.gridLayout_2.addWidget(self.sliderMax, 3, 1, 1, 1)
        self.groupBoxCm = QtWidgets.QGroupBox(self.tabImage)
        self.groupBoxCm.setObjectName("groupBoxCm")
        self.gridLayout_2.addWidget(self.groupBoxCm, 5, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.tabImage)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 4, 0, 1, 1)
        self.sliderBlending = QtWidgets.QSlider(self.tabImage)
        self.sliderBlending.setMaximum(20)
        self.sliderBlending.setSingleStep(1)
        self.sliderBlending.setPageStep(2)
        self.sliderBlending.setProperty("value", 20)
        self.sliderBlending.setOrientation(QtCore.Qt.Horizontal)
        self.sliderBlending.setObjectName("sliderBlending")
        self.gridLayout_2.addWidget(self.sliderBlending, 4, 1, 1, 1)
        self.gridLayout_2.setRowMinimumHeight(0, 1)
        self.gridLayout_2.setRowMinimumHeight(1, 1)
        self.gridLayout_2.setRowMinimumHeight(2, 1)
        self.gridLayout_2.setRowMinimumHeight(3, 1)
        self.gridLayout_2.setRowMinimumHeight(4, 20)
        self.gridLayout_2.setRowMinimumHeight(5, 1)
        self.tabWidget.addTab(self.tabImage, "")
        self.tabRoi = QtWidgets.QWidget()
        self.tabRoi.setObjectName("tabRoi")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabRoi)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.buttonRemoveRoi = QtWidgets.QPushButton(self.tabRoi)
        self.buttonRemoveRoi.setObjectName("buttonRemoveRoi")
        self.gridLayout.addWidget(self.buttonRemoveRoi, 1, 1, 1, 1)
        self.listRoi = QtWidgets.QListView(self.tabRoi)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listRoi.sizePolicy().hasHeightForWidth())
        self.listRoi.setSizePolicy(sizePolicy)
        self.listRoi.setObjectName("listRoi")
        self.gridLayout.addWidget(self.listRoi, 0, 0, 1, 2)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabRoi, "")
        self.tabMarkers = QtWidgets.QWidget()
        self.tabMarkers.setObjectName("tabMarkers")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tabMarkers)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.listWidget = QtWidgets.QListWidget(self.tabMarkers)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout_4.addWidget(self.listWidget, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.tabMarkers)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_4.addWidget(self.pushButton, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabMarkers, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineeditAtlasRef = QtWidgets.QLineEdit(self.centralwidget)
        self.lineeditAtlasRef.setMaxLength(10)
        self.lineeditAtlasRef.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineeditAtlasRef.setObjectName("lineeditAtlasRef")
        self.horizontalLayout_3.addWidget(self.lineeditAtlasRef)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        self.groupBoxData = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxData.setObjectName("groupBoxData")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBoxData)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.buttonSaveData = QtWidgets.QPushButton(self.groupBoxData)
        self.buttonSaveData.setMaximumSize(QtCore.QSize(80, 16777215))
        self.buttonSaveData.setObjectName("buttonSaveData")
        self.horizontalLayout_2.addWidget(self.buttonSaveData)
        self.buttonLoadData = QtWidgets.QPushButton(self.groupBoxData)
        self.buttonLoadData.setMaximumSize(QtCore.QSize(80, 16777215))
        self.buttonLoadData.setObjectName("buttonLoadData")
        self.horizontalLayout_2.addWidget(self.buttonLoadData)
        self.verticalLayout_2.addWidget(self.groupBoxData)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2.setStretch(0, 10)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 1)
        self.verticalLayout_2.setStretch(4, 1)
        self.verticalLayout_2.setStretch(5, 1)
        self.gridLayout_7.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem3, 1, 1, 1, 1)
        self.buttonHome = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonHome.sizePolicy().hasHeightForWidth())
        self.buttonHome.setSizePolicy(sizePolicy)
        self.buttonHome.setMinimumSize(QtCore.QSize(0, 32))
        self.buttonHome.setMaximumSize(QtCore.QSize(32, 32))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/home.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonHome.setIcon(icon1)
        self.buttonHome.setIconSize(QtCore.QSize(20, 20))
        self.buttonHome.setObjectName("buttonHome")
        self.gridLayout_6.addWidget(self.buttonHome, 1, 2, 1, 1)
        self.buttonZoom = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonZoom.sizePolicy().hasHeightForWidth())
        self.buttonZoom.setSizePolicy(sizePolicy)
        self.buttonZoom.setMinimumSize(QtCore.QSize(0, 32))
        self.buttonZoom.setMaximumSize(QtCore.QSize(32, 32))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/zoom.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonZoom.setIcon(icon2)
        self.buttonZoom.setIconSize(QtCore.QSize(20, 20))
        self.buttonZoom.setCheckable(True)
        self.buttonZoom.setObjectName("buttonZoom")
        self.gridLayout_6.addWidget(self.buttonZoom, 1, 3, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_6.addWidget(self.line_3, 1, 4, 1, 1)
        self.buttonAddMarker = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonAddMarker.sizePolicy().hasHeightForWidth())
        self.buttonAddMarker.setSizePolicy(sizePolicy)
        self.buttonAddMarker.setMinimumSize(QtCore.QSize(0, 32))
        self.buttonAddMarker.setMaximumSize(QtCore.QSize(32, 32))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/addmarker.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonAddMarker.setIcon(icon3)
        self.buttonAddMarker.setIconSize(QtCore.QSize(20, 20))
        self.buttonAddMarker.setCheckable(True)
        self.buttonAddMarker.setObjectName("buttonAddMarker")
        self.gridLayout_6.addWidget(self.buttonAddMarker, 1, 5, 1, 1)
        self.buttonRemoveMarker = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonRemoveMarker.sizePolicy().hasHeightForWidth())
        self.buttonRemoveMarker.setSizePolicy(sizePolicy)
        self.buttonRemoveMarker.setMinimumSize(QtCore.QSize(0, 32))
        self.buttonRemoveMarker.setMaximumSize(QtCore.QSize(32, 32))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/removemarker.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonRemoveMarker.setIcon(icon4)
        self.buttonRemoveMarker.setIconSize(QtCore.QSize(20, 20))
        self.buttonRemoveMarker.setCheckable(True)
        self.buttonRemoveMarker.setObjectName("buttonRemoveMarker")
        self.gridLayout_6.addWidget(self.buttonRemoveMarker, 1, 6, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_6.addWidget(self.line_4, 1, 7, 1, 1)
        self.buttonAddRoi = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonAddRoi.sizePolicy().hasHeightForWidth())
        self.buttonAddRoi.setSizePolicy(sizePolicy)
        self.buttonAddRoi.setMinimumSize(QtCore.QSize(0, 32))
        self.buttonAddRoi.setMaximumSize(QtCore.QSize(32, 32))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/roi.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonAddRoi.setIcon(icon5)
        self.buttonAddRoi.setIconSize(QtCore.QSize(20, 20))
        self.buttonAddRoi.setCheckable(True)
        self.buttonAddRoi.setObjectName("buttonAddRoi")
        self.gridLayout_6.addWidget(self.buttonAddRoi, 1, 8, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_6.addWidget(self.line_5, 1, 9, 1, 1)
        self.buttonShowMarkers = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonShowMarkers.sizePolicy().hasHeightForWidth())
        self.buttonShowMarkers.setSizePolicy(sizePolicy)
        self.buttonShowMarkers.setMinimumSize(QtCore.QSize(0, 32))
        self.buttonShowMarkers.setMaximumSize(QtCore.QSize(32, 32))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/markervisible.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon6.addPixmap(QtGui.QPixmap(":/markerhidden.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.buttonShowMarkers.setIcon(icon6)
        self.buttonShowMarkers.setIconSize(QtCore.QSize(20, 20))
        self.buttonShowMarkers.setCheckable(True)
        self.buttonShowMarkers.setChecked(False)
        self.buttonShowMarkers.setObjectName("buttonShowMarkers")
        self.gridLayout_6.addWidget(self.buttonShowMarkers, 1, 10, 1, 1)
        self.buttonShowRoi = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonShowRoi.sizePolicy().hasHeightForWidth())
        self.buttonShowRoi.setSizePolicy(sizePolicy)
        self.buttonShowRoi.setMinimumSize(QtCore.QSize(0, 32))
        self.buttonShowRoi.setMaximumSize(QtCore.QSize(32, 32))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/roivisible.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon7.addPixmap(QtGui.QPixmap(":/roihidden.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.buttonShowRoi.setIcon(icon7)
        self.buttonShowRoi.setIconSize(QtCore.QSize(20, 20))
        self.buttonShowRoi.setCheckable(True)
        self.buttonShowRoi.setChecked(False)
        self.buttonShowRoi.setObjectName("buttonShowRoi")
        self.gridLayout_6.addWidget(self.buttonShowRoi, 1, 11, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem4, 1, 12, 1, 1)
        self.canvas = MplCanvas(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy)
        self.canvas.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.canvas.setObjectName("canvas")
        self.gridLayout_6.addWidget(self.canvas, 0, 0, 1, 13)
        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 1, 1, 1)
        self.gridLayout_7.setColumnStretch(0, 1)
        self.gridLayout_7.setColumnStretch(1, 5)
        self.gridLayout_8.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1051, 27))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_2.setObjectName("toolBar_2")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_2)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setMenuRole(QtWidgets.QAction.QuitRole)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpenNext = QtWidgets.QAction(MainWindow)
        self.actionOpenNext.setObjectName("actionOpenNext")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionOpenNext)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ROI Manager"))
        self.label.setText(_translate("MainWindow", "Display range"))
        self.labelMin.setText(_translate("MainWindow", "Min"))
        self.sliderMin.setToolTip(_translate("MainWindow", "Minimum display value"))
        self.labelMax.setText(_translate("MainWindow", "Max"))
        self.sliderMax.setToolTip(_translate("MainWindow", "Maximum display value"))
        self.groupBoxCm.setTitle(_translate("MainWindow", "Colourmap"))
        self.label_3.setText(_translate("MainWindow", "Blending"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabImage), _translate("MainWindow", "Image"))
        self.buttonRemoveRoi.setText(_translate("MainWindow", "Remove"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRoi), _translate("MainWindow", "ROIs"))
        self.pushButton.setText(_translate("MainWindow", "New marker set"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMarkers), _translate("MainWindow", "Markers"))
        self.label_2.setText(_translate("MainWindow", "Atlas reference:"))
        self.lineeditAtlasRef.setToolTip(_translate("MainWindow", "Atlas reference number"))
        self.groupBoxData.setTitle(_translate("MainWindow", "Data"))
        self.buttonSaveData.setToolTip(_translate("MainWindow", "Save data set"))
        self.buttonSaveData.setText(_translate("MainWindow", "Save"))
        self.buttonLoadData.setToolTip(_translate("MainWindow", "Load data set"))
        self.buttonLoadData.setText(_translate("MainWindow", "Load"))
        self.buttonHome.setToolTip(_translate("MainWindow", "Reset view"))
        self.buttonZoom.setToolTip(_translate("MainWindow", "Toggle pan/zoom"))
        self.buttonAddMarker.setToolTip(_translate("MainWindow", "Add marker"))
        self.buttonRemoveMarker.setToolTip(_translate("MainWindow", "Remove marker"))
        self.buttonAddRoi.setToolTip(_translate("MainWindow", "Add ROI"))
        self.buttonShowMarkers.setToolTip(_translate("MainWindow", "View/hide markers"))
        self.buttonShowRoi.setToolTip(_translate("MainWindow", "View/hide ROIs"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.toolBar_2.setWindowTitle(_translate("MainWindow", "toolBar_2"))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open PatchMaster file"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionOpenNext.setText(_translate("MainWindow", "Open next"))
        self.actionOpenNext.setShortcut(_translate("MainWindow", "Ctrl+N"))

from mplcanvas import MplCanvas
from . import resources_rc
