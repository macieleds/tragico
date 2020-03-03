from flask_restful import Resource, reqparse
from models.produto import ProdutosModel


class Produtos(Resource):
    def get(self):
        return {'produtos': [produto.json() for produto in ProdutosModel.query.all()]} #Equivalente - SELECT * FROM JOBS  

class Produto(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('modelo', type=str, required=True, help="O campo 'modelo' é de preenchimento obrigatório.")
    atributos.add_argument('estrelas', type=float)
    atributos.add_argument('valor', type=float, required=True, help="O campo 'diaria' é de preenchimento obrigatório.")
    atributos.add_argument('cidade', type=str, required=True, help="O campo 'cidade' é de preenchimento obrigatório.")
    
    def get (self, produto_id):
        produto = ProdutosModel.find_produto(produto_id)
        if produto:
            return produto.json()
        return {'message': 'Produto não encontrado.'}, 404 # not found  
            
                  
    def post (self, produto_id):
        
        if ProdutosModel.find_produto(produto_id):
            return {"message": "Esse id de produto '({})' já existe.".format(produto_id)}, 400 #Bad Request
        dados = Produto.atributos.parse_args()
        produto = ProdutosModel(produto_id, **dados)  
        try:
            produto.save_produto()
        except: 
            return {'message': 'Ocorreu um erro interno ao salvar as informações'}, #500 Internal Server Error
        return produto.json()


    def put (self, produto_id):
        dados = Produto.atributos.parse_args()        
        produto_encontrado = ProdutosModel.find_produto(produto_id)   
        if produto_encontrado:
            produto_encontrado.update_produto(**dados)
            produto_encontrado.save_produto()
            return produto_encontrado.json(), 200 # OK  
        produto = ProdutosModel(produto_id, **dados) 
        
        try:
            produto.save_produto()
        except: 
            return {'message': 'Ocorreu um erro interno ao salvar as informações'}, #500 Internal Server Error
        return produto.json(), 201 #criado
        
    
    def delete (self, produto_id):
        produto = ProdutosModel.find_produto(produto_id)
        if produto:
            try:
                produto.delete_produto()
            except:
                return {'message': 'Ocorreu um erro interno ao remover as informações'} #500 Internal Server Error
            return {'message': 'Produto deletado.'}    
        return {'message': 'Produto não encontrado.'}, 404 #not found