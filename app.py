import flet as ft  # Importa a biblioteca Flet para criação da interface gráfica
from banco_dados import  remover_turma, listar_turma, adicionar_aluno_na_turma, adicionar_turma, adicionar_aluno, filtrar_alunos_por_turma, filtrar_alunos_por_nome, remover_aluno, atualizar_aluno, listar_alunos
from datetime import datetime  # Importa as funções para listar alunos e turmas do banco de dados

def app(page: ft.Page):  # Função principal que recebe a página como parâmetro

    def tela_inicial():
        page.controls.clear()  # Limpa a página
        page.title = 'controle de alunos'  # Define o título da página
        page.theme_mode = ft.ThemeMode.LIGHT  # Define o tema da página como claro
        page.padding = ft.padding.only(top=20, left=35)  # Define o padding da página

        # Criação do título do aplicativo
        titulo = ft.Text(
            "Sistema de Cadastro de Alunos",  # Texto do título
            size=30,  # Tamanho da fonte
            weight=ft.FontWeight.BOLD,  # Peso da fonte (negrito)
            color=ft.colors.BLUE,  # Cor do texto
            text_align=ft.TextAlign.END,  # Alinhamento do texto (direita)
        )
        page.add(titulo)
        
        page.add(
                    ft.Column([ 
                        ft.FloatingActionButton(icon=ft.Icons.SCHOOL_ROUNDED, text="Alunos", on_click=alunos_menu),
                        ft.FloatingActionButton(icon=ft.Icons.PEOPLE_ALT_ROUNDED, text="Turmas", on_click=turmas_menu),
                    ])
                )

    # Função para mostrar a segunda tela
    def alunos_menu(e):
        page.controls.clear()  # Limpa a página
        page.add(
            ft.Column(
                [
                    ft.ElevatedButton(icon=ft.Icons.ARROW_BACK,text="Voltar", on_click=lambda e: tela_inicial())
                ]
            )
        )
        page.update()

        botões = [
                ft.FloatingActionButton(icon=ft.Icons.ADD_BOX, text='Adicionar aluno'),
                 ft.FloatingActionButton(icon=ft.Icons.PEOPLE, text='Pesquisar alunos'),
                ft.FloatingActionButton(icon=ft.Icons.ADD_BOX, text='Adicionar aluno na turma'),
                ft.FloatingActionButton(icon=ft.Icons.DOWNLOADING_OUTLINED, text='Atualizar aluno'),
                ft.FloatingActionButton(icon=ft.Icons.PEOPLE, text='Todos os alunos', on_click=lista_alunos),
                ft.FloatingActionButton(icon=ft.Icons.HIGHLIGHT_REMOVE_OUTLINED, text='Remover aluno')
            ]

            # Organizando os botões na tela em uma coluna
        page.add(ft.Column(controls=botões))

        page.update()  # Atualiza a página
    

        
    def lista_alunos(e):
        page.controls.clear()  # Limpa a página
        page.add(
                ft.Column(
                    [
                        ft.ElevatedButton(icon=ft.Icons.ARROW_BACK,text="Voltar", on_click=alunos_menu)
                    ]
                )
            )
        page.update()
        alunos = listar_alunos()  # Obtém a lista de alunos do banco de dados
        # Cria uma tabela para exibir os dados dos alunos
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Idade")),
                ft.DataColumn(ft.Text("Faixa")),
                ft.DataColumn(ft.Text("Número")),
                ft.DataColumn(ft.Text("Data de Nascimento")),
                ft.DataColumn(ft.Text("Data de Cadastro")),
                ft.DataColumn(ft.Text("Turma")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(aluno.id))),
                        ft.DataCell(ft.Text(aluno.nome)),
                        ft.DataCell(ft.Text(str(aluno.idade))),
                        ft.DataCell(ft.Text(aluno.faixa)),
                        ft.DataCell(ft.Text(aluno.numero)),
                        ft.DataCell(ft.Text(aluno.data_nascimento)),
                        ft.DataCell(ft.Text(aluno.data_cadastro)),
                        ft.DataCell(ft.Text(str(aluno.turma.nome))),
                    ]
                )
                for aluno in alunos  # Para cada aluno na lista, cria uma linha na tabela
            ]
        )

        # Cria uma coluna com a tabela de alunos e a opção de rolagem automática
        content = ft.Column(
            controls=[table],
            scroll=ft.ScrollMode.AUTO,
            width=2000,
            height=600
        )

        # Adiciona o conteúdo com rolagem à página
        page.add(content)
        page.update()  # Atualiza a página

    
    def turmas_menu(e): 
        page.controls.clear()  # Limpa a página
        page.add(
            ft.Column(
                [
                    ft.ElevatedButton(icon=ft.Icons.ARROW_BACK,text="Voltar", on_click=lambda e: tela_inicial())
                ]
            )
        )
        page.update()
        
        # Recupera a lista de turmas
        turmas = listar_turma()
        
        botoes_turmas = []
        for turma in turmas:
            page.add(ft.FloatingActionButton(icon=ft.Icons.PEOPLE, text='Todos os alunos', on_click=lista_alunos))
            botoes_turmas.append(
                ft.FloatingActionButton(
                    icon=ft.Icons.PEOPLE_ALT_ROUNDED,
                    text=f'{turma.nome}',
                    on_click=lambda e, t=turma: filtrar_alunos_turma(t.id)
                )
            )

        # Exibe todos os botões dentro de uma coluna
        page.add(ft.Column(controls=botoes_turmas))
        
        # Atualiza a página
        page.update()
    
    def filtrar_alunos_turma(id_turma):
        page.controls.clear()  # Limpa a página
        page.add(
                ft.Column(
                    [
                        ft.ElevatedButton(icon=ft.Icons.ARROW_BACK,text="Voltar", on_click=turmas_menu)
                    ]
                )
            )
        page.update()
        alunos = filtrar_alunos_por_turma(id_turma)
        # Cria uma tabela para exibir os dados dos alunos
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Idade")),
                ft.DataColumn(ft.Text("Faixa")),
                ft.DataColumn(ft.Text("Número")),
                ft.DataColumn(ft.Text("Data de Nascimento")),
                ft.DataColumn(ft.Text("Data de Cadastro")),
                ft.DataColumn(ft.Text("Turma")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(aluno.id))),
                        ft.DataCell(ft.Text(aluno.nome)),
                        ft.DataCell(ft.Text(str(aluno.idade))),
                        ft.DataCell(ft.Text(aluno.faixa)),
                        ft.DataCell(ft.Text(aluno.numero)),
                        ft.DataCell(ft.Text(aluno.data_nascimento)),
                        ft.DataCell(ft.Text(aluno.data_cadastro)),
                        ft.DataCell(ft.Text(str(aluno.turma.nome))),
                    ]
                )
                for aluno in alunos  # Para cada aluno na lista, cria uma linha na tabela
            ]
        )

        # Cria uma coluna com a tabela de alunos e a opção de rolagem automática
        content = ft.Column(
            controls=[table],
            scroll=ft.ScrollMode.AUTO,
            width=2000,
            height=600
        )

        # Adiciona o conteúdo com rolagem à página
        page.add(content)
        page.update()  # Atualiza a página






    tela_inicial()
ft.app(app)
