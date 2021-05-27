from nfelib.v4_00 import leiauteNFe_sub as parser
from tkinter import filedialog, Tk
import psycopg2
from JanelaConexaoBanco import JanelaConexaoBanco as credenciaisBanco
import PySimpleGUI as sg

def conectaBanco(db_host,db_nome,db_usuario,db_senha,db_porta):
    try:
        conexao = psycopg2.connect(dbname=db_nome,user=db_usuario,password=db_senha,host=db_host,port=db_porta)

    except:
        sg.popup(f'Ocorreu um erro ao tentar conectar ao Banco de Dados.'
                 f' Verifique se os dados foram digitados corretamente.')
        exit(1)

    return conexao

def escolheArquivos():
    root = Tk()
    root.withdraw()
    caminho_arquivos = filedialog.askopenfilenames()

    return caminho_arquivos

def assinatura_sql(nomeTabela):

    if(nomeTabela == "invoices"):
        # assinatura = f"INSERT INTO {nomeTabela}(id,created_at,updated_at,number,model,serie,note_issue_date,note_entry_date,cfop," \
        #                      f"nfe_Key,cnpj_emit,cnpj_dest,amount,bc_icms_amount,icms_amount,bc_icms_st_amount,icms_st_amount," \
        #                      f"ecf_serial_number,document_type,ref_nfe,operation_nature,additional_data,arquivo_nfe)\n"

        assinatura = f"INSERT INTO {nomeTabela}(id,created_at,updated_at,number,model,serie,cfop," \
                     f"nfe_Key,invoice_at,operation_at,amount,bc_icms_amount,icms_amount,bc_icms_st_amount,icms_st_amount," \
                     f"ecf_serial_number,document_type,adapt,ref_nfe,operation_nature,additional_data,owner_id,participant_id," \
                     f"taxpayer_id,arquivo_nfe)\n"

    elif(nomeTabela == "items"):
        assinatura = f"INSERT INTO {nomeTabela} (id,created_at, updated_at,product_code,quantity,amount,unit_measure," \
                     f"item_type,item_type_id,description,cfop,bc_icms_amount,brute_total_value,icms_aliquot,icms_amount," \
                     f"bc_icms_st_amount,st_aliquot,icms_st_amount,item_sequential_number,cest,barcode,framing_code,situation," \
                     f"tax_situation)\n"
    assinatura += "VALUES "
    return assinatura

def adiciona_valores_invoices(file,nota,conexao):
    id = "uuid_generate_v4()"
    created_at = "now()"
    updated_at = "now()"
    number  = nota.infNFe.ide.nNF
    model = nota.infNFe.ide.mod
    serie = nota.infNFe.ide.serie
    # note_issue_date = nota.infNFe.ide.dhEmi.replace("T", " ")
    # note_entry_date = nota.infNFe.ide.dhSaiEnt.replace("T", " ")
    cfop = nota.infNFe.det[0].prod.CFOP
    nfe_key = nota.infNFe.Id.replace("NFe", "")
    invoice_at = nota.infNFe.ide.dhEmi.replace("T", " ")
    operation_at = nota.infNFe.ide.dhSaiEnt.replace("T", " ")
    # cnpj_emit = nota.infNFe.emit.CNPJ
    # cnpj_dest = nota.infNFe.dest.CNPJ
    amount = nota.infNFe.total.ICMSTot.vNF
    bc_icms_amount = nota.infNFe.total.ICMSTot.vBC
    icms_amount = nota.infNFe.total.ICMSTot.vICMS
    bc_icms_st_amount = nota.infNFe.total.ICMSTot.vBCST
    icms_st_amount = nota.infNFe.total.ICMSTot.vST
    ecf_serial_number = "null"
    document_type = "55 - NF-e"
    adapt = False
    ref_nfe = "null"
    operation_nature = nota.infNFe.ide.natOp
    # additional_data = "null"
    additional_data = nota.infNFe.infAdic.infCpl.replace("					","")

    owner_id = 1

    ids = buscaIDs(nota.infNFe.emit.CNPJ, nota.infNFe.dest.CNPJ, conexao)
    # participant_id é aquele com que nosso cliente compra ou vende produtos.
    participant_id = ids['idParticipant']
    # taxpayer_id é o nosso cliente ALTERNATIVA: RECEBER O ID DO TAXPAYER E SOMENTE BUSCAR O DO PARTICIPANT.
    taxpayer_id = ids['idTaxPayer']

    arquivo_nfe = adiciona_arquivo_nfe(file)

    sql = f'({id},{created_at},{updated_at},{number},\'{model}\',\'{serie}\',{cfop},' \
           f'\'{nfe_key}\',\'{invoice_at}\',\'{operation_at}\',{amount},{bc_icms_amount},{icms_amount},{bc_icms_st_amount},' \
           f'{icms_st_amount},{ecf_serial_number},\'{document_type}\',{ref_nfe},\'{operation_nature}\',\'{additional_data}\',' \
           f'{owner_id}, {participant_id}, {taxpayer_id},\'{arquivo_nfe}\')'

    return sql

