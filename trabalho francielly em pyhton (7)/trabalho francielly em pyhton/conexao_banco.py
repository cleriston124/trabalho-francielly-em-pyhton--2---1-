import mysql.connector

conexao=mysql.connector.connect(host='localhost',database='clientes', user='root',password='@Cleriston13mestre')
if conexao.is_connected():
    print("banco conectado com sucesso")
    cursor=conexao.cursor()

