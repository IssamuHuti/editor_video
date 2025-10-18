import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QListWidget,
    QVBoxLayout, QHBoxLayout, QToolBar, QSlider,
    QStackedWidget, QLabel, QPushButton, QFileDialog
)
from PySide6.QtCore import Qt, Signal
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
        acaoPaginaAnimacao   = QAction('Animacao', self)
        acaoPaginaConcatenar = QAction('Concatenar', self)
        acaoPaginaAplicacoes = QAction('Aplicacoes', self)

        acaoPaginaRecortar.triggered.connect(lambda: self.stack.setCurrentIndex(0))
        acaoPaginaAudio.triggered.connect(lambda: self.stack.setCurrentIndex(1))
        acaoPaginaPosicao.triggered.connect(lambda: self.stack.setCurrentIndex(2))
        acaoPaginaIluminacao.triggered.connect(lambda: self.stack.setCurrentIndex(3))
        acaoPaginaAnimacao.triggered.connect(lambda: self.stack.setCurrentIndex(4))
        acaoPaginaConcatenar.triggered.connect(lambda: self.stack.setCurrentIndex(5))
        acaoPaginaAplicacoes.triggered.connect(lambda: self.stack.setCurrentIndex(6))

        self.menuVertical.addAction(acaoPaginaRecortar)
        self.menuVertical.addAction(acaoPaginaAudio)
        self.menuVertical.addAction(acaoPaginaPosicao)
        self.menuVertical.addAction(acaoPaginaIluminacao)
        self.menuVertical.addAction(acaoPaginaAnimacao)
        self.menuVertical.addAction(acaoPaginaConcatenar)
        self.menuVertical.addAction(acaoPaginaAplicacoes)

        layoutPrincipal.addWidget(self.menuVertical, 1.5)

        layoutCentral = QVBoxLayout()

        self.videoWidget = VideoWidgetInterativo(self)
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
        self.tempoAtual = ''
        self.tempoTotal = ''
        self.tempoTotal = ''

        self.temporizador = QLabel("00:00:00 / 00:00:00")

        self.avancar = QPushButton('+5')
        self.voltar  = QPushButton('-5')

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.audioOutput.setVolume(0.5)

        layoutSlider = QHBoxLayout()
        layoutSlider.addWidget(self.temporizador)
        layoutSlider.addWidget(self.voltar)
        layoutSlider.addWidget(self.avancar)
        layoutSlider.addWidget(self.slider, 6)
        layoutSlider.addWidget(self.volumeSlider, 1)

        layoutReprodutor = QVBoxLayout()
        layoutReprodutor.addWidget(self.videoWidget)
        layoutReprodutor.addLayout(layoutSlider)

        layoutCentral.addLayout(layoutReprodutor, 8)

        self.stack = QStackedWidget()
        self.stack.addWidget(Recortar())
        self.stack.addWidget(Audio())
        self.stack.addWidget(Posicao())
        self.stack.addWidget(Iluminacao())
        self.stack.addWidget(Animacao())
        self.stack.addWidget(Concatenar())
        self.stack.addWidget(Aplicacoes())

        layoutCentral.addWidget(self.stack, 2)
        layoutPrincipal.addLayout(layoutCentral, 7)

        layoutListas = QVBoxLayout()
        botaoCarregarVideo = QPushButton('Carregar Video')
        self.caixaBotaoRecortes = CaixaLista('Recortados', [0, 1, 2, 3])
        self.caixaBotaoEditados = CaixaLista('Editados', [0, 1, 2, 3])
        self.caixaVideoMemes = CaixaLista('Memes', [0, 1, 2, 3])
        self.caixaBotaoSalvos = CaixaLista('Salvos', [0, 1, 2, 3])

        layoutListas.addWidget(botaoCarregarVideo)
        layoutListas.addWidget(self.caixaBotaoRecortes)
        layoutListas.addWidget(self.caixaBotaoEditados)
        layoutListas.addWidget(self.caixaVideoMemes)
        layoutListas.addWidget(self.caixaBotaoSalvos)
        layoutListas.addStretch()

        layoutPrincipal.addLayout(layoutListas, 1.5)

        botaoCarregarVideo.clicked.connect(self.abrirVideo)       # carrega um video do computador
        self.volumeSlider.valueChanged.connect(self.ajusteVolume) # regula o volume do video
        self.player.positionChanged.connect(self.atualizarSlider) # atualiza o slider conforme video roda
        self.slider.sliderMoved.connect(self.player.setPosition)  # mover o slider permite alterar o momento do video
        self.videoWidget.select.connect(self.alternarPlayPause)   # pausa e continua o video
        self.avancar.clicked.connect(self.avancarSlider)
        self.voltar.clicked.connect(self.voltarSlider)

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

        self.tempoAtual = QTime(0, 0, 0).addMSecs(posicao)
        self.tempoTotal = QTime(0, 0, 0).addMSecs(duracao)
        self.tempoTotal = QTime(0, 0, 0).addMSecs(duracao)

        self.temporizador.setText(f"{self.tempoAtual.toString('hh:mm:ss')} / {self.tempoTotal.toString('hh:mm:ss')}")
        self.temporizador.setText(f"{self.tempoAtual.toString('hh:mm:ss')} / {self.tempoTotal.toString('hh:mm:ss')}")
        
    def avancarSlider(self):
        novaPosicao = self.player.position() + 5000
        self.player.setPosition(novaPosicao)
        self.slider.setValue(novaPosicao)

    def voltarSlider(self):
        novaPosicao = self.player.position() - 5000
        self.player.setPosition(novaPosicao)
        self.slider.setValue(novaPosicao)

    def alternarPlayPause(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()


class Recortar(QWidget):
    def __init__(self):
        super().__init__()
        layoutRecortar = QVBoxLayout(self)
        layoutRecortar.addWidget(TelaPrincipal.temporizador) # problemas com importacao
        layoutRecortar.addWidget(TelaPrincipal.slider)
        self.duracao = TelaPrincipal.tempoTotal
        self.momento = TelaPrincipal.tempoAtual

        layoutCorpoRecortar = QHBoxLayout(self)

        layoutTrechosRecortar = QVBoxLayout
        layoutInicioRecorte = QHBoxLayout()
        layoutInicioRecorte.addWidget(QLabel('Inicio:'))
        botaoInicioRecorte = QPushButton('Selecionar')
        layoutInicioRecorte.addWidget(botaoInicioRecorte)

        layoutFinalRecorte  = QHBoxLayout()
        layoutFinalRecorte.addWidget(QLabel('Final:'))
        botaoFinalRecorte = QPushButton('Selecionar')
        layoutFinalRecorte.addWidget(botaoFinalRecorte)

        comecoRecorte = ''
        finalRecorte  = ''

        layoutTrechosRecortar.addLayout(layoutInicioRecorte)
        layoutTrechosRecortar.addLayout(layoutFinalRecorte)
        layoutTrechosRecortar.addWidget(QLabel('Recorte'))
        layoutTrechosRecortar.addWidget(QPushButton('Recorte'))

        listaRecortes = QListWidget()

        layoutCorpoRecortar.addWidget(QPushButton('Aplicar'))
        layoutCorpoRecortar.addWidget(listaRecortes)


class Audio(QWidget):
    def __init__(self):
        super().__init__()
        layoutAudio = QVBoxLayout(self)
        layoutAudio.addWidget(QLabel('Audio'))
        layoutAudio.addWidget(QPushButton('Aplicar'))


class Posicao(QWidget):
    def __init__(self):
        super().__init__()
        layoutPosicao = QVBoxLayout(self)
        layoutPosicao.addWidget(QLabel('Posicao'))
        layoutPosicao.addWidget(QPushButton('Aplicar'))


class Iluminacao(QWidget):
    def __init__(self):
        super().__init__()
        layoutIluminacao = QVBoxLayout(self)
        layoutIluminacao.addWidget(QLabel('Iluminacao'))
        layoutIluminacao.addWidget(QPushButton('Aplicar'))


class Animacao(QWidget):
    def __init__(self):
        super().__init__()
        layoutAnimacao = QVBoxLayout(self)
        layoutAnimacao.addWidget(QLabel('Animacao'))
        layoutAnimacao.addWidget(QPushButton('Aplicar'))


class Concatenar(QWidget):
    def __init__(self):
        super().__init__()
        layoutConcatenar = QVBoxLayout(self)
        layoutConcatenar.addWidget(QLabel('Concatenar'))
        layoutConcatenar.addWidget(QPushButton('Aplicar'))


class Aplicacoes(QWidget):
    def __init__(self):
        super().__init__()
        layoutAplicacoes = QVBoxLayout(self)
        layoutAplicacoes.addWidget(QLabel('Aplicacoes'))
        layoutAplicacoes.addWidget(QPushButton('Aplicar'))


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
