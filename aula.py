import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

# Cria a aplicação
# hospeda toda a aplicação do programa
app = QApplication(sys.argv)

janela = QWidget() # Cria uma janela simples
# QWidget é a base visual de todo o projeto
janela.setWindowTitle("Minha Primeira Janela")
janela.resize(300, 200)  # Largura x Altura



janela.show()  # Exibe a janela
# Executa o loop da aplicação
app.exec()