import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QToolBar, QSlider,
    QStackedWidget, QLabel, QPushButton, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, QTime


class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Editor de Video')
        self.setFixedSize(1200,650)

        central = QWidget()
        self.setCentralWidget(central)

        layoutPrincipal = QHBoxLayout(central)

        self.menuVertical = QToolBar("Menu Lateral")
        self.menuVertical.setOrientation(Qt.Vertical)
        self.menuVertical.setMovable(False)

        acaoPaginaRecortar   = QAction('Recortar', self)
        acaoPaginaAudio      = QAction('Audio', self)
        acaoPaginaPosicao    = QAction('Posicao', self)
        acaoPaginaIluminacao = QAction('Iluminacao', self)

        acaoPaginaRecortar.triggered.connect(lambda: self.stack.setCurrentIndex(0))
        acaoPaginaAudio.triggered.connect(lambda: self.stack.setCurrentIndex(1))
        acaoPaginaPosicao.triggered.connect(lambda: self.stack.setCurrentIndex(2))
        acaoPaginaIluminacao.triggered.connect(lambda: self.stack.setCurrentIndex(3))

        self.menuVertical.addAction(acaoPaginaRecortar)
        self.menuVertical.addAction(acaoPaginaAudio)
        self.menuVertical.addAction(acaoPaginaPosicao)
        self.menuVertical.addAction(acaoPaginaIluminacao)

        layoutPrincipal.addWidget(self.menuVertical, 1.5)

        layoutCentral = QVBoxLayout()

        self.videoWidget = QVideoWidget(self)
        self.player      = QMediaPlayer(self)
        self.audioOutput = QAudioOutput(self)
        self.player.setAudioOutput(self.audioOutput)
        self.player.setVideoOutput(self.videoWidget)

        self.slider = ConfigSlider(Qt.Horizontal)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal { height: 8px; background: #ccc; }
            QSlider::handle:horizontal { width: 16px; background: #444; border-radius: 8px; }
            QSlider::sub-page:horizontal { background: #0080ff; }
        """)
        self.slider.setMouseTracking(True)
        self.slider.setMinimum(0)
        self.slider.setMaximum(int(self.player.duration()))

        self.temporizador = QLabel("00:00:00 / 00:00:00")

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.audioOutput.setVolume(0.5)

        layoutSlider = QHBoxLayout()
        layoutSlider.addWidget(self.temporizador)
        layoutSlider.addWidget(self.slider, 6)
        layoutSlider.addWidget(self.volumeSlider, 2)

        layoutReprodutor = QVBoxLayout()
        layoutReprodutor.addWidget(self.videoWidget)
        layoutReprodutor.addLayout(layoutSlider)

        layoutCentral.addLayout(layoutReprodutor, 8)

        self.stack = QStackedWidget()
        self.stack.addWidget(Recortar())
        self.stack.addWidget(Audio())
        self.stack.addWidget(Posicao())
        self.stack.addWidget(Iluminacao())

        layoutCentral.addWidget(self.stack, 2)
        layoutPrincipal.addLayout(layoutCentral, 7)

        layoutListas = QVBoxLayout()
        botaoCarregarVideo = QPushButton('Carregar Video')

        layoutListas.addWidget(botaoCarregarVideo)
        layoutListas.addWidget(QLabel('Listas'))

        layoutPrincipal.addLayout(layoutListas, 1.5)

        botaoCarregarVideo.clicked.connect(self.abrirVideo)
        self.volumeSlider.valueChanged.connect(self.ajusteVolume)
        self.player.positionChanged.connect(self.atualizarSlider)

    def abrirVideo(self):
        arquivo, _ = QFileDialog.getOpenFileName( # serve para selecionar arquivos de vídeo
            self, "Escolher vídeo", "", "Vídeos (*.mp4 *.avi *.mov *.mkv)"
        )
        if arquivo:
            self.player.setSource(QUrl.fromLocalFile(arquivo))
            self.player.play()

    def ajusteVolume(self, valor):
        self.audioOutput.setVolume(valor / 100)

    def atualizarSlider(self, posicao):
        duracao = self.player.duration()
        self.slider.setMaximum(duracao)
        self.slider.setValue(posicao)

        tempoAtual = QTime(0, 0, 0).addMSecs(posicao)
        tempoTotal = QTime(0, 0, 0).addMSecs(duracao)
        self.temporizador.setText(f"{tempoAtual.toString('hh:mm:ss')} / {tempoTotal.toString('hh:mm:ss')}")


class Recortar(QWidget):
    def __init__(self):
        super().__init__()
        layoutRecortar = QVBoxLayout(self)
        layoutRecortar.addWidget(QLabel('Recorte'))
        layoutRecortar.addWidget(QPushButton('Salvar'))


class Audio(QWidget):
    def __init__(self):
        super().__init__()
        layoutAudio = QVBoxLayout(self)
        layoutAudio.addWidget(QLabel('Audio'))
        layoutAudio.addWidget(QPushButton('Salvar'))


class Posicao(QWidget):
    def __init__(self):
        super().__init__()
        layoutPosicao = QVBoxLayout(self)
        layoutPosicao.addWidget(QLabel('Posicao'))
        layoutPosicao.addWidget(QPushButton('Salvar'))


class Iluminacao(QWidget):
    def __init__(self):
        super().__init__()
        layoutIluminacao = QVBoxLayout(self)
        layoutIluminacao.addWidget(QLabel('Iluminacao'))
        layoutIluminacao.addWidget(QPushButton('Salvar'))


class ConfigSlider(QSlider):
    def __init__(self, orientacao, parent=None):
        super().__init__(orientacao, parent)
        self.setMouseTracking(True)
        self.setMinimum(0)
        self.setMaximum(100000)
        
        self.inicio_recorte = None
        self.fim_recorte = None
        self.setFixedHeight(30)

        self.recortes = []
        self.inicio_temp = None

        self.caixaFlutuante = QLabel("00:00:00", self)
        self.caixaFlutuante.setStyleSheet(""" 
            QSlider::groove:horizontal {
                height: 12px;
                background: #ccc;
                border-radius: 6px;
            }
            QSlider::handle:horizontal {
                background: #0078d7;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
        """)
        self.caixaFlutuante.setVisible(False)

    def leaveEvent(self, event):
        self.caixaFlutuante.setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaPrincipal()
    janela.show()
    app.exec()
