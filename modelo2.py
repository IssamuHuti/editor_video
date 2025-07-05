import sys
import os
import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QComboBox, QFileDialog,
    QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QMessageBox, QSlider
)
from PySide6.QtCore import QUrl, Qt, QTime, QTimer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput


class TelaCarregarRecortar(QWidget):
    def __init__(self):
        super().__init__()
        layoutPrincipalCarregarRecortar = QVBoxLayout()

        layoutCarregarRecortar = QHBoxLayout()

        layoutCarregarVideo = QVBoxLayout()

        self.videoWidget = QVideoWidget()
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.player.setVideoOutput(self.videoWidget)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal { height: 8px; background: #ccc; }
            QSlider::handle:horizontal { width: 16px; background: #444; border-radius: 8px; }
            QSlider::sub-page:horizontal { background: #0080ff; }
        """)

        layoutBotoes = QHBoxLayout()
        botaoCarregar = QPushButton('Carregar')
        botaoRecortar = QPushButton('Recortar')
        botaoEditar = QPushButton('Editar')
        botaoSalvar = QPushButton('Salvar')

        botaoCarregar.clicked.connect(self.carregarVideo)
        self.player.positionChanged.connect(self.atualizar_slider)
        self.slider.sliderMoved.connect(self.player.setPosition)

        layoutBotoes.addWidget(botaoCarregar)
        layoutBotoes.addWidget(botaoRecortar)
        layoutBotoes.addWidget(botaoEditar)
        layoutBotoes.addWidget(botaoSalvar)

        layoutCarregarVideo.addWidget(self.videoWidget)
        layoutCarregarVideo.addWidget(self.slider)
        layoutCarregarVideo.addLayout(layoutBotoes)


        layoutVideosRecortados = QVBoxLayout()

        recortes = QLabel('Videos recortados')
        recortes.setStyleSheet("color: black; background-color: lightgray; border: 1px solid black;")
        recortes.setAlignment(Qt.AlignCenter)
        layoutVideosRecortados.addWidget(recortes)

        layoutCarregarRecortar.addLayout(layoutCarregarVideo, 8)
        layoutCarregarRecortar.addLayout(layoutVideosRecortados, 2)

        layoutPrincipalCarregarRecortar.addLayout(layoutCarregarRecortar)
        self.setLayout(layoutPrincipalCarregarRecortar)

    def carregarVideo(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Abrir vídeo", "", "Vídeo (*.mp4 *.avi *.mkv *.mov)")
        if caminho:
            self.player.setSource(QUrl.fromLocalFile(caminho))
            self.player.play()
    
    def atualizar_slider(self, posicao):
        self.slider.setMaximum(self.player.duration())
        self.slider.setValue(posicao)


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


class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Editor de Video')
        self.setFixedSize(1300,650)

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

        botaoCarregar = QPushButton('Carregar')
        botaoCarregar.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        botaoEditar = QPushButton('Editar')
        botaoEditar.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        botaoSalvar = QPushButton('Salvar')
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
