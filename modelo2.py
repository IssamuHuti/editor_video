import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QComboBox, QFileDialog,
    QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QMessageBox
)
from PySide6.QtCore import Qt


class TelaCarregarRecortar(QWidget):
    def __init__(self):
        super().__init__()
        layoutPrincipalCarregarRecortar = QVBoxLayout()

        layoutCarregarRecortar = QHBoxLayout()

        layoutCarregarVideo = QVBoxLayout()



        layoutCarregarVideo.addWidget(QLabel('Carregue o vídeo')) # aparece antes de carregar o video, desaparece depois de carregar
        layoutCarregarVideo.setAlignment(Qt.AlignCenter)
        layoutCarregarVideo.addStretch()

        layoutBotoes = QHBoxLayout()
        botaoRecortar = QPushButton('Recortar')
        botaoEditar = QPushButton('Editar')
        botaoSalvar = QPushButton('Salvar')

        layoutBotoes.addWidget(botaoRecortar)
        layoutBotoes.addWidget(botaoEditar)
        layoutBotoes.addWidget(botaoSalvar)

        layoutCarregarVideo.addLayout(layoutBotoes)

        layoutVideosRecortados = QVBoxLayout()



        layoutCarregarRecortar.addLayout(layoutCarregarVideo)
        layoutCarregarRecortar.addLayout(layoutVideosRecortados)

        layoutPrincipalCarregarRecortar.addLayout(layoutCarregarRecortar)
        self.setLayout(layoutPrincipalCarregarRecortar)


class TelaEditar(QWidget):
    def __init__(self):
        super().__init__()
        layoutPrincipalEditar = QVBoxLayout()

        layoutEdicao = QHBoxLayout()

        layoutVideoEdicao = QVBoxLayout()



        layoutVideoEdicao.addWidget(QLabel('Edição'))
        layoutVideoEdicao.addWidget(QLabel('Escolha o vídeo')) # desaparece após escolher o vídeo
        layoutVideoEdicao.setAlignment(Qt.AlignCenter)

        layoutConfigEdicao = QVBoxLayout()



        layoutEdicao.addLayout(layoutVideoEdicao)
        layoutEdicao.addLayout(layoutConfigEdicao)

        layoutPrincipalEditar.addLayout(layoutEdicao)
        self.setLayout(layoutPrincipalEditar)


class TelaSalvar(QWidget):
    def __init__(self):
        super().__init__()
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

        

        layoutSalvar.addLayout(layoutVideoRecortado)
        layoutSalvar.addLayout(layoutSelecaoVideos)

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
        menuLateral.addWidget(botaoConfig)
        menuLateral.addStretch()
        menuLateral.addWidget(QLabel('Versão 1.0.0'))

        layoutPrincipal = QHBoxLayout()
        layoutPrincipal.addLayout(menuLateral)
        layoutPrincipal.addWidget(self.stack)

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
