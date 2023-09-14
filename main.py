import sys
import os
import time
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
    QHBoxLayout,
    QFormLayout,
    QProgressBar,
    QStackedWidget,
    QMessageBox, QCheckBox,
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from resize import image_collage

size_map = {
    "3": (1200, 1800),
    "4": (1200, 1800),
    "5": (1200, 1800),
    "6": (1200, 1800),
}
if getattr(sys, 'frozen', None):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(__file__)


class GenerateThread(QThread):
    progress_update = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, folder_path, selected_size, selected_layout):
        super().__init__()
        self.folder_path = folder_path
        self.selected_size = selected_size
        self.selected_layout = list(set(selected_layout))

    def run(self):
        image_files = self.get_image_files(self.folder_path)
        total_files = len(image_files)

        def callback(path, index):
            progress = int(index / total_files * 100)
            self.progress_update.emit(progress)

        image_collage(self.folder_path, size_map[str(self.selected_size)], self.selected_layout, callback)

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


class ImageCollage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("图片生成工具")
        self.setWindowIcon(QIcon(os.path.join(basedir, "images/collage.png")))  # 替换成你的应用程序图标文件
        self.setGeometry(100, 100, 600, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.folder_line_edit = QLineEdit(self)
        self.folder_line_edit.setDisabled(True)
        layout.addWidget(self.folder_line_edit)

        select_folder_button = QPushButton("选择文件夹")
        select_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(select_folder_button)

        tab_widget = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        tab_widget.addTab(tab1, "尺寸")
        tab_widget.addTab(tab2, "布局")
        tab_widget.addTab(tab2, "布局")
        layout.addWidget(tab_widget)

        size_layout = QVBoxLayout(tab1)

        label = QLabel("请选择相纸尺寸:")
        size_layout.addWidget(label)

        # self.size_radio_3inch = QRadioButton("3寸")
        # self.size_radio_4inch = QRadioButton("4寸")
        # self.size_radio_5inch = QRadioButton("5寸")
        self.size_radio_6inch = QRadioButton("6寸")

        radio_layout = QFormLayout()
        # radio_layout.addRow(self.size_radio_3inch)
        # radio_layout.addRow(self.size_radio_4inch)
        # radio_layout.addRow(self.size_radio_5inch)
        radio_layout.addRow(self.size_radio_6inch)

        size_layout.addLayout(radio_layout)

        layout_layout = QVBoxLayout(tab2)

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
        self.layout_radio_9 = QCheckBox("随机")

        pixmap_1 = QPixmap(os.path.join(basedir, "images/layout-1.png"))
        pixmap_2 = QPixmap(os.path.join(basedir, "images/layout-2.png"))
        pixmap_3 = QPixmap(os.path.join(basedir, "images/layout-3.png"))
        pixmap_4 = QPixmap(os.path.join(basedir, "images/layout-4.png"))
        pixmap_5 = QPixmap(os.path.join(basedir, "images/layout-5.png"))
        pixmap_6 = QPixmap(os.path.join(basedir, "images/layout-6.png"))
        pixmap_7 = QPixmap(os.path.join(basedir, "images/layout-7.png"))
        pixmap_8 = QPixmap(os.path.join(basedir, "images/layout-8.png"))
        pixmap_9 = QPixmap(os.path.join(basedir, "images/random.png"))

        pixmap_1 = pixmap_1.scaled(50, 50)
        pixmap_2 = pixmap_2.scaled(50, 50)
        pixmap_3 = pixmap_3.scaled(50, 50)
        pixmap_4 = pixmap_4.scaled(50, 50)
        pixmap_5 = pixmap_5.scaled(50, 50)
        pixmap_6 = pixmap_6.scaled(50, 50)
        pixmap_7 = pixmap_7.scaled(50, 50)
        pixmap_8 = pixmap_8.scaled(50, 50)
        pixmap_9 = pixmap_9.scaled(50, 50)

        label_1 = QLabel()
        label_1.setPixmap(pixmap_1)
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
        label_7.setPixmap(pixmap_6)
        self.layout_radio_7.toggled.connect(lambda: self.show_image(label_7, pixmap_7))

        label_8 = QLabel()
        label_8.setPixmap(pixmap_8)
        self.layout_radio_8.toggled.connect(lambda: self.show_image(label_8, pixmap_8))

        label_9 = QLabel()
        label_9.setPixmap(pixmap_9)
        self.layout_radio_9.toggled.connect(lambda: self.show_image(label_9, pixmap_9))


        radio_layout_layout = QHBoxLayout()
        radio_layout_layout.addWidget(self.layout_radio_1)
        radio_layout_layout.addWidget(label_1)
        radio_layout_layout.addWidget(self.layout_radio_2)
        radio_layout_layout.addWidget(label_2)
        radio_layout_layout.addWidget(self.layout_radio_3)
        radio_layout_layout.addWidget(label_3)

        layout_layout.addLayout(radio_layout_layout)

        radio_layout_layout_2 = QHBoxLayout()
        radio_layout_layout_2.addWidget(self.layout_radio_4)
        radio_layout_layout_2.addWidget(label_4)
        radio_layout_layout_2.addWidget(self.layout_radio_5)
        radio_layout_layout_2.addWidget(label_5)
        radio_layout_layout_2.addWidget(self.layout_radio_6)
        radio_layout_layout_2.addWidget(label_6)

        layout_layout.addLayout(radio_layout_layout_2)

        radio_layout_layout_3 = QHBoxLayout()
        radio_layout_layout_3.addWidget(self.layout_radio_7)
        radio_layout_layout_3.addWidget(label_7)
        radio_layout_layout_3.addWidget(self.layout_radio_8)
        radio_layout_layout_3.addWidget(label_8)
        radio_layout_layout_3.addWidget(self.layout_radio_9)
        radio_layout_layout_3.addWidget(label_9)

        layout_layout.addLayout(radio_layout_layout_3)

        # 在 __init__ 方法中为每个单选按钮连接点击事件
        # self.size_radio_3inch.clicked.connect(self.size_radio_clicked)
        # self.size_radio_4inch.clicked.connect(self.size_radio_clicked)
        # self.size_radio_5inch.clicked.connect(self.size_radio_clicked)
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


        self.generate_button = QPushButton("生成")
        self.generate_button.setDisabled(True)
        self.generate_button.clicked.connect(self.start_generation)
        layout.addWidget(self.generate_button)

        central_widget.setLayout(layout)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QWidget {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: 1px solid #007BFF;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
                border: 1px solid #0056b3;
            }
            QPushButton:disabled {
                background-color: #ccc;
                border: 1px solid #ccc;
            }
            QLineEdit {
                border: 1px solid #ccc;
                padding: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                background-color: white;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #007BFF;
                color: white;
                min-width: 100px;
                padding: 5px 10px;
            }
            QTabBar::tab:selected {
                background-color: #0056b3;
            }
            QRadioButton {
                padding: 5px;
            }
            QProgressBar {
                text-align: center;
                height: 64px;
            }
            QProgressBar::chunk {
                background-color: #007BFF;
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
        self.selected_size = 0
        self.selected_layout = set()

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
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.show()

    def size_radio_clicked(self):
        # if self.size_radio_3inch.isChecked():
        #     self.selected_size = 3
        # elif self.size_radio_4inch.isChecked():
        #     self.selected_size = 4
        # elif self.size_radio_5inch.isChecked():
        #     self.selected_size = 5
        # elif self.size_radio_6inch.isChecked():
        if self.size_radio_6inch.isChecked():
            self.selected_size = 6
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

        self.mask_widget.setVisible(True)
        self.generate_button.setDisabled(True)
        self.disable_size_radio_buttons()
        self.disable_layout_radio_buttons()

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.layout().addWidget(self.progress_bar)

        self.worker_thread = GenerateThread(folder_path, selected_size, list(selected_layout))
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
        # return any(
        #     [self.size_radio_3inch.isChecked(), self.size_radio_4inch.isChecked(), self.size_radio_5inch.isChecked(),
        #      self.size_radio_6inch.isChecked()])
        return any(
            [self.size_radio_6inch.isChecked()])

    def layout_radio_selected(self):
        return any([self.layout_radio_1.isChecked(), self.layout_radio_2.isChecked(), self.layout_radio_3.isChecked(),
                    self.layout_radio_4.isChecked(), self.layout_radio_5.isChecked(), self.layout_radio_6.isChecked()])

    def disable_size_radio_buttons(self):
        # self.size_radio_3inch.setDisabled(True)
        # self.size_radio_4inch.setDisabled(True)
        # self.size_radio_5inch.setDisabled(True)
        self.size_radio_6inch.setDisabled(True)

    def enable_size_radio_buttons(self):
        # self.size_radio_3inch.setDisabled(False)
        # self.size_radio_4inch.setDisabled(False)
        # self.size_radio_5inch.setDisabled(False)
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
