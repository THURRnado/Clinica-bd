from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from datetime import datetime


#Tela de inicio

def tela_inicio(request):

    # Executar uma consulta SQL para selecionar todos os dados da tabela pacientes
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Pacientes")
        resultados = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute('''
        SELECT p.id
        FROM pacientes p
        WHERE p.id IN (
                       SELECT id_paciente 
                       FROM internado
        )
        
        ''' )
        resultados2 = [row[0] for row in cursor.fetchall()]

    return render(request, 'telaInicio.html', {'pacientes':resultados, 'consulta_marcada':resultados2})


#LISTAR TABELA

def mostrar_pessoas(request):
    # Executar uma consulta SQL para selecionar todos os dados da tabela pacientes
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Pacientes")
        resultados = cursor.fetchall()

    # Renderizar um template com os resultados da consulta
    return render(request, 'index.html', {'resultados': resultados})


def mostrar_medicos(request):
    # Executar uma consulta SQL para selecionar todos os dados da tabela médico
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM medico")
        resultados = cursor.fetchall()

    # Renderizar um template com os resultados da consulta
    return render(request, 'form-medico.html', {'resultados': resultados})


def mostrar_quartos(request):
    # Executar uma consulta SQL para selecionar todos os dados da tabela quarto
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM quarto")
        resultados = cursor.fetchall()

    # Renderizar um template com os resultados da consulta
    return render(request, 'form-quarto.html', {'resultados': resultados})



#ADICIONAR ELEMENTO

def adicionar_elemento_paciente(id, nome, idade, sexo, peso, altura, cpf):
    with connection.cursor() as cursor:
        # Consulta SQL para inserir um novo elemento na tabela
        sql = "INSERT INTO Pacientes (id, nome, idade, sexo, peso, altura, cpf) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        # Valores a serem inseridos
        valores = (id, nome, idade, sexo, peso, altura, cpf)
        # Executar a consulta SQL
        cursor.execute(sql, valores)

