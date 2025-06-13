import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFormLayout, QStackedLayout
)
from PySide6.QtCore import Qt

def enviar_dados():
    nome = campoNome.text()
    idade = campoIdade.text()
    profissao = campoProfissao.text()
    
    QMessageBox.information(janela, "Dados enviados", f"Nome     : {nome}\nIdade     : {idade}\nProfissao: {profissao}")

def verificacao():
    usuario = campoUsuario.text().strip()
    senha = campoSenha.text().strip()
    validarUsuario = False
    validarSenha = False

    if usuario in usuarios:
        validarUsuario = True
    else:
        QMessageBox.warning(janela, "Atenção", "Usuario inexistente!")
    
    if senha == '1234':
        validarSenha = True
    else:
        QMessageBox.warning(janela, "Atenção", "Senha incorreta!")

    if validarUsuario == True and validarSenha == True:
        stack_layout.setCurrentIndex(1)

def alternar_tema():
    global tema_escuro
    tema_escuro = not tema_escuro
    if tema_escuro:
        app.setStyleSheet(ESTILO_ESCURO)
        botaoTema.setText("☀️ Modo Claro")
    else:
        app.setStyleSheet(ESTILO_CLARO)
        botaoTema.setText("🌙 Modo Escuro")

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

app = QApplication(sys.argv)

janela = QWidget()
janela.setWindowTitle("Janela de teste")
janela.resize(400, 250)

tema_escuro = False

# ===== Tela Login =====
telaLogin = QWidget()
layoutLogin = QVBoxLayout()

formLogin = QFormLayout()
campoUsuario = QLineEdit()
campoSenha = QLineEdit()
campoSenha.setEchoMode(QLineEdit.Password)
formLogin.addRow("Usuário:", campoUsuario)
formLogin.addRow("Senha:", campoSenha)

botaoEntrar = QPushButton("Entrar")

layoutLogin.addLayout(formLogin)
layoutLogin.addWidget(botaoEntrar)

telaLogin.setLayout(layoutLogin)

# ===== Tela Principal =====
telaPrincipal = QWidget()
layoutPrincipal = QHBoxLayout()

layoutColEsquerda = QVBoxLayout()
botao1 = QPushButton('Opção 1')
botao2 = QPushButton('Opção 2')
botao3 = QPushButton('Opção 3')
botaoTema = QPushButton("🌙 Modo Escuro")
botaoLogin = QPushButton('Voltar Login')
layoutColEsquerda.addWidget(botao1)
layoutColEsquerda.addWidget(botao2)
layoutColEsquerda.addWidget(botao3)
layoutColEsquerda.addWidget(botaoTema)
layoutColEsquerda.addWidget(botaoLogin)

botaoTema.clicked.connect(alternar_tema)

layoutPrincipal.addLayout(layoutColEsquerda)

titulo = QLabel('Preencha as seguintes informações')
titulo.setAlignment(Qt.AlignCenter)
layoutColDireita = QVBoxLayout()
layoutColDireita.addWidget(titulo)

formulario = QFormLayout()
campoNome = QLineEdit()
campoIdade = QLineEdit()
campoProfissao = QLineEdit()

formulario.addRow('Nome     :', campoNome)
formulario.addRow('Idade    :', campoIdade)
formulario.addRow('Profissao:', campoProfissao)
layoutColDireita.addLayout(formulario)

botaoEnviar = QPushButton('Enviar')
layoutColDireita.addWidget(botaoEnviar)

layoutPrincipal.addLayout(layoutColDireita)

botaoEnviar.clicked.connect(enviar_dados)
formulario.addRow(botaoEnviar)

telaPrincipal.setLayout(layoutPrincipal)


# ===== Troca de Tela =====
stack_layout = QStackedLayout() 
stack_layout.addWidget(telaLogin)
stack_layout.addWidget(telaPrincipal)

botaoEntrar.clicked.connect(verificacao)
botaoLogin.clicked.connect(lambda: stack_layout.setCurrentIndex(0))

janela.setLayout(stack_layout)

app.setStyleSheet(ESTILO_CLARO) 

janela.show()

app.exec()
