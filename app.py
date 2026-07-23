import bcrypt
import os
from flask import session
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import conectar
from datetime import datetime
from datetime import date
from zoneinfo import ZoneInfo

app = Flask(__name__)
def criptografar_senha(senha):
    return bcrypt.hashpw(
        senha.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verificar_senha(senha, hash_senha):
    return bcrypt.checkpw(
        senha.encode("utf-8"),
        hash_senha.encode("utf-8")
    )
app.secret_key = os.getenv("SECRET_KEY", "meutrue-secret-2026")

SENHA_ADMIN = os.getenv("SENHA_ADMIN", "AMT123456")
CORS(app)


@app.route("/")
def home():
    return "API MEUTRUE funcionando!"


@app.route("/api/cadastro", methods=["POST"])
def cadastro():
    try:
        dados = request.get_json()

        conexao = conectar()
        cursor = conexao.cursor()

        # Verifica CPF
        cursor.execute(
            "SELECT id FROM usuarios WHERE cpf = %s",
            (dados["cpf"],)
        )

        if cursor.fetchone():
            cursor.close()
            conexao.close()

            return jsonify({
                "sucesso": False,
                "mensagem": "CPF já cadastrado."
            }), 400

        # Verifica e-mail
        cursor.execute(
            "SELECT id FROM usuarios WHERE email = %s",
            (dados["email"],)
        )

        if cursor.fetchone():
            cursor.close()
            conexao.close()

            return jsonify({
                "sucesso": False,
                "mensagem": "E-mail já cadastrado."
            }), 400

        # Data e hora de Fortaleza
        agora = datetime.now(ZoneInfo("America/Fortaleza"))

        sql = """
        INSERT INTO usuarios
        (
            nome,
            cpf,
            email,
            telefone,
            sexo,
            data_nascimento,
            meio_transporte,
            dias_utilizacao_semana,
            cep,
            rua,
            bairro,
            cidade,
            aceite_lgpd,
            data_cadastro
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """

        valores = (
            dados["nome"],
            dados["cpf"],
            dados["email"],
            dados["telefone"],
            dados["sexo"],
            dados["data_nascimento"],
            dados["meio_transporte"],
            dados["dias_utilizacao_semana"],
            dados["cep"],
            dados["rua"],
            dados["bairro"],
            dados["cidade"],
            1,
            agora
        )

        cursor.execute(sql, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({
            "sucesso": True,
            "mensagem": "Cadastro realizado com sucesso."
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 500

# ============================================================
# FUNÇÃO PARA CONVERTER DATAS EM JSON
# ============================================================

def serialize(valor):
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    return valor


# ============================================================
# RELATÓRIOS
# ============================================================

@app.route("/api/relatorios", methods=["GET"])
def relatorios():

    try:

        conexao = conectar()
        cursor = conexao.cursor()

        # Total
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]

        # Hoje
        cursor.execute("""
            SELECT COUNT(*)
            FROM usuarios
            WHERE DATE(data_cadastro)=CURDATE()
        """)
        hoje = cursor.fetchone()[0]

        # Mês
        cursor.execute("""
            SELECT COUNT(*)
            FROM usuarios
            WHERE YEAR(data_cadastro)=YEAR(CURDATE())
            AND MONTH(data_cadastro)=MONTH(CURDATE())
        """)
        mes = cursor.fetchone()[0]

        # Ano
        cursor.execute("""
            SELECT COUNT(*)
            FROM usuarios
            WHERE YEAR(data_cadastro)=YEAR(CURDATE())
        """)
        ano = cursor.fetchone()[0]

        # Cidade
        cursor.execute("""
            SELECT cidade, COUNT(*)
            FROM usuarios
            GROUP BY cidade
            ORDER BY COUNT(*) DESC
        """)

        cidades = []

        for cidade, quantidade in cursor.fetchall():
            cidades.append({
                "cidade": cidade,
                "total": quantidade
            })

        # Bairro
        cursor.execute("""
            SELECT bairro, COUNT(*)
            FROM usuarios
            GROUP BY bairro
            ORDER BY COUNT(*) DESC
        """)

        bairros = []

        for bairro, quantidade in cursor.fetchall():
            bairros.append({
                "bairro": bairro,
                "total": quantidade
            })

        # Cadastros por dia
        cursor.execute("""
            SELECT DATE(data_cadastro), COUNT(*)
            FROM usuarios
            GROUP BY DATE(data_cadastro)
            ORDER BY DATE(data_cadastro)
        """)

        dias = []

        for dia, quantidade in cursor.fetchall():
            dias.append({
                "dia": serialize(dia),
                "total": quantidade
            })

                # Primeiro cadastro
        cursor.execute("SELECT MIN(data_cadastro) FROM usuarios")
        primeiro = serialize(cursor.fetchone()[0])

        # Último cadastro
        cursor.execute("SELECT MAX(data_cadastro) FROM usuarios")
        ultimo = serialize(cursor.fetchone()[0])

        # Quantidade cidades
        cursor.execute("SELECT COUNT(DISTINCT cidade) FROM usuarios")
        total_cidades = cursor.fetchone()[0]

        # Quantidade bairros
        cursor.execute("SELECT COUNT(DISTINCT bairro) FROM usuarios")
        total_bairros = cursor.fetchone()[0]

        # ============================================================
        # Meio de transporte
        # ============================================================

        cursor.execute("""
            SELECT meio_transporte, COUNT(*)
            FROM usuarios
            GROUP BY meio_transporte
            ORDER BY COUNT(*) DESC
        """)

        meios_transporte = []

        for meio, quantidade in cursor.fetchall():
            meios_transporte.append({
                "meio_transporte": meio,
                "total": quantidade
            })

        # ============================================================
        # Dias de utilização por semana
        # ============================================================

        cursor.execute("""
            SELECT dias_utilizacao_semana, COUNT(*)
            FROM usuarios
            GROUP BY dias_utilizacao_semana
            ORDER BY dias_utilizacao_semana
        """)

        dias_utilizacao = []

        for dias_semana, quantidade in cursor.fetchall():
            dias_utilizacao.append({
                "dias": dias_semana,
                "total": quantidade
            })

        cursor.close()
        conexao.close()

        return jsonify({

            "total": total,
            "hoje": hoje,
            "mes": mes,
            "ano": ano,

            "cidades": cidades,

            "bairros": bairros,

            "cadastros_por_dia": dias,

            "primeiro_cadastro": primeiro,

            "ultimo_cadastro": ultimo,

            "total_cidades": total_cidades,

            "total_bairros": total_bairros,

            "meios_transporte": meios_transporte,

            "dias_utilizacao": dias_utilizacao

        })

    except Exception as erro:

        return jsonify({
            "erro": str(erro)
        }), 500
    
# ============================================================
# LISTA DE USUÁRIOS
# ============================================================

@app.route("/api/usuarios", methods=["GET"])
def usuarios():

    try:

        conexao = conectar()

        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""

            SELECT *

            FROM usuarios

            ORDER BY data_cadastro DESC

        """)

        dados = cursor.fetchall()

        cursor.close()

        conexao.close()

        return jsonify(dados)

    except Exception as erro:

        return jsonify({

            "erro": str(erro)

        }), 500
    
    # ==========================================
# LOGIN ADMIN
# ==========================================

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    try:
        dados = request.get_json()

        usuario = dados.get("usuario", "")
        senha = dados.get("password", "")

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM administradores
            WHERE usuario=%s
            AND ativo=1
        """, (usuario,))

        admin = cursor.fetchone()

        cursor.close()
        conexao.close()

        if admin and verificar_senha(senha, admin["senha"]):
            session["admin"] = admin["usuario"]

            return jsonify({
                "success": True,
                "nome": admin["nome"]
            })

        return jsonify({
            "success": False,
            "message": "Usuário ou senha inválidos."
        }), 401

    except Exception as e:
        return jsonify({
            "success": False,
            "erro": str(e)
        }), 500
# ==========================================
# VERIFICAR LOGIN
# ==========================================

@app.route("/api/admin/verificar", methods=["GET"])
def admin_verificar():

    if session.get("admin"):
        return jsonify({
            "logado": True
        })

    return jsonify({
        "logado": False
    }), 401


# ==========================================
# LOGOUT
# ==========================================

@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():

    session.clear()

    return jsonify({
        "success": True
    })

# ==========================================
# NOVO ACESSO (USUÁRIO JÁ CADASTRADO)
# ==========================================

@app.route("/api/acesso", methods=["POST"])
def novo_acesso():

    try:

        dados = request.get_json()
        print("Dados recebidos")

        cpf = dados.get("cpf")
        print("CPF:", cpf)

        if not cpf:
            return jsonify({
                "success": False,
                "message": "CPF é obrigatório."
            }), 400

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        # Procura o usuário pelo CPF
        cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE cpf = %s
        """, (cpf,))

        usuario = cursor.fetchone()
        print("USUARIO", usuario)

        if not usuario:
            cursor.close()
            conexao.close()

            return jsonify({
                "success": False,
                "message": "CPF não encontrado."
            }), 404

        # Data e hora atual
        agora = datetime.now(ZoneInfo("America/Fortaleza"))

        # Atualiza o último acesso
        cursor.execute("""
            UPDATE usuarios
            SET ultimo_acesso = %s
            WHERE id = %s
        """, (
            agora,
            usuario["id"]
        ))

        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({
            "success": True,
            "nome": usuario["Nome"],
            "ultimo_acesso": agora.isoformat()
        })

    except Exception as e:
        import traceback

        print("===== ERRO NOVO ACESSO =====")
        traceback.print_exc()
        print("============================")

        return jsonify({
            "success": False,
            "erro": str(e)
        }), 500

@app.route("/gerar-hash/<senha>")
def gerar_hash(senha):
    return criptografar_senha(senha)

if __name__ == "__main__":
    print("API iniciando...")
    app.run(host="0.0.0.0", port=5000, debug=True)