from flask import Blueprint
from flask import render_template, request, redirect
from models import Credor, Endereco, Contato
from database import db

bp_credores = Blueprint("credores", __name__,template_folder="templates")

@bp_credores.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    if request.method =='GET':
        return render_template('cadastrar_credores.html')

    if request.method =='POST':
        cnpj = request.form.get('cnpj')
        nome = request.form.get('nome')
        nomecontato = request.form.get('contato')
        telefone = request.form.get('telefone')
        whatsapp = request.form.get('whatsapp')
        email = request.form.get('email')

        contato = Contato(nomecontato,telefone, email, whatsapp)
        db.session.add(contato)
        db.session.commit()
        contatoId = contato.id


        credor = Credor(cnpj, nome, contatoId)
        db.session.add(credor)
        db.session.commit()
        return redirect('/credores/consultar')
@bp_credores.route('/consultar')
def consultar():
     credores = Credor.query.all()
     return render_template('consultar_credores.html', credores=credores)

@bp_credores.route('/editar/<string:cnpj>', methods=['GET','POST'])
def atualizar(cnpj):
    credor = Credor.query.get(cnpj)
    if request.method =='GET':
        return render_template('usuarios_update.html', u = credor)
    if request.method =='POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        credor.nome = nome
        credor.email = email
        db.session.add(credor)
        db.session.commit()
        return redirect('/credores/recovery')

@bp_credores.route('/delete/<string:cnpj>', methods=['GET','POST'])
def delete(cnpj):
    credor = Credor.query.get(cnpj)
    if request.method =='GET':
        return render_template('excluir_credores.html', u = credor)
    if request.method =='POST':
        db.session.delete(credor)
        db.session.commit()
        return redirect('/credores/consultar')