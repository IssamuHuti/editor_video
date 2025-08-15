import sys
import os
import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QComboBox, QFileDialog, QListWidgetItem, QToolBar, QLineEdit,
    QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QMessageBox, QSlider, QListWidget, QFrame, QSizePolicy, QSpinBox
)
from PySide6.QtCore import QUrl, Qt, QTime, QTimer, Signal
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtGui import QMouseEvent, QPainter, QColor, QAction, QIcon
from moviepy.editor import VideoFileClip, vfx, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
import moviepy.config as mpyconf


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
                botao.clicked.connect(self.carregarVideoRecortar)
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

    def carregarVideoRecortar(self):
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
        self.stack.widget(1).atualizarListas()
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
        botoesEdicao = ['Video', 'Cor', 'Audio', 'Edicoes Realizadas']
        self.listaEdicaoRealiza = QListWidget()
        self.edicoesAplicadas = []  # lista de (func, nome, params)

        for botao in botoesEdicao:
            botaoEdicao = QPushButton(botao)
            layoutColunaEdicao.addWidget(botaoEdicao)

            if botao == 'Video':
                botaoEdicao.clicked.connect(self.ferramentaVideo)
            elif botao == 'Cor':
                botaoEdicao.clicked.connect(self.ferramentaCor)
            elif botao == 'Audio':
                botaoEdicao.clicked.connect(self.ferramentaAudio)
            elif botao == 'Edicoes Realizadas':
                botaoEdicao.clicked.connect(self.ferramentaEdicoesRealizadas)
        
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
     
        self.layoutVideoEdicao.addWidget(self.videoWidgetEditor)
        self.layoutVideoEdicao.addLayout(self.layoutTempoEditor)

        self.layoutBotoesFerramenta = QVBoxLayout()
        self.layoutVideoEdicao.addLayout(self.layoutBotoesFerramenta)

        opcoes_texto = [
            self.instanciaTelaCarregar.listaVideosRecortados.item(i).text() for i in range(
                self.instanciaTelaCarregar.listaVideosRecortados.count()
                )
        ]

        layoutSelecaoVideosEditar = QVBoxLayout()
        self.caixaBotaoRecortes = CaixaLista('Vídeos recortados', opcoes_texto)
        self.caixaBotaoEditados = CaixaLista('Vídeos editados', [])
        layoutSelecaoVideosEditar.addWidget(self.caixaBotaoRecortes)
        layoutSelecaoVideosEditar.addWidget(self.caixaBotaoEditados)
        layoutSelecaoVideosEditar.addStretch()
        
        self.botaoCarregar = QPushButton('Carregar')
        self.botaoSalvar = QPushButton('Salvar Edicao')
        self.botaoSalvarEditar = QPushButton('Salvar')
        layoutSelecaoVideosEditar.addWidget(self.botaoCarregar)
        layoutSelecaoVideosEditar.addWidget(self.botaoSalvar)
        layoutSelecaoVideosEditar.addWidget(self.botaoSalvarEditar)

        layoutPrincipalEditar.addLayout(layoutColunaEdicao, 0.5)
        layoutPrincipalEditar.addLayout(self.layoutVideoEdicao, 7.5)
        layoutPrincipalEditar.addLayout(layoutSelecaoVideosEditar, 2)

        self.setLayout(layoutPrincipalEditar)

        self.botaoCarregar.clicked.connect(self.carregarVideoEditar)
        self.botaoSalvarEditar.clicked.connect(self.trocarTelaSalvar)
        self.botaoSalvar.clicked.connect(self.salvarVideoEditado)
        self.caixaBotaoRecortes.lista.itemDoubleClicked.connect(self.reproduzirVideo)
        self.caixaBotaoEditados.lista.itemDoubleClicked.connect(self.reproduzirVideo) # incompleto
        self.playerEditor.positionChanged.connect(self.atualizarSlider)
        self.videoWidgetEditor.select.connect(self.alternarPlayPause)
        self.listaEdicaoRealiza.itemDoubleClicked.connect(self.removerEdicaoUI)

        self.caminhoVideoEditor = None
        self.temp_preview_path = os.path.join('pastaRecorte', 'temp_preview.mp4')
        self.videoOriginal = None
        self.videoEditado = None

