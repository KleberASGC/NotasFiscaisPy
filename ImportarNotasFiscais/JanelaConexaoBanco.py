import PySimpleGUI as sg

class JanelaConexaoBanco:
    def __init__(self):
        layout = [
            [sg.Text('Host:', size=(25, 0)), sg.Input(key='host')],
            [sg.Text('Porta (Por padrão é 5432):',size=(25,0)),sg.Input(key='porta')],
            [sg.Text('Nome do Banco:',size=(25,0)), sg.Input(key='nomeBanco')],
            [sg.Text('Usuário:',size=(25,0)), sg.Input(key='usuario')],
            [sg.Text('Senha:',size=(25,0)), sg.Input(key='senha')],
            [sg.Button('Conectar ao Banco')]

        ]

        janela = sg.Window("Conectar ao Banco").layout(layout)

        self.button, self.values = janela.Read()



    def getCredenciais(self):
        return self.values

