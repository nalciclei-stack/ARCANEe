from flask import Flask, render_template, request, redirect, session, url_for
import random

app = Flask(__name__)
app.secret_key = "noxus_nutri_2026"

# =========================================================
# BASE DE DADOS COMPLETA (MANTIDA INTEGRALMENTE)
# =========================================================

ARTIGOS_WIKI = {
    "Patologias Metabólicas": {
        "Obesidade": {
            "o_que_e": "A obesidade é uma doença crônica caracterizada pelo acúmulo excessivo de gordura corporal...",
            "recomendacoes": "Adotar alimentação baseada em alimentos in natura...",
            "cor": "#10b981"
        },
        "Diabetes Mellitus": {
            "o_que_e": "O diabetes mellitus é uma doença metabólica caracterizada pelo aumento da glicose...",
            "recomendacoes": "Controlar ingestão de carboidratos, priorizar alimentos de baixo índice glicêmico...",
            "cor": "#059669"
        },
        "Hipertensão Arterial": {
            "o_que_e": "A hipertensão arterial é uma condição crônica caracterizada pela elevação persistente...",
            "recomendacoes": "Reduzir consumo de sal, evitar alimentos industrializados...",
            "cor": "#047857"
        },
        "Dislipidemias": {
            "o_que_e": "Alterações nos níveis de lipídios no sangue, como colesterol e triglicerídeos...",
            "recomendacoes": "Reduzir gorduras saturadas, evitar frituras...",
            "cor": "#065f46"
        }
    },
    "Ciclos da Vida": {
        "Aleitamento Materno": {
            "o_que_e": "O aleitamento materno é a alimentação do bebê exclusivamente com leite materno...",
            "recomendacoes": "Manter amamentação exclusiva até 6 meses...",
            "cor": "#10b981"
        },
        "Introdução Alimentar": {
            "o_que_e": "A introdução alimentar é a fase em que novos alimentos são inseridos...",
            "recomendacoes": "Oferecer alimentos naturais e variados...",
            "cor": "#059669"
        }
    },
    "Carências Nutricionais": {
        "Desnutrição": {
            "o_que_e": "A desnutrição é caracterizada pela deficiência de energia e nutrientes...",
            "recomendacoes": "Aumentar densidade calórica da dieta...",
            "cor": "#10b981"
        }
    }
}

# =========================================================
# ROTAS
# =========================================================

@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/home")
def home():
    return render_template("home.html")

# LOGIN ATUALIZADO (USUÁRIO: admin | SENHA: 1234)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get("username")
        password = request.form.get("password") # Pega a senha do form
        
        # Verifica se é o admin ou login via Google (que não manda senha aqui)
        if user_name == "admin" and password == "1234":
            session["user"] = user_name
            return redirect(url_for("home"))
        elif user_name and not password: # Fallback para campo vazio se necessário
             session["user"] = user_name
             return redirect(url_for("home"))
        else:
            return render_template("login.html", erro="Usuário ou senha incorretos!")
            
    return render_template("login.html")

# ROTA PARA LOGIN GOOGLE
@app.route("/login/google")
def login_google():
    session["user"] = "Usuário Google"
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/anamnese", methods=["GET","POST"])
def anamnese():
    resultado = None
    if request.method == "POST":
        try:
            peso_raw = request.form["peso"].replace(',', '.').strip()
            altura_raw = request.form["altura"].replace(',', '.').strip()
            peso = float(peso_raw)
            altura = float(altura_raw)
            if altura > 3: altura = altura / 100
            imc = peso / (altura ** 2)

            if imc < 18.5: classificacao, risco = "Abaixo do peso", "Risco de desnutrição"
            elif imc < 25: classificacao, risco = "Peso adequado", "Baixo risco"
            elif imc < 30: classificacao, risco = "Sobrepeso", "Risco aumentado"
            else: classificacao, risco = "Obesidade", "Risco elevado"

            resultado = {
                "imc": round(imc, 2),
                "classificacao": classificacao,
                "risco": risco,
                "aviso": "⚠️ Esta análise é uma estimativa e não substitui um nutricionista."
            }
        except Exception:
            resultado = {"erro": "Por favor, insira apenas números."}
    return render_template("anamnese.html", resultado=resultado)

@app.route("/biblioteca", methods=["GET","POST"])
def biblioteca():
    query = request.form.get("busca", "").lower()
    resultados = {}
    if query:
        for categoria, itens in ARTIGOS_WIKI.items():
            sub_resultados = {t: i for t, i in itens.items() if query in t.lower() or query in i['o_que_e'].lower()}
            if sub_resultados: resultados[categoria] = sub_resultados
    else:
        resultados = ARTIGOS_WIKI
    return render_template("biblioteca.html", artigos=resultados, busca=query)

@app.route("/kindred", methods=["GET","POST"])
def kindred():
    resposta = None
    if request.method == "POST":
        respostas = ["Creatina ajuda na força.", "Proteína recupera músculo.", "Sono regula hormônios."]
        resposta = random.choice(respostas)
    return render_template("kindred.html", resposta=resposta)

@app.route("/premium")
def premium():
    return render_template("premium.html")

@app.route("/consulta", methods=["GET","POST"])
def consulta():
    mensagem = None
    if request.method == "POST":
        nome = request.form.get("nome")
        data = request.form.get("data")
        mensagem = f"✔ Consulta solicitada para {nome} no dia {data}."
    return render_template("consulta.html", mensagem=mensagem)

if __name__ == "__main__":
    app.run(debug=True)