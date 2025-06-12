import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFormLayout, QStackedLayout
)

def enviar_dados():
    nome = campo_nome.text()
    idade = campo_idade.text()
    profissao = campo_profissao.text()
    
    QMessageBox.information(janela, "Dados enviados", f"Nome     : {nome}\nIdade     : {idade}\nProfissao: {profissao}")

def mostrarTelaPrincipal():
    stack_layout.setCurrentIndex(1) # seleciona o widget informado no indice selecionado

def mostrarTelaLogin():
    stack_layout.setCurrentIndex(0) # seleciona o widget informado no indice selecionado

app = QApplication(sys.argv)

janela = QWidget()
janela.setWindowTitle("Janela de teste")
janela.resize(400, 250)

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
botaoLogin = QPushButton('Voltar Login')
layoutColEsquerda.addWidget(botao1)
layoutColEsquerda.addWidget(botao2)
layoutColEsquerda.addWidget(botao3)
layoutColEsquerda.addWidget(botaoLogin)

layoutPrincipal.addLayout(layoutColEsquerda)


layoutColDireita = QVBoxLayout()
titulo = QLabel('Preencha as seguintes informações')
layoutColDireita.addWidget(titulo)

formulario = QFormLayout()
campo_nome = QLineEdit()
campo_idade = QLineEdit()
campo_profissao = QLineEdit()

formulario.addRow('Nome     :', campo_nome)
formulario.addRow('Idade    :', campo_idade)
formulario.addRow('Profissao:', campo_profissao)
layoutColDireita.addLayout(formulario)

botaoEnviar = QPushButton('Enviar')
layoutColDireita.addWidget(botaoEnviar)

layoutPrincipal.addLayout(layoutColDireita)

botaoEnviar.clicked.connect(enviar_dados)
formulario.addRow(botaoEnviar)

telaPrincipal.setLayout(layoutPrincipal)


# ===== Troca de Tela =====
stack_layout = QStackedLayout() # cria o layout que vai conter várias telas (widgets)
stack_layout.addWidget(telaLogin) # adiciona o QWidget informado na variável 'telaLogin' # indice (0)
stack_layout.addWidget(telaPrincipal) # adiciona o QWidget informado na variável 'telaPrincipal' # indice (1)
# Cada tela (geralmente um QWidget) é adicionada como uma “aba oculta”.
# como o widget 'telaLogin' está indicado no indice (0), assim que o aplicativo for inicializado, vai abrir essa widget

botaoEntrar.clicked.connect(mostrarTelaPrincipal) # altera a indice de acordo com o indice informado na função
botaoLogin.clicked.connect(mostrarTelaLogin) # altera a indice de acordo com o indice informado na função

janela.setLayout(stack_layout) # seleciona a variável que está contendo as demais widgets
janela.show()

app.exec()
