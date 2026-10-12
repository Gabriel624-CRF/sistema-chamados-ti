from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 
app = Flask(__name__)

# Chave usada para manter a sessão do usuário.
# Em um projeto real, use uma chave secreta mais forte.
app.secret_key = "sistema-chamados-ti-chave-demo"

def criar_banco():
    conexao = sqlite3.connect("chamados.db")

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT COLLATE BINARY UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chamados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        prioridade TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pendente',
        usuario_id INTEGER NOT NULL,
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
""")

    conexao.commit()
    conexao.close()

# Usuários de demonstração
USUARIOS = {
    "demo": {
        "senha": "demo123",
        "perfil": "usuario"
    },
    "tecnico": {
        "senha": "tec123",
        "perfil": "tecnico"
    }
}


@app.route("/")
def inicio():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():

    mensagem = None

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "").strip()

        conexao = sqlite3.connect("chamados.db")
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT usuario, senha, perfil
            FROM usuarios
            WHERE usuario = ?
        """, (usuario,))

        dados_usuario = cursor.fetchone()

        conexao.close()

        if dados_usuario and dados_usuario[1] == senha:

            session["usuario"] = dados_usuario[0]
            session["perfil"] = dados_usuario[2]

            if dados_usuario[2] == "usuario":
                return redirect(url_for("usuario"))

            if dados_usuario[2] == "tecnico":
                return redirect(url_for("tecnico"))

        mensagem = "Usuário ou senha incorretos."

    return render_template("login.html", mensagem=mensagem)

@app.route("/usuario", methods=["GET", "POST"])
def usuario():
    if "usuario" not in session:
        return redirect(url_for("login"))

    if session.get("perfil") != "usuario":
        return redirect(url_for("tecnico"))

    mensagem = None

    if request.method == "POST":
        opcao = request.form.get("opcao", "").strip()

        if opcao == "1":
            return redirect(url_for("abrir_chamado"))

        opcoes = {
            "1": "Você escolheu: Abrir chamado.",
            "2": "Você escolheu: Visualizar meus chamados.",
            "3": "Você escolheu: Consultar andamento."
        
        }

        mensagem = opcoes.get(
            opcao,
            "Opção inválida. Digite um número de 1 a 3."
        )

    return render_template(
        "usuario.html",
        usuario=session["usuario"],
        mensagem=mensagem
    )


@app.route("/tecnico", methods=["GET", "POST"])
def tecnico():
    if "usuario" not in session:
        return redirect(url_for("login"))

    if session.get("perfil") != "tecnico":
        return redirect(url_for("usuario"))

    mensagem = None

    if request.method == "POST":
        opcao = request.form.get("opcao", "").strip()

        if opcao == "1":
            return redirect(url_for("chamados_pendentes"))

        if opcao == "7":
            return redirect(url_for("cadastrar_usuario"))

        opcoes = {
            "1": "Você escolheu: Visualizar chamados pendentes.",
            "2": "Você escolheu: Assumir chamado.",
            "3": "Você escolheu: Chamados em atendimento.",
            "4": "Você escolheu: Atualizar chamado.",
            "5": "Você escolheu: Encerrar chamado.",
            "6": "Você escolheu: Visualizar histórico.",
        }

        mensagem = opcoes.get(
            opcao,
            "Opção inválida. Digite um número de 1 a 7."
        )

    return render_template(
        "tecnico.html",
        usuario=session["usuario"],
        mensagem=mensagem
    )

@app.route("/cadastrar-usuario")
def cadastrar_usuario():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if session.get("perfil") != "tecnico":
        return redirect(url_for("usuario"))

    return render_template("cadastrar_usuario.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def inserir_usuarios_iniciais():
    conexao = sqlite3.connect("chamados.db")
    cursor = conexao.cursor()

    usuarios = [
        ("demo", "demo123", "usuario"),
        ("tecnico", "tec123", "tecnico")
    ]

    for usuario, senha, perfil in usuarios:
        cursor.execute("""
            INSERT OR IGNORE INTO usuarios (usuario, senha, perfil)
            VALUES (?, ?, ?)
        """, (usuario, senha, perfil))

    conexao.commit()
    conexao.close()

@app.route("/chamados-pendentes")
def chamados_pendentes():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if session.get("perfil") != "tecnico":
        return redirect(url_for("usuario"))

    return render_template("chamados_pendentes.html")

@app.route("/chamado-detalhes")
def chamado_detalhes():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if session.get("perfil") != "tecnico":
        return redirect(url_for("usuario"))

    return render_template("chamado_detalhes.html")

@app.route("/abrir-chamado", methods=["GET", "POST"])
@app.route("/abrir-chamado", methods=["GET", "POST"])
def abrir_chamado():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if session.get("perfil") != "usuario":
        return redirect(url_for("tecnico"))

    if request.method == "POST":

        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        prioridade = request.form.get("prioridade", "").strip()

        conexao = sqlite3.connect("chamados.db")
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE usuario = ?
        """, (session["usuario"],))

        usuario = cursor.fetchone()

        if usuario:
            cursor.execute("""
                INSERT INTO chamados
                (titulo, descricao, prioridade, usuario_id)
                VALUES (?, ?, ?, ?)
            """, (
                titulo,
                descricao,
                prioridade,
                usuario[0]
            ))

            conexao.commit()

        conexao.close()

        return redirect(url_for("usuario"))

    return render_template("abrir_chamado.html")

if __name__ == "__main__":
    criar_banco()
    inserir_usuarios_iniciais()
    app.run(debug=True)