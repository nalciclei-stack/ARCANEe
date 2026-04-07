from flask import Flask, render_template, request, redirect, session, url_for
import random

app = Flask(__name__)
app.secret_key = "noxus_nutri_2026"

# =========================================================
# BASE DE DADOS COMPLETA E CORRIGIDA (SEM CORTES)
# =========================================================

ARTIGOS_WIKI = {
    "Patologias Metabólicas": {
        "Obesidade": {
            "o_que_e": "A obesidade é uma doença crônica complexa caracterizada pelo acúmulo excessivo de gordura corporal, resultante de um desequilíbrio persistente entre a ingestão calórica e o gasto energético. É um fator de risco primário para doenças cardiovasculares, diabetes tipo 2 e certas neoplasias.",
            "recomendacoes": "Adotar alimentação baseada em alimentos in natura, aumentar o consumo de fibras, priorizar proteínas magras e estabelecer uma rotina regular de exercícios físicos monitorados.",
            "cor": "#10b981"
        },
        "Diabetes Mellitus": {
            "o_que_e": "O diabetes mellitus é um distúrbio metabólico de etiologia múltipla, caracterizado por hiperglicemia crônica resultante de defeitos na secreção ou na ação da insulina. Pode levar a danos a longo prazo em órgãos como rins, olhos e sistema circulatório.",
            "recomendacoes": "Controlar rigorosamente a ingestão de carboidratos simples, priorizar alimentos de baixo índice glicêmico (integrais) e monitorar a glicemia capilar conforme orientação médica.",
            "cor": "#059669"
        },
        "Hipertensão Arterial": {
            "o_que_e": "A hipertensão arterial é uma condição clínica multifatorial caracterizada pela elevação sustentada dos níveis pressóricos (≥ 140/90 mmHg). Frequentemente é assintomática, mas aumenta significativamente o risco de infarto e AVC.",
            "recomendacoes": "Reduzir drasticamente o consumo de sódio (sal), evitar embutidos e ultraprocessados, e aumentar a ingestão de potássio através de frutas e vegetais frescos.",
            "cor": "#047857"
        },
        "Dislipidemias": {
            "o_que_e": "As dislipidemias são alterações nos níveis de lipídios circulantes, apresentando elevação do colesterol LDL, triglicerídeos ou redução do HDL. Podem levar à formação de placas de ateroma nas artérias.",
            "recomendacoes": "Reduzir o consumo de gorduras saturadas e trans, evitar frituras e alimentos gordurosos, e incluir fontes de gorduras insaturadas como azeite de oliva e oleaginosas.",
            "cor": "#065f46"
        }
    },
    "Ciclos da Vida": {
        "Aleitamento Materno": {
            "o_que_e": "O aleitamento materno é a estratégia isolada que mais previne mortes em crianças menores de cinco anos. O leite humano é nutricionalmente completo e contém anticorpos essenciais para a proteção imunológica do lactente.",
            "recomendacoes": "Manter amamentação exclusiva até os 6 meses de vida, sem oferta de água ou chás, e continuada até os 2 anos ou mais junto à alimentação complementar.",
            "cor": "#10b981"
        },
        "Introdução Alimentar": {
            "o_que_e": "A introdução alimentar é a fase de transição iniciada aos 6 meses, onde novos grupos alimentares são inseridos gradualmente. É fundamental para o desenvolvimento do paladar e coordenação motora da criança.",
            "recomendacoes": "Oferecer alimentos naturais amassados (não liquidificados), variando cores e texturas, respeitando sempre os sinais de saciedade da criança.",
            "cor": "#059669"
        }
    },
    "Carências Nutricionais": {
        "Desnutrição": {
            "o_que_e": "A desnutrição é um estado patológico causado pela deficiência crônica de energia e nutrientes essenciais, resultando em perda de massa magra, comprometimento do sistema imune e atraso no desenvolvimento.",
            "recomendacoes": "Aumentar a densidade calórica e proteica da dieta através de fracionamento das refeições e uso de suplementos sob supervisão de nutricionista.",
            "cor": "#10b981"
        }
    }
}

# =========================================================
# ARMAZENAMENTO DE CONSULTAS (ADIÇÃO)
# =========================================================
DADOS_CONSULTAS = []

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
        password = request.form.get("password") 
        
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
    # VERIFICAÇÃO DE LOGIN: Se não houver usuário na sessão, manda para o login
    if not session.get("user"):
        return redirect(url_for("login"))

    mensagem = None
    if request.method == "POST":
        nome = request.form.get("nome")
        data = request.form.get("data")
        
        # ADIÇÃO: Salvando os dados sem alterar a lógica da mensagem
        DADOS_CONSULTAS.append({"nome": nome, "data": data})
        
        mensagem = f"✔ Consulta solicitada para {nome} no dia {data}."
    return render_template("consulta.html", mensagem=mensagem)

# =========================================================
# NOVA ROTA: DASHBOARD DO NUTRICIONISTA (ADIÇÃO)
# =========================================================
@app.route("/dashboard_nutri")
def dashboard_nutri():
    if session.get("user") == "admin":
        return render_template("dashboard.html", consultas=DADOS_CONSULTAS)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)