from flask import Blueprint
from flask import render_template, request, redirect
from models import Credor, Endereco, Contato, Conta, Pagamento
from database import db
from datetime import datetime
from sqlalchemy import select, insert, delete, update, func
from credores import consultarCredores


bp_contas = Blueprint("contas", __name__,template_folder="templates")

@bp_contas.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    if request.method =='POST':
        cnpj = request.form.get('cnpj')
        descricao = request.form.get('descricao')
        valor = request.form.get('valor')
        vencimento = datetime.strptime(request.form.get('vencimento'), "%d/%m/%Y")

        conta = Conta(descricao=descricao, credor_cnpj=cnpj, valor=valor, vencimento=vencimento)
        db.session.add(conta)
        db.session.commit()
        
    contas = consultarContas()
    credores = consultarCredores()
    contexto = {'contas': contas, "credores": credores }
    
    return render_template('cadastrar_contas.html', context=contexto)

@bp_contas.route('/consultar')
def consultarContas():  
    #  sqlContas = select(Conta.descricao, Credor.nome.label("credor"), Conta.valor, Conta.vencimento, Pagamento.valor.label("ValorPago"),Pagamento.multa, Pagamento.juros, Pagamento.data_pagamento, func.sum(Pagamento.valor>0).label("Pago")).where(Credor.cnpj == Conta.credor_cnpj, Conta.id==Pagamento.conta_id)
    #  sqlContas = select(Conta.descricao, Credor.nome.label("credor"), Conta.valor, Conta.vencimento)
    #  contas = db.session.execute(sqlContas).all()

    contas = Conta.query.all()
    return contas

@bp_contas.route('/editar/<int:contaId>', methods=['GET','POST'])
def editar(contaId):
    conta  = Conta.query.get(contaId)
    if request.method =='POST':
        cnpj = request.form.get('cnpj')
        descricao = request.form.get('descricao')
        valor = request.form.get('valor')
        vencimento = datetime.strptime(request.form.get('vencimento'), "%d/%m/%Y")
        
        print(cnpj, descricao, valor, vencimento)

        conta = Conta(descricao=descricao, credor_cnpj=cnpj, valor=valor, vencimento=vencimento)
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

@bp_contas.route('/delete/<string:cnpj>', methods=['GET','POST'])
def delete(cnpj):
    conta = Conta.query.get(cnpj)
    contexto = {
        "conta": conta
    }
    if request.method =='GET':
        return render_template('excluir_contas.html', context=contexto)
    if request.method =='POST':
        db.session.delete(conta)
        db.session.commit()
        return redirect('/contas/consultar')