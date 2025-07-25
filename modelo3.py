import sys
import os
import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QComboBox, QFileDialog, QListWidgetItem, QToolBar,
    QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QMessageBox, QSlider, QListWidget, QFrame
)
from PySide6.QtCore import QUrl, Qt, QTime, QTimer, Signal
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtGui import QMouseEvent, QPainter, QColor, QAction
from moviepy.editor import VideoFileClip


class TelaCarregarRecortar(QWidget):
    def __init__(self):
        super().__init__()

        self.player = QMediaPlayer(self)
        self.audioOutput = QAudioOutput(self)
        self.player.setAudioOutput(self.audioOutput)

        self.videoWidget = VideoWidgetInterativo(self)
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


class TelaEditar(QWidget):
    def __init__(self):
        super().__init__()


class TelaSalvar(QWidget):
    def __init__(self):
        super().__init__()


class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Editor de Video')
        self.setFixedSize(1200,650)

        self.carregar = TelaCarregarRecortar()
        self.edicao = TelaEditar()
        self.salvar = TelaSalvar()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.carregar)
        self.stack.addWidget(self.edicao)
        self.stack.addWidget(self.salvar)

        botaoCarregar = QPushButton('CARREGAR')
        botaoEditar = QPushButton('EDITAR')
        botaoSalvar = QPushButton('SALVAR')
        botaoConfig = QPushButton('Configuração')

        menuLateral = QVBoxLayout()
        menuLateral.addWidget(botaoCarregar)
        menuLateral.addWidget(botaoEditar)
        menuLateral.addWidget(botaoSalvar)
        menuLateral.addStretch()
        menuLateral.addWidget(botaoConfig)
        menuLateral.addWidget(QLabel('Versão 1.0.0'))

        layoutPrincipal = QHBoxLayout()
        layoutPrincipal.addLayout(menuLateral, 1)
        layoutPrincipal.addWidget(self.stack, 9)

        container = QWidget()
        container.setLayout(layoutPrincipal)
        self.setCentralWidget(container)

        botaoCarregar.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        botaoEditar.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        botaoSalvar.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        botaoConfig.clicked.connect(lambda: self.stack.setCurrentIndex(3))


class CaixaLista(QFrame):
    def __init__(self, titulo, opcoes, funcaoExpandir=None):
        super().__init__()
        self.expandirLista = funcaoExpandir

        self.botaoLista = QPushButton(titulo)
        self.lista = QListWidget()
        self.lista.addItems(opcoes)
        self.lista.setVisible(False)

        layoutCaixaLista = QVBoxLayout(self)
        layoutCaixaLista.setContentsMargins(0, 0, 0, 0)
        layoutCaixaLista.addWidget(self.botaoLista)
        layoutCaixaLista.addWidget(self.lista)

        self.botaoLista.clicked.connect(self.esconderLista)

    def esconderLista(self):
        self.lista.setVisible(not self.lista.isVisible())
        if self.expandirLista:
            self.expandirLista()
    
    def listaExpandida(self):
        return self.lista.isVisible()
    
    def alturaExpansao(self):
        return self.botaoLista.height() + (self.lista.sizeHintForRow(0) * self.lista.count() if self.listaExpandida() else 0)


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

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            pos = event.position().x() if hasattr(event, 'position') else event.x()
            valor = self.minimum() + ((self.maximum() - self.minimum()) * pos) / self.width()

            for inicio, fim in self.recortes:
                if inicio <= valor <= fim:
                    self.recortes.remove((inicio, fim))
                    self.update()
                    return
                
            if self.inicio_temp is None:
                self.inicio_temp = valor
            else:
                inicio = float(min(self.inicio_temp, valor))
                fim = float(max(self.inicio_temp, valor))
                self.recortes.append((inicio, fim))
                self.inicio_temp = None
                self.update()

        else:
            super().mousePressEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.recortes:
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 255, 0, 100))

            for inicio, fim in self.recortes:
                inicio_x = int(self.width() * (inicio - self.minimum()) / (self.maximum() - self.minimum()))
                fim_x = int(self.width() * (fim - self.minimum()) / (self.maximum() - self.minimum()))
                painter.drawRect(inicio_x, 0, fim_x - inicio_x, self.height())

            painter.end()


class VideoWidgetInterativo(QVideoWidget):
    select = Signal()  # Sinal personalizado

    def mousePressEvent(self, event):
        self.select.emit()  # Emite o sinal quando o vídeo for clicado
        super().mousePressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaPrincipal()
    janela.show()
    app.exec()