def buscaIDs(cnpjEmit, cnpjDest, conexao):
    cursor = conexao.cursor()
    cursor.execute(f"SELECT id FROM taxpayers WHERE cnpj = \'{formataCNPJ(cnpjEmit)}\'")

    ids = dict()
    idTaxPayerList = cursor.fetchall()

    if len(idTaxPayerList) == 0:
        cursor.execute(f'SELECT id FROM taxpayers WHERE cnpj = \'{formataCNPJ(cnpjDest)}\'')
        idTaxPayerList = cursor.fetchall()
        idTaxPayerTuple = idTaxPayerList[0]
        idTaxPayer = idTaxPayerTuple[0]
        ids['idParticipant'] = buscaIDParticipant(cnpjEmit,conexao)

    else:
        ids['idParticipant'] = buscaIDParticipant(cnpjDest,conexao)
        idTaxPayerTuple = idTaxPayerList[0]
        idTaxPayer = idTaxPayerTuple[0]

    ids['idTaxPayer'] = idTaxPayer
    cursor.close()
    return ids

def formataCNPJ(cnpj):
    cnpjFormatado = f'{cnpj[0]}{cnpj[1]}.{cnpj[2]}{cnpj[3]}{cnpj[4]}.{cnpj[5]}{cnpj[6]}{cnpj[7]}/{cnpj[8]}{cnpj[9]}{cnpj[10]}{cnpj[11]}-{cnpj[12]}{cnpj[13]}'

    return cnpjFormatado

def buscaIDParticipant(cnpj, conexao):
    cursor = conexao.cursor()
    cursor.execute(f"SELECT id FROM participants WHERE cnpj = \'{cnpj}\'")

    idParticipantList = cursor.fetchall()
    idParticipantTuple = idParticipantList[0]
    idParticipant = idParticipantTuple[0]

    cursor.close()
    return idParticipant

def adiciona_arquivo_nfe(file):
    arquivo = open(file, 'r')
    linhas = arquivo.readlines()

    xml = ""
    for linha in linhas:
        xml += linha
    arquivo.close()
    return xml

