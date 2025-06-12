import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFormLayout, QStackedLayout
)

# Definir a ação do botão
def ao_clicar():
    QMessageBox.information(janela, "Ação", "Você clicou no botão!") 
    # informar em qual janela será exibido, titulo da mensagem, texto da mensagem

# Função ao clicar no botão
def enviar_dados():
    nome = campo_nome.text()
    idade = campo_idade.text()
    
    # Mostra os dados com uma mensagem
    QMessageBox.information(janela, "Dados enviados", f"Nome: {nome}\nEmail: {idade}")

# Funções para alternar entre as telas
def mostrar_tela_cadastro():
    stack_layout.setCurrentIndex(1) # .setCurrentIndex = Troca para a tela de índice

def mostrar_tela_login():
    stack_layout.setCurrentIndex(0) # .setCurrentIndex = Troca para a tela de índice


# Cria a aplicação
# hospeda toda a aplicação do programa
app = QApplication(sys.argv)

janela = QWidget() # Cria uma janela simples
# QWidget é a base visual de todo o projeto
janela.setWindowTitle("Janela de teste")
janela.resize(300, 300)  # Largura x Altura

# ===== Tela de Login =====
tela_login = QWidget()
layout_login = QVBoxLayout()

form_login = QFormLayout()
campo_usuario = QLineEdit()
campo_senha = QLineEdit()
campo_senha.setEchoMode(QLineEdit.Password)
form_login.addRow("Usuário:", campo_usuario)
form_login.addRow("Senha:", campo_senha)

botao_entrar = QPushButton("Entrar")

layout_login.addLayout(form_login)
layout_login.addWidget(botao_entrar)

tela_login.setLayout(layout_login)


# ===== Tela de Cadastro =====

# Criar o layout vertical e adicionar os botões
# Layout vertical principal
tela_cadastro = QWidget()
layout_cadastro = QVBoxLayout() # cria um campo onde possibilita o desenvolvimento visual do aplicativo

# Adiciona um título dentro do layout
titulo = QLabel("Escolha uma opção:")
layout_cadastro.addWidget(titulo)

# Layout horizontal com dois botões
layout_botoes = QHBoxLayout()
botao1 = QPushButton('Opção 1') # QPushButton cria o botão
botao2 = QPushButton('Opção 2')
# botao1 = QPushButton('Inicio', parent=janela) # parent=janela permite que o botão seja criada dentro da janela
# botao2 = QPushButton('Meio', parent=janela)
# botao1.move(5,5) # Posição X e Y do botão dentro da janela / substituido por layout.addWidget(botao1)
# botao2.move(5,40) # Posição X e Y do botão dentro da janela / substituido por layout.addWidget(botao2)
layout_botoes.addWidget(botao1) # adiciona um novo componente visual dentro do espaço estabelecido do layout
layout_botoes.addWidget(botao2)

# Adiciona o layout horizontal dentro do vertical
layout_cadastro.addLayout(layout_botoes)

# Campos de entrada
# Layout de formulário
formulario = QFormLayout()

campo_nome = QLineEdit()
campo_idade = QLineEdit()
campo_senha = QLineEdit()
campo_senha.setEchoMode(QLineEdit.Password) #.setEchoMode = Oculta senha no campo de texto

formulario.addRow("Nome:", campo_nome)
formulario.addRow("Idade:", campo_idade)
formulario.addRow("Senha:", campo_senha)

botao_voltar_login = QPushButton("Voltar para Login")

# Botão final centralizado
layout_cadastro.addLayout(formulario)

botao_enviar = QPushButton("Enviar")
layout_cadastro.addWidget(botao_enviar)

layout_cadastro.addWidget(botao_voltar_login)

botao1.clicked.connect(ao_clicar)  # Conectar o clique à função
botao2.clicked.connect(ao_clicar)  # Conectar o clique à função
botao_enviar.clicked.connect(enviar_dados)

# Adiciona o botão ao final do formulário
formulario.addRow(botao_enviar)

# Aplicar o layout à janela/aplicativo
tela_cadastro.setLayout(layout_cadastro)

# ===== Layout que troca telas =====
stack_layout = QStackedLayout() # Empilha várias telas/layouts e mostra só uma
stack_layout.addWidget(tela_login)     # índice 0
stack_layout.addWidget(tela_cadastro)  # índice 1

botao_entrar.clicked.connect(mostrar_tela_cadastro)
botao_voltar_login.clicked.connect(mostrar_tela_login)

janela.setLayout(stack_layout)
janela.show()  # Exibe a janela
# Executa o loop da aplicação
app.exec()
