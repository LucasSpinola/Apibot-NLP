import nltk
import io
import numpy as np
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

import json

from app.api import le_perguntas
from app.text_processing import clear_phrases, create_bag_of_words, string_to_tfidf

nltk.download('stopwords')

def maior_similaridade(word, bag_of_words):
  #cria um array numpy que indica a similaridade da frase com cada uma das outras frases do bag of words usando o produto interno do numpy
  comp = np.array([np.inner(word, np.array(frase)) for frase in bag_of_words])

  if comp.max() == 0:
    return("Erro")
  #retorna o índice correspondente oo valor de maior similaridade
  return(comp.argmax())

def npl(pergunta):

  data = le_perguntas()

  lista_perguntas = [data.json()[id]['pergunta'] for id in data.json()]
  lista_respostas = [data.json()[id]['resposta'] for id in data.json()]

  # cria objeto do tipo PorterStemmer 
  ps = PorterStemmer()
  # Baixa a lista de stopwords em português
  all_stopwords = stopwords.words('portuguese') 

  pergunta_limpa = clear_phrases(pergunta, ps, all_stopwords)

  #cria a bag of words que representa cada pergunta da lista de perguntas e um objeto CountVectorizer que serve para transformar outras palavras no tipo de representação da lista
  bow, cv = create_bag_of_words(lista_perguntas)

  #vetor tfidf que representa a pergunta no formato numpy
  vetor_frase = string_to_tfidf(pergunta_limpa, cv)

  #pega o índice de maior similaridade com a frase
  index = maior_similaridade(vetor_frase, bow)

  if index == "Erro": return("Infelizmente não encontrei nenhuma resposta para sua pergunta!") 
  
  return(lista_respostas[index])
