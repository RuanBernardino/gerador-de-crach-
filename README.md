# Gerador de Carteirinhas com Firebase

Este é um aplicativo de desktop em Python para gerar carteirinhas de alunos, utilizando a biblioteca `CustomTkinter` para a interface gráfica, além de armazenar as informações dos alunos no **Firebase Firestore**.

## Funcionalidades

- Interface gráfica intuitiva usando `CustomTkinter`.
- Geração de carteirinhas com foto, nome, sobrenome, R.A e série.
- Armazenamento das informações dos alunos no Firebase Firestore.
- Pré-visualização da carteirinha gerada antes de salvar.
- Busca de alunos pelo R.A com carregamento automático das informações.

## Requisitos

- Python 3.7 ou superior
- Conta no Firebase com Firestore ativado
- Credenciais do Firebase (arquivo JSON)

### Bibliotecas necessárias

As bibliotecas necessárias podem ser instaladas usando o comando abaixo:

```bash
pip install customtkinter tkinter Pillow firebase-admin