def adiciona_valores_items(nota):
    produtos = nota.infNFe.det

    sql = ""
    i = 0
    for produto in produtos:
        id = "uuid_generate_v4()"
        created_at = "now()"
        updated_at = "now()"
        product_code = produto.prod.cProd
        quantity = produto.prod.qCom
        amount = produto.prod.vUnCom
        unit_measure = produto.prod.uTrib
        item_type = "00"
        item_type_id = produto.prod.NCM
        description = produto.prod.xProd
        cfop = produto.prod.CFOP

        if(produto.imposto.ICMS.ICMS00 is not None):
            bc_icms_amount = produto.imposto.ICMS.ICMS00.vBC
            icms_aliquot = produto.imposto.ICMS.ICMS00.pICMS
            icms_amount = produto.imposto.ICMS.ICMS00.vICMS
            bc_icms_st_amount = 0
            icms_st_amount = 0
            st_aliquot = 0
            tax_situation = produto.imposto.ICMS.ICMS00.CST

        elif(produto.imposto.ICMS.ICMS10 is not None):
            bc_icms_amount = produto.imposto.ICMS.ICMS10.vBC
            icms_aliquot = produto.imposto.ICMS.ICMS10.pICMS
            icms_amount = produto.imposto.ICMS.ICMS10.vICMS
            bc_icms_st_amount = produto.imposto.ICMS.ICMS10.vBCST
            st_aliquot = produto.imposto.ICMS.ICMS10.pICMSST
            icms_st_amount = produto.imposto.ICMS.ICMS10.vICMSST
            tax_situation = produto.imposto.ICMS.ICMS10.CST

        elif(produto.imposto.ICMS.ICMS20 is not None):
            bc_icms_amount = produto.imposto.ICMS.ICMS20.vBC
            icms_aliquot = produto.imposto.ICMS.ICMS20.pICMS
            icms_amount = produto.imposto.ICMS.ICMS20.vICMS
            bc_icms_st_amount = 0
            icms_st_amount = 0
            st_aliquot = 0
            tax_situation = produto.imposto.ICMS.ICMS20.CST

        elif(produto.imposto.ICMS.ICMS30 is not None):
            bc_icms_st_amount = produto.imposto.ICMS.ICMS30.vBCST
            st_aliquot = produto.imposto.ICMS.ICMS30.pICMSST
            icms_st_amount = produto.imposto.ICMS.ICMS30.vICMSST
            bc_icms_amount = 0
            icms_aliquot = 0
            icms_amount = 0
            tax_situation = produto.imposto.ICMS.ICMS30.CST

        elif (produto.impostos.ICMS.ICMS40 is not None):
            bc_icms_amount = 0
            icms_aliquot = 0
            icms_amount = 0
            bc_icms_st_amount = 0
            icms_st_amount = 0
            st_aliquot = 0
            tax_situation = produto.imposto.ICMS.ICMS40.CEST

        elif(produto.impostos.ICMS.ICMS51 is not None):
            bc_icms_amount = produto.imposto.ICMS.ICMS51.vBC
            icms_aliquot = produto.imposto.ICMS.ICMS51.pICMS
            icms_amount = produto.imposto.ICMS.ICMS51.vICMS
            bc_icms_amount = 0
            icms_aliquot = 0
            icms_amount = 0
            tax_situation = produto.imposto.ICMS.ICMS51.CEST

        elif (produto.impostos.ICMS.ICMS60 is not None):
            bc_icms_amount = 0
            icms_aliquot = 0
            icms_amount = 0
            bc_icms_st_amount = 0
            icms_st_amount = 0
            st_aliquot = 0
            tax_situation = produto.imposto.ICMS.ICMS60.CEST


        elif(produto.impostos.ICMS.ICMS70 is not None):
            bc_icms_amount = produto.imposto.ICMS.ICMS70.vBC
            icms_aliquot = produto.imposto.ICMS.ICMS70.pICMS
            icms_amount = produto.imposto.ICMS.ICMS70.vICMS
            bc_icms_st_amount = produto.imposto.ICMS.ICMS70.vBCST
            st_aliquot = produto.imposto.ICMS.ICMS70.pICMSST
            icms_st_amount = produto.imposto.ICMS.ICMS70.vICMSST
            tax_situation = produto.imposto.ICMS.ICMS70.CEST

        elif(produto.impostos.ICMS.ICMS90 is not None):
            bc_icms_amount = produto.imposto.ICMS.ICMS90.vBC
            icms_aliquot = produto.imposto.ICMS.ICMS90.pICMS
            icms_amount = produto.imposto.ICMS.ICMS90.vICMS
            bc_icms_st_amount = produto.imposto.ICMS.ICMS90.vBCST
            st_aliquot = produto.imposto.ICMS.ICMS90.pICMSST
            icms_st_amount = produto.imposto.ICMS.ICMS90.vICMSST
            tax_situation = produto.imposto.ICMS.ICMS90.CEST

        elif(produto.impostos.ICMS.ICMSPart is not None):
            bc_icms_amount = produto.imposto.ICMS.ICMSPart.vBC
            icms_aliquot = produto.imposto.ICMS.ICMSPart.pICMS
            icms_amount = produto.imposto.ICMS.ICMSPart.vICMS
            bc_icms_st_amount = produto.imposto.ICMS.ICMSPart.vBCST
            st_aliquot = produto.imposto.ICMS.ICMSPart.pICMSST
            icms_st_amount = produto.imposto.ICMS.ICMSPart.vICMSST
            tax_situation = produto.imposto.ICMS.ICMSPart.CEST

        else:
            bc_icms_amount = 0
            icms_aliquot = 0
            icms_amount = 0
            bc_icms_st_amount = 0
            icms_st_amount = 0
            st_aliquot = 0
            tax_situation = -1

        brute_total_value = produto.prod.vProd
        item_sequential_number = (i+1)
        cest = produto.prod.CEST
        barcode = produto.prod.cEANTrib
        framing_code = "null"
        situation = 0
        sql += f'({id},\'{created_at}\',\'{updated_at}\',\'{product_code}\',{quantity},{amount},\'{unit_measure}\',' \
           f'\'{item_type}\',{item_type_id},\'{description}\',{cfop},{bc_icms_amount},{brute_total_value},' \
           f'{icms_aliquot},{icms_amount},{bc_icms_st_amount},{st_aliquot},{icms_st_amount},{item_sequential_number},' \
           f'{cest},\'{barcode}\',\'{framing_code}\',{situation},\'{tax_situation}\')'

        if(i < (len(produtos) - 1)):
            sql += ",\n"
        i += 1

    return sql.replace("None", "null")

