"""
EcoScore - Sistema de Hábitos Sustentáveis

Principais funcionalidades:
1. Gerenciamento de usuários:
   - Cadastro, login e logout.
   - Proteção de rotas com login_required.

2. Avaliação de hábitos sustentáveis:
   - Recebe respostas do usuário sobre hábitos ambientais e pessoais.
   - Calcula score ambiental, score pessoal, total e nível.
   - Gera alertas para hábitos não cumpridos.
   - Salva resultados em arquivo JSON.

3. Renderização de páginas:
   - Páginas principais: index, score, resultado e links.
   - Páginas auxiliares: pagina1, pagina2, pagina3, pagina4.

4. Funções de suporte:
   - Salvar resultados em JSON.
   - Definir nível baseado no score.
   - Carregar e salvar usuários.

5. Segurança:
   - Uso de session para controle de login.
   - Flash para mensagens de aviso e sucesso.
"""

from flask import Flask, render_template, request, redirect, flash, session, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Ecoscore007'  # chave para sessão e flash

# Caminhos dos arquivos
ARQUIVO_JSON = "resultados.json"
USUARIOS_JSON = "usuarios.json"

# -------------------- FUNÇÕES DE SUPORTE --------------------

# Função para salvar resultados em JSON
def salvar_resultado(dados):
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            historico = json.load(f)
    else:
        historico = []

    historico.append(dados)

    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=4, ensure_ascii=False)

# Função para definir nível
def nivel_por_score(total):
    if total >= 75:
        return "Protetor"
    elif total >= 50:
        return "Guardião"
    elif total >= 25:
        return "Sustentável"
    else:
        return "Iniciante Verde"

# -------------------- FUNÇÕES DE LOGIN --------------------

