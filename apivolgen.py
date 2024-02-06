from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required
import mysql.connector

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = True

# Configuração do banco de dados
db_config = {
    'host': 'tms.cr5qqops6qpx.sa-east-1.rds.amazonaws.com',
    'user': 'root',
    'password': 'NunesST2023',
    'database': 'tms',
}

# Função para conectar ao banco de dados
def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro de conexão ao banco de dados: {err}")
        return None

# Rota para receber dados de cadastro via POST
@app.route('/cadastro', methods=['POST'])
def cadastrar():
    data = request.get_json()

    callType = data.get('callType')
    callDirection = data.get('callDirection')
    agent = data.get('agent')
    agentFirstName = data.get('agentFirstName')
    number = data.get('number')
    callStartTimeLocal = data.get('callStartTimeLocal')
    callEstablishedTimeLocal = data.get('callEstablishedTimeLocal')
    callEndTimeLocal = data.get('callEndTimeLocal')

    # Conectar ao banco de dados
    conexao = connect_db()
    cursor = conexao.cursor()

    # Inserir dados na tabela
    cursor.execute("""
        INSERT INTO cadastro 
        (callTypes, callDirection, extNumber, agentName, callNumber, callStartTime, CallEstablishedTime, callEndTime, cliente) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (callType, callDirection, agent, agentFirstName, number, callStartTimeLocal, callEstablishedTimeLocal, callEndTimeLocal))

    # Commit para salvar as alterações no banco de dados
    conexao.commit()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conexao.close()

    return jsonify({'message': 'Cadastro realizado com sucesso'}), 201

@app.route('/contatotel', methods=['GET'])
def busca():
    numero_telefone = request.args.get('telefone')

    # Conectar ao banco de dados
    conn = connect_db()
    if conn is None:
        return jsonify({'error': 'Erro de conexão ao banco de dados'}), 500

    cursor = conn.cursor()

    # Consultar o banco de dados com base no número de telefone
    cursor.execute("SELECT * FROM Contacts WHERE telefone=%s limit 1;", (numero_telefone,))
    resultado = cursor.fetchall()
    conn.close()

@app.route('/contatoemail', methods=['GET'])
def buscaemail():
    email = request.args.get('email')

    # Conectar ao banco de dados
    conn = connect_db()
    if conn is None:
        return jsonify({'error': 'Erro de conexão ao banco de dados'}), 500

    cursor = conn.cursor()

    # Consultar o banco de dados com base no número de telefone
    cursor.execute("SELECT * FROM Contacts WHERE email=%s limit 1;", (email,))
    resultado = cursor.fetchall()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)