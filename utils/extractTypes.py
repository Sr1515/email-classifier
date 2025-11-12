from abc import ABC, abstractmethod
import pdfplumber

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
    
