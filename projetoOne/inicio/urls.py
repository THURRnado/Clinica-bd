from django.urls import path
from .views import mostrar_pessoas, adicionar_paciente, excluir_pessoa, editar_pessoa, filtrar_pacientes_tabela, tela_inicio, filtrar_pacientes_inicio, mostrar_medicos, adicionar_medico, excluir_medico, editar_medico, filtrar_medico_tabela, mostrar_quartos, adicionar_quarto, excluir_quarto, editar_quarto, filtrar_quarto_tabela, consulta_elementos, adicionar_internado, tabela_relatorio, mostrar_consultas, excluir_consulta, tabela_historico

urlpatterns = [
    path('', tela_inicio, name='tela_inicio'),
    
    path('tabela_pacientes', mostrar_pessoas, name='inicio'),
    path('adicionar_paciente', adicionar_paciente, name='adicionar_elemento_paciente'),
    path('excluir_paciente/<int:paciente_id>/', excluir_pessoa, name='excluir_pessoa'),
    path('editar_paciente/<int:paciente_id>/', editar_pessoa, name='editar_pessoa'),
    path('paciente_filtrado_tabela', filtrar_pacientes_tabela, name='filtrar_pacientes_tabela'),
    path('paciente_filtrado_inicio', filtrar_pacientes_inicio, name='filtrar_pacientes_inicio'),

    path('tabela_medicos', mostrar_medicos, name='tabela_medico'),
    path('adicionar_medico', adicionar_medico, name='adicionar_elemento_medico'),
    path('excluir_medico/<int:medico_id>/', excluir_medico, name='excluir_medico'),
    path('editar_medico/<int:medico_id>/', editar_medico, name='editar_medico'),
    path('medico_filtrado_tabela', filtrar_medico_tabela, name='filtrar_medico_tabela'),

    path('tabela_quartos', mostrar_quartos, name='tabela_quarto'),
    path('adicionar_quarto', adicionar_quarto, name='adicionar_elemento_quarto'),
    path('excluir_quarto/<int:quarto_cod>/', excluir_quarto, name='excluir_quarto'),
    path('editar_quarto/<int:quarto_cod>/', editar_quarto, name='editar_quarto'),
    path('quarto_filtrado_tabela', filtrar_quarto_tabela, name='filtrar_quarto_tabela'),

    path('marcar_consulta', consulta_elementos, name='marcar_consulta'),
    path('adicionar_consulta', adicionar_internado, name='adicionar_elemento_internado'),
    path('tabela_consultas', mostrar_consultas, name='tabela_consultas'),
    path('excluir_consulta/<int:paciente_id>/', excluir_consulta, name='excluir_consulta'),

    path('tabela_relatorio', tabela_relatorio, name='tabela_relatorio'),
    path('tabela_historico', tabela_historico, name='tabela_historico'),
    #path('tabela_relatorio', Receitas, name='tabela_relatorio'),

    # Outros padrões de URL
]
