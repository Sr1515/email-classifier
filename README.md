# Email-Classifier

Esta é uma aplicação **web** desenvolvida em **Python (Flask)** focada na **classificação e processamento de e-mails**, utilizando **Inteligência Artificial** e **Processamento de Linguagem Natural (NLP)**.

---

## Tecnologias Principais

| Categoria                   | Tecnologia                                                                              | Uso Principal                                               |
| :-------------------------- | :-------------------------------------------------------------------------------------- | :---------------------------------------------------------- |
| **Backend/Web**             | [Flask](https://flask.palletsprojects.com/)                                             | Micro-framework para estruturação da aplicação.             |
| **Inteligência Artificial** | [Gemini](https://ai.google.dev/)                                                        | Motor de IA para classificação e processamento de conteúdo. |
| **NLP**                     | [spaCy](https://spacy.io/)                                                              | Processamento de Linguagem Natural e extração de dados.     |
| **Banco de Dados**          | SQLite + [Peewee](http://docs.peewee-orm.com/en/latest/)                                | Banco de dados leve e ORM (Object-Relational Mapper).       |
| **Frontend/UI**             | [Jinja2](https://jinja.palletsprojects.com/) + [Tailwind CSS](https://tailwindcss.com/) | Template engine e framework CSS utility-first.              |
| **Utilitários**             | [pdfplumber](https://github.com/jsvine/pdfplumber)                                      | Extração de texto de PDFs anexados.                         |

---

## Instalação e Execução Local

### Pré-requisitos

Antes de começar, garanta que você tenha instalado:

- **Python 3.8+**
- **pip**

---

### Configurar Ambiente Virtual e Dependências

É recomendado o uso de um **ambiente virtual (venv)** para isolar as dependências do projeto.

#### Criar e Ativar o Ambiente

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente
# Linux/macOS:
source venv/bin/activate

# Windows (PowerShell):
# .\venv\Scripts\Activate.ps1
```

#### Instalar Dependências

```bash
pip install -r requirements.txt
```

> Se estiver usando o **spaCy**, talvez seja necessário baixar o modelo de idioma após a instalação:
>
> ```bash
> python -m spacy download pt_core_news_sm
> ```

---

### Configurar Variáveis de Ambiente (`.env`)

Crie um arquivo chamado **`.env`** na raiz do projeto com o seguinte conteúdo:

```ini
GEMINI_API_KEY="SUA_CHAVE_DE_API_DO_GOOGLE_GEMINI"
PORT=5000
```

> Substitua `"SUA_CHAVE_DE_API_DO_GOOGLE_GEMINI"` pela sua chave real obtida no [Google AI Studio](https://aistudio.google.com/).

---

### Executar a Aplicação

Com o ambiente virtual ativo, rode o servidor Flask:

```bash
python3 main.py
```

Acesse a aplicação no navegador:  
**[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## Estrutura do Projeto

```
EMAILCLASSIFICATION/
├── models/                     # Modelos de dados (Peewee)
├── routes/                     # Rotas da aplicação Flask
├── templates/                  # Arquivos HTML (Jinja2)
├── utils/                      # Funções auxiliares e IA/NLP
├── .env.example                # Exemplo de variáveis de ambiente
├── database.py                 # Configuração do banco de dados
├── main.py                     # Ponto de entrada da aplicação
└── requirements.txt            # Dependências do Python
```

---

## Funcionalidades Principais

- Upload e leitura de e-mails (inclusive anexos PDF)
- Classificação automática via **IA Gemini**
- Processamento de texto com **spaCy**
- Armazenamento e histórico de classificações no banco SQLite
- Interface web simples com **Tailwind CSS**

---
