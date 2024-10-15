from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf

def bert_predict(datas):
    """
    Produit des prédictions classifiées de Bert

    Parameters:
    datas: le dataset texte
    """

    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    datas = list(map(lambda x: tokenizer(x, return_tensors="tf"), datas))
    model = TFBertForSequenceClassification.from_pretrained(model_name)

    outputs = model(datas)
    logits = outputs.logits

    probabilities = tf.nn.softmax(logits, axis=-1)
    prediction = tf.argmax(probabilities, axis=1).numpy()[0]

    return prediction

def bert_binaire_classifier(prediction):
    """
    le modèle pré-entraîné "nlptown/bert-base-multilingual-uncased-sentiment" produit des prédictions
    à 5 classes : 0 1 des sentiments négatifs, 2 neutre, 3 et 4 positifs
    l'application n'utilise qu'une prédiction binaire, alors j'ajoute une couche de classification basée sur des conditions simples :
    si 2 ou 3 ou 4 alors sentiments positifs sinon sentiments négatifs 
    """

    binary_prediction = 0
    if prediction in [2, 3, 4]:
        binary_prediction = 1
    
    return binary_prediction

def process_transform_text(texts):
    """
    Applique toutes les démarches de prédictions : pré-traitements des texts, et ensuite pour chaque texte, une prédiction de sentiment positif ou négatif
    puis retourne le tout dans une liste
    """
    return list(map(lambda x: bert_binaire_classifier(bert_predict(x)), texts))