def adicionar_paciente(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        sexo = request.POST.get('sexo')
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        cpf = request.POST.get('cpf')
        
        adicionar_elemento_paciente(id, nome, idade, sexo, peso, altura, cpf)
        
        return redirect('inicio')
    else:
        return render(request, 'form-adicionar-paciente.html')
    

def adicionar_elemento_medico(id_medico, nome, especializacao):

    with connection.cursor() as cursor:
        # Consulta SQL para inserir um novo elemento na tabela
        sql = "INSERT INTO medico (id_medico, nome, especializacao) VALUES (%s, %s, %s)"
        # Valores a serem inseridos
        valores = (id_medico, nome, especializacao)
        # Executar a consulta SQL
        cursor.execute(sql, valores)

def adicionar_medico(request):
    if request.method == 'POST':
        id_medico = request.POST.get('id_medico')
        nome = request.POST.get('nome')
        especializacao = request.POST.get('especializacao')
        
        adicionar_elemento_medico(id_medico, nome, especializacao)
        
        return redirect('tabela_medico')
    else:
        return render(request, 'form-adicionar-medico.html')
    

def adicionar_elemento_quarto(cod_quarto, numero_quarto):

    with connection.cursor() as cursor:
        # Consulta SQL para inserir um novo elemento na tabela
        sql = "INSERT INTO quarto (cod_quarto, numero_quarto) VALUES (%s, %s)"
        # Valores a serem inseridos
        valores = (cod_quarto, numero_quarto)
        # Executar a consulta SQL
        cursor.execute(sql, valores)

def adicionar_quarto(request):
    if request.method == 'POST':
        cod_quarto = request.POST.get('cod_quarto')
        numero_quarto = request.POST.get('numero_quarto')
        
        adicionar_elemento_quarto(cod_quarto, numero_quarto)
        
        return redirect('tabela_quarto')
    else:
        return render(request, 'form-adicionar-quarto.html')
    



#EXCLUIR ELEMENTO

def excluir_pessoa(request, paciente_id):
    if request.method == 'POST':
        # Se conectando ao banco de dados e execute a consulta SQL para excluir o paciente
        with connection.cursor() as cursor:
            sql = "DELETE FROM Pacientes WHERE id = %s"
            cursor.execute(sql, [paciente_id])
        
         # Retornar uma resposta JSON indicando que o paciente foi excluída com sucesso
        return redirect('inicio')
    else:
        # Retornar uma resposta de erro se a solicitação não for POST
        return HttpResponse('Apenas requisições POST são permitidas para excluir uma pessoa.')
    

def excluir_medico(request, medico_id):
    if request.method == 'POST':
        # Se conectando ao banco de dados e execute a consulta SQL para excluir o medico
        with connection.cursor() as cursor:
            sql = "DELETE FROM medico WHERE id_medico = %s"
            cursor.execute(sql, [medico_id])
        
         # Retornar uma resposta JSON indicando que o medico foi excluída com sucesso
        return redirect('tabela_medico')
    else:
        # Retornar uma resposta de erro se a solicitação não for POST
        return HttpResponse('Apenas requisições POST são permitidas para excluir uma pessoa.')
    

def excluir_quarto(request, quarto_cod):
    if request.method == 'POST':
        # Se conectando ao banco de dados e execute a consulta SQL para excluir o quarto
        with connection.cursor() as cursor:
            sql = "DELETE FROM quarto WHERE cod_quarto = %s"
            cursor.execute(sql, [quarto_cod])
        
         # Retornar uma resposta JSON indicando que o quarto foi excluída com sucesso
        return redirect('tabela_quarto')
    else:
        # Retornar uma resposta de erro se a solicitação não for POST
        return HttpResponse('Apenas requisições POST são permitidas para excluir uma pessoa.')

    

#EDITAR ELEMENTO
    
def editar_pessoa(request, paciente_id):
    if request.method == 'GET':
        # Consultar o banco de dados para obter os dados da pessoa com o ID fornecido
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Pacientes WHERE id = %s"
            cursor.execute(sql, [paciente_id])
            pessoa = cursor.fetchone()
        
        # Renderizar um formulário de edição com os dados da pessoa
        return render(request, 'form-editar-paciente.html', {'pessoa': pessoa})
    elif request.method == 'POST':
        # Obter os dados do formulário de edição
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        sexo = request.POST.get('sexo')
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        cpf = request.POST.get('cpf')
        
        # Atualizar os dados da pessoa no banco de dados
        with connection.cursor() as cursor:
            sql = "UPDATE Pacientes SET nome = %s, idade = %s, sexo = %s, peso = %s, altura = %s, cpf = %s WHERE id = %s"
            cursor.execute(sql, [nome, idade, sexo, peso, altura, cpf, paciente_id])
        
        # Redirecionar de volta para a página inicial após a edição
        return redirect('inicio')
    

def editar_medico(request, medico_id):
    if request.method == 'GET':
        # Consultar o banco de dados para obter os dados do medico com o ID fornecido
        with connection.cursor() as cursor:
            sql = "SELECT * FROM medico WHERE id_medico = %s"
            cursor.execute(sql, [medico_id])
            pessoa = cursor.fetchone()
        
        # Renderizar um formulário de edição com os dados do medico
        return render(request, 'form-editar-medico.html', {'pessoa': pessoa})
    elif request.method == 'POST':
        # Obter os dados do formulário de edição
        nome = request.POST.get('nome')
        especializacao = request.POST.get('especializacao')
        
        # Atualizar os dados do medico no banco de dados
        with connection.cursor() as cursor:
            sql = "UPDATE medico SET nome = %s, especializacao = %s WHERE id_medico = %s"
            cursor.execute(sql, [nome, especializacao, medico_id])
        
        # Redirecionar de volta para a página inicial após a edição
        return redirect('tabela_medico')
    

def editar_quarto(request, quarto_cod):
    if request.method == 'GET':
        # Consultar o banco de dados para obter os dados da pessoa com o ID fornecido
        with connection.cursor() as cursor:
            sql = "SELECT * FROM quarto WHERE cod_quarto = %s"
            cursor.execute(sql, [quarto_cod])
            pessoa = cursor.fetchone()
        
        # Renderizar um formulário de edição com os dados do quarto
        return render(request, 'form-editar-quarto.html', {'pessoa': pessoa})
    elif request.method == 'POST':
        # Obter os dados do formulário de edição
        numero_quarto = request.POST.get('numero_quarto')
        
        # Atualizar os dados do quarto no banco de dados
        with connection.cursor() as cursor:
            sql = "UPDATE quarto SET numero_quarto = %s WHERE cod_quarto = %s"
            cursor.execute(sql, [numero_quarto, quarto_cod])
        
        # Redirecionar de volta para a página inicial após a edição
        return redirect('tabela_quarto')
    

#FILTRAR ELEMENTO

def filtrar_medico_tabela(request):
    # Verificar se o parâmetro de consulta 'nome' está presente na solicitação GET
    if 'nome' in request.GET:
        nome = request.GET['nome']
        # Consultar o banco de dados para obter os medicos com o nome fornecido
        with connection.cursor() as cursor:
            sql = "SELECT * FROM medico WHERE nome LIKE %s"
            cursor.execute(sql, ['%' + nome + '%'])
            resultados = cursor.fetchall()
    else:
        # Se nenhum nome foi fornecido, retornar todos os medicos
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM medico")
            resultados = cursor.fetchall()

    # Renderizar o template com os resultados da consulta
    return render(request, 'form-medico.html', {'resultados': resultados})


def filtrar_pacientes_tabela(request):
    # Verificar se o parâmetro de consulta 'nome' está presente na solicitação GET
    if 'nome' in request.GET:
        nome = request.GET['nome']
        # Consultar o banco de dados para obter os pacientes com o nome fornecido
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Pacientes WHERE nome LIKE %s"
            cursor.execute(sql, ['%' + nome + '%'])
            resultados = cursor.fetchall()
    else:
        # Se nenhum nome foi fornecido, retornar todos os pacientes
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Pacientes")
            resultados = cursor.fetchall()

    # Renderizar o template com os resultados da consulta
    return render(request, 'index.html', {'resultados': resultados})


def filtrar_quarto_tabela(request):
    # Verificar se o parâmetro de consulta 'nome' está presente na solicitação GET
    if 'numero_quarto' in request.GET:
        numero_quarto = request.GET['numero_quarto']
        # Consultar o banco de dados para obter os qaurtos com o numero fornecido
        with connection.cursor() as cursor:
            sql = "SELECT * FROM quarto WHERE numero_quarto LIKE %s"
            cursor.execute(sql, ['%' + numero_quarto + '%'])
            resultados = cursor.fetchall()
    else:
        # Se nenhum nome foi fornecido, retornar todos os quartos
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM quarto")
            resultados = cursor.fetchall()

    # Renderizar o template com os resultados da consulta
    return render(request, 'form-quarto.html', {'resultados': resultados})


def filtrar_pacientes_inicio(request):
    # Verificar se o parâmetro de consulta 'nome' está presente na solicitação GET
    if 'nome' in request.GET:
        nome = request.GET['nome']
        # Consultar o banco de dados para obter os pacientes com o nome fornecido
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Pacientes WHERE nome LIKE %s"
            cursor.execute(sql, ['%' + nome + '%'])
            resultados = cursor.fetchall()
    else:
        # Se nenhum nome foi fornecido, retornar todos os pacientes
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Pacientes")
            resultados = cursor.fetchall()

    # Renderizar o template com os resultados da consulta
    return render(request, 'telaInicio.html', {'pacientes': resultados})


#CONSULTA

def mostrar_consultas(request):
    with connection.cursor() as cursor:
            cursor.execute('''SELECT p.id ,m.nome, p.nome, q.numero_quarto, i.data_internado  
                              FROM internado i, quarto q, medico m, pacientes p
                              WHERE i.id_paciente = p.id AND i.id_medico = m.id_medico AND i.cod_quarto = q.cod_quarto''')
            resultados = cursor.fetchall()
    
    return render(request, 'form-consultas.html', {'consultas':resultados})


def excluir_consulta(request, paciente_id):
    if request.method == 'POST':
        # Se conectando ao banco de dados e execute a consulta SQL para excluir a pessoa
        with connection.cursor() as cursor:
            sql = "DELETE FROM internado WHERE id_paciente = %s"
            cursor.execute(sql, [paciente_id])
        
         # Retornar uma resposta JSON indicando que a pessoa foi excluída com sucesso
        return redirect('tabela_consultas')
    else:
        # Retornar uma resposta de erro se a solicitação não for POST
        return HttpResponse('Apenas requisições POST são permitidas para excluir uma pessoa.')



def consulta_elementos(request):
    with connection.cursor() as cursor:
        # Consulta SQL para selecionar médicos que não estão na tabela internado
        sql_medicos = """
            SELECT id_medico, nome AS nome_medico, especializacao
            FROM medico m
        """
        cursor.execute(sql_medicos)
        medicos = cursor.fetchall()

        # Consulta SQL para selecionar pacientes
        sql_pacientes = """
            SELECT p.id, p.nome AS nome_paciente
            FROM pacientes p
            WHERE p.id NOT IN(
                SELECT id_paciente
                FROM internado
            )
        """
        cursor.execute(sql_pacientes)
        pacientes = cursor.fetchall()

        # Consulta SQL para selecionar quartos
        sql_quartos = """
            SELECT q.cod_quarto, q.numero_quarto
            FROM quarto q
            WHERE q.cod_quarto NOT IN(
                SELECT cod_quarto
                FROM internado
            )
        """
        cursor.execute(sql_quartos)
        quartos = cursor.fetchall()

        data_atual = datetime.now().strftime('%Y-%m-%dT%H:%M')  

    return render(request, 'form-internado.html', {'medicos': medicos, 'pacientes': pacientes, 'quartos': quartos, 'data_atual': data_atual})


def adicionar_elemento_internado(id_medico, id_paciente, data_internado, cod_quarto):

    with connection.cursor() as cursor:
        # Consulta SQL para inserir um novo elemento na tabela
        sql = "INSERT INTO internado (id_medico, id_paciente, data_internado, cod_quarto) VALUES (%s, %s, %s, %s)"
        # Valores a serem inseridos
        valores = (id_medico, id_paciente, data_internado, cod_quarto)
        # Executar a consulta SQL
        cursor.execute(sql, valores)

def adicionar_internado(request):
    if request.method == 'POST':
        id_medico = request.POST.get('id_medico')
        id_paciente = request.POST.get('id_paciente')
        data_internado = request.POST.get('data_internado')
        cod_quarto = request.POST.get('cod_quarto')
        
        adicionar_elemento_internado(id_medico, id_paciente, data_internado, cod_quarto)
        
        return redirect('tela_inicio')
    else:
        return render(request, 'form-adicionar-internado.html')


#RELATORIO

def tabela_relatorio(request):
    # Executar uma consulta SQL para selecionar todos os dados da tabela relatorio
    with connection.cursor() as cursor:
        cursor.execute("SELECT num_consultas FROM relatorio")
        resultados2 = cursor.fetchall()
        
        for resultado in resultados2:
            num_consultas = resultado[0]

            # Chamar a stored procedure para calcular a receita
            cursor.execute("CALL Receita(%s, @valor_total)", [num_consultas])

            # Selecionar o valor calculado da variável @valor_total
            cursor.execute("SELECT @valor_total")
            valor_total = cursor.fetchone()[0]

            # Atualizar a coluna receita na tabela relatorio com o valor calculado
            cursor.execute("UPDATE relatorio SET receita = %s WHERE num_consultas = %s", [valor_total, num_consultas])

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM relatorio")
        resultados = cursor.fetchall()

    return render(request, 'relatorio.html', {'relatorio':resultados})



#HISTORICO


def tabela_historico(request):
    # Executar uma consulta SQL para selecionar todos os dados da tabela pessoas
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM historico")
        resultados = cursor.fetchall()

    return render(request, 'historico.html', {'historico':resultados})