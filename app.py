from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app) # Permite a comunicação com o seu arquivo HTML

# Função para conectar ao Banco de Dados SQLite (cria o banco automaticamente se não existir)
def conectar_banco():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    # Cria a tabela de blocos se ela ainda não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocos (
            nome TEXT PRIMARY KEY,
            texto TEXT
        )
    """)
    conexao.commit()
    return conexao

# ROTA PYTHON 1: Buscar o texto de um bloco existente
@app.route("/buscar/<nome_do_bloco>", methods=["GET"])
def buscar_bloco(nome_do_bloco):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT texto FROM blocos WHERE nome = ?", (nome_do_bloco,))
    resultado = cursor.fetchone()
    conexao.close()

    if resultado:
        return jsonify({"texto": resultado[0]})
    else:
        return jsonify({"texto": ""}) # Retorna vazio se o bloco nunca foi salvo

# ROTA PYTHON 2: Salvar ou atualizar o texto de um bloco
@app.route("/salvar", methods=["POST"])
def salvar_bloco():
    dados = request.json
    nome = dados.get("nome")
    texto = dados.get("texto")

    conexao = conectar_banco()
    cursor = conexao.cursor()
    # INSERT OR REPLACE adiciona se for novo, ou atualiza se já existir o mesmo nome
    cursor.execute("INSERT OR REPLACE INTO blocos (nome, texto) VALUES (?, ?)", (nome, texto))
    conexao.commit()
    conexao.close()

    return jsonify({"status": "sucesso"})

if __name__ == "__main__":
    app.run(debug=True)

