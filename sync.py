from database import conectar
from database_amt import conectar_amt


def sincronizar_pendentes():

    print("Sincronizador iniciado...")

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM fila_sincronizacao
        WHERE status = 'PENDENTE'
        ORDER BY id
    """)

    fila = cursor.fetchall()

    print(f"Encontrados {len(fila)} registro(s) pendente(s).")

    for item in fila:

        try:

            print(f"Sincronizando registro {item['registro_id']}...")

            cursor.execute("""
                SELECT *
                FROM usuarios
                WHERE id = %s
            """, (item["registro_id"],))

            usuario = cursor.fetchone()

            if not usuario:
                print("Usuário não encontrado.")
                continue

            conexao_amt = conectar_amt()
            cursor_amt = conexao_amt.cursor()

            cursor_amt.execute("""
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
                    numero,
                    bairro,
                    cidade,
                    latitude,
                    longitude,
                    aceite_lgpd,
                    data_cadastro
                )
                VALUES
                (
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (

                usuario["nome"],
                usuario["cpf"],
                usuario["email"],
                usuario["telefone"],
                usuario["sexo"],
                usuario["data_nascimento"],
                usuario["meio_transporte"],
                usuario["dias_utilizacao_semana"],
                usuario["cep"],
                usuario["rua"],
                usuario["numero"],
                usuario["bairro"],
                usuario["cidade"],
                usuario["latitude"],
                usuario["longitude"],
                usuario["aceite_lgpd"],
                usuario["data_cadastro"]

            ))

            conexao_amt.commit()

            cursor.execute("""
                UPDATE fila_sincronizacao
                SET
                    status = 'SINCRONIZADO',
                    data_sincronizacao = NOW()
                WHERE id = %s
            """, (item["id"],))

            conexao.commit()

            cursor_amt.close()
            conexao_amt.close()

            print("Enviado para o banco da AMT.")

        except Exception as erro:

            print(f"Erro ao sincronizar registro {item['registro_id']}: {erro}")

            cursor.execute("""
                UPDATE fila_sincronizacao
                SET
                    status = 'ERRO',
                    tentativas = tentativas + 1,
                    ultimo_erro = %s
                WHERE id = %s
            """, (
                str(erro),
                item["id"]
            ))

            conexao.commit()

    cursor.close()
    conexao.close()