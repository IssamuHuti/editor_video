import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFormLayout, QStackedLayout
)
from PySide6.QtCore import Qt

class JanelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janela de Login")
        self.resize(400, 250)

        layoutPrincipal = QHBoxLayout()

        layoutColEsquerda = QVBoxLayout()
        botao1 = QPushButton('Opção 1')
        botao2 = QPushButton('Opção 2')
        botao3 = QPushButton('Opção 3')
        self.botaoTema = QPushButton("🌙 Modo Escuro")
        botaoLogin = QPushButton('Voltar Login')
        layoutColEsquerda.addWidget(botao1)
        layoutColEsquerda.addWidget(botao2)
        layoutColEsquerda.addWidget(botao3)
        layoutColEsquerda.addWidget(self.botaoTema)
        layoutColEsquerda.addWidget(botaoLogin)

        self.botaoTema.clicked.connect(self.alternar_tema)
        botaoLogin.clicked.connect(lambda: stack_layout.setCurrentIndex(0))

        layoutPrincipal.addLayout(layoutColEsquerda)

        titulo = QLabel('Preencha as seguintes informações')
        titulo.setAlignment(Qt.AlignCenter)
        layoutColDireita = QVBoxLayout()
        layoutColDireita.addWidget(titulo)

        formulario = QFormLayout()
        self.campoNome = QLineEdit()
        self.campoIdade = QLineEdit()
        self.campoProfissao = QLineEdit()

        formulario.addRow('Nome     :', self.campoNome)
        formulario.addRow('Idade    :', self.campoIdade)
        formulario.addRow('Profissao:', self.campoProfissao)
        layoutColDireita.addLayout(formulario)

        botaoEnviar = QPushButton('Enviar')
        botaoEnviar.clicked.connect(self.enviar_dados)
        layoutColDireita.addWidget(botaoEnviar)

        layoutPrincipal.addLayout(layoutColDireita)
        self.setLayout(layoutPrincipal)

    def enviar_dados(self):
        nome = self.campoNome.text()
        idade = self.campoIdade.text()
        profissao = self.campoProfissao.text()
        
        QMessageBox.information(self, "Dados enviados", f"Nome     : {nome}\nIdade     : {idade}\nProfissao: {profissao}")

    def alternar_tema(self):
        global tema_escuro
        tema_escuro = not tema_escuro
        if tema_escuro:
            app.setStyleSheet(ESTILO_ESCURO)
            self.botaoTema.setText("☀️ Modo Claro")
        else:
            app.setStyleSheet(ESTILO_CLARO)
            self.botaoTema.setText("🌙 Modo Escuro")


class JanelaLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janela de Login")
        self.resize(400, 250)

        layout = QVBoxLayout()
        formLogin = QFormLayout()

        self.campoUsuario = QLineEdit()
        self.campoSenha = QLineEdit()
        self.campoSenha.setEchoMode(QLineEdit.Password)
        formLogin.addRow("Usuário:", self.campoUsuario)
        formLogin.addRow("Senha:", self.campoSenha)

        self.botaoEntrar = QPushButton("Entrar")
        self.botaoEntrar.clicked.connect(self.verificacao)

        layout.addLayout(formLogin)
        layout.addWidget(self.botaoEntrar)

        self.setLayout(layout)

    def verificacao(self):
        usuario = self.campoUsuario.text().strip()
        senha = self.campoSenha.text().strip()

        if usuario not in usuarios:
            QMessageBox.warning(self, "Atenção", "Usuario inexistente!")
            return
        
        if senha != '1234':
            QMessageBox.warning(self, "Atenção", "Senha incorreta!")
            return

        stack_layout.setCurrentIndex(1)


class JanelaBoasVindas(QWidget):
    def __init__(self, nome):
        super().__init__()
        self.setWindowTitle("Boas-vindas")
        self.resize(250, 100)

        layoutBoasVindas = QVBoxLayout()
        mensagem = QLabel(f"Olá, {nome}! Bem-vindo ao aplicativo.")
        layoutBoasVindas.addWidget(mensagem)

        self.setLayout(layoutBoasVindas)


ESTILO_CLARO = """
    QWidget {
        background-color: #ffffff;
        color: #000000;
    }
    QPushButton {
        background-color: #e0e0e0;
        border: none;
        padding: 6px;
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
        border: none;
        padding: 6px;
    }
"""

usuarios = ['lucas', 'joao', 'carlos']
tema_escuro = False

app = QApplication(sys.argv)
app.setStyleSheet(ESTILO_CLARO)

# ===== Troca de Tela =====
stack_layout = QStackedLayout() 
loginWidget = JanelaLogin()
principalWidget = JanelaPrincipal()

stack_layout.addWidget(loginWidget)
stack_layout.addWidget(principalWidget)

stacked_widget = QWidget()
stacked_widget.setLayout(stack_layout)

stacked_widget.show()

app.exec()
