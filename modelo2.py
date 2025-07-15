import sys
import os
import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QComboBox, QFileDialog, QListWidgetItem,
    QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QMessageBox, QSlider, QListWidget
)
from PySide6.QtCore import QUrl, Qt, QTime, QTimer, Signal
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtGui import QMouseEvent, QPainter, QColor
from moviepy.editor import VideoFileClip


class TelaCarregarRecortar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recorte de Vídeo")
        self.resize(800, 500)

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

        # Botões
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
                botao.clicked.connect(self.trocarTelaEditar)
            elif texto == "Salvar":
                botao.clicked.connect(self.trocarTelaSalvar)
            
        # Layout tempo
        self.temporizador = QLabel("00:00:00 / 00:00:00")
        layoutTempo = QHBoxLayout()
        layoutTempo.addWidget(self.temporizador)
        layoutTempo.addWidget(self.slider)

        # Layout vídeo
        layoutVideo = QVBoxLayout()
        layoutVideo.addWidget(self.videoWidget)
        layoutVideo.addLayout(layoutTempo)
        layoutVideo.addLayout(layoutBotoes)

        self.listaVideosRecortados = QListWidget()
        self.caminhosRecortes = []

        # Lista recortes
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

    def carregarVideo(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Abrir vídeo", "", "Vídeo (*.mp4 *.avi *.mkv *.mov)")
        if caminho:
            self.caminhoVideo = caminho
            self.player.setSource(QUrl.fromLocalFile(caminho))
            self.player.play()

            # Corrigindo o máximo do slider com base na duração real do vídeo
            video = VideoFileClip(caminho)
            duracao = video.duration  # Em segundos (float)
            self.slider.setMinimum(0)
            self.slider.setMaximum(duracao)  # ← Corrige a base do slider

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
        ...

    def trocarTelaSalvar(self):
        ...

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


class TelaEditar(QWidget):
    def __init__(self, telaCarregada):
        super().__init__()
        self.instanciaTelaCarregar = telaCarregada # ← aqui está a instância com os recortes

        pastaRecorte = 'pastaRecorte'
        if not os.path.exists(pastaRecorte):
            os.mkdir(pastaRecorte)

        layoutPrincipalEditar = QHBoxLayout()

        layoutVideoEdicao = QVBoxLayout()

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
        layoutTempoEditor = QHBoxLayout()
        layoutTempoEditor.addWidget(self.temporizadorEditor)
        layoutTempoEditor.addWidget(self.sliderEditor)

        layoutVideoEdicao.addWidget(self.videoWidgetEditor)
        layoutVideoEdicao.addLayout(layoutTempoEditor) # desaparece após escolher o vídeo

        layoutSelecaoVideos = QVBoxLayout()

        self.listaVideosRecortadosEdicao = QListWidget()
        for i in range(self.instanciaTelaCarregar.listaVideosRecortados.count()):
            item_text = self.instanciaTelaCarregar.listaVideosRecortados.item(i).text()
            self.listaVideosRecortadosEdicao.addItem(item_text)

        layoutSelecaoVideos.addWidget(QLabel('Vídeos recortados'))
        layoutSelecaoVideos.addWidget(self.listaVideosRecortadosEdicao)

        layoutPrincipalEditar.addLayout(layoutVideoEdicao, 8)
        layoutPrincipalEditar.addLayout(layoutSelecaoVideos, 2)

        self.setLayout(layoutPrincipalEditar)

        self.listaVideosRecortadosEdicao.itemDoubleClicked.connect(self.reproduzirVideo)
        self.playerEditor.positionChanged.connect(self.atualizarSlider)
        self.videoWidgetEditor.select.connect(self.alternarPlayPause)

    def reproduzirVideo(self, item):
        indiceEditar = self.listaVideosRecortadosEdicao.row(item)
        caminhoEditar = self.instanciaTelaCarregar.caminhosRecortes[indiceEditar]
        self.playerEditor.setSource(QUrl.fromLocalFile(caminhoEditar))
        self.playerEditor.play()
    
    def atualizarSlider(self, posicao):
        duracao = self.playerEditor.duration()
        self.sliderEditor.setMaximum(duracao)
        self.sliderEditor.setValue(posicao)

        tempoAtual = QTime(0, 0, 0).addMSecs(posicao)
        tempoTotal = QTime(0, 0, 0).addMSecs(duracao)
        self.temporizadorEditor.setText(f"{tempoAtual.toString('hh:mm:ss')} / {tempoTotal.toString('hh:mm:ss')}")
    
    def alternarPlayPause(self):
        if self.playerEditor.playbackState() == QMediaPlayer.PlayingState:
            self.playerEditor.pause()
        else:
            self.playerEditor.play()


class TelaSalvar(QWidget):
    def __init__(self):
        super().__init__()

        novosVideos = 'novosVideos'
        if not os.path.exists(novosVideos):
            os.mkdir(novosVideos)

        layoutPrincipalSalvar = QVBoxLayout()

        layoutSalvar = QHBoxLayout()

        layoutVideoRecortado = QVBoxLayout()



        botaoSalvar = QPushButton('Salvar')

        layoutVideoRecortado.addWidget(QLabel('Escolha o vídeo')) # desaparece após escolher o vídeo
        layoutVideoRecortado.setAlignment(Qt.AlignCenter)

        layoutVideoRecortado.addStretch()
        layoutVideoRecortado.addWidget(botaoSalvar)

        layoutSelecaoVideos = QVBoxLayout()

        menuSalvar = QLabel('Videos a salvar')
        menuSalvar.setStyleSheet("color: black; background-color: lightgray; border: 1px solid black;")
        menuSalvar.setAlignment(Qt.AlignCenter)
        layoutSelecaoVideos.addWidget(menuSalvar)

        layoutSalvar.addLayout(layoutVideoRecortado, 8)
        layoutSalvar.addLayout(layoutSelecaoVideos, 2)

        layoutPrincipalSalvar.addLayout(layoutSalvar)
        self.setLayout(layoutPrincipalSalvar)

        botaoSalvar.clicked.connect(self.salvar)
    
    def salvar(self):
        confirmacao = QMessageBox.question(
            self,
            'Confirmação',
            'Deseja salvar o video?',
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmacao == QMessageBox.Yes:
            QMessageBox.information(self, 'Salvo', 'O video foi salvo')
            os.chdir('novosVideos')
            
            # configurar para que crie uma pasta por dia que salvar o video # datetime
            # salvar o video com moviepy

            os.chdir('..')

        else:
            QMessageBox.information(self, 'Editar Video', 'Edite novamente o video')


class TelaConfiguracao(QWidget):
    def __init__(self, temaInicial):
        super().__init__()
        layoutPrincipalConfig = QVBoxLayout()

        self.opcaoTemas = QComboBox()
        self.opcaoTemas.addItems(['Escuro', 'Claro'])
        self.opcaoTemas.setCurrentText(temaInicial)

        layoutTema = QHBoxLayout()
        layoutTema.addWidget(QLabel('Cores app: '))
        layoutTema.addWidget(self.opcaoTemas)
        layoutTema.addStretch()

        layoutPrincipalConfig.addWidget(QLabel('Configurações'))
        layoutPrincipalConfig.addLayout(layoutTema)
        layoutPrincipalConfig.addStretch()

        self.setLayout(layoutPrincipalConfig)

        self.opcaoTemas.currentTextChanged.connect(self.alterarTema)

    def alterarTema(self, texto):
        temaSelecionada = texto
        if temaSelecionada == 'Escuro':
            app.setStyleSheet(ESTILO_ESCURO)
        elif temaSelecionada == 'Claro':
            app.setStyleSheet(ESTILO_CLARO)


class ConfigSlider(QSlider):
    def __init__(self, orientacao, parent=None):
        super().__init__(orientacao, parent)
        self.setMouseTracking(True)
        self.setMinimum(0)
        self.setMaximum(100000)
        
        self.inicio_recorte = None
        self.fim_recorte = None
        self.setFixedHeight(30)  # Aumenta o tamanho do widget inteiro

        self.recortes = []  # Lista de (inicio, fim)
        self.inicio_temp = None  # Marca o primeiro clique

        self.caixaFlutuante = QLabel("00:00:00", self)
        # Aumenta a espessura visual do groove e handle
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

# a função não está funcionando
    # def mouseMoveEvent(self, event):
    #     super().mouseMoveEvent(event)  # MANTÉM O COMPORTAMENTO PADRÃO DO SLIDER

    #     valorMinimo = self.minimum()
    #     valorMaximo = self.maximum()
    #     if valorMaximo - valorMinimo == 0: # Evita divisão por zero
    #         return
        
    #     largura = self.width()
    #     pos = event.pos().x() # event.pos() retorna QPoint
    #     valor = valorMinimo + ((valorMaximo - valorMinimo) * pos) / largura #
    #     valor = int(valor)

    #     # Formata o tempo como hh:mm:ss
    #     tempo = QTime(0, 0, 0).addMSecs(valor)
    #     self.caixaFlutuante.setText(tempo.toString("hh:mm:ss"))
    #     self.caixaFlutuante.adjustSize()

    #     # Posiciona a caixa
    #     x = int(event.position().x()) - self.caixaFlutuante.width() // 2
    #     y = -self.caixaFlutuante.height() - 5  # um pouco acima do groove
    #     self.caixaFlutuante.move(x, y)
    #     self.caixaFlutuante.setVisible(True)

    def leaveEvent(self, event):
        self.caixaFlutuante.setVisible(False)
        # super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        # Calcula o valor clicado
        if event.button() == Qt.RightButton:
            pos = event.position().x() if hasattr(event, 'position') else event.x()
            valor = self.minimum() + ((self.maximum() - self.minimum()) * pos) / self.width()

            # Verifica se o clique está dentro de uma região marcada
            for inicio, fim in self.recortes:
                if inicio <= valor <= fim:
                    self.recortes.remove((inicio, fim))
                    self.update()
                    return
                
            # Alternância lógica: primeiro início, depois fim
            if self.inicio_temp is None:
                self.inicio_temp = valor
            else:
                inicio = float(min(self.inicio_temp, valor))
                fim = float(max(self.inicio_temp, valor))
                self.recortes.append((inicio, fim))
                self.inicio_temp = None
                self.update() # Reforça a pintura

        else:
            super().mousePressEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.recortes:
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 255, 0, 100))  # Verde transparente

            # Calcula posição em pixels dos limites marcados
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


