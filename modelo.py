import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFormLayout
)

def enviar_dados():
    nome = campo_nome.text()
    idade = campo_idade.text()
    profissao = campo_profissao.text()
    
    QMessageBox.information(janela, "Dados enviados", f"Nome     : {nome}\nIdade     : {idade}\nProfissao: {profissao}")

app = QApplication(sys.argv)

janela = QWidget()
janela.setWindowTitle("Janela de teste")
janela.resize(400, 250)

layoutPrincipal = QHBoxLayout()

layoutColEsquerda = QVBoxLayout()
botao1 = QPushButton('Opção 1')
botao2 = QPushButton('Opção 2')
botao3 = QPushButton('Opção 3')
layoutColEsquerda.addWidget(botao1)
layoutColEsquerda.addWidget(botao2)
layoutColEsquerda.addWidget(botao3)

layoutPrincipal.addLayout(layoutColEsquerda)


layoutColDireita = QVBoxLayout()
titulo = QLabel('Preencha as seguintes informações')
layoutColDireita.addWidget(titulo)

campo_nome = QLineEdit()
campo_idade = QLineEdit()
campo_profissao = QLineEdit()

formulario = QFormLayout()
formulario.addRow('Nome     :', campo_nome)
formulario.addRow('Idade    :', campo_idade)
formulario.addRow('Profissao:', campo_profissao)
layoutColDireita.addLayout(formulario)

botao_enviar = QPushButton('Enviar')
layoutColDireita.addWidget(botao_enviar)

layoutPrincipal.addLayout(layoutColDireita)

botao_enviar.clicked.connect(enviar_dados)

janela.setLayout(layoutPrincipal)
janela.show()

app.exec()