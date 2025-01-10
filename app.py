import flet as ft
from banco_dados import listar_alunos, listar_turma

def app(page: ft.Page):
    # Aplica o tema personalizado para as barras de rolagem
    page.theme_mode = ft.ThemeMode.DARK
    
    def listar_aluno(e):  # Adiciona o parâmetro 'e' para o evento
        # Recupera a lista de alunos e turmas
        alunos = listar_alunos()
        
        # Cria a tabela com os dados dos alunos
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Idade")),
                ft.DataColumn(ft.Text("Faixa")),
                ft.DataColumn(ft.Text("Foto")),
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
                        ft.DataCell(ft.Text(aluno.foto_perfil)),
                        ft.DataCell(ft.Text(aluno.numero)),
                        ft.DataCell(ft.Text(aluno.data_nascimento)),
                        ft.DataCell(ft.Text(aluno.data_cadastro)),
                        ft.DataCell(ft.Text(str(aluno.turma.nome))) ,
                    ]
                )
                for aluno in alunos
            ]
        )
        # Exibe a tabela dentro do contêiner
        page.add(table)
        page.update()

    def listar_turmas(e):
        # Recupera a lista de turmas
        turmas = listar_turma()
        
        # Cria a tabela com os dados das turmas
        table = ft.DataTable(
            columns=[

                ft.DataColumn(ft.Text("Nome")),

            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.FloatingActionButton(turma.nome)),
                    ]
                )
                for turma in turmas
            ]
        )
        # Exibe a tabela dentro do contêiner
        page.add(table)
        page.update()

    # Adiciona os botões flutuantes
    page.add(
        ft.Column([
            ft.FloatingActionButton(icon=ft.Icons.SCHOOL_ROUNDED, text="Alunos", on_click=listar_aluno),
            ft.FloatingActionButton(icon=ft.Icons.PEOPLE_ALT_ROUNDED, text="Turmas", on_click=listar_turmas),
        ])
    )

ft.app(app)