class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Editor de Video')
        self.setFixedSize(1200,650)

        temaInicial = TelaConfiguracao('Escuro')
        temaInicial.alterarTema('Escuro')

        self.carregar = TelaCarregarRecortar()
        self.edicao = QWidget()
        self.salvar = TelaSalvar()
        self.config = TelaConfiguracao('Escuro')

        self.stack = QStackedWidget()
        self.stack.addWidget(self.carregar)
        self.stack.addWidget(self.edicao)
        self.stack.addWidget(self.salvar)
        self.stack.addWidget(self.config)

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
        botaoEditar.clicked.connect(self.abrirTelaEditar)
        botaoSalvar.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        botaoConfig.clicked.connect(lambda: self.stack.setCurrentIndex(3))
    
    def abrirTelaEditar(self):
        if not self.carregar.caminhosRecortes:
            QMessageBox.warning(self, "Aviso", "Nenhum vídeo recortado disponível.")
            return

        # Cria nova tela com dados atualizados
        novaTelaEditar = TelaEditar(self.carregar)

        # Substitui widget antigo
        self.stack.removeWidget(self.edicao)
        self.edicao.deleteLater()
        self.edicao = novaTelaEditar

        self.stack.insertWidget(1, self.edicao)  # Reinsere na posição 1
        self.stack.setCurrentIndex(1)  # Troca para a tela de edição


ESTILO_CLARO = """
    QWidget {
        background-color: #ffffff;
        color: #000000;
    }
    QPushButton {
        background-color: #e0e0e0;
        color: black;
        border: 2px;
        padding: 10px;
    }
    QComboBox {
        background-color: #e0e0e0;
        color: black;
        border: 2px;
        padding: 5px;
    }
"""

ESTILO_ESCURO = """
    QWidget {
        background-color: #2e2e2e;
        color: #ffffff;
    }
    QPushButton {
        background-color: #444;
        color: white;
        border: 2px;
        padding: 10px;
    }
    QComboBox {
        background-color: #444;
        color: white;
        border: 2px;
        padding: 5px;
    }
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaPrincipal()
    janela.show()
    app.exec()
