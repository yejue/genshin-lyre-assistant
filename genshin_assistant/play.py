import json
from pathlib import Path

from libs.simulation import Simulator
from . import settings


class Play:
    """演奏类"""
    song_dir = settings.SONG_DIR

    def __init__(self):
        self.play_list = []  # 演奏按键列表
        self.simulator = Simulator()

    def get_song_list(self):
        """返回歌曲路径对象列表"""
        song_list = Path(self.song_dir).iterdir()
        return list(song_list)

    def load_song(self, song_path):
        """加载歌曲到按键队列"""
        with open(song_path) as f:
            song_conf = json.loads(f.read())

        self.play_list = song_conf["press_list"]

    def play_one_beat(self):
        """演奏一个节拍"""
        if self.play_list:
            key = self.play_list.pop(0)
            for k in list(key):
                self.simulator.send_key(k)
