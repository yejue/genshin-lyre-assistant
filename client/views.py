import uuid
import json
import system_hotkey

from pathlib import Path
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QMessageBox
from PyQt5.QtCore import pyqtSignal

from genshin_assistant.play import Play
from genshin_assistant.settings import SONG_DIR
from .ui.lyre_assitant import Ui_lyre_assitant
from .ui.editor import Ui_editor
from . import constant


class EditorView(QWidget, Ui_editor):
    """编写曲谱页面视图"""
    def __init__(self, assistant_signals):
        super().__init__()
        self.setupUi(self)
        self.set_addition_ui()
        self.set_slot_function()

        self.assistant_signals = assistant_signals  # 风琴助手首页的信号表

    def set_addition_ui(self):
        """额外的 UI 设置"""
        self.tb_msg_area.setMarkdown(constant.EDITOR_TIPS)

    def set_slot_function(self):
        """统一设置绑定槽函数"""
        self.pb_save.clicked.connect(self.save_song)  # 保存按钮

    def save_song(self):
        """曲谱保存"""
        temp_dict = {"beat_frequency": 0.3}

        song_name = self.le_song_name.text().strip()
        if song_name == "":
            song_name = f"未命名曲谱_{uuid.uuid4().hex[:4]}"  # 曲谱名为空时自动保存

        song_list = self.te_edit_area.toPlainText().split("\n")
        song_list_ = []

        for k in song_list:  # 过滤空白曲谱
            if k.strip() == "":
                continue
            song_list_.append(k)

        temp_dict["press_list"] = song_list_
        with open(Path(SONG_DIR).joinpath(song_name), "w") as f:  # 保存到曲谱目录
            f.write(json.dumps(temp_dict))

        self.assistant_signals["fresh_signal"].emit("editor")
        QMessageBox.information(self, "风琴写者", "保存成功", QMessageBox.Ok)
        self.hide()


class AssistantView(QWidget, Ui_lyre_assitant):
    """风琴助手视窗"""
    hotkey_signal = pyqtSignal(str)  # 热键发送信号
    fresh_signal = pyqtSignal(str)  # 页面刷新

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 界面初始化
        self.play = Play()  # 实例化风琴演奏类
        self.set_song_list()
        self.set_addition_ui()  # Designer 额外的 UI 设置

        self.play_one = system_hotkey.SystemHotkey()  # 弹奏热键
        self.set_slot_function()  # 绑定槽函数
        self.editor = EditorView({"fresh_signal": self.fresh_signal})

    def set_addition_ui(self):
        """额外的 UI 设置"""

        # 初始按键状态
        self.pb_stop.setEnabled(False)  # 停止按键置灰

        # 歌曲列表设置
        self.tw_song.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 列表不可编辑
        self.tw_song.hideColumn(1)  # 隐藏歌曲路径字段
        self.tw_song.horizontalHeader().setVisible(False)  # 隐藏表头
        self.tw_song.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 列宽重新分配

    def set_slot_function(self):
        """统一设置绑定槽函数"""
        self.pb_play.clicked.connect(self.play_start)  # 开始按钮
        self.pb_stop.clicked.connect(self.play_stop)  # 停止按钮
        self.pb_edit.clicked.connect(self.show_editor)  # 编写按钮
        self.fresh_signal.connect(self.set_song_list)  # 刷新页面

    def set_song_list(self):
        """获取曲目表"""
        song_list_obj = self.play.get_song_list()
        self.tw_song.setRowCount(0)  # 清空列表
        for index, obj in enumerate(song_list_obj):
            name_item = QTableWidgetItem(obj.name)
            name_path = QTableWidgetItem(str(obj.absolute()))

            self.tw_song.setRowCount(self.tw_song.rowCount()+1)  # 将歌曲列表更新到表格
            self.tw_song.setItem(index, 0, name_item)
            self.tw_song.setItem(index, 1, name_path)

    def hotkey_pressed_event(self, hotkey):
        """热键相应事件"""
        print(hotkey)
        # 检验演奏列表是否为空，空则取消注册快捷键，将停止按键置灰，将 start 置白
        if not self.play.play_list:
            self.play_one.unregister(constant.PLAY_HOT_KEY)
            self.pb_stop.setEnabled(False)
            self.pb_play.setEnabled(True)
        else:
            self.play.play_one_beat()

    def play_start(self):
        """演奏开始"""
        # 1. 将演奏歌曲按键加载到演奏列表
        current_row = self.tw_song.currentRow()
        if current_row == -1:
            return
        song_path = self.tw_song.item(current_row, 1).text()
        self.play.load_song(song_path)
        # 2. 更新按键状态
        self.pb_play.setEnabled(False)
        self.pb_stop.setEnabled(True)

        self.play_one.register(constant.PLAY_HOT_KEY, callback=self.hotkey_pressed_event)  # 注册弹奏热键

    def play_stop(self):
        """演奏停止"""
        self.play_one.unregister(constant.PLAY_HOT_KEY)  # 取消注册弹奏热键
        self.play.play_list = []  # 清空按键列表

        self.pb_play.setEnabled(True)
        self.pb_stop.setEnabled(False)

    def closeEvent(self, a0) -> None:
        """窗口关闭事件"""
        if constant.PLAY_HOT_KEY in self.play_one.keybinds:
            self.play_one.unregister(constant.PLAY_HOT_KEY)  # 取消注册弹奏热键

    def show_editor(self):
        """编写曲谱视图"""
        self.editor.show()
