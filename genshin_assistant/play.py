import json
import time
from pathlib import Path

from libs.simulation import Simulator
from . import settings


class PlaySong:
    """演奏类"""
    song_dir = settings.SONG_DIR

    @staticmethod
    def get_song_conf(filepath):
        """获取演奏歌曲对象"""
        with open(filepath) as f:
            song_conf = json.loads(f.read())
        return song_conf

    def get_song_list(self):
        """获取歌曲列表"""
        song_list = Path(self.song_dir).iterdir()
        return list(song_list)

    def play(self, song):
        """演奏"""
        time.sleep(3)

        song_conf = self.get_song_conf(song)
        press_list = song_conf["press_list"]
        beat_frequency = song_conf["beat_frequency"]
        simulator = Simulator()  # 实例化模拟按键类

        while len(press_list) > 0:
            per_press = press_list.pop(0)
            per_press_list = list(per_press)  # 将每一个按键拆分成列表
            for k in per_press_list:
                simulator.send_key(k)
            time.sleep(beat_frequency)  # 按照节拍时间休眠

    def run(self):
        while True:
            song_obj_list = self.get_song_list()
            song_list = [item.name for item in song_obj_list]

            for i, song in enumerate(song_list):
                print(i, song)

            select = int(input("请选择歌曲>>>"))
            select_song = song_obj_list[select]
            self.play(select_song)


class Play:
    """演奏类"""
    song_dir = settings.SONG_DIR

    def __init__(self):
        self.play_list = []  # 演奏按键列表

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
        pass
