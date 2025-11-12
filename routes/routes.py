from main import app
from flask import request, render_template
from utils.extractProcessorText import extract_text, preprocess_text
from utils.aiSender import classify_email
from models.categories_email import EmailCategory

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/processing', methods=["POST"])
def processing():
    file = request.files.get("file")
    produtivos = request.form.get("produtivos", "")
    manual_text  = request.form.get("texto_manual", "")
    improdutivos = request.form.get("improdutivos", "")
    
    produtivos_list = [x.strip() for x in produtivos.split(",") if x.strip()]
    improdutivos_list = [x.strip() for x in improdutivos.split(",") if x.strip()]
    
    
    if not file and not manual_text:
        return "Nenhum arquivo enviado!", 400

    if manual_text:
        text = preprocess_text(manual_text)
    else:
        try:
            text = extract_text(file)
        except ValueError as e:
            return str(e), 400

    if not text.strip():
        return "Não foi possível extrair texto do arquivo.", 400

    result = classify_email(text, produtivos_list, improdutivos_list)

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

    return render_template(
        "result.html",
        filename=file.filename,
        categoria=categoria,
        resposta=resposta,
        texto=text
    )