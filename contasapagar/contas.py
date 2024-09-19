from flask import Blueprint
from flask import render_template, request, redirect
from models import Credor, Endereco, Contato, Conta, Pagamento
from database import db
from datetime import datetime, date
from sqlalchemy import select, insert, delete, update, func
from credores import consultarCredores
from dateutil.relativedelta import relativedelta

bp_contas = Blueprint("contas", __name__,template_folder="templates")

@bp_contas.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    if request.method =='POST':
        cnpj = request.form.get('cnpj')
        descricao = request.form.get('descricao')
        valor = request.form.get('valor').replace(",", ".")
        vencimento = datetime.strptime(request.form.get('vencimento'), "%Y-%m-%d")

        conta = Conta(descricao=descricao, credor_cnpj=cnpj, valor=valor, vencimento=vencimento)
        db.session.add(conta)
        db.session.commit()
        
    # contas = consultarContas()[0]
    contas = consultarContas()
    # pagamento = consultarContas()[1]
    credores = consultarCredores()
    # contexto = {'contas': contas, "credores": credores, "pagamento": pagamento }
    contexto = {'contas': contas, "credores": credores,}
    
    return render_template('cadastrar_contas.html', context=contexto)

@bp_contas.route('/consultar')
def consultarContas():  
    # sqlContas = select(Conta.descricao, Credor.nome.label("credor"), Conta.valor, Conta.vencimento, Pagamento.valor.label("ValorPago"),Pagamento.multa, Pagamento.juros, Pagamento.data_pagamento, func.sum(Pagamento.valor>0).label("Pago")).where(Credor.cnpj == Conta.credor_cnpj, Conta.id==Pagamento.conta_id)
    # sqlContas = select(Conta.descricao, Credor.nome.label("credor"), Conta.valor, Conta.vencimento)
    # contas = db.session.execute(sqlContas).all()

    contas = Conta.query.all()
    dataAtual = date.today()
    for conta in contas:
        pagamento = Pagamento.query.all()
        # for a in range(len(pagamento)): 
        #     if (conta.id != pagamento[a].conta_id):
        #         print("Id: ", conta.id, "Pagamento conta id: ", pagamento[a].conta_id)
        #         print("Não há este id na tabela de pagamentos")
        #     else:
        #         print("Enconrou a Conta cujo id é: ", conta.id)
        if (dataAtual > conta.vencimento):
            multa = conta.valor*2/100 # a multa padrão por atraso é de 2% sobre o valor principal
            atraso = abs(relativedelta(dataAtual,conta.vencimento))
            diasAtraso = atraso.days
            juros = conta.valor*(0.01/30)*diasAtraso
            # print("Dias:", diasAtraso, "Multa:", multa, "Juros:",juros)

            if  len(pagamento) <= 0 :
                print("Entro no if len pagamento<=0")
                pagamento = Pagamento(conta.id, multa, juros)
                db.session.add(pagamento)
                db.session.commit()

            else:
                for i in range(len(pagamento)):
                    if pagamento[i].conta_id == conta.id:
                        # print(conta)
                        pagamento[i].juros = juros
                        pagamento[i].multa = multa

                # for pag in pagamento:
                #     if pag.conta_id ==conta.id:
                #         pag.multa = multa
                #         pag.juros = juros
                #         print(pag.multa)
                # return contas, pagamento

    # for conta in contas:
    #     qrPagamento = Pagamento.query.filter_by(conta_id=conta.id)
    #     teste = db.session.execute(qrPagamento)
    #     lista_tupla = teste.fetchone()
    #     pagamento = list(lista_tupla)
    #     print("lista: ", lista_tupla)
    #     if (dataAtual > conta.vencimento):
    #         multa = conta.valor*2/100 # a multa padrão por atraso é de 2% sobre o valor principal
    #         atraso = abs(relativedelta(dataAtual,conta.vencimento))
    #         diasAtraso = atraso.days
    #         juros = conta.valor*(0.01/30)*diasAtraso
    #         print("Dias:", diasAtraso, "Multa:", multa, "Juros:",juros)
    #         if  pagamento == []:
    #             pagamento = Pagamento(conta.id, multa, juros)
    #             db.session.add(pagamento)
    #             db.session.commit()

    #         else:
    #             # pagamento = Pagamento.query.get(pagamento.id)
    #             # lista = list(pagamento)
    #             print(pagamento)       

    return contas

@bp_contas.route('/editar/<int:contaId>', methods=['GET','POST'])
def editar(contaId):
    conta  = Conta.query.get(contaId)
    if request.method =='POST':
        cnpj = request.form.get('cnpj')
        descricao = request.form.get('descricao')
        valor = request.form.get('valor').replace(",", ".")
        valor = ''.join(valor.split()).replace('R$', '')
        vencimento = datetime.strptime(request.form.get('vencimento'), "%Y-%m-%d")

        conta.credor_cnpj = cnpj
        conta.descriacao  = descricao    
        conta.valor       = valor
        conta.vencimento  = vencimento   

        db.session.add(conta)
        db.session.commit()        

        return redirect('/contas/cadastrar')
    
    contas = consultarContas()
    credores = consultarCredores()
    contexto = {
        "conta": conta,
        "contas": contas,
        "credores": credores
    }
    return render_template('editar_contas.html', context=contexto)

@bp_contas.route('/delete/<int:contaId>', methods=['GET','POST'])
def delete(contaId):
    conta = Conta.query.get(contaId)
    if request.method =='POST':
        db.session.delete(conta)
        db.session.commit()
        return redirect('/contas/cadastrar')
    contas = consultarContas()
    contexto = {
        "conta": conta,
        "contas": contas,
    }   
    return render_template('excluir_contas.html', context=contexto)
