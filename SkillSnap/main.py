import sys
import os
from PyQt5.QtCore import QLibraryInfo
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QLabel, QLineEdit,
    QPushButton, QVBoxLayout
)

# fix Qt plugin path
plugin_path = QLibraryInfo.location(QLibraryInfo.PluginsPath)
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
os.environ["QT_MAC_WANTS_LAYER"] = "1"

import google.generativeai as genai
from dotenv import load_dotenv



load_dotenv()
genai.configure(api_key=os.getenv("PLEASE_DONT_STEAL_MY_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


class Window(QWidget):
    def __init__(self):
        super().__init__()   # I have no Idea what this does.

        #bug fix
        self.label: QLabel       = None
        self.textbox: QLineEdit  = None
        self.button: QPushButton = None
        self.result_label: QLabel = None

        self._setup_ui()

    def _setup_ui(self):

        self.label  = QLabel("Describe your story:")
        self.textbox = QLineEdit()
        self.button = QPushButton("Submit")
        self.result_label = QLabel("")


        self.button.clicked.connect(self.on_click)

        # lay out
        vbox = QVBoxLayout(self)
        for w in (self.label, self.textbox, self.button, self.result_label):
            vbox.addWidget(w)

        self.setWindowTitle("User Input Example")
        self.show()

    def on_click(self):
        user_input = self.textbox.text().strip()
        if not user_input:
            return

        prompt = f"Turn this Snapchat story into a college app-worthy achievement or insight: {user_input}"
        response = model.generate_content(prompt, stream=True)

        text = ""
        for chunk in response:
            if getattr(chunk, "text", None):
                text += chunk.text

        self.result_label.setText(text)
        self.textbox.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
