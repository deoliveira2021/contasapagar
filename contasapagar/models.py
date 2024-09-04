from database import db

## Estrutura da tabela de contato
class Contato(db.Model):
    __tablename__ = "contato"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    telefone = db.Column(db.String(11))
    email = db.Column(db.String(150))
    whatsapp = db.Column(db.String(11))


    def __init__(self, nome, telefone, email, whatsapp):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.whatsapp = whatsapp

    def __repr__(self):
        return "Contato: {}".format(self.nome)

## Estrutura da tabela de endereço
class Endereco(db.Model):
    __tablename__ = "endereco"
    cep = db.Column(db.String(8), primary_key=True)
    logradouro = db.Column(db.String(150))
    numero = db.Column(db.String(6))
    complemento = db.Column(db.String(50))
    cidade = db.Column(db.String(150))
    uf = db.Column(db.String(2))



    def __init__(self,cep, logradouro, numero, complemento, cidade, uf):
        self.cep = cep
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.cidade = cidade
        self.uf = uf

    def __repr__(self):
        return "Endereco: {}".format(self.cep)

    
## Estrutura da tabela de credores
class Credor(db.Model):
    __tablename__ ="credor"
    cnpj = db.Column(db.String(14), primary_key=True)
    nome = db.Column(db.String(150))
    ender_cep = db.Column(db.String(8),db.ForeignKey("endereco.cep"))
    contato_id = db.Column(db.Integer,db.ForeignKey("contato.id"))
 
    def __init__(self,cnpj, nome, ender_cep, contato_id):
    # def __init__(self,cnpj, nome, contato_id):
        self.cnpj = cnpj
        self.nome = nome
        self.ender_cep = ender_cep
        self.contato_id = contato_id

    def __repr__(self):
        return "Credor: {}".format(self.nome)

## Estrutura da tabela de contas a pagar
class Conta(db.Model):
    __tablename__ ="conta"
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(150))
    credor_cnpj = db.Column(db.String(14),db.ForeignKey('credor.cnpj'))
    valor = db.Column(db.Double)
    vencimento = db.Column(db.Date)

    def __init__(self, descricao, credor_cnpj, valor, vencimento):
        self.descricao = descricao
        self.credor_cnpj = credor_cnpj
        self.valor = valor
        self.vencimento = vencimento

    def __repr__(self):
        return "Conta: {}".format(self.descricao)
    
class Pagamento(db.Model):
    __tablename__ ="pagamento"
    id = db.Column(db.Integer, primary_key=True)
    data_pagamento = db.Column(db.Date)
    conta_id = db.Column(db.Integer,db.ForeignKey('conta.id'))
    valor = db.Column(db.Double)
    multa = db.Column(db.Double)
    juros = db.Column(db.Double)
    
    def __init__(self, data_pagamento, conta_id, valor, multa,juros):
        self.data_pagamento = data_pagamento
        self.conta_id = conta_id
        self.valor = valor
        self.multa = multa
        self.juros = juros

    def __repr__(self):
        return "pagamento: {}".format(self.data_pagamento)    