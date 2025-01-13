import flet as ft  # Importa a biblioteca Flet para criação da interface gráfica
from banco_dados import  remover_turma, listar_turma, adicionar_aluno_na_turma, adicionar_turma, adicionar_aluno, filtrar_alunos_por_turma, filtrar_alunos_por_nome, remover_aluno, atualizar_aluno, listar_alunos
import datetime # Importa as funções para listar alunos e turmas do banco de dados

def app(page: ft.Page):  # Função principal que recebe a página como parâmetro
    def page_resize(e):
        page.value = f"{page.width} px"
        page.update()

        page.on_resize = page_resize

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
                ft.FloatingActionButton(icon=ft.Icons.ADD_BOX, text='Adicionar aluno', on_click=add_aluno),
                ft.FloatingActionButton(icon=ft.Icons.PEOPLE, text='Pesquisar alunos'),
                ft.FloatingActionButton(icon=ft.Icons.DOWNLOADING_OUTLINED, text='Atualizar aluno'),
                ft.FloatingActionButton(icon=ft.Icons.PEOPLE, text='Todos os alunos', on_click=lista_alunos),
                ft.FloatingActionButton(icon=ft.Icons.HIGHLIGHT_REMOVE_OUTLINED, text='Remover aluno', on_click=delete_aluno)
            ]

            # Organizando os botões na tela em uma coluna
        page.add(ft.Column(controls=botões))

        page.update()  # Atualiza a página

    def salvar_aluno(e):
        nome = nome_input.value
        idade = int(idade_input.value)
        faixa = faixa_dropdown.value
        foto_perfil = foto_input.value
        numero = numero_input.value
        data_nascimento = data_nascimento_input.value
        nome_turma = nome_turma_input.value

        adicionar_aluno(nome, idade, faixa, foto_perfil, numero, data_nascimento, nome_turma)

        # Exibe uma mensagem de sucesso
        page.add(ft.Text("Aluno salvo com sucesso!", color=ft.colors.GREEN))

    # Função para criar a interface do formulário
    def add_aluno(e):
        page.controls.clear()  # Limpa a página
        page.add(
            ft.Column(
                [
                    ft.ElevatedButton(icon=ft.Icons.ARROW_BACK, text="Voltar", on_click=alunos_menu)
                ]
            )
        )
        turmas = listar_turma()

        # Inputs do formulário
        global nome_input, idade_input, faixa_dropdown, foto_input, numero_input, data_nascimento_input, data_cadastro_input, nome_turma_input
        
        nome_input = ft.TextField(label="Nome", autofocus=True, width=400)
        idade_input = ft.TextField(label="Idade", keyboard_type=ft.KeyboardType.NUMBER, width=400)
        faixa_dropdown = ft.Dropdown(
            label="Escolha a faixa do aluno",
            width=400,
            options=[
                ft.dropdown.Option("Branca"),
                ft.dropdown.Option("Amarela"),
                ft.dropdown.Option("Laranja"),
                ft.dropdown.Option("Verde"),
                ft.dropdown.Option("Azul"),
                ft.dropdown.Option("Roxa"),
                ft.dropdown.Option("Marrom"),
                ft.dropdown.Option("Preta"),
                ft.dropdown.Option("Coral"),
                ft.dropdown.Option("Vermelha")
            ]
        )
        foto_input = ft.TextField(label="Foto", width=400)
        numero_input = ft.TextField(label="Número", width=400)
        data_nascimento_input = ft.DatePicker(
            first_date=datetime.date(1900, 1, 1),
            last_date=datetime.date(2025, 12, 1),
            on_dismiss=""
        )

        # Inicialize open_celender com um valor padrão
        open_celender = None
        nome_turma_input = None  # Garantir que sempre exista essa variável
        open_celender = ft.ElevatedButton(
                text='Data de nascimento', 
                icon=ft.Icons.CALENDAR_MONTH, 
                on_click= lambda e: page.open(data_nascimento_input)
            )
        if turmas:

            nome_turma_input = ft.Dropdown(
                label="Escolha a turma do aluno",
                options=[(ft.dropdown.Option(turma.nome)) for turma in turmas], 
                width=400
            )
        else:
            # Caso não tenha turmas, exibe mensagem
            nao_tem_turmas = ft.Text("Não tem turmas")
            nome_turma_input = nao_tem_turmas  # Exibe a mensagem ao invés de um dropdown

        # Adicionando os campos e o botão de salvar
        page.add(
            ft.Column(
                [
                    nome_input,
                    idade_input,
                    faixa_dropdown,
                    foto_input,
                    numero_input,
                    open_celender,  # Fallback se não houver open_celender
                    nome_turma_input,  # Pode ser o dropdown ou a mensagem
                    ft.ElevatedButton(text="Salvar", on_click=salvar_aluno)
                ]
            )
        )
        
        page.update()

    def delete_aluno(e):
        page.controls.clear()  # Limpa a página
        page.add(
            ft.Column(
                [
                    ft.ElevatedButton(icon=ft.Icons.ARROW_BACK, text="Voltar", on_click=alunos_menu)
                ]
            )
        )

    # Função para listar os alunos
    def lista_alunos(e):
        page.controls.clear()  # Limpa a página
        page.add(
            ft.Column(
                [
                    ft.ElevatedButton(icon=ft.Icons.ARROW_BACK, text="Voltar", on_click=alunos_menu)
                ]
            )
        )
        page.update()

        alunos = listar_alunos()  # Obtém a lista de alunos do banco de dados

        painel = ft.ExpansionPanelList(
            expand_icon_color=ft.Colors.BLUE,
            elevation=8,
            divider_color=ft.Colors.BLUE,
        )

        # Criação da lista de alunos e suas tabelas
        for aluno in alunos:
            exp = ft.ExpansionPanel(
                header=ft.ListTile(title=ft.Text(f"{aluno.nome}")),
            )

            # Definindo a tabela de dados para o aluno
            tabela = ft.DataTable(
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
                            ft.DataCell(ft.Text(str(aluno.data_nascimento))),
                            ft.DataCell(ft.Text(str(aluno.data_cadastro))),
                            ft.DataCell(ft.Text(str(aluno.turma.nome))),
                        ]
                    )
                ]
            )

            # Criando um painel para o aluno com o botão de exclusão
            exp.content = ft.Column(
                [
                    tabela,
                    ft.ListTile(
                        title=ft.Text(f"Excluir aluno"),
                        subtitle=ft.Text(f"Pressione o ícone para excluir"),
                        trailing=ft.IconButton(ft.Icons.DELETE, on_click=lambda e, aluno=aluno: remover_aluno(aluno.nome))
                    )
                ]
            )

            painel.controls.append(exp)

        # Adicionando o painel à página
        page.add(painel)
        page.update()

   

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
        
        
        page.add(
                ft.Column(
                    controls=[
                        ft.FloatingActionButton(icon=ft.Icons.PEOPLE, text='Todos os alunos', on_click=lista_alunos),
                        ft.FloatingActionButton(icon=ft.Icons.ADD_BOX, text='Adicionar turma', on_click=add_turma)
                    ]
                )
            )
        botoes_turmas = []
        for turma in turmas:
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


    def salvar_turma(e):
        nome_turma = nome_input.value

        adicionar_turma(nome_turma)

        # Exibe uma mensagem de sucesso
        page.add(ft.Text("Turma salva com sucesso!", color=ft.colors.GREEN))

    
    def add_turma(e):
        page.controls.clear()  # Limpa a página
        page.add(
            ft.Column(
                    [
                        ft.ElevatedButton(icon=ft.Icons.ARROW_BACK, text="Voltar", on_click=turmas_menu)
                    ]
                )
            )
        turmas = listar_turma()

            # Inputs do formulário
        global nome_input
            
        nome_input = ft.TextField(label="Nome", autofocus=True, width=400)  # Define a largura para 200 pixels


        page.add(
            ft.Column(
                    [
                        nome_input,
                        ft.ElevatedButton(text="Salvar", on_click=salvar_turma)
                    ]
                )
            )
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
