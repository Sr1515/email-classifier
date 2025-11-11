from abc import ABC, abstractmethod
import pdfplumber
import json
import re
import spacy
from main import model

nlp = spacy.load("pt_core_news_sm")

email_category = {
    "Produtivo": "Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).",
    "Improdutivo": "Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos)." 
}

class BaseExtractor(ABC): 
    @abstractmethod
    def can_handler(self, filename: str) -> bool:
        pass
    
    @abstractmethod
    def extract(self, file) -> str:
        pass
    
class TxtExtractor(BaseExtractor):
    def can_handler(self, filename):
        return filename.lower().endswith(".txt")
    
    def extract(self, file):
        return file.read().decode("utf-8")

class PDFExtractor(BaseExtractor):
    def can_handler(self, filename):
        return filename.lower().endswith(".pdf")
    
    def extract(self, file):
        content = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    content += page.extract_text() + "\n"
                    
        return content
    
class ExtractorFactory:
    def __init__(self):
        self.extractors = [TxtExtractor(), PDFExtractor()]

    def get_extractor(self, filename: str) -> BaseExtractor:
        for extractor in self.extractors:
            if extractor.can_handler(filename):
                return extractor
        raise ValueError(f"Tipo de arquivo não suportado: {filename}")
    
def preprocess_text(text: str) -> str:
    text = text.lower()
    content = nlp(text)
    tokens = [
        token.lemma_ for token in content
        if not token.is_stop and not token.is_punct and not token.like_num
    ]
    return " ".join(tokens)

def extract_text(file):
    factory = ExtractorFactory()
    extractor = factory.get_extractor(file.filename)
    raw_text = extractor.extract(file)
    cleaned_text = preprocess_text(raw_text)
    return cleaned_text

def classify_email(text):
    prompt = f"""
    Você é um assistente que classifica e-mails.

    As categorias que você deve classficar são:
    - Produtivo: {email_category['Produtivo']}
    - Improdutivo: {email_category['Improdutivo']}

    O que você precisa fazer:
    - Classifique o email abaixo como Produtivo ou Improdutivo
      e gere uma resposta automática adequada.

    O que retornar:
    - Retorne somente um JSON no seguinte formato: 
    {{
      "categoria": "Produtivo ou Improdutivo",
      "resposta": "Texto da resposta automática"
    }}

    Email:
    {text}    
    """

    response = model.generate_content(prompt)
    raw_text = response.candidates[0].content.parts[0].text

    cleaned = re.sub(r"```(?:json)?", "", raw_text).strip()

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        return {"erro": "Falha ao decodificar JSON", "texto": cleaned}

    return result