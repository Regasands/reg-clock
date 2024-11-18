from PyQt6.QtWidgets import QApplication
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import sys

# Инициализация приложения
app = QApplication(sys.argv)

# Мультимедиа-код
audio_output = QAudioOutput()
player = QMediaPlayer()
player.setAudioOutput(audio_output)

audio_output.setVolume(100)
media = QUrl.fromLocalFile("C:/path/to/your/audio.mp3")
player.setSource(media)
player.play()

# Чтобы приложение не завершилось сразу
sys.exit(app.exec())
