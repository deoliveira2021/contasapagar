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
    cidade = db.Column(db.String(150))
    uf = db.Column(db.String(2))
    complemento = db.Column(db.String(50))



    def __init__(self,cep, nome, telefone, email, whatsapp):
        self.cep = cep
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.whatsapp = whatsapp

    def __repr__(self):
        return "Endereco: {}".format(self.cep)

    
## Estrutura da tabela de credores
class Credor(db.Model):
    __tablename__ ="credor"
    cnpj = db.Column(db.String(14), primary_key=True)
    nome = db.Column(db.String(150))
    ender_cep = db.Column(db.String(8),db.ForeignKey("endereco.cep"))
    contato_id = db.Column(db.Integer,db.ForeignKey("contato.id"))
 
    # def __init__(self,cnpj, nome, ender_cep, contato_id):
    def __init__(self,cnpj, nome, contato_id):
        self.cnpj = cnpj
        self.nome = nome
        # self.ender_cep = ender_cep
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