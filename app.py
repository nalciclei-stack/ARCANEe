from flask import Flask, render_template, request

app = Flask(__name__)

condicoes = {
    "obesidade": {
        "titulo": "Obesidade",
        "definicao": "Doença crônica multifatorial caracterizada pelo acúmulo excessivo de gordura corporal, associada a risco aumentado de morbimortalidade.",
        "fisiopatologia": "Relacionada ao balanço energético positivo crônico, resistência à insulina, inflamação sistêmica de baixo grau e alterações hormonais como leptina e grelina.",
        "diagnostico": "IMC ≥ 30 kg/m², circunferência abdominal elevada e avaliação de composição corporal.",
        "tratamento": "Déficit calórico moderado, dieta rica em fibras, proteínas adequadas, controle de carboidratos simples, exercício físico estruturado.",
        "evidencia": "Diretrizes baseadas em OMS, ADA e estudos clínicos randomizados sobre restrição energética e terapia comportamental."
    },
    "diabetes": {
        "titulo": "Diabetes Mellitus Tipo 2",
        "definicao": "Distúrbio metabólico caracterizado por hiperglicemia persistente devido à resistência insulínica e/ou deficiência relativa de insulina.",
        "fisiopatologia": "Resistência periférica à insulina, aumento da produção hepática de glicose e disfunção progressiva das células beta pancreáticas.",
        "diagnostico": "Glicemia ≥126 mg/dL em jejum ou HbA1c ≥6,5%.",
        "tratamento": "Controle de carboidratos, baixo índice glicêmico, fracionamento alimentar, fibras solúveis, controle de peso.",
        "evidencia": "Baseado em diretrizes da American Diabetes Association e revisões sistemáticas recentes."
    },
    "hipertensao": {
        "titulo": "Hipertensão Arterial",
        "definicao": "Condição clínica caracterizada por níveis elevados e sustentados de pressão arterial.",
        "fisiopatologia": "Ativação do sistema renina-angiotensina, retenção de sódio, disfunção endotelial.",
        "diagnostico": "PA ≥ 140/90 mmHg em múltiplas aferições.",
        "tratamento": "Dieta DASH, redução de sódio (<2g/dia), aumento de potássio, frutas, vegetais.",
        "evidencia": "Diretrizes da Sociedade Brasileira de Cardiologia e meta-análises sobre dieta DASH."
    }
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/anamnese", methods=["GET", "POST"])
def anamnese():
    if request.method == "POST":
        peso = float(request.form["peso"])
        altura = float(request.form["altura"]) / 100
        imc = peso / (altura ** 2)

        if imc < 18.5:
            diagnostico = "Baixo peso"
            explicacao = "IMC abaixo do recomendado. Pode indicar déficit energético ou nutricional."
        elif 18.5 <= imc < 25:
            diagnostico = "Eutrofia"
            explicacao = "IMC dentro da faixa adequada."
        elif 25 <= imc < 30:
            diagnostico = "Sobrepeso"
            explicacao = "Risco aumentado para doenças metabólicas."
        else:
            diagnostico = "Obesidade"
            explicacao = "Alto risco cardiometabólico. Recomenda-se acompanhamento profissional."

        return render_template("resultado.html", imc=round(imc,2), diagnostico=diagnostico, explicacao=explicacao)

    return render_template("anamnese.html")

@app.route("/biblioteca")
def biblioteca():
    return render_template("biblioteca.html", condicoes=condicoes)

@app.route("/condicao/<nome>")
def condicao(nome):
    dados = condicoes.get(nome)
    return render_template("condicao.html", dados=dados)

@app.route("/servicos")
def servicos():
    return render_template("servicos.html")

if __name__ == "__main__":
    app.run(debug=True)