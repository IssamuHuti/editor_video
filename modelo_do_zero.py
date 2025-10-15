import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QToolBar,
    QStackedWidget, QLabel, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction


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
        self.menuVertical.setFixedWidth(120)

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

        layoutPrincipal.addWidget(self.menuVertical)

        layoutCentral = QVBoxLayout()

        self.stack = QStackedWidget()
        self.stack.addWidget(Recortar())
        self.stack.addWidget(Audio())
        self.stack.addWidget(Posicao())
        self.stack.addWidget(Iluminacao())

        layoutCentral.addWidget(QLabel('Video'), 6)
        layoutCentral.addWidget(self.stack, 4)

        layoutPrincipal.addLayout(layoutCentral, 8.5)

        layoutListas = QVBoxLayout()
        layoutListas.addWidget(QPushButton('Carregar Video'))
        layoutListas.addWidget(QLabel('Listas'))

        layoutPrincipal.addLayout(layoutListas, 1.5)


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


# configuração do layout do video
class Video():
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaPrincipal()
    janela.show()
    app.exec()
