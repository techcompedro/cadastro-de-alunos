from escola_db import  remover_turma, listar_turma, adicionar_aluno_na_turma, adicionar_turma, adicionar_aluno, filtrar_alunos_por_turma, filtrar_alunos_por_nome, remover_aluno, atualizar_aluno, listar_alunos
from datetime import datetime

while True:
    print('----MENU----\n'
          '1 - Adicionar aluno\n'
          '2 - Adicionar turma\n'
          '3 - Adicionar aluno na turma\n'
          '4 - Atualizar aluno\n'
          '5 - Listar alunos\n'
          '6 - Listar turmas\n'
          '7 - Filtrar por nome\n'
          '8 - Filtrar por turma\n'
          '9 - Remover aluno\n'
          '10 - Remover turma\n'
          '------------\n')

    num_escolhido = int(input('Digite sua opção:'))

    # Adicionar aluno
    if num_escolhido == 1:
        nome = input('Digite o nome do aluno: ')
        idade = int(input('Digite a idade do aluno: '))
        faixa = input('Digite a cor da faixa do aluno: ')
        foto_perfil = input('Foto de perfil do aluno: ')
        numero = int(input('Digite o número do aluno: '))
        aniversario = input('Digite a data de nascimento do aluno (formato DD/MM/AAAA): ')
        
        try:
            # Converte a data de nascimento para o formato datetime
            data_nascimento = datetime.strptime(aniversario, "%d/%m/%Y").date()
        except ValueError:
            print("Formato de data inválido! Por favor, use DD/MM/AAAA.")
            continue
        
        nome_turma = input('Digite o nome da turma do aluno: ')

        # Chama a função de adicionar aluno, passando a turma como parâmetro
        adicionar_aluno(nome, idade, faixa, foto_perfil, numero, data_nascimento, nome_turma)

    # Adicionar turma
    elif num_escolhido == 2:
        nome_turma = input('Digite o nome da turma:')
        adicionar_turma(nome_turma)
    
    # Adicionar aluno na turma
    elif num_escolhido == 3:
        nome = int(input('Digite o nome do aluno para mover para outra turma ou adicionar: '))
        nova_turma = input('Digite o nome da nova turma: ')
        adicionar_aluno_na_turma(nome, nova_turma)
    
    # Atualizar aluno
    elif num_escolhido == 4:
        aluno_id = int(input('Digite o ID do aluno para atualizar: '))
        novo_nome = input('Digite o novo nome do aluno (deixe em branco para não alterar): ')
        nova_idade = input('Digite a nova idade do aluno (deixe em branco para não alterar): ')
        nova_idade = int(nova_idade) if nova_idade else None
        nova_turma = input('Digite a nova turma do aluno (deixe em branco para não alterar): ')
        nova_faixa = input('Digite a nova faixa do aluno (deixe em branco para não alterar): ')
        nova_foto = input('Digite a nova foto de perfil (deixe em branco para não alterar): ')
        novo_numero = input('Digite o novo número do aluno (deixe em branco para não alterar): ')
        novo_numero = int(novo_numero) if novo_numero else None
        novo_aniversario = input('Digite o novo aniversário do aluno (deixe em branco para não alterar): ')
        
        if novo_aniversario:
            try:
                novo_aniversario = datetime.strptime(novo_aniversario, "%d/%m/%Y").date()
            except ValueError:
                print("Formato de data inválido! Por favor, use DD/MM/AAAA.")
                continue

        atualizar_aluno(aluno_id, novo_nome, nova_idade, nova_turma, nova_faixa, nova_foto, novo_numero, novo_aniversario)

    # Listar alunos
    elif num_escolhido == 5:
        print('LISTA DE ALUNOS')
        listar_alunos()
    
    # Listar turmas
    elif num_escolhido == 6:
        print('LISTA DE TURMAS')
        listar_turma()
    
    # Filtrar por nome
    elif num_escolhido == 7:
        nome = input('Digite o nome do aluno: ')
        filtrar_alunos_por_nome(nome)
    
    # Filtrar por turma
    elif num_escolhido == 8:
        turma = input('Digite a turma: ')
        filtrar_alunos_por_turma(turma)
    
    # Remover aluno
    elif num_escolhido == 9:
        nome = input('Digite o nome do aluno para remover: ')
        remover_aluno(nome)
        
    # Remover turma
    elif num_escolhido == 10:
        print('tem certeza qque queer remover uma turma \n'
              'caso remova todos os alunos dessa turma vão ser excluidos\n'
              'Digite 1 para remover\n'
              'Digite 2 para não remover\n')
        escolha = int(input('Qual a sua escolha:'))
        nome = input('Digite o nome do turma para remover: ')
        remover_turma(nome)

    else:
        print('Digite um valor que esteja no menu.')
        break
