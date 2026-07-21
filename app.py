from flask import Flask, request, jsonify
from flask_cors import CORS
from database import conectar

app = Flask(__name__)
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

        sql = """
        INSERT INTO usuarios
        (nome, cpf, email, telefone, cep, rua, bairro, cidade)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        valores = (
            dados["nome"],
            dados["cpf"],
            dados["email"],
            dados["telefone"],
            dados["cep"],
            dados["rua"],
            dados["bairro"],
            dados["cidade"]
        )

        cursor.execute(sql, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({"mensagem": "Cadastro realizado com sucesso"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)