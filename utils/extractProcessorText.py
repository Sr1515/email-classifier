from utils.extractTypes import ExtractorFactory
import spacy

nlp = spacy.load("pt_core_news_sm")

def extract_text(file):
    factory = ExtractorFactory()
    extractor = factory.get_extractor(file.filename)
    raw_text = extractor.extract(file)
    cleaned_text = preprocess_text(raw_text)
    return cleaned_text

def preprocess_text(text: str) -> str:
    text = text.lower()
    content = nlp(text)
    tokens = [
        token.lemma_ for token in content
        if not token.is_stop and not token.is_punct and not token.like_num
    ]
    return " ".join(tokens)