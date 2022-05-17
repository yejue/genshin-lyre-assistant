from pathlib import Path

# 项目根路径
BASE_DIR = Path(__file__).parent.parent

# 歌曲目录
SONG_DIR = Path(BASE_DIR).joinpath("source/song")

# 应用图标路径
ICON_PATH = "source/img/anemo.png"
