from .views import AssistantView


class MainController:
    """主控制类"""

    def __init__(self):
        self.assistant_view = AssistantView()

    def run(self):
        self.assistant_view.show()  # 打开助手主窗口
