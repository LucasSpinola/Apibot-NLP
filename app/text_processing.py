from sklearn.feature_extraction.text import CountVectorizer 

import numpy as np
import re

def create_bag_of_words(phrases_list):

  #usa o construtor específico da classe CountVectorizer que passa como parâmetro a quantidade máxima de palavras que devem ser selecionadas 
  cv = CountVectorizer(max_features = 150)
  #chama o método fit_transform da classe CountVectorizer passando como parâmetro um vetor de frases, desta forma extraindo as 150 palavras que mais aparecem nesse vetor. Depois transforma em um Array.
  X = cv.fit_transform(phrases_list).toarray() 

  return(X, cv)

def string_to_tfidf(phrase, cv):

  #cria um vetor tfidf  que representa a frase
  tfidf_vector = cv.transform([phrase]).toarray()

  #transforma o vetor tfidf em um vetor numpy
  tfidf_np_vector = np.array(tfidf_vector[0])

  return(tfidf_np_vector)

def clear_phrases(text, porter, pt_stopwords): 

  text = text.lower()
  text = re.sub('[^a-zA-Záàâãéèêíïóôõöúçñ]', ' ', text)

  #faz o split para poder usar as stopwords em português
  text = text.split()

  #Limpa cada palavra do texto usando stemmer retirando as stopwords
  text = [porter.stem(word) for word in text if not word in set(pt_stopwords)]

  #junta as palavras do texto em uma só string
  text = ' '.join(text)

  return(text)