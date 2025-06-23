import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QFormLayout, QStackedLayout
)
from PySide6.QtCore import Qt

class JanelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janela de Login")
        self.resize(800, 500)

        layoutPrincipal = QHBoxLayout()

        layoutEsquerdo, self.botaoTema = LayoutPreDefinido.layoutEsquerdo(stackLayout, LayoutPreDefinido.alternarTema)
        layoutPrincipal.addLayout(layoutEsquerdo)

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


class LayoutPreDefinido():
    @staticmethod # torna o método abaixo um método utilizavel mesmo sem informar self instânciando com o objeto informado na classe
    def layoutEsquerdo(stackLayout, alternarTema):
        layoutColEsquerda = QVBoxLayout()
        botaoHome = QPushButton('Home')
        botao2 = QPushButton('Opção 2')
        botao3 = QPushButton('Opção 3')
        botaoTema = QPushButton("🌙 Modo Escuro")
        botaoLogin = QPushButton('Voltar Login')
        layoutColEsquerda.addWidget(botaoHome)
        layoutColEsquerda.addWidget(botaoTema)
        layoutColEsquerda.addWidget(botao2)
        layoutColEsquerda.addWidget(botao3)
        layoutColEsquerda.addWidget(botaoLogin)

        botaoTema.clicked.connect(alternarTema)
        botaoLogin.clicked.connect(lambda: stackLayout.setCurrentIndex(0))
        botaoHome.clicked.connect(lambda: stackLayout.setCurrentIndex(1))
        botao2.clicked.connect(lambda: stackLayout.setCurrentIndex(2))
        botao3.clicked.connect(lambda: stackLayout.setCurrentIndex(3))

        return layoutColEsquerda, botaoTema
    
    def alternarTema(self):
        global temaEscuro
        temaEscuro = not temaEscuro
        if temaEscuro:
            app.setStyleSheet(ESTILO_ESCURO)
            self.botaoTema.setText("☀️ Modo Claro")
        else:
            app.setStyleSheet(ESTILO_CLARO)
            self.botaoTema.setText("🌙 Modo Escuro")

class JanelaLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janela de Login")
        self.resize(800, 500)

        layoutLogin = QVBoxLayout()
        formLogin = QFormLayout()

        self.campoUsuario = QLineEdit()
        self.campoSenha = QLineEdit()
        self.campoSenha.setEchoMode(QLineEdit.Password)
        formLogin.addRow("Usuário:", self.campoUsuario)
        formLogin.addRow("Senha:", self.campoSenha)

        self.botaoEntrar = QPushButton("Entrar")
        self.botaoEntrar.clicked.connect(self.verificacao) # self.verificacao está puxando o nome da classe como referencia 'self' e 'verificacao' está indicando o método dentro da classe

        layoutLogin.addLayout(formLogin)
        layoutLogin.addWidget(self.botaoEntrar)

        self.setLayout(layoutLogin)

    def verificacao(self):
        usuario = self.campoUsuario.text().strip()
        senha = self.campoSenha.text().strip()

        if usuario not in usuarios:
            QMessageBox.warning(self, "Atenção", "Usuario inexistente!")
            return
        
        if senha != '1234':
            QMessageBox.warning(self, "Atenção", "Senha incorreta!")
            return

        stackLayout.setCurrentIndex(1)
        boas_vindas = JanelaBoasVindas(usuario)
        boas_vindas.show()
        self.close()


class JanelaBoasVindas(QWidget):
    def __init__(self, nome):
        super().__init__()
        self.setWindowTitle("Boas-vindas")
        self.resize(400, 100)

        layoutBoasVindas = QVBoxLayout()
        mensagem = QLabel(f"Olá, {nome}! Bem-vindo ao aplicativo.")
        layoutBoasVindas.addWidget(mensagem)

        self.setLayout(layoutBoasVindas)
        

class JanelaOpcao2(QWidget):
    def __init__(self, stackLayout):
        super().__init__()
        self.setWindowTitle("Janela de Login")
        self.resize(800, 500)

        layoutBase2 = QHBoxLayout()
        
        layoutEsquerdo, self.botaoTema = LayoutPreDefinido.layoutEsquerdo(stackLayout, LayoutPreDefinido.alternarTema)
        layoutBase2.addLayout(layoutEsquerdo)

        layoutDireita = QVBoxLayout()
        informacao2 = QLabel('Janela 2')
        layoutDireita.addWidget(informacao2)
        layoutBase2.addLayout(layoutDireita)

        self.setLayout(layoutBase2)
        

class JanelaOpcao3(QWidget):
    def __init__(self, stackLayout):
        super().__init__()
        self.setWindowTitle("Janela de Login")
        self.resize(800, 500)

        layoutBase3 = QHBoxLayout()
        
        layoutEsquerdo, self.botaoTema = LayoutPreDefinido.layoutEsquerdo(stackLayout, LayoutPreDefinido.alternarTema)
        layoutBase3.addLayout(layoutEsquerdo)

        layoutDireita = QVBoxLayout()
        informacao3 = QLabel('Janela 3')
        layoutDireita.addWidget(informacao3)
        layoutBase3.addLayout(layoutDireita)

        self.setLayout(layoutBase3)


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
temaEscuro = False

app = QApplication(sys.argv)
app.setStyleSheet(ESTILO_CLARO)

# ===== Troca de Tela =====
stackLayout = QStackedLayout() 
loginWidget = JanelaLogin()
principalWidget = JanelaPrincipal()
opcao2Widget = JanelaOpcao2(stackLayout)
opcao3Widget = JanelaOpcao3(stackLayout)

stackLayout.addWidget(loginWidget)
stackLayout.addWidget(principalWidget)
stackLayout.addWidget(opcao2Widget)
stackLayout.addWidget(opcao3Widget)

stacked_widget = QWidget()
stacked_widget.setLayout(stackLayout)

stacked_widget.show()

app.exec()
