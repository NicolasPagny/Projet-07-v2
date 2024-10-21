from transformers import BertTokenizer, BertForSequenceClassification
import torch
from torch.nn.functional import softmax

def bert_predict(datas, model):
    """
    Produit des prédictions classifiées de Bert

    Parameters:
    datas: le dataset texte sous forme de tenseurs PyTorch
    model: le modèle BERT à utiliser
    """
    # Ne pas calculer les gradients pour la prédiction
    with torch.no_grad():
        # Obtenir les logits du modèle
        outputs = model(**datas)
        logits = outputs.logits

    # Calculer les probabilités
    probabilities = softmax(logits, dim=-1)

    # Obtenir la prédiction
    prediction = torch.argmax(probabilities, dim=1).numpy()

    return prediction

def process_transform_text(texts):
    """
    Applique toutes les démarches de prédictions : pré-traitements des textes,
    et ensuite pour chaque texte, une prédiction de sentiment positif ou négatif,
    puis retourne le tout dans une liste.
    """
    # Charger le modèle et le tokenizer
    model = BertForSequenceClassification.from_pretrained("nicolaspagny/bert-analyse-sentiment-projet07")
    tokenizer = BertTokenizer.from_pretrained("nicolaspagny/bert-analyse-sentiment-projet07")

    # Tokenisation des textes
    datas = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

    # Effectuer les prédictions
    predictions = bert_predict(datas, model)
    
    return predictions.tolist()  # Retourner les prédictions sous forme de liste