def carregar_usuarios():
    if not os.path.exists(USUARIOS_JSON):
        return {}
    with open(USUARIOS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(USUARIOS_JSON, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4)

def usuario_logado():
    return "usuario" in session

# Decorador para proteger rotas
def login_required(func):
    def wrapper(*args, **kwargs):
        if not usuario_logado():
            flash("Você precisa estar logado para acessar essa página.")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# -------------------- ROTAS DE LOGIN --------------------

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        usuarios = carregar_usuarios()

        if usuario in usuarios and usuarios[usuario] == senha:
            session["usuario"] = usuario
            flash("Login realizado com sucesso!")
            return redirect(url_for("index"))
        else:
            return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        usuarios = carregar_usuarios()

        if usuario in usuarios:
            return render_template("register.html", erro="Usuário já existe!")

        usuarios[usuario] = senha
        salvar_usuarios(usuarios)

        flash("Cadastro realizado com sucesso! Faça login.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Você saiu da conta.")
    return redirect(url_for("login"))

# -------------------- ROTAS DO ECOSCORE --------------------

@app.route("/index.html")
@login_required
def index():
    return render_template("index.html", usuario=session.get("usuario"))

@app.route("/score.html")
@login_required
def score():
    return render_template("score.html")

@app.route("/resultado.html")
@login_required
def resultado():
    return render_template("resultado.html")

@app.route("/pagina1")
@login_required
def pagina1():
    return render_template("pagina1.html")

@app.route("/pagina2")
@login_required
def pagina2():
    return render_template("pagina2.html")

@app.route("/pagina3")
@login_required
def pagina3():
    return render_template("pagina3.html")

@app.route("/pagina4")
@login_required
def pagina4():
    return render_template("pagina4.html")

@app.route("/links")
@login_required
def links():
    return render_template("links.html")

# -------------------- ROTA DE AVALIAÇÃO --------------------

@app.route("/avaliar", methods=["POST"])
@login_required
def avaliar():
    economia_agua = request.form.get("economia_agua") == "sim"
    consumo_energia = request.form.get("consumo_energia") == "sim"
    reducao_lixo = request.form.get("reducao_lixo") == "sim"
    reutilizacao = request.form.get("reutilizacao") == "sim"
    alimentacao_sustentavel = request.form.get("alimentacao_sustentavel") == "sim"
    transporte = request.form.get("transporte") == "sim"
    separar_lixo = request.form.get("separar_lixo") == "sim"
    descarte_correto = request.form.get("descarte_correto") == "sim"
    escolhas_inteligentes = request.form.get("escolhas_inteligentes") == "sim"
    consumo_consciente = request.form.get("consumo_consciente") == "sim"
    valorize_existente = request.form.get("valorize_existente") == "sim"

    habitos = {
        "Feche a torneira ao escovar os dentes e ao ensaboar a louça. Evite deixar a água correr desnecessariamente.": (economia_agua, "ambiental"),
        "Apague as luzes ao sair de um cômodo e desligue aparelhos eletrônicos quando não estiverem em uso. Isso economiza energia e reduz a conta de luz.": (consumo_energia, "ambiental"),
        "Evite o uso de descartáveis, compre produtos a granel e use os dois lados do papel sempre que possível. Reduz a produção de lixo e protege recursos naturais.": (reducao_lixo, "ambiental"),
        "Reutilize embalagens e conserte objetos antes de descartá-los. Dê uma nova vida aos itens e reduza o desperdício.": (reutilizacao, "ambiental"),
        "Evite desperdício de comida. Planeje suas refeições e aproveite sobras para diminuir impacto ambiental e economizar dinheiro.": (alimentacao_sustentavel, "pessoal"),
        "Use transporte público, bicicleta ou caminhe sempre que possível. Isso reduz emissões de poluentes e melhora sua saúde.": (transporte, "ambiental"),
        "Separe corretamente materiais recicláveis do lixo comum. Plástico, vidro, papel e metal devem ir para recipientes de coleta seletiva.": (separar_lixo, "ambiental"),
        "Descarte pilhas, baterias e lâmpadas em pontos de coleta. Eles estão disponíveis em farmácias, mercados, órgãos públicos e lojas de eletrônicos. Procure um próximo de você!": (descarte_correto, "ambiental"),
        "Ao comprar eletrodomésticos, escolha modelos eficientes em consumo de energia, identificados pelo selo Procel ou similares. Economiza energia e dinheiro.": (escolhas_inteligentes, "ambiental"),
        "Compre produtos de forma consciente e sustentável. Verifique a origem e prefira empresas que adotam práticas responsáveis e éticas.": (consumo_consciente, "pessoal"),
        "Prefira roupas e brinquedos usados, incentivando a economia circular. Doe ou compre itens em brechós e grupos de troca.": (valorize_existente, "pessoal"),
    }

    score_ambiental = 0
    score_pessoal = 0
    alertas = []

    for dica, (cumprido, categoria) in habitos.items():
        if cumprido:
            if categoria == "ambiental":
                score_ambiental += 10
            else:
                score_pessoal += 10
        else:
            alertas.append(dica)

    total = min(score_ambiental + score_pessoal, 100)
    nivel = nivel_por_score(total)

    if total >= 80:
        resultado = "🥇 Excelente! Seus hábitos sustentáveis são muito bons."
    elif 50 <= total < 80:
        resultado = "⚠️ Regular. Alguns hábitos precisam de atenção."
    else:
        resultado = "❌ Ruim. É importante melhorar seus hábitos sustentáveis."

    dados = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score_ambiental": score_ambiental,
        "score_pessoal": score_pessoal,
        "total": total,
        "nivel": nivel,
        "resultado": resultado,
        "usuario": session.get("usuario")
    }
    salvar_resultado(dados)

    return render_template(
        "resultado.html",
        score=total,
        score_ambiental=score_ambiental,
        score_pessoal=score_pessoal,
        nivel=nivel,
        resultado=resultado,
        alertas=alertas
    )

# -------------------- MAIN --------------------
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)