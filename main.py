import sys
import os
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QFileDialog,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QRadioButton,
    QFormLayout,
    QProgressBar,
    QStackedWidget,
    QMessageBox,
    QCheckBox, QHBoxLayout, QSlider, QColorDialog, QFrame,
)
from PyQt6.QtGui import QPixmap, QIcon, QPalette
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.uic.properties import QtGui

from resize import image_collage

# 图像尺寸的常量
SIZE_3_INCH = 3
SIZE_6_INCH = 6
if getattr(sys, 'frozen', None):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(__file__)
# 配置字典
config = {
    SIZE_3_INCH: (1200, 1800),
    SIZE_6_INCH: (1200, 1800),
}


class GenerateThread(QThread):
    progress_update = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, folder_path, selected_size, selected_layout, border_color, border_size):
        super().__init__()
        self.folder_path = folder_path
        self.border_color = border_color
        self.border_size = border_size
        self.selected_size = selected_size
        self.selected_layout = list(set(selected_layout))

    def run(self):
        image_files = self.get_image_files(self.folder_path)
        total_files = len(image_files)

        def callback(path, index):
            progress = int(index / total_files * 100)
            self.progress_update.emit(progress)

        image_collage(self.folder_path, config[self.selected_size], self.selected_layout, self.border_size,
                      self.border_color, callback)
        progress = int(100)
        self.progress_update.emit(progress)
        self.finished.emit()

    def get_image_files(self, folder_path):
        image_files = []
        valid_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'cr2']
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_extension = file.split(".")[-1].lower()
                if file_extension in valid_extensions:
                    image_files.append(os.path.join(root, file))
        return image_files


class ColorButton(QPushButton):
    '''
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).
    '''

    colorChanged = pyqtSignal(object)

    def __init__(self, *args, color=None, callback=None, **kwargs):
        super(ColorButton, self).__init__(*args, **kwargs)

        self._color = None
        self._default = color
        self.callback = callback
        self.pressed.connect(self.onColorPicker)

        # Set the initial/default state.
        self.setColor(self._default)

    def setColor(self, color):
        print("set color", color)
        if color != self._color:
            self._color = color
            self.colorChanged.emit(color)
        if self._color:
            self.setStyleSheet("background-color: %s;" % self._color)
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):

        dlg = QColorDialog(self)
        col = dlg.getColor()
        if col.isValid():
            self.setColor(col.name())

    def mousePressEvent(self, e):
        print("mouse...", e)
        if e.button() == Qt.MouseButton.RightButton:
            self.setColor(self._default)

        return super(ColorButton, self).mousePressEvent(e)


