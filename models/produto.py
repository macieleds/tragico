from sql_alchemy import banco

class ProdutosModel(banco.Model):
    __tablename__ = 'produtos'
    
    produto_id = banco.Column(banco.String, primary_key=True)
    modelo = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    valor = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))

    def __init__(self, produto_id, modelo, estrelas, valor, cidade):
        self.produto_id = produto_id
        self.modelo = modelo
        self.estrelas = estrelas
        self.valor = valor
        self.cidade = cidade
    
    def json(self):
        return {
            'produto_id': self.produto_id,
            'modelo': self.modelo,
            'estrelas': self.estrelas,
            'valor': self.valor,
            'cidade': self.cidade
        }    

    @classmethod
    def find_produto(cls, produto_id):
        produto = cls.query.filter_by(produto_id=produto_id).first()  #Comando executado ex.: SELECT * FROM produtos WHERE produto_id = $produto_id LIMIT=1
        if produto: 
            return produto
        return None
    
    def save_produto(self):
        banco.session.add(self)
        banco.session.commit()
        
    def update_produto(self, modelo, estrelas, valor, cidade):
        self.modelo = modelo
        self.estrelas = estrelas
        self.valor = valor
        self.cidade = cidade
        
    def delete_produto(self):
        banco.session.delete(self)
        banco.session.commit()    
        