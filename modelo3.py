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


class TelaRecortar(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

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

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.audioOutput.setVolume(0.5)

        self.contagemClips = 1
        layoutBotoes = QHBoxLayout()
        for texto in ["Carregar", "Recortar", "Editar", "Salvar"]:
            botao = QPushButton(texto)
            layoutBotoes.addWidget(botao)
            if texto == "Carregar":
                botao.clicked.connect(self.carregarVideo)
            elif texto == "Recortar":
                botao.clicked.connect(self.recortarVideo)
            elif texto == "Editar":
                botao.clicked.connect(self.trocarTelaEditar) # como trocar tela ?
            elif texto == "Salvar":
                botao.clicked.connect(self.trocarTelaSalvar) # como trocar tela ?
            
        self.temporizador = QLabel("00:00:00 / 00:00:00")

        layoutTempo = QHBoxLayout()
        layoutTempo.addWidget(self.temporizador)
        layoutTempo.addWidget(self.slider, 6)
        layoutTempo.addWidget(self.volumeSlider, 2)

        layoutVideo = QVBoxLayout()
        layoutVideo.addWidget(self.videoWidget)
        layoutVideo.addLayout(layoutTempo)
        layoutVideo.addLayout(layoutBotoes)

        self.listaVideosRecortados = QListWidget()
        self.caminhosRecortes = []

        self.layoutRecortes = QVBoxLayout()
        self.layoutRecortes.addWidget(QLabel("Vídeos recortados"))
        self.layoutRecortes.addWidget(self.listaVideosRecortados)

        layoutPrincipal = QHBoxLayout()
        layoutPrincipal.addLayout(layoutVideo, 8)
        layoutPrincipal.addLayout(self.layoutRecortes, 2)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layoutPrincipal)
        self.setLayout(mainLayout)

        self.player.positionChanged.connect(self.atualizarSlider)
        self.player.durationChanged.connect(lambda dur: self.slider.setMaximum(dur))
        self.listaVideosRecortados.itemDoubleClicked.connect(self.carregarRecortes)
        self.slider.sliderMoved.connect(self.player.setPosition)
        self.videoWidget.select.connect(self.alternarPlayPause)
        self.volumeSlider.valueChanged.connect(self.ajusteVolume)

    def carregarVideo(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Abrir vídeo", "", "Vídeo (*.mp4 *.avi *.mkv *.mov)")
        if caminho:
            self.caminhoVideo = caminho
            self.player.setSource(QUrl.fromLocalFile(caminho))
            self.player.play()

            video = VideoFileClip(caminho)
            duracao = video.duration
            self.slider.setMinimum(0)
            self.slider.setMaximum(duracao)

    def recortarVideo(self):
        trechosRecorte = self.slider.recortes
        videoRecortar = VideoFileClip(self.caminhoVideo)

        pastaRecortes = 'recortes'
        if not os.path.exists(pastaRecortes):
            os.mkdir(pastaRecortes)

        for inicio, fim in trechosRecorte:
            inicio = inicio / 1000
            fim = fim / 1000

            clipVideo = videoRecortar.subclip(inicio, fim)

            nomeArquivoRecortado = f'videoRecortado{self.contagemClips}.mp4'
            caminhoArquivoRecortado = os.path.join(pastaRecortes, nomeArquivoRecortado)

            clipVideo.write_videofile(caminhoArquivoRecortado)

            item = QListWidgetItem(nomeArquivoRecortado)
            self.listaVideosRecortados.addItem(item)
            self.caminhosRecortes.append(caminhoArquivoRecortado)
            
            self.contagemClips += 1

    def trocarTelaEditar(self):
        self.stack.setCurrentIndex(1)

    def trocarTelaSalvar(self):
        self.stack.setCurrentIndex(2)

    def atualizarSlider(self, posicao):
        duracao = self.player.duration()
        self.slider.setMaximum(duracao)
        self.slider.setValue(posicao)

        tempoAtual = QTime(0, 0, 0).addMSecs(posicao)
        tempoTotal = QTime(0, 0, 0).addMSecs(duracao)
        self.temporizador.setText(f"{tempoAtual.toString('hh:mm:ss')} / {tempoTotal.toString('hh:mm:ss')}")

    def alternarPlayPause(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def carregarRecortes(self, item):
        indice = self.listaVideosRecortados.row(item)
        caminho = self.caminhosRecortes[indice]
        self.player.setSource(QUrl.fromLocalFile(caminho))
        self.player.play()

    def ajusteVolume(self, valor):
        self.audioOutput.setVolume(valor / 100)


class TelaEditar(QWidget):
    def __init__(self, telaCarregada, stack):
        super().__init__()
        self.instanciaTelaCarregar = telaCarregada
        self.stack = stack

        pastaRecorte = 'pastaRecorte'
        if not os.path.exists(pastaRecorte):
            os.mkdir(pastaRecorte)

        layoutPrincipalEditar = QHBoxLayout()

        layoutColunaEdicao = QVBoxLayout()

        self.ferramentaUtilizada = 'Video'
        botoesEdicao = ['Video', 'Cor', 'Audio']
        for botao in botoesEdicao:
            botaoEdicao = QPushButton(botao)
            layoutColunaEdicao.addWidget(botaoEdicao)

            if botao == 'Video':
                botaoEdicao.clicked.connect(self.ferramentaVideo)
            elif botao == 'Cor':
                botaoEdicao.clicked.connect(self.ferramentaCor)
            elif botao == 'Audio':
                botaoEdicao.clicked.connect(self.ferramentaAudio)
        
        layoutColunaEdicao.addStretch()

        self.layoutVideoEdicao = QVBoxLayout()

        self.playerEditor = QMediaPlayer(self)
        self.audioEditor = QAudioOutput()
        self.playerEditor.setAudioOutput(self.audioEditor)

        self.videoWidgetEditor = VideoWidgetInterativo(self)
        self.playerEditor.setVideoOutput(self.videoWidgetEditor)

        self.sliderEditor = ConfigSlider(Qt.Horizontal)
        self.sliderEditor.setStyleSheet("""
            QSlider::groove:horizontal { height: 8px; background: #ccc; }
            QSlider::handle:horizontal { width: 16px; background: #444; border-radius: 8px; }
            QSlider::sub-page:horizontal { background: #0080ff; }
        """)
        self.sliderEditor.setMouseTracking(True)
        self.sliderEditor.setMinimum(0)
        self.sliderEditor.setMaximum(int(self.playerEditor.duration()))

        self.temporizadorEditor = QLabel("00:00:00 / 00:00:00")
        self.layoutTempoEditor = QHBoxLayout()
        self.layoutTempoEditor.addWidget(self.temporizadorEditor)
        self.layoutTempoEditor.addWidget(self.sliderEditor)

        self.layoutBotoesVideo = QHBoxLayout()
        self.botaoCarregar = QPushButton('Carregar')
        self.botaoSalvar = QPushButton('Salvar')
        self.layoutBotoesVideo.addWidget(self.botaoCarregar)
        self.layoutBotoesVideo.addWidget(self.botaoSalvar)

        self.layoutBotoesCor = QHBoxLayout()
        botoesCor = ['Brilho', 'Tonalidade', 'Preto/Branco']
        for botao in botoesCor:
            botaoCor = QPushButton(botao)
            self.layoutBotoesCor.addWidget(botaoCor)

        self.layoutBotoesAudio = QVBoxLayout()
        botoesAudio = ['Volume video', 'Som de fundo']
        for slider in botoesAudio:
            sliderAudio = QSlider(Qt.Horizontal)
            layoutConfigAudio = QHBoxLayout()
            if slider == 'Som de fundo':
                botaoSelecaoAudio = QPushButton('Carregar audio')
                layoutConfigAudio.addWidget(botaoSelecaoAudio)
            layoutConfigAudio.addWidget(QLabel(slider), 2)
            layoutConfigAudio.addWidget(sliderAudio, 8)
            self.layoutBotoesAudio.addLayout(layoutConfigAudio)
        
        self.layoutVideoEdicao.addWidget(self.videoWidgetEditor)
        self.layoutVideoEdicao.addLayout(self.layoutTempoEditor)
        if self.ferramentaUtilizada == 'Video':
            self.layoutVideoEdicao.addLayout(self.layoutBotoesVideo)
        elif self.ferramentaUtilizada == 'Cor':
            self.layoutVideoEdicao.addLayout(self.layoutBotoesCor)
        elif self.ferramentaUtilizada == 'Audio':
            self.layoutVideoEdicao.addLayout(self.layoutBotoesAudio)

        opcoes_texto = [
            self.instanciaTelaCarregar.listaVideosRecortados.item(i).text() for i in range(
                self.instanciaTelaCarregar.listaVideosRecortados.count()
                )
        ]

        layoutSelecaoVideos = QVBoxLayout()
        self.caixaBotaoRecortes = CaixaLista('Vídeos recortados', opcoes_texto)
        self.caixaBotaoEditados = CaixaLista('Vídeos editados', opcoes_texto)
        layoutSelecaoVideos.addWidget(self.caixaBotaoRecortes)
        layoutSelecaoVideos.addWidget(self.caixaBotaoEditados)
        layoutSelecaoVideos.addStretch()

        layoutPrincipalEditar.addLayout(layoutColunaEdicao, 0.5)
        layoutPrincipalEditar.addLayout(self.layoutVideoEdicao, 7.5)
        layoutPrincipalEditar.addLayout(layoutSelecaoVideos, 2)

        self.setLayout(layoutPrincipalEditar)

        self.botaoSalvar.clicked.connect(self.trocarTelaSalvar)

    def ferramentaVideo(self):
        self.ferramentaUtilizada = 'Video'
        self.atualizarFerramentaEdicao()
    
    def ferramentaCor(self):
        self.ferramentaUtilizada = 'Cor'
        self.atualizarFerramentaEdicao()
    
    def ferramentaAudio(self):
        self.ferramentaUtilizada = 'Audio'
        self.atualizarFerramentaEdicao()
    
    def trocarTelaSalvar(self):
        self.stack.setCurrentIndex(2)


class TelaSalvar(QWidget):
    def __init__(self):
        super().__init__()


class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Editor de Video')
        self.setFixedSize(1200,650)

        self.stack = QStackedWidget()

        self.carregar = TelaRecortar(self.stack)
        self.edicao = TelaEditar(self.carregar, self.stack)
        self.salvar = TelaSalvar()

        self.stack.addWidget(self.carregar)
        self.stack.addWidget(self.edicao)
        self.stack.addWidget(self.salvar)

        botaoCarregar = QPushButton('RECORTAR')
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
