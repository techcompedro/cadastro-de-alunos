import flet as ft  # Importa a biblioteca Flet para criação da interface gráfica
from banco_dados import  filtrar_alunos_por_id, remover_turma, listar_turma, adicionar_aluno_na_turma, adicionar_turma, adicionar_aluno, filtrar_alunos_por_turma, filtrar_alunos_por_nome, remover_aluno, atualizar_aluno, listar_alunos
import datetime # Importa as funções para listar alunos e turmas do banco de dados
import time as t
def app(page: ft.Page):  # Função principal que recebe a página como parâmetro
    def page_resize(e):
        page.value = f"{page.width} px"
        page.update()

        page.on_resize = page_resize
    # Configura o alinhamento global da página
    page.window_width = 1150
    page.window_min_height = 500
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 1  # Remove espaçamentos extras
    
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
            color=ft.Colors.BLUE,  # Cor do texto
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
                ft.FloatingActionButton(icon=ft.Icons.PEOPLE, text='Todos os alunos', on_click=lista_alunos),
                ft.FloatingActionButton(icon=ft.Icons.ADD_BOX, text='Adicionar aluno', on_click=add_aluno),
                ft.FloatingActionButton(icon=ft.Icons.PEOPLE, text='Pesquisar alunos',on_click=atu_aluno),
            ]

            # Organizando os botões na tela em uma coluna
        page.add(ft.Column(controls=botões))

        page.update()  # Atualiza a página


    def salvar_aluno(e):
                  # Função para abrir o modal
        def open_modal(aluno):
            # Cria o conteúdo do modal
            dialog = ft.AlertDialog(
                ft.Text(f"Aluno {aluno} salvo com sucesso!", color=ft.colors.GREEN),
                content=ft.Text(),
                actions=[
                    ft.TextButton("Fechar", on_click=close_modal),
                ],
            )
            # Mostra o modal
            page.dialog = dialog
            dialog.open = True
            page.update()

        # Função para fechar o modal
        def close_modal(e):
            page.dialog.open = False
            page.update()
        
        nome = nome_input.value
        
        idade = int(idade_input.value)
        faixa = faixa_dropdown.value
        foto_perfil = foto_input.value
        numero = numero_input.value
        data_nascimento = data_nascimento_input.value
        nome_turma = nome_turma_input.value

        adicionar_aluno(nome, idade, faixa, foto_perfil, numero, data_nascimento, nome_turma)
        open_modal(nome)
        # Exibe uma mensagem de sucesso
        

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
        cadastro_aluno = ft.Text('Cadastro de alunos',
                size=30,  # Tamanho da fonte
                weight=ft.FontWeight.BOLD,  # Peso da fonte (negrito)
                color=ft.colors.BLUE,  # Cor do texto
                text_align=ft.TextAlign.CENTER, )
        page.add(cadastro_aluno)
        
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
                    ft.ElevatedButton(text="Salvar", on_click=salvar_aluno),
                   

                ]
            )
        )
        
        page.update()


    def salvar_aluno_atualizar(aluno_id, nome_input, idade_input, faixa_input, foto_input, numero_input, data_nascimento_input, nome_turma_input):
        """
        Atualiza os dados do aluno no banco.
        """
        try:
            aluno_id = int(aluno_id.value if hasattr(aluno_id, 'value') else aluno_id)
            nome = nome_input.value if hasattr(nome_input, 'value') else nome_input
            idade = int(idade_input.value if hasattr(idade_input, 'value') else idade_input)
            faixa = faixa_input.value if hasattr(faixa_input, 'value') else faixa_input
            foto_perfil = foto_input.value if hasattr(foto_input, 'value') else foto_input
            numero = numero_input.value if hasattr(numero_input, 'value') else numero_input
            data_nascimento = data_nascimento_input.value if hasattr(data_nascimento_input, 'value') else data_nascimento_input
            nome_turma = nome_turma_input.value if hasattr(nome_turma_input, 'value') else nome_turma_input

            atualizar_aluno(
                aluno_id=aluno_id,
                novo_nome=nome,
                nova_idade=idade,
                nova_faixa=faixa,
                nova_foto=foto_perfil,
                novo_numero=numero,
                nova_data_nascimento=data_nascimento,
                nova_turma=nome_turma,
            )

            snack = ft.SnackBar(content=ft.Text("Aluno atualizado com sucesso."))
            page.overlay.append(snack)
            snack.open()

        except Exception as e:
            snack = ft.SnackBar(content=ft.Text(f"Erro ao atualizar aluno: {str(e)}"))
            page.overlay.append(snack)
            snack.open()

    def criar_inputs_aluno(aluno, turmas):
        """
        Cria os campos de entrada para edição do aluno.
        """
        return {
            "aluno_id_text": ft.Text(f"{aluno.id}"),
            "nome_input": ft.TextField(f"{aluno.nome}", label="Nome", autofocus=True, width=400),
            "idade_input": ft.TextField(f"{aluno.idade}", label="Idade", keyboard_type=ft.KeyboardType.NUMBER, width=400),
            "faixa_input": ft.Dropdown(
                label="Escolha a faixa do aluno",
                width=400,
                options=[ft.dropdown.Option(faixa) for faixa in ["Branca", "Amarela", "Laranja", "Verde", "Azul", "Roxa", "Marrom", "Preta", "Coral", "Vermelha"]],
                value=aluno.faixa
            ),
            "foto_input": ft.TextField(f"{aluno.foto_perfil}", label="Foto", width=400),
            "numero_input": ft.TextField(f"{aluno.numero}", label="Número", width=400),
            "data_nascimento_input": ft.TextField(f"{aluno.data_nascimento}", label="Data de Nascimento", width=400),
            "nome_turma_input": ft.Dropdown(
                label="Escolha a turma do aluno",
                options=[ft.dropdown.Option(turma.nome) for turma in turmas],
                width=400,
                value=aluno.turma.nome
            ) if turmas else ft.Text("Não tem turmas")
        }

    def criar_botoes_aluno(aluno, inputs):
        """
        Cria os botões para salvar e excluir aluno.
        """
        salvar_btn = ft.ElevatedButton(
            text="Salvar",
            on_click=lambda e: salvar_aluno_atualizar(
                inputs['aluno_id_text'], inputs['nome_input'], inputs['idade_input'], inputs['faixa_input'],
                inputs['foto_input'], inputs['numero_input'], inputs['data_nascimento_input'], inputs['nome_turma_input']
            )
        )

        excluir_btn = ft.ElevatedButton(
            text="Excluir",
            icon=ft.Icons.DELETE,
            on_click=lambda e: remover_aluno(aluno.nome)
        )

        return salvar_btn, excluir_btn

    def exibir_alunos(lista_alunos, turmas):
        """
        Exibe a lista de alunos com os campos de edição.
        """
        alunos_cards = []
        painel = ft.ExpansionPanelList(
            expand_icon_color=ft.Colors.BLUE,
            elevation=8,
            divider_color=ft.Colors.BLUE,
        )

        for aluno in lista_alunos:
            exp = ft.ExpansionPanel(
                header=ft.ListTile(title=ft.Text(f"Nome: {aluno.nome}   Faixa: {aluno.faixa}    Turma: {aluno.turma.nome}", size=18))
            )    
            inputs = criar_inputs_aluno(aluno, turmas)
            salvar_btn, excluir_btn = criar_botoes_aluno(aluno, inputs)

            exp.content = ft.Column(
                [
                    ft.Text(f"ID: {aluno.id}", size=18),
                    inputs['nome_input'],
                    inputs['idade_input'],
                    inputs['faixa_input'],
                    inputs['foto_input'],
                    inputs['numero_input'],
                    inputs['data_nascimento_input'],
                    inputs['nome_turma_input'],
                    ft.Row([salvar_btn, excluir_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(height=1, thickness=2),
                ]
            )
            painel.controls.append(exp)
        scrollable_area = ft.Column(
                [painel],
                scroll=ft.ScrollMode.AUTO,  # Ativa o scroll automático
                expand=True,  # Expande para ocupar o máximo de espaço disponível
            )

        page.add(scrollable_area)
        page.update()

    def atu_aluno_dois(e, campo_de_pesquisa, turmas):
        """
        Realiza a pesquisa de alunos pelo nome.
        """
        if not campo_de_pesquisa.value or not campo_de_pesquisa.value.strip():
            snack = ft.SnackBar(content=ft.Text("Por favor, insira um nome para a pesquisa."))
            page.overlay.append(snack)
            snack.open()
            return

        alunos = filtrar_alunos_por_nome(campo_de_pesquisa.value)
        if not alunos:
            snack = ft.SnackBar(content=ft.Text("Nenhum aluno encontrado."))
            page.overlay.append(snack)
            snack.open()
        else:
            exibir_alunos(alunos, turmas)

    def atu_aluno(e):
        """
        Tela de atualização de aluno.
        """
        page.controls.clear()
         # Criação do título do aplicativo
        text = ft.Text(
            "aqui é para pesquisar,  editar e remover aluno",  # Texto do título
            size=30,  # Tamanho da fonte
            weight=ft.FontWeight.BOLD,  # Peso da fonte (negrito)
            color=ft.Colors.BLUE,  # Cor do texto
            text_align=ft.TextAlign.END,  # Alinhamento do texto (direita)
        )
        page.add(text)
        
        voltar_btn = ft.ElevatedButton(icon=ft.Icons.ARROW_BACK, text="Voltar", on_click=alunos_menu)
        campo_de_pesquisa = ft.TextField(label="Pesquisa por Nome", autofocus=True,)
        turmas = listar_turma()

        btn_pesquisa = ft.ElevatedButton(
            text="Pesquisar",
            on_click=lambda e: atu_aluno_dois(e, campo_de_pesquisa, turmas)
        )

        page.add(voltar_btn, campo_de_pesquisa, btn_pesquisa)
        page.update()

    def lista_alunos(e):
        page.controls.clear()  # Limpa a página
        voltar_btn = ft.ElevatedButton(
            icon=ft.Icons.ARROW_BACK,
            text="Voltar",
            on_click=turmas_menu,
        )
        page.update()
        alunos = listar_alunos()
        # Cria uma tabela para exibir os dados dos alunos
         # Painel de expansão para alunos
        painel = ft.ExpansionPanelList(
            expand_icon_color=ft.Colors.BLUE,
            elevation=8,
            divider_color=ft.Colors.BLUE,
        )

        # Adiciona cada aluno ao painel
        for aluno in alunos:
            # Criando o painel para cada aluno
            exp = ft.ExpansionPanel(
                header=ft.ListTile(title=ft.Text(f"Nome: {aluno.nome}   Faixa: {aluno.faixa}    turma: {aluno.turma.nome}", size=18))
            )

            # Criando a tabela de dados
            tabela = ft.DataTable(
                width=900,
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Nome")),
                    ft.DataColumn(ft.Text("Idade")),
                    ft.DataColumn(ft.Text("Faixa")),
                    ft.DataColumn(ft.Text("Número")),
                    ft.DataColumn(ft.Text("Data de Nascimento")),
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
                            ft.DataCell(ft.Text(str(aluno.data_nascimento.strftime("%Y-%m-%d")))),
                            ft.DataCell(ft.Text(str(aluno.turma.nome))),
                        ]
                    )
                ],
            )

            # Conteúdo do painel de cada aluno
            exp.content = ft.Column(
                [
                    tabela,
                    ft.ListTile(
                        title=ft.Text("Excluir aluno"),
                        subtitle=ft.Text("Pressione o ícone para excluir"),
                        trailing=ft.IconButton(
                            ft.Icons.DELETE,
                            on_click=lambda e, aluno=aluno: remover_aluno(aluno.nome),
                        ),
                    ),
                ]
            )

            # Adiciona o painel do aluno à lista de painéis
            painel.controls.append(exp)

        # Envolve o painel em um Column com scroll
        scrollable_area = ft.Column(
            [painel],
            scroll=ft.ScrollMode.AUTO,  # Ativa o scroll automático
            expand=True,  # Expande para ocupar o máximo de espaço disponível
        )

        # Adiciona os controles à página
        page.add(
            ft.Column(
                [
                    voltar_btn,
                    scrollable_area,
                ],
                expand=True,  # Expande para ocupar o espaço da página
            )
        )
        page.update()



    def delete_turma(e):
        page.controls.clear()  # Limpa a página
        page.add(
            ft.Column(
                [
                    ft.ElevatedButton(icon=ft.Icons.ARROW_BACK, text="Voltar", on_click=turmas_menu)
                ]
            )
        )
        aviso = ft.Text(
            'Se você excluir uma turma, os alunos dessa turma serão todos excluídos',  
            size=25,  
            weight=ft.FontWeight.BOLD,  
            text_align=ft.TextAlign.CENTER
        )
        page.add(aviso)

        painel = ft.ExpansionPanelList(
            expand_icon_color=ft.Colors.BLUE,
            elevation=8,
            divider_color=ft.Colors.BLUE,
        )

        turmas = listar_turma()  # Busca todas as turmas
        
        for turma in turmas:
            exp = ft.ExpansionPanel(
                header=ft.ListTile(title=ft.Text(f"{turma.nome}"))
            )

            tabela = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Turma")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(turma.id))),
                            ft.DataCell(ft.Text(str(turma.nome))),
                        ]
                    )
                ]
            )

            exp.content = ft.Column(
                [
                    tabela,
                    ft.ListTile(
                        title=ft.Text(f"Excluir turma"),
                        subtitle=ft.Text(f"Pressione o ícone para excluir"),
                        trailing=ft.IconButton(
                            ft.Icons.DELETE,
                            on_click=lambda e, turma=turma: remover_turma(turma.nome)
                        )
                    )
                ]
            )
            painel.controls.append(exp)

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
                ft.Row(
                    controls=[
                        ft.FloatingActionButton(icon=ft.Icons.PEOPLE, text='Todos os alunos', on_click=lista_alunos),
                        ft.FloatingActionButton(icon=ft.Icons.ADD_BOX, text='Adicionar turma', on_click=add_turma),
                        ft.FloatingActionButton(icon=ft.Icons.DELETE, text='Remover turma', on_click=delete_turma),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER  # Alinha os botões à esquerda na linha
                )
            ]
        )
    )


        turmas_text = ft.Text('Turmas',
                size=30,  # Tamanho da fonte
                weight=ft.FontWeight.BOLD,  # Peso da fonte (negrito)
                color=ft.colors.BLUE,  # Cor do texto
                text_align=ft.TextAlign.CENTER, )
        page.add(turmas_text)
        
        
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
        cadastro_turma = ft.Text('Cadastro de turmas',
                size=30,  # Tamanho da fonte
                weight=ft.FontWeight.BOLD,  # Peso da fonte (negrito)
                color=ft.colors.BLUE,  # Cor do texto
                text_align=ft.TextAlign.CENTER, )
        page.add(cadastro_turma)
        
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
        voltar_btn = ft.ElevatedButton(
            icon=ft.Icons.ARROW_BACK,
            text="Voltar",
            on_click=turmas_menu,
        )
        page.update()
        alunos = filtrar_alunos_por_turma(id_turma)
        # Cria uma tabela para exibir os dados dos alunos
         # Painel de expansão para alunos
        painel = ft.ExpansionPanelList(
            expand_icon_color=ft.Colors.BLUE,
            elevation=8,
            divider_color=ft.Colors.BLUE,
        )

        # Adiciona cada aluno ao painel
        for aluno in alunos:
            # Criando o painel para cada aluno
            d = aluno.data_nascimento.strftime("%Y-%m-%d")
            exp = ft.ExpansionPanel(
                header=ft.ListTile(title=ft.Text(f"Nome: {aluno.nome}   Faixa: {aluno.faixa}    turma: {aluno.turma.nome}", size=18))
            )

            # Criando a tabela de dados
            tabela = ft.DataTable(
                width=900,
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Nome")),
                    ft.DataColumn(ft.Text("Idade")),
                    ft.DataColumn(ft.Text("Faixa")),
                    ft.DataColumn(ft.Text("Número")),
                    ft.DataColumn(ft.Text("Data de Nascimento")),
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
                            ft.DataCell(ft.Text(str(d))),
                            ft.DataCell(ft.Text(str(aluno.turma.nome))),
                        ]
                    )
                ],
            )

            # Conteúdo do painel de cada aluno
            exp.content = ft.Column(
                [
                    tabela,
                    ft.ListTile(
                        title=ft.Text("Excluir aluno"),
                        subtitle=ft.Text("Pressione o ícone para excluir"),
                        trailing=ft.IconButton(
                            ft.Icons.DELETE,
                            on_click=lambda e, aluno=aluno: remover_aluno(aluno.nome),
                        ),
                    ),
                ]
            )

            # Adiciona o painel do aluno à lista de painéis
            painel.controls.append(exp)

        # Envolve o painel em um Column com scroll
        scrollable_area = ft.Column(
            [painel],
            scroll=ft.ScrollMode.AUTO,  # Ativa o scroll automático
            expand=True,  # Expande para ocupar o máximo de espaço disponível
        )

        # Adiciona os controles à página
        page.add(
            ft.Column(
                [
                    voltar_btn,
                    scrollable_area,
                ],
                expand=True,  # Expande para ocupar o espaço da página
            )
        )
        page.update()







    tela_inicial()
ft.app(app)