# Funcionalidades layout
    def carregarVideoEditar(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Abrir vídeo", "", "Vídeo (*.mp4 *.avi *.mkv *.mov)")
        if not caminho:
            return

        # Guarda caminho do original (evita manter VideoFileClip aberto)
        self.caminhoVideoEditor = caminho
        self.edicoesAplicadas.clear()
        self.listaEdicaoRealiza.clear()

        # Duração em ms para o QSlider (Qt usa milissegundos)
        with VideoFileClip(caminho) as video:
            duracao_ms = int(video.duration * 1000)

        # Player Qt
        self.playerEditor.setSource(QUrl.fromLocalFile(caminho))
        self.playerEditor.play()

        self.sliderEditor.setMinimum(0)
        self.sliderEditor.setMaximum(duracao_ms)

    def ferramentaVideo(self):
        self.ferramentaUtilizada = 'Video'
        self.atualizarFerramentaEdicao()
    
    def ferramentaCor(self):
        self.ferramentaUtilizada = 'Cor'
        self.atualizarFerramentaEdicao()
    
    def ferramentaAudio(self):
        self.ferramentaUtilizada = 'Audio'
        self.atualizarFerramentaEdicao()
    
    def ferramentaEdicoesRealizadas(self):
        self.ferramentaUtilizada = 'Edicoes Realizadas'
        self.atualizarFerramentaEdicao()
    
    def trocarTelaSalvar(self):
        self.stack.setCurrentIndex(2)

    def alternarPlayPause(self):
        if self.playerEditor.playbackState() == QMediaPlayer.PlayingState:
            self.playerEditor.pause()
        else:
            self.playerEditor.play()

    def reproduzirVideo(self, item):
        indiceEditar = self.caixaBotaoRecortes.lista.row(item)
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
    
    def atualizarListas(self):
        # Limpa e recarrega as listas
        self.caixaBotaoRecortes.lista.clear()
        for i in range(self.instanciaTelaCarregar.listaVideosRecortados.count()):
            self.caixaBotaoRecortes.lista.addItem(
                self.instanciaTelaCarregar.listaVideosRecortados.item(i).text()
            )

    def atualizarFerramentaEdicao(self):
        # Limpa widgets do layoutVideoEdicao
        while self.layoutBotoesFerramenta.count():
            item = self.layoutBotoesFerramenta.takeAt(0)

            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                self.limparLayout(item.layout())

        if self.ferramentaUtilizada == 'Video':
            layoutVideo = QVBoxLayout()

            # Linha de giro com caixa numérica + botões
            layoutGirar = QHBoxLayout()
            self.spinGraus = QSpinBox()
            self.spinGraus.setRange(0, 359)
            self.spinGraus.setValue(0)
            self.spinGraus.setSuffix("°")
            self.spinGraus.setFixedWidth(70)

            btnGirarEsquerda = QPushButton()
            btnGirarEsquerda.setIcon(QIcon.fromTheme("object-rotate-left"))
            btnGirarDireita = QPushButton()
            btnGirarDireita.setIcon(QIcon.fromTheme("object-rotate-right"))

            btnAplicarGiro = QPushButton("Aplicar Giro")

            layoutGirar.addWidget(QLabel("Ângulo:"))
            layoutGirar.addWidget(self.spinGraus)
            layoutGirar.addWidget(btnGirarEsquerda)
            layoutGirar.addWidget(btnGirarDireita)
            layoutGirar.addWidget(btnAplicarGiro)

            layoutOutros = QHBoxLayout()
            botaoEspelhar = QPushButton('Espelhar')
            botaoVelocidade = QPushButton('Velocidade')
            botaoMesclar = QPushButton('Mesclar')
            
            layoutOutros.addWidget(botaoEspelhar)
            layoutOutros.addWidget(botaoVelocidade)
            layoutOutros.addWidget(botaoMesclar)

            layoutVideo.addLayout(layoutGirar)
            layoutVideo.addLayout(layoutOutros)

            self.layoutBotoesFerramenta.addLayout(layoutVideo)

            btnAplicarGiro.clicked.connect(lambda: self.girarVideo(self.spinGraus.value()))
            btnGirarEsquerda.clicked.connect(lambda: self.girarVideo(self.spinGraus.value() - 45))
            btnGirarDireita.clicked.connect(lambda: self.girarVideo(self.spinGraus.value() + 45))
            botaoEspelhar.clicked.connect(self.espelharVideo)
            botaoVelocidade.clicked.connect(self.velocidadeVideo)
            botaoMesclar.clicked.connect(self.mesclarVideo)

        elif self.ferramentaUtilizada == 'Cor':
            layout = QHBoxLayout()
            for nome in ['Brilho', 'Tonalidade', 'Preto/Branco']:
                layout.addWidget(QPushButton(nome))
            self.layoutBotoesFerramenta.addLayout(layout)

        elif self.ferramentaUtilizada == 'Audio':
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(8)

            # Linha: Volume video
            linha_vol = QHBoxLayout()
            linha_vol.setContentsMargins(0, 0, 0, 0)
            linha_vol.setSpacing(8)
            linha_vol.addWidget(QLabel('Volume vídeo'), 2)
            slider_vol = QSlider(Qt.Horizontal)
            slider_vol.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            linha_vol.addWidget(slider_vol, 8)
            layout.addLayout(linha_vol)

            # Linha: Som do video
            linha_som = QHBoxLayout()
            linha_som.setContentsMargins(0, 0, 0, 0)
            linha_som.setSpacing(8)
            linha_som.addWidget(QLabel('Som do vídeo'), 2)
            slider_som = QSlider(Qt.Horizontal)
            slider_som.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            linha_som.addWidget(slider_som, 8)
            layout.addLayout(linha_som)

            # Linha: Carregar audio (sem criar linha extra acidental)
            linha_carregar = QHBoxLayout()
            linha_carregar.setContentsMargins(0, 0, 0, 0)
            linha_carregar.setSpacing(8)
            btn_carregar = QPushButton('Carregar áudio')
            btn_carregar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            campo_nome = QLineEdit()
            campo_nome.setPlaceholderText('Nome do áudio / caminho')
            linha_carregar.addWidget(btn_carregar)
            linha_carregar.addWidget(campo_nome, 1)
            layout.addLayout(linha_carregar)

            self.layoutBotoesFerramenta.addLayout(layout)
        
        elif self.ferramentaUtilizada == 'Edicoes Realizadas':
            latyoutListaEdicaoRealizada = QVBoxLayout()
            titulo = QLabel('Edições Realizadas')
            titulo.setStyleSheet("font-weight: 600;")
            latyoutListaEdicaoRealizada.addWidget(titulo)
            latyoutListaEdicaoRealizada.addWidget(self.listaEdicaoRealiza)
            latyoutListaEdicaoRealizada.setContentsMargins(0, 0, 0, 0)
            latyoutListaEdicaoRealizada.setSpacing(8)

            self.layoutBotoesFerramenta.addLayout(latyoutListaEdicaoRealizada)

    def limparLayout(self, layout):
        # Remove todos os widgets e sublayouts recursivamente.
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                self.limparLayout(item.layout())

# Aplicação/Remoção edição
    def aplicarEdicao(self, func, nome, **kwargs):
        """Empilha a edição (func) e reprocesa a partir do original."""
        if not self.caminhoVideoEditor:
            # Evita erro se usuário clicar antes de carregar vídeo
            return

        self.edicoesAplicadas.append((func, nome, kwargs))
        # Mostra no QListWidget
        rotulo = nome if not kwargs else f"{nome} {kwargs}"
        self.listaEdicaoRealiza.addItem(rotulo)
        self.reprocessarVideo()
    
    def reprocessarVideo(self):
        """Recria o preview do zero aplicando as edições na ordem."""
        if not self.caminhoVideoEditor:
            return

        # Abre clip do original a cada reprocessamento (evita locks e side-effects)
        clip = VideoFileClip(self.caminhoVideoEditor)
        try:
            for func, _, params in self.edicoesAplicadas:
                clip = func(clip, **params)

            # Exporta preview
            temp_path = self.temp_preview_path
            # Fecha player antes de reabrir a mesma URL no Windows (evita lock)
            # (opcional) self.playerEditor.stop()

            clip.write_videofile(
                temp_path,
                codec="libx264",
                audio_codec="aac",
                verbose=False,
                logger=None
            )

            # Recarrega preview no player
            self.playerEditor.setSource(QUrl.fromLocalFile(temp_path))
            self.playerEditor.play()

        finally:
            # Fecha o último objeto (importante no Windows)
            try:
                clip.close()
            except Exception:
                pass

    def removerEdicao(self, indice):
        # Remove edição da lista e reprocessa vídeo.
        if 0 <= indice < len(self.edicoesAplicadas):
            self.edicoesAplicadas.pop(indice)
            self.listaEdicaoRealiza.takeItem(indice)
            self.reprocessarVideo()

    def registrarEdicao(self, nome, **kwargs):
        # Adiciona ao QListWidget
        self.listaEdicaoRealiza.addItem(f"{nome} - {kwargs}")
        
        # (Opcional) Se quiser manter um histórico em lista Python também:
        if not hasattr(self, "historicoEdicoes"):
            self.historicoEdicoes = []
        self.historicoEdicoes.append((nome, kwargs))

        # Chama aplicação dos efeitos
        self.aplicarEdicoes()

    def aplicarEdicoes(self):
        # Aqui você aplica os efeitos no vídeo com base nas edições registradas.
        if hasattr(self, "historicoEdicoes"):
            for nome, params in self.historicoEdicoes:
                print(f"Aplicando efeito {nome} com parâmetros {params}")
                # Aqui entraria a lógica real de aplicar o efeito no vídeo

    def limparEdicoes(self):
        # Remove todas as edições
        self.listaEdicaoRealiza.clear()
        if hasattr(self, "historicoEdicoes"):
            self.historicoEdicoes.clear()
        self.aplicarEdicoes()
    
    def removerEdicaoUI(self, item):
        indice = self.listaEdicaoRealiza.row(item)
        self.removerEdicao(indice)

    def salvarVideoEditado(self):
        pastaEditados = "pastaEditados"
        if not os.path.exists(pastaEditados):
            os.mkdir(pastaEditados)

        nome_arquivo = os.path.splitext(os.path.basename(self.caminhoVideoEditor))[0] + "_editado.mp4"
        caminho_saida = os.path.join(pastaEditados, nome_arquivo)

        self.videoEditado.write_videofile(caminho_saida, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        self.caixaBotaoEditados.lista.addItem(nome_arquivo)
        if not hasattr(self, "caminhosEditados"):
            self.caminhosEditados = []
        self.caminhosEditados.append(caminho_saida)

        print(f"Vídeo salvo em: {caminho_saida}")

# EFEITOS
    def girarVideo(self, graus):
        if graus < 0:
            graus += 360
        elif graus >= 360:
            graus -= 360

        self.spinGraus.setValue(graus)
        self.aplicarEdicao(lambda clip, g=graus: clip.rotate(g), f"Girar {graus}°")

    def espelharVideo(self, clip=None):
        self.aplicarEdicao(lambda clip: clip.fx(vfx.mirror_x), "Espelhar")

    def velocidadeVideo(self, clip=None, factor=1.5):
        # Ex.: fator fixo; se quiser, peça via QInputDialog.getDouble(...)
        fator = 1.5
        self.aplicarEdicao(lambda clip, f: clip.fx(vfx.speedx, f), f"Velocidade {fator}x", f=fator)

    def mesclarVideo(self):
        ...



class TelaSalvar(QWidget):
    def __init__(self, telaCarregada, stack):
        super().__init__()
        self.instanciaTelaCarregar = telaCarregada
        self.stack = stack

        layoutPrincipalSalvar = QHBoxLayout()

        self.layoutColunaSalvar = QVBoxLayout()

        self.playerSalvar = QMediaPlayer(self)
        self.audioSalvar = QAudioOutput()
        self.playerSalvar.setAudioOutput(self.audioSalvar)

        self.videoWidgetSalvar = VideoWidgetInterativo(self)
        self.playerSalvar.setVideoOutput(self.videoWidgetSalvar)

        self.sliderSalvar = ConfigSlider(Qt.Horizontal)
        self.sliderSalvar.setStyleSheet("""
            QSlider::groove:horizontal { height: 8px; background: #ccc; }
            QSlider::handle:horizontal { width: 16px; background: #444; border-radius: 8px; }
            QSlider::sub-page:horizontal { background: #0080ff; }
        """)
        self.sliderSalvar.setMouseTracking(True)
        self.sliderSalvar.setMinimum(0)
        self.sliderSalvar.setMaximum(int(self.playerSalvar.duration()))

        self.temporizadorSalvar = QLabel("00:00:00 / 00:00:00")
        self.layoutTempoSalvar = QHBoxLayout()
        self.layoutTempoSalvar.addWidget(self.temporizadorSalvar)
        self.layoutTempoSalvar.addWidget(self.sliderSalvar)

        linhaBotoes = QHBoxLayout()
        for botao in ['Recortar', 'Editar', 'Salvar']:
            botaoPaginaSalvar = QPushButton(botao)
            linhaBotoes.addWidget(botaoPaginaSalvar)

            if botao == 'Recortar':
                botaoPaginaSalvar.clicked.connect(self.trocarTelaRecortar)
            elif botao == 'Editar':
                botaoPaginaSalvar.clicked.connect(self.trocarTelaEditar)
            else:
                ...

        self.layoutColunaSalvar.addWidget(self.videoWidgetSalvar)
        self.layoutColunaSalvar.addLayout(self.layoutTempoSalvar)
        self.layoutColunaSalvar.addLayout(linhaBotoes)

        opcoes_texto = [
            self.instanciaTelaCarregar.listaVideosRecortados.item(i).text() for i in range(
                self.instanciaTelaCarregar.listaVideosRecortados.count()
                )
        ]

        layoutSelecaoVideosEditar = QVBoxLayout()
        self.caixaBotaoRecortes = CaixaLista('Vídeos recortados', opcoes_texto)
        self.caixaBotaoEditados = CaixaLista('Vídeos editados', opcoes_texto)
        layoutSelecaoVideosEditar.addWidget(self.caixaBotaoRecortes)
        layoutSelecaoVideosEditar.addWidget(self.caixaBotaoEditados)
        layoutSelecaoVideosEditar.addStretch()

        layoutPrincipalSalvar.addLayout(self.layoutColunaSalvar, 8)
        layoutPrincipalSalvar.addLayout(layoutSelecaoVideosEditar, 2)
        self.setLayout(layoutPrincipalSalvar)

    def trocarTelaRecortar(self):
        self.stack.setCurrentIndex(0)

    def trocarTelaEditar(self):
        self.stack.setCurrentIndex(1)


class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Editor de Video')
        self.setFixedSize(1200,650)

        self.stack = QStackedWidget()

        self.carregar = TelaRecortar(self.stack)
        self.edicao = TelaEditar(self.carregar, self.stack)
        self.salvar = TelaSalvar(self.carregar, self.stack)

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
