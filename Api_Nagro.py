from flask import Flask, request
import Scraping
import json

app = Flask("Nagro")

@app.route("/scraping",methods=["POST"])
def Api_Scraping():
    req = request.get_json() # recebe o request
    dados = Scraping.Scrapy(req['cpf_cnpj']) #aplica a raspagem
    if len(dados) == 0:
        list = []
        list.append({'LOG': 'Não a registros disponivel para essa entrada!'})
        return json.dumps(list,indent=4,ensure_ascii=False).encode('utf8')
    return json.dumps(dados,indent=4,ensure_ascii=False).encode('utf8') #retorna o json

app.run()
