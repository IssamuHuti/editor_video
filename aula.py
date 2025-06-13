import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFormLayout, QStackedLayout
)
from PySide6.QtCore import Qt # importa um modelo parecido com CSS do HTML

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

# Função para alternar o tema
def alternar_tema():
    global tema_escuro # Permite alterar a variável tema_escuro dentro da função
    tema_escuro = not tema_escuro
    if tema_escuro:
        app.setStyleSheet(ESTILO_ESCURO)
        botao_tema.setText("☀️ Modo Claro")
    else:
        app.setStyleSheet(ESTILO_CLARO)
        botao_tema.setText("🌙 Modo Escuro")


# Estilos em QSS (como CSS)
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


# Cria a aplicação
# hospeda toda a aplicação do programa
app = QApplication(sys.argv)

janela = QWidget() # Cria uma janela simples
# QWidget é a base visual de todo o projeto
janela.setWindowTitle("Janela de teste")
janela.resize(300, 300)  # Largura x Altura

tema_escuro = False  # Começa no modo claro

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
titulo.setAlignment(Qt.AlignCenter)
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

botao_tema = QPushButton("🌙 Modo Escuro")
botao_tema.clicked.connect(alternar_tema)
layout_botoes.addWidget(botao_tema)

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
stack_layout = QStackedLayout() # cria o layout que vai conter várias telas (widgets)
stack_layout.addWidget(tela_login) # adiciona o QWidget informado na variável 'tela_login' # indice (0)
stack_layout.addWidget(tela_cadastro) # adiciona o QWidget informado na variável 'tela_cadastro' # indice (1)
# Cada tela (geralmente um QWidget) é adicionada como uma “aba oculta”.
# como o widget 'telaLogin' está indicado no indice (0), assim que o aplicativo for inicializado, vai abrir essa widget

botao_entrar.clicked.connect(mostrar_tela_cadastro) # altera a indice de acordo com o indice informado na função
botao_voltar_login.clicked.connect(mostrar_tela_login) # altera a indice de acordo com o indice informado na função

janela.setLayout(stack_layout) # seleciona a variável que está contendo as demais widgets

# Aplica estilo inicial (claro)
app.setStyleSheet(ESTILO_CLARO) # Aplica uma aparência personalizada globalmente

janela.show()  # Exibe a janela
# Executa o loop da aplicação
app.exec()
