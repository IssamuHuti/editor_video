import sys
import os
import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QComboBox, QFileDialog,
    QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QMessageBox, QSlider, QListWidget
)
from PySide6.QtCore import QUrl, Qt, QTime, QTimer, Signal
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtGui import QMouseEvent, QPainter, QColor


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

        self.player.positionChanged.connect(self.atualizarSlider)
        self.player.durationChanged.connect(lambda dur: self.slider.setMaximum(dur))
        self.slider.sliderMoved.connect(self.player.setPosition)
        self.videoWidget.select.connect(self.alternarPlayPause)

        # Botões
        layoutBotoes = QHBoxLayout()
        for texto in ["Carregar", "Recortar", "Editar", "Salvar"]:
            botao = QPushButton(texto)
            layoutBotoes.addWidget(botao)
            if texto == "Carregar":
                botao.clicked.connect(self.carregarVideo)

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

        # Lista recortes
        layoutRecortes = QVBoxLayout()
        layoutRecortes.addWidget(QLabel("Vídeos recortados"))
        layoutRecortes.addWidget(QListWidget())

        layoutPrincipal = QHBoxLayout()
        layoutPrincipal.addLayout(layoutVideo, 8)
        layoutPrincipal.addLayout(layoutRecortes, 2)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layoutPrincipal)
        self.setLayout(mainLayout)

    def carregarVideo(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Abrir vídeo", "", "Vídeo (*.mp4 *.avi *.mkv *.mov)")
        if caminho:
            self.player.setSource(QUrl.fromLocalFile(caminho))
            self.player.play()

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


class TelaEditar(QWidget):
    def __init__(self):
        super().__init__()

        pastaRecorte = 'pastaRecorte'
        if not os.path.exists(pastaRecorte):
            os.mkdir(pastaRecorte)

        layoutPrincipalEditar = QVBoxLayout()

        layoutEdicao = QHBoxLayout()

        layoutVideoEdicao = QVBoxLayout()



        layoutVideoEdicao.addWidget(QLabel('Edição'))
        layoutVideoEdicao.addWidget(QLabel('Escolha o vídeo')) # desaparece após escolher o vídeo
        layoutVideoEdicao.setAlignment(Qt.AlignCenter)

        layoutConfigEdicao = QVBoxLayout()

        menuEdicao = QLabel('Ferramentas')
        menuEdicao.setStyleSheet("color: black; background-color: lightgray; border: 1px solid black;")
        menuEdicao.setAlignment(Qt.AlignCenter)
        layoutConfigEdicao.addWidget(menuEdicao)

        layoutEdicao.addLayout(layoutVideoEdicao, 8)
        layoutEdicao.addLayout(layoutConfigEdicao, 2)

        layoutPrincipalEditar.addLayout(layoutEdicao)
        self.setLayout(layoutPrincipalEditar)


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
        botaoSalvar.clicked.connect(self.salvar)

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
        self.opcaoTemas.currentTextChanged.connect(self.alterarTema)

        layoutTema = QHBoxLayout()
        layoutTema.addWidget(QLabel('Cores app: '))
        layoutTema.addWidget(self.opcaoTemas)
        layoutTema.addStretch()

        layoutPrincipalConfig.addWidget(QLabel('Configurações'))
        layoutPrincipalConfig.addLayout(layoutTema)
        layoutPrincipalConfig.addStretch()

        self.setLayout(layoutPrincipalConfig)

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

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)  # MANTÉM O COMPORTAMENTO PADRÃO DO SLIDER

        valorMinimo = self.minimum()
        valorMaximo = self.maximum()
        if valorMaximo - valorMinimo == 0: # Evita divisão por zero
            return
        
        largura = self.width()
        pos = event.pos().x() # event.pos() retorna QPoint
        valor = valorMinimo + ((valorMaximo - valorMinimo) * pos) / largura #
        valor = int(valor)

        # Formata o tempo como hh:mm:ss
        tempo = QTime(0, 0, 0).addMSecs(valor)
        self.caixaFlutuante.setText(tempo.toString("hh:mm:ss"))
        self.caixaFlutuante.adjustSize()

        # Posiciona a caixa
        x = int(event.position().x()) - self.caixaFlutuante.width() // 2
        y = -self.caixaFlutuante.height() - 5  # um pouco acima do groove
        self.caixaFlutuante.move(x, y)
        self.caixaFlutuante.setVisible(True)

    def leaveEvent(self, event):
        self.caixaFlutuante.setVisible(False)
        # super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        # Calcula o valor clicado
        if event.button() == Qt.RightButton:
            pos = event.position().x() if hasattr(event, 'position') else event.x()
            valor = self.minimum() + ((self.maximum() - self.minimum()) * pos) / self.width()
            # valor = int(valor)

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
                inicio = min(valor, self.inicio_temp, valor)
                fim = max(valor, self.inicio_temp, valor)
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
        self.edicao = TelaEditar()
        self.salvar = TelaSalvar()
        self.config = TelaConfiguracao('Escuro')

        self.stack = QStackedWidget()
        self.stack.addWidget(self.carregar)
        self.stack.addWidget(self.edicao)
        self.stack.addWidget(self.salvar)
        self.stack.addWidget(self.config)

        botaoCarregar = QPushButton('CARREGAR')
        botaoCarregar.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        botaoEditar = QPushButton('EDITAR')
        botaoEditar.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        botaoSalvar = QPushButton('SALVAR')
        botaoSalvar.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        
        botaoConfig = QPushButton('Configuração')
        botaoConfig.clicked.connect(lambda: self.stack.setCurrentIndex(3))

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
