from nfelib.v4_00 import leiauteNFe_sub as parser
from tkinter import filedialog, Tk


def assinatura_sql(nomeTabela):

    if(nomeTabela == "invoices"):
        assinatura = f"INSERT INTO {nomeTabela}(created_at,updated_at,number,model,serie,note_issue_date,note_entry_date,cfop," \
                     f"nfe_Key,cnpj_emit,cnpj_dest,amount,bc_icms_amount,icms_amount,bc_icms_st_amount,icms_st_amount," \
                     f"ecf_serial_number,document_type,ref_nfe,operation_nature,additional_data,arquivo_nfe)\n"

    elif(nomeTabela == "items"):
        assinatura = f"INSERT INTO {nomeTabela} (created_at, updated_at,product_code,quantity,amount,unit_measure," \
                     f"item_type,item_type_id,description,cfop,bc_icms_amount,brute_total_value,icms_aliquot,icms_amount," \
                     f"bc_icms_st_amount,st_aliquot,icms_st_amount,item_sequential_number,cest,barcode,framing_code,situation," \
                     f"tax_situation)\n"
    assinatura += "VALUES "
    return assinatura

def adiciona_valores_invoices(file,nota):
    created_at = "now()"
    updated_at = "now()"
    number  = nota.infNFe.ide.nNF
    model = nota.infNFe.ide.mod
    serie = nota.infNFe.ide.serie
    note_issue_date = nota.infNFe.ide.dhEmi.replace("T", " ")
    note_entry_date = nota.infNFe.ide.dhSaiEnt.replace("T", " ")
    cfop = nota.infNFe.det[0].prod.CFOP
    nfe_key = nota.infNFe.Id.replace("NFe", "")
    cnpj_emit = nota.infNFe.emit.CNPJ
    cnpj_dest = nota.infNFe.dest.CNPJ
    amount = nota.infNFe.total.ICMSTot.vNF
    bc_icms_amount = nota.infNFe.total.ICMSTot.vBC
    icms_amount = nota.infNFe.total.ICMSTot.vICMS
    bc_icms_st_amount = nota.infNFe.total.ICMSTot.vBCST
    icms_st_amount = nota.infNFe.total.ICMSTot.vST
    ecf_serial_number = "null"
    document_type = "55 - NF-e"
    ref_nfe = "null"
    operation_nature = nota.infNFe.ide.natOp
    additional_data = nota.infNFe.infAdic.infCpl.replace("					","")
    arquivo_nfe = adiciona_arquivo_nfe(file)

    return f'{created_at},{updated_at},{number},\'{model}\',\'{serie}\',\'{note_issue_date}\',\'{note_entry_date}\',{cfop},' \
           f'\'{nfe_key}\',\'{cnpj_emit}\',\'{cnpj_dest}\',{amount},{bc_icms_amount},{icms_amount},{bc_icms_st_amount},' \
           f'{icms_st_amount},{ecf_serial_number},\'{document_type}\',{ref_nfe},\'{operation_nature}\',\'{additional_data}\',' \
           f'\'{arquivo_nfe}\''

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
    for produto in produtos:
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

        elif(produto.imposto.ICMS.ICMS10 is not None):
            bc_icms_amount = produto.imposto.ICMS.ICMS10.vBC
            icms_aliquot = produto.imposto.ICMS.ICMS10.pICMS
            icms_amount = produto.imposto.ICMS.ICMS10.vICMS
            bc_icms_st_amount = produto.imposto.ICMS.ICMS10.vBCST
            st_aliquot = produto.imposto.ICMS.ICMS10.pICMSST
            icms_st_amount = produto.imposto.ICMS.ICMS10.vICMSST

        elif(produto.imposto.ICMS.ICMS20 is not None):
            bc_icms_amount = produto.imposto.ICMS.ICMS20.vBC
            icms_aliquot = produto.imposto.ICMS.ICMS20.pICMS
            icms_amount = produto.imposto.ICMS.ICMS20.vICMS

        elif(produto.imposto.ICMS.ICMS30 is not None):
            bc_icms_st_amount = produto.imposto.ICMS.ICMS30.vBCST
            st_aliquot = produto.imposto.ICMS.ICMS30.pICMSST
            icms_st_amount = produto.imposto.ICMS.ICMS30.vICMSST

        elif(produto.impostos.ICMS.ICMS51 is not None):
            bc_icms_amount = produto.imposto.ICMS.ICMS51.vBC
            icms_aliquot = produto.imposto.ICMS.ICMS51.pICMS
            icms_amount = produto.imposto.ICMS.ICMS51.vICMS

        elif(produto.impostos.ICMS.ICMS70 is not None):
            bc_icms_amount = produto.imposto.ICMS.ICMS70.vBC
            icms_aliquot = produto.imposto.ICMS.ICMS70.pICMS
            icms_amount = produto.imposto.ICMS.ICMS70.vICMS
            bc_icms_st_amount = produto.imposto.ICMS.ICMS70.vBCST
            st_aliquot = produto.imposto.ICMS.ICMS70.pICMSST
            icms_st_amount = produto.imposto.ICMS.ICMS70.vICMSST

        elif(produto.impostos.ICMS.ICMS90 is not None):
            bc_icms_amount = produto.imposto.ICMS.ICMS90.vBC
            icms_aliquot = produto.imposto.ICMS.ICMS90.pICMS
            icms_amount = produto.imposto.ICMS.ICMS90.vICMS
            bc_icms_st_amount = produto.imposto.ICMS.ICMS90.vBCST
            st_aliquot = produto.imposto.ICMS.ICMS90.pICMSST
            icms_st_amount = produto.imposto.ICMS.ICMS90.vICMSST

        elif(produto.impostos.ICMS.ICMSPart is not None):
            bc_icms_amount = produto.imposto.ICMS.ICMSPart.vBC
            icms_aliquot = produto.imposto.ICMS.ICMSPart.pICMS
            icms_amount = produto.imposto.ICMS.ICMSPart.vICMS
            bc_icms_st_amount = produto.imposto.ICMS.ICMSPart.vBCST
            st_aliquot = produto.imposto.ICMS.ICMSPart.pICMSST
            icms_st_amount = produto.imposto.ICMS.ICMSPart.vICMSST

        else:




        brute_total_value = produto.prod.vProd


        item_sequential_number
        cest
        barcode
        framing_code
        situation
        tax_situation








if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilenames()
    for file in file_path:
        nota = parser.parse(file)
        # assinaturaInvoices = assinatura_sql("invoices")
        # assinaturaItems = assinatura_sql("items")
        # valoresInvoices = adiciona_valores_invoices(file,nota)
        # sqlInvoices = (f'{assinaturaInvoices} ({valoresInvoices})')
        print(nota.infNFe.det[0].imposto.ICMS.ICMS00)






    # arquivo = open('file.txt', 'w')
    # arquivo.close()


    #     arquivo.write(nota.infNFe.emit.CNPJ)
    #     arquivo.write(" ")
    #
    # arquivo.close()





