
#Primeiramente é só um esboço.
def coletaDadosGerais(notaFiscal):
    pass
    numeroOrdem = 0
    dataMovimentacao = ""
    chaveNota = ""
    ecf = ""
    modeloDocumento = ""
    serieDocumento = ""
    numeroDocumento = ""
    codRemetDest = ""
    cfop = ""
    numeroSequencial = 0
    dadosGerais = {

        "numeroOrdem": numeroOrdem,
        "dataMovimentacao": dataMovimentacao,
        "chaveNota": chaveNota,
        "ecf": ecf,
        "modeloDocumento": modeloDocumento,
        "serieDocumento": serieDocumento,
        "numeroDocumento": numeroDocumento,
        "codRemetDest": codRemetDest,
        "cfop": cfop,
        "numeroSequencial": numeroSequencial

    }

    return dadosGerais

def coletaDadosEntrada(notaFiscal):
    quantidadeMercadoriaEntrada = 0
    valorTotalImposto = 0
    dadosEntrada = {

        "quantidadeMercadoriaEntrada": quantidadeMercadoriaEntrada,
        "valorTotalImposto": valorTotalImposto

    }
    return dadosEntrada

def coletaDadosSaida(notaFiscal):
    quantidadeMercadoriaSaida = 0
#Campo 14 (Depende do campo 23, e deve ser preenchido somente na saída.)
    #campo14 = campo23


    enquadramentoLegal = ""
    if(enquadramentoLegal == "1"):
        # campo15 = quantidadeMercadoriaSaida * campo14
        # campo16 = ""
        # campo17 = ""
        # campo18 = ""
        # campo19 = ""


    elif(enquadramentoLegal == "2"):
        # campo16 = quantidadeMercadoriaSaida * campo14
        # campo15 = ""
        # campo17 = ""
        # campo18 = ""
        # campo19 = ""

    elif(enquadramentoLegal == "3"):
        # campo17 = quantidadeMercadoriaSaida * campo14
        # campo15 = ""
        # campo16 = ""
        # campo18 = ""
        # campo19 = ""

    elif(enquadramentoLegal == "4"):
        # campo18 = quantidadeMercadoriaSaida * campo14
        # campo15 = ""
        # campo16 = ""
        # campo17 = ""
        # campo19 = ""

    elif(enquadramentoLegal == "0"):
        # campo19 = quantidadeMercadoriasSaida
        # campo15 = ""
        # campo16 = ""
        # campo17 = ""
        # campo18 = ""



