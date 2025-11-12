import json
import re
from main import model

email_category = {
    "Produtivo": "Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).",
    "Improdutivo": "Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos)." 
}

def classify_email(text, produtivos=None, improdutivos=None):
    produtivos = produtivos or []
    improdutivos = improdutivos or []

    if produtivos:
        produtivos_str = f"Palavras-chave: {', '.join(produtivos)}"
    else:
        produtivos_str = f"Descrição Padrão: {email_category['Produtivo']}"

    if improdutivos:
        improdutivos_str = f"Palavras-chave: {', '.join(improdutivos)}"
    else:
        improdutivos_str = f"Descrição Padrão: {email_category['Improdutivo']}"
    
    prompt = f"""
    Você é um assistente que classifica e-mails com foco em produtividade.

    As categorias que você deve considerar para classificação são:
    - Critérios para 'Produtivo': {produtivos_str}
    - Critérios para 'Improdutivo': {improdutivos_str}

    O que você precisa fazer:
    - Classifique o email abaixo como 'Produtivo' ou 'Improdutivo' 
      levando em conta os critérios acima e o contexto do texto.
    - Gere uma resposta automática curta (máximo 50 palavras) e profissional, 
      adequada ao tom e ao conteúdo do email original.

    O que retornar:
    - Retorne somente um JSON no seguinte formato: 
    {{
      "categoria": "Produtivo ou Improdutivo",
      "resposta": "Texto da resposta automática"
    }}

    Email para Classificar:
    ---
    {text}
    """

    try:
        response = model.generate_content(prompt)
        raw_text = response.candidates[0].content.parts[0].text
        cleaned = re.sub(r"```(?:json)?", "", raw_text).strip()
    
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        return {"erro": "Falha ao decodificar JSON", "texto": cleaned}

    return result

    