class ImageCollage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("图片生成工具")
        self.setWindowIcon(QIcon(os.path.join(basedir, "images/collage.png")))  # 替换成你的应用程序图标文件
        # self.setGeometry(100, 100, 400, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        vbox = QVBoxLayout()

        tab_widget = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab_widget.addTab(tab2, "布局")
        tab_widget.addTab(tab3, "边框")
        tab_widget.addTab(tab1, "尺寸")
        border_layout = QVBoxLayout(tab3)
        border_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        vbox.addWidget(tab_widget)
        border_label = QLabel("请选择边框尺寸:")
        border_layout.addWidget(border_label)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)  # 最小缩放比例为10%
        slider.setMaximum(24)  # 最大缩放比例为200%
        slider.setSingleStep(1)  # 缩放步长为10%
        slider.setValue(6)  # 初始缩放比例为100%
        slider.valueChanged.connect(self.update_border_size)
        border_layout.addWidget(slider)

        color_label = QLabel("选择颜色:")
        border_layout.addWidget(color_label)

        # self.color_display_label = QPushButton()
        # self.color_display_label.setFixedSize(20, 20)  # 设置颜色显示框的大小
        # border_layout.addWidget(self.color_display_label)

        self.color_button = ColorButton(color="#fff")
        self.color_button.setFixedSize(20, 20)
        # # color_button.show()
        self.color_button.colorChanged.connect(self.selectColor)
        border_layout.addWidget(self.color_button)

        size_layout = QVBoxLayout(tab1)
        size_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        label = QLabel("请选择相纸尺寸:")
        size_layout.addWidget(label)

        self.size_radio_6inch = QRadioButton("6寸")
        self.size_radio_6inch.setChecked(True)
        radio_layout = QFormLayout()
        radio_layout.addRow(self.size_radio_6inch)

        size_layout.addLayout(radio_layout)

        layout_layout = QVBoxLayout(tab2)
        layout_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_label = QLabel("请选择布局:")
        layout_layout.addWidget(layout_label)

        self.layout_radio_1 = QCheckBox("布局一")
        self.layout_radio_2 = QCheckBox("布局二")
        self.layout_radio_3 = QCheckBox("布局三")
        self.layout_radio_4 = QCheckBox("布局四")
        self.layout_radio_5 = QCheckBox("布局五")
        self.layout_radio_6 = QCheckBox("布局六")
        self.layout_radio_7 = QCheckBox("布局七")
        self.layout_radio_8 = QCheckBox("布局八")
        self.layout_radio_9 = QCheckBox("布局九")
        self.layout_radio_10 = QCheckBox("布局十")

        pixmap_1 = QPixmap(os.path.join(basedir, "images/layout-1.svg"))
        pixmap_2 = QPixmap(os.path.join(basedir, "images/layout-2.svg"))
        pixmap_3 = QPixmap(os.path.join(basedir, "images/layout-3.svg"))
        pixmap_4 = QPixmap(os.path.join(basedir, "images/layout-4.svg"))
        pixmap_5 = QPixmap(os.path.join(basedir, "images/layout-5.svg"))
        pixmap_6 = QPixmap(os.path.join(basedir, "images/layout-6.svg"))
        pixmap_7 = QPixmap(os.path.join(basedir, "images/layout-7.svg"))
        pixmap_8 = QPixmap(os.path.join(basedir, "images/layout-8.svg"))
        pixmap_9 = QPixmap(os.path.join(basedir, "images/layout-9.svg"))
        pixmap_10 = QPixmap(os.path.join(basedir, "images/layout-10.svg"))

        pixmap_1 = pixmap_1.scaled(64, 64)
        pixmap_2 = pixmap_2.scaled(64, 64)
        pixmap_3 = pixmap_3.scaled(64, 64)
        pixmap_4 = pixmap_4.scaled(64, 64)
        pixmap_5 = pixmap_5.scaled(64, 64)
        pixmap_6 = pixmap_6.scaled(64, 64)
        pixmap_7 = pixmap_7.scaled(64, 64)
        pixmap_8 = pixmap_8.scaled(64, 64)
        pixmap_9 = pixmap_9.scaled(64, 64)
        pixmap_10 = pixmap_10.scaled(64, 64)

        label_1 = QLabel()
        label_1.setPixmap(pixmap_1)
        self.layout_radio_1.setChecked(True)
        self.layout_radio_1.toggled.connect(lambda: self.show_image(label_1, pixmap_1))

        label_2 = QLabel()
        label_2.setPixmap(pixmap_2)
        self.layout_radio_2.toggled.connect(lambda: self.show_image(label_2, pixmap_2))

        label_3 = QLabel()
        label_3.setPixmap(pixmap_3)
        self.layout_radio_3.toggled.connect(lambda: self.show_image(label_3, pixmap_3))
        label_4 = QLabel()
        label_4.setPixmap(pixmap_4)
        self.layout_radio_4.toggled.connect(lambda: self.show_image(label_4, pixmap_4))

        label_5 = QLabel()
        label_5.setPixmap(pixmap_5)
        self.layout_radio_5.toggled.connect(lambda: self.show_image(label_5, pixmap_5))

        label_6 = QLabel()
        label_6.setPixmap(pixmap_6)
        self.layout_radio_6.toggled.connect(lambda: self.show_image(label_6, pixmap_6))

        label_7 = QLabel()
        label_7.setPixmap(pixmap_7)
        self.layout_radio_7.toggled.connect(lambda: self.show_image(label_7, pixmap_7))

        label_8 = QLabel()
        label_8.setPixmap(pixmap_8)
        self.layout_radio_8.toggled.connect(lambda: self.show_image(label_8, pixmap_8))

        label_9 = QLabel()
        label_9.setPixmap(pixmap_9)
        self.layout_radio_9.toggled.connect(lambda: self.show_image(label_9, pixmap_9))
        label_10 = QLabel()
        label_10.setPixmap(pixmap_10)
        self.layout_radio_10.toggled.connect(lambda: self.show_image(label_10, pixmap_10))

        radio_layout_layout = QHBoxLayout()
        radio_layout_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        radio_layout_layout.addWidget(self.layout_radio_1)
        radio_layout_layout.addWidget(label_1)
        radio_layout_layout.addWidget(self.layout_radio_2)
        radio_layout_layout.addWidget(label_2)
        radio_layout_layout.addWidget(self.layout_radio_3)
        radio_layout_layout.addWidget(label_3)

        layout_layout.addLayout(radio_layout_layout)

        radio_layout_layout_2 = QHBoxLayout()
        radio_layout_layout_2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        radio_layout_layout_2.addWidget(self.layout_radio_4)
        radio_layout_layout_2.addWidget(label_4)
        radio_layout_layout_2.addWidget(self.layout_radio_5)
        radio_layout_layout_2.addWidget(label_5)
        radio_layout_layout_2.addWidget(self.layout_radio_6)
        radio_layout_layout_2.addWidget(label_6)

        layout_layout.addLayout(radio_layout_layout_2)

        radio_layout_layout_3 = QHBoxLayout()
        radio_layout_layout_3.setAlignment(Qt.AlignmentFlag.AlignLeft)
        radio_layout_layout_3.addWidget(self.layout_radio_7)
        radio_layout_layout_3.addWidget(label_7)
        radio_layout_layout_3.addWidget(self.layout_radio_8)
        radio_layout_layout_3.addWidget(label_8)
        radio_layout_layout_3.addWidget(self.layout_radio_9)
        radio_layout_layout_3.addWidget(label_9)

        layout_layout.addLayout(radio_layout_layout_3)

        radio_layout_layout_4 = QHBoxLayout()
        radio_layout_layout_4.setAlignment(Qt.AlignmentFlag.AlignLeft)
        radio_layout_layout_4.addWidget(self.layout_radio_10)
        radio_layout_layout_4.addWidget(label_10)
        layout_layout.addLayout(radio_layout_layout_4)

        self.size_radio_6inch.clicked.connect(self.size_radio_clicked)

        self.layout_radio_1.clicked.connect(self.layout_radio_clicked)
        self.layout_radio_2.clicked.connect(self.layout_radio_clicked)
        self.layout_radio_3.clicked.connect(self.layout_radio_clicked)
        self.layout_radio_4.clicked.connect(self.layout_radio_clicked)
        self.layout_radio_5.clicked.connect(self.layout_radio_clicked)
        self.layout_radio_6.clicked.connect(self.layout_radio_clicked)
        self.layout_radio_7.clicked.connect(self.layout_radio_clicked)
        self.layout_radio_8.clicked.connect(self.layout_radio_clicked)
        self.layout_radio_9.clicked.connect(self.layout_radio_clicked)
        self.layout_radio_10.clicked.connect(self.layout_radio_clicked)

        self.folder_line_edit = QLineEdit(self)
        self.folder_line_edit.setDisabled(True)
        vbox.addWidget(self.folder_line_edit)

        select_folder_button = QPushButton("选择文件夹")
        select_folder_button.clicked.connect(self.select_folder)
        vbox.addWidget(select_folder_button)
        self.generate_button = QPushButton("生成")
        self.generate_button.setDisabled(True)
        self.generate_button.clicked.connect(self.start_generation)
        vbox.addWidget(self.generate_button)

        central_widget.setLayout(vbox)

        self.setStyleSheet("""
            QProgressBar {
                text-align: center;
                height: 64px;
            }
            QProgressBar::chunk {
                # background-color: #007BFF;
                width: 5px;
            }
        """)

        self.mask_widget = QWidget(self)
        self.mask_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
        self.mask_widget.setVisible(False)

        self.loading_label = QLabel(self.mask_widget)
        self.loading_label.setText("加载中...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet("background-color: white; color: black;")
        self.loading_label.setGeometry(0, 0, self.width(), self.height())

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(central_widget)
        self.stacked_widget.addWidget(self.mask_widget)
        self.setCentralWidget(self.stacked_widget)

        self.worker_thread = None

        # 添加参数校验变量
        self.folder_selected = False
        self.size_selected = False
        self.layout_selected = False
        self.border_size = 5
        self.border_color = '#fff'
        self.selected_size = SIZE_6_INCH
        self.selected_layout = {1}

    def selectColor(self, color):
        self.border_color = color

    def update_border_size(self, border_size):
        self.border_size = border_size

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self.folder_line_edit.setText(folder)
            self.folder_selected = True
            print(f"选择的文件夹: {folder}")
        else:
            self.folder_selected = False
            self.folder_line_edit.setText(None)
        # 更新生成按钮状态
        self.update_generate_button_state()

    def show_image(self, label, pixmap):
        pass

    def size_radio_clicked(self):
        if self.size_radio_6inch.isChecked():
            self.selected_size = SIZE_6_INCH
        self.update_generate_button_state()

    def layout_radio_clicked(self):
        if self.layout_radio_1.isChecked():
            self.selected_layout.add(1)
        if self.layout_radio_2.isChecked():
            self.selected_layout.add(2)
        if self.layout_radio_3.isChecked():
            self.selected_layout.add(3)
        if self.layout_radio_4.isChecked():
            self.selected_layout.add(4)
        if self.layout_radio_5.isChecked():
            self.selected_layout.add(5)
        if self.layout_radio_6.isChecked():
            self.selected_layout.add(6)

        self.update_generate_button_state()

    def start_generation(self):
        # 检查参数是否选择
        if not self.folder_selected or not self.size_radio_selected() or not self.layout_radio_selected():
            QMessageBox.critical(self, "错误", "请选择文件夹、尺寸和布局")
            return

        # 获取用户选择的文件夹、尺寸和布局
        folder_path = self.folder_line_edit.text()
        selected_size = self.selected_size  # 使用成员变量存储选中的尺寸
        selected_layout = self.selected_layout  # 使用成员变量存储选中的布局
        border_color = self.border_color  # 使用成员变量存储选中的布局
        border_size = self.border_size  # 使用成员变量存储选中的布局

        self.mask_widget.setVisible(True)
        self.generate_button.setDisabled(True)
        self.disable_size_radio_buttons()
        self.disable_layout_radio_buttons()

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setGeometry(0, 0, self.width(), self.height())
        self.layout().addWidget(self.progress_bar)

        self.worker_thread = GenerateThread(folder_path, selected_size, list(selected_layout), border_color,
                                            border_size)
        self.worker_thread.finished.connect(self.end_generation)
        self.worker_thread.progress_update.connect(self.update_progress)
        self.worker_thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def end_generation(self):
        self.generate_button.setDisabled(False)
        self.enable_size_radio_buttons()
        self.enable_layout_radio_buttons()
        self.mask_widget.setVisible(False)
        self.layout().removeWidget(self.progress_bar)
        self.progress_bar.deleteLater()
        self.progress_bar = None
        QMessageBox.information(self, "通知", "生成任务已完成！")

    def size_radio_selected(self):
        return any([self.size_radio_6inch.isChecked()])

    def layout_radio_selected(self):
        return any([self.layout_radio_1.isChecked(), self.layout_radio_2.isChecked(), self.layout_radio_3.isChecked(),
                    self.layout_radio_4.isChecked(), self.layout_radio_5.isChecked(), self.layout_radio_6.isChecked()])

    def disable_size_radio_buttons(self):
        self.size_radio_6inch.setDisabled(True)

    def enable_size_radio_buttons(self):
        self.size_radio_6inch.setDisabled(False)

    def disable_layout_radio_buttons(self):
        self.layout_radio_1.setDisabled(True)
        self.layout_radio_2.setDisabled(True)
        self.layout_radio_3.setDisabled(True)
        self.layout_radio_4.setDisabled(True)
        self.layout_radio_5.setDisabled(True)
        self.layout_radio_6.setDisabled(True)

    def enable_layout_radio_buttons(self):
        self.layout_radio_1.setDisabled(False)
        self.layout_radio_2.setDisabled(False)
        self.layout_radio_3.setDisabled(False)
        self.layout_radio_4.setDisabled(False)
        self.layout_radio_5.setDisabled(False)
        self.layout_radio_6.setDisabled(False)

    def update_generate_button_state(self):
        # 检查所有参数是否选择，如果是则启用生成按钮，否则禁用
        if self.folder_selected and self.size_radio_selected() and self.layout_radio_selected():
            self.generate_button.setDisabled(False)
        else:
            self.generate_button.setDisabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCollage()
    window.show()
    sys.exit(app.exec())
