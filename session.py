from persist import insert 

class Session:

    status = 1
    placa_carro = ''
    url_imagem = ''
    nome_orgao = ''
    descricao = ''
    lat = ''
    lon = ''

    def __init__(self, id, nome, recipient_id):
        self.id = id
        self.nome = nome
        self.recipient_id = recipient_id

    def incremento(self):
        self.status += 1 

    def inserir(self):
        insert(self.placa_carro, self.nome_orgao, self.url_imagem, self.descricao, self.lat, self.lon)   