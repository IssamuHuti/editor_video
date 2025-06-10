import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFormLayout
)

def ao_clicar():
    QMessageBox.information(janela, "Ação", "Você clicou no botão!")

def enviar_dados():
    nome = campo_nome.text()
    idade = campo_idade.text()
    
    QMessageBox.information(janela, "Dados enviados", f"Nome: {nome}\nEmail: {idade}")

app = QApplication(sys.argv)

janela = QWidget()
janela.setWindowTitle("Janela de teste")
janela.resize(400, 250)

layoutPrincipal = QHBoxLayout()

layoutColEsquerda = QVBoxLayout()



layoutColDireita = QVBoxLayout()



janela.show()

app.exec()