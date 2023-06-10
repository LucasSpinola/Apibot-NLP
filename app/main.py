from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from app.nlp import npl
from app.api import cria_log, get_id_resposta, guardar_requisicao, contagem, requisicao_banco, verificar_id, get_resposta, retornar_contagem, guardar_requisicao_erro
import datetime
import json

app = FastAPI()



class Pergunta(BaseModel): 
    mensagem: str

contador_rep = []


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/pergunta")
def fazer_perguntas(pergunta: Pergunta):
    user_respostas = pergunta.mensagem
    resposta = npl(user_respostas)
    resp_banco = get_resposta(resposta)
    id_resposta = get_id_resposta(resposta)
    solict = requisicao_banco(resposta)
    data = datetime.datetime.now()
    
    if resposta == "Infelizmente não encontrei nenhuma resposta para sua pergunta!":    
        cria_log(str(pergunta.mensagem))
        guardar_requisicao_erro(user_respostas, str(data)[0:10:1])
    
    elif solict == None:
        contador = 1
        contador_rep.append(contador)
        id_resposta = get_id_resposta(resposta)
        guardar_requisicao(resposta, id_resposta, str(data)[0:10:1], contador)
    
    elif solict == resposta:
        list = []
        valor = retornar_contagem(resposta)
        list.append(valor)
        contador = list[0] + 1
        id_resposta_banco = verificar_id(resposta)
        contagem(id_resposta_banco, contador)
    
      
    return(resposta)
        
    