def insereBanco(conexao,sql):

    cursor = conexao.cursor()

    cursor.execute(sql)
    conexao.commit()

    cursor.close()


if __name__ == '__main__':

    janelaCredenciais = credenciaisBanco()
    credenciais = janelaCredenciais.getCredenciais()

    conexao = conectaBanco(credenciais['host'], credenciais['nomeBanco'],
                           credenciais['usuario'], credenciais['senha'], credenciais['porta'])

    sg.popup(f'Selecione os arquivos de nota fiscal eletrônica que deseja inserir num banco de dados.')

    caminho_arquivos = escolheArquivos()

    inseridos = list()
    errosNaConversao = list()
    errosNaInsercao = list()

    for file in caminho_arquivos:
        try:
            nota = parser.parse(file)
        except:
            errosNaConversao.append(file)
            continue
        assinaturaInvoices = assinatura_sql("invoices")
        valoresInvoices = adiciona_valores_invoices(file,nota,conexao)
        sqlInvoices = f'{assinaturaInvoices} {valoresInvoices}'

        assinaturaItems = assinatura_sql("items")
        valoresItems = adiciona_valores_items(nota)
        sqlItems = f'{assinaturaItems} {valoresItems}'

        try:
            insereBanco(conexao,sqlInvoices)
            insereBanco(conexao,sqlItems)
            inseridos.append(nota.infNFe.Id)
        except Exception as e:
            errosNaInsercao.append(nota.infNFe.Id)
            print(e)

    if(len(errosNaInsercao) != 0):
        sg.popup(f'{len(inseridos)} Arquivos inseridos com sucesso no Banco de Dados.\n'
                 f'Ocorreram erros ao tentar adicionar os arquivos:\n {errosNaInsercao}\n no Banco de Dados.')
    else:
        sg.popup(f' {len(inseridos)} Arquivos inseridos com sucesso no Banco de Dados.')

    if(len(errosNaConversao) != 0):
        sg.popup(f'Ocorreram erros na conversão de alguns arquivos. \n'
                 f'Certifique-se de que os arquivos: \n {errosNaConversao} \n são arquivos de Notas Fiscais Eletrônicas.')

    conexao.close()












