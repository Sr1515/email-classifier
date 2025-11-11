from main import app
from flask import request, render_template, jsonify
from utils import extract_text, classify_email
from models.categories_email import EmailCategory

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/processing', methods=["POST"])
def processing():
    file = request.files.get("file")
    
    if not file:
        return "Nenhum arquivo enviado!", 400
    
    try:
        text = extract_text(file)
    except ValueError as e:
        return str(e), 400

    if not text.strip():
        return "Não foi possível extrair texto do arquivo.", 400
    
    result = classify_email(text)

    if isinstance(result, str): 
        return f"Erro ao classificar: {result}", 500

    categoria = result.get("categoria", "Desconhecida")
    resposta = result.get("resposta", "Sem resposta gerada.")

    produtivo = categoria.lower().startswith("produtivo")
    
    EmailCategory.create(
        title=file.filename,
        body=text,
        productive=produtivo
    )
    
    return jsonify({
         "arquivo": file.filename,
         "categoria": categoria,
         "resposta": resposta
    })

    # return render_template(
    #     "result.html",
    #     filename=file.filename,
    #     categoria=categoria,
    #     resposta=resposta,
    #     texto=text
    # )