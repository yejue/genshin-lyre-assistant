from PyQt5.QtWidgets import QWidget, QAbstractItemView

from genshin_assistant.play import PlaySong
from .ui.fengqin import Ui_fengqin_assitant


class AssistantView(QWidget, Ui_fengqin_assitant):
    """风琴助手视窗"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 界面初始化
        self.play = PlaySong()  # 实例化风琴演奏类
        self.set_song_list()
        self.set_addition_ui()  # Designer 额外的 UI 设置

    def set_addition_ui(self):
        """额外的 UI 设置"""
        self.lw_song.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 歌曲列表不可编辑

    def set_song_list(self):
        """获取曲目表"""
        song_list_obj = self.play.get_song_list()
        song_list = [item.name for item in song_list_obj]

        self.lw_song.addItems(song_list)
