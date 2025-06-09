import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel
)

# Definir a ação do botão
def ao_clicar():
    QMessageBox.information(janela, "Ação", "Você clicou no botão!") 
    # informar em qual janela será exibido, titulo da mensagem, texto da mensagem

# Cria a aplicação
# hospeda toda a aplicação do programa
app = QApplication(sys.argv)

janela = QWidget() # Cria uma janela simples
# QWidget é a base visual de todo o projeto
janela.setWindowTitle("Janela de teste")
janela.resize(300, 200)  # Largura x Altura

# Criar o layout vertical e adicionar os botões
# Layout vertical principal
layout_principal = QVBoxLayout() # cria um campo onde possibilita o desenvolvimento visual do aplicativo

# Adiciona um título dentro do layout
titulo = QLabel("Escolha uma opção:")
layout_principal.addWidget(titulo)

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
layout_principal.addLayout(layout_botoes)

# Botão final centralizado
botao_final = QPushButton("Confirmar")
layout_principal.addWidget(botao_final)

# Aplicar o layout à janela/aplicativo
janela.setLayout(layout_principal)

botao1.clicked.connect(ao_clicar)  # Conectar o clique à função
botao2.clicked.connect(ao_clicar)  # Conectar o clique à função

janela.show()  # Exibe a janela
# Executa o loop da aplicação
app.exec()
