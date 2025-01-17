from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime, date


# Configuração do banco de dados
engine = create_engine("sqlite:///C:/Users/pedro/OneDrive/Documentos/projetos/cadastro-de-alunos/escola_jiu_jitsu.db", echo=True)

Base = declarative_base()


# Modelo de Turma
class Turma(Base):
    __tablename__ = 'turmas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True)  # Nome da turma
    alunos = relationship("Aluno", back_populates="turma")  # Relacionamento com Aluno

# Modelo de Aluno
class Aluno(Base):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    faixa = Column(String, nullable=False)
    foto_perfil = Column(String)
    numero = Column(Integer)
    data_nascimento = Column(DateTime, nullable=True)  # Data de nascimento
    data_cadastro = Column(DateTime, default=datetime.utcnow)  # Data de cadastro
    turma_id = Column(Integer, ForeignKey('turmas.id'))  # Chave estrangeira para a turma
    turma = relationship("Turma", back_populates="alunos")  # Relacionamento com Turma

# Criar uma sessão
Session = sessionmaker(bind=engine)
session = Session()

# Função para criar as tabelas no banco de dados
def criar_tabelas():
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")

# Função para adicionar uma turma
def adicionar_turma(nome_turma):
    nova_turma = Turma(nome=nome_turma)
    session.add(nova_turma)
    session.commit()
    print(f"Turma '{nome_turma}' adicionada com sucesso!")

# Função para adicionar um aluno com relação à turma
def adicionar_aluno(nome, idade, faixa, foto_perfil, numero, data_nascimento, nome_turma):
    # Buscando a turma pelo nome
    turma = session.query(Turma).filter_by(nome=nome_turma).first()

    # Convertendo a data de nascimento para o tipo correto (como objeto de data)
    if isinstance(data_nascimento, datetime):
        data_nascimento = data_nascimento.strftime("%Y-%m-%d")# Mantém a data sem o horário
    else:
        try:
            # Se for uma string, tenta converter para datetime e depois extrai a data
            data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y").date()
        except ValueError as e:
            print(f"Erro na conversão da data: {e}")
            return  # Aqui você pode retornar ou lançar uma exceção, caso prefira

    print(f"data_nascimento após conversão: {data_nascimento}, tipo: {type(data_nascimento)}")

    # Garantindo que data_cadastro seja datetime
    data_e_hora_atual = datetime.now()
    data_somente_data = data_e_hora_atual.strftime("%Y-%m-%d | %H:%M")
    data_cadastro = data_somente_data  # Não é necessário formatar se for um campo datetime

    # Caso a turma não exista, cria uma nova turma
    if not turma:
        print(f"Turma '{nome_turma}' não encontrada. Criando turma...")
        turma = Turma(nome=nome_turma)
        session.add(turma)
        session.commit()

    # Criando um novo aluno
    novo_aluno = Aluno(
        nome=nome,
        idade=idade,
        faixa=faixa,
        foto_perfil=foto_perfil,  # Garantir que seja o tipo de dado correto
        numero=numero,
        data_nascimento=data_nascimento,  # Passando a data como objeto datetime.date
        data_cadastro=data_cadastro,      # Passando datetime como objeto datetime
        turma_id=turma.id  # Relacionando o aluno com a turma
    )
    
    # Tentando adicionar o aluno no banco de dados
    try:
        session.add(novo_aluno)
        session.commit()
        print(f"Aluno '{nome}' adicionado com sucesso!")
    except Exception as e:
        session.rollback()
        print(f"Erro ao adicionar aluno: {e}")

# Função para listar todos os alunos
def listar_alunos():
    alunos = session.query(Aluno).all()
    return alunos
        
# Função para listar todas as turmas
def listar_turma():
    turmas = session.query(Turma).all()
    return turmas

# Função para filtrar alunos por nome
def filtrar_alunos_por_nome(nome):
    if not isinstance(nome, str):
        return []
    alunos = session.query(Aluno).filter(func.lower(Aluno.nome).like(f"%{nome.lower()}%")).all()
    return alunos


def filtrar_alunos_por_id(id):
    alunos = session.query(Aluno).filter(Aluno.id == id).all()
    return alunos


def quantos_alunos():
    total_alunos = session.query(Aluno).count()
    total_turmas = session.query(Turma).count()
    return total_alunos, total_turmas
    

# Função para filtrar alunos por turma
def filtrar_alunos_por_turma(id_turma):
    alunos = session.query(Aluno).filter(Aluno.turma_id == id_turma).all()
    return alunos

def atualizar_aluno(aluno_id, novo_nome=None, nova_idade=None, nova_faixa=None, nova_foto=None, novo_numero=None, nova_data_nascimento=None, nova_data_cadastro=None, nova_turma=None):
    if nova_data_nascimento:
        try:
            data_nascimento = datetime.strptime(nova_data_nascimento, "%Y-%m-%d %H:%M:%S").date()
        except ValueError:
            print("Formato de data inválido. Use o formato 'YYYY-MM-DD HH:MM:SS'.")
            return
    else:
        data_nascimento = None

    aluno = session.query(Aluno).filter_by(id=aluno_id).first()
    if aluno:
        if novo_nome:
            aluno.nome = novo_nome
        if nova_idade is not None:
            aluno.idade = nova_idade
        if nova_faixa:
            aluno.faixa = nova_faixa
        if nova_foto:
            aluno.foto_perfil = nova_foto
        if novo_numero:
            aluno.numero = novo_numero
        if nova_data_nascimento:
            aluno.data_nascimento = data_nascimento
        if nova_data_cadastro:
            aluno.data_cadastro = nova_data_cadastro
        if nova_turma:
            turma = session.query(Turma).filter_by(nome=nova_turma).first()
            if turma:
                aluno.turma = turma
            else:
                print(f"Turma '{nova_turma}' não encontrada.")
        session.commit()
        print(f"Aluno ID {aluno_id} atualizado com sucesso!")
    else:
        print(f"Aluno ID {aluno_id} não encontrado.")

# Função para remover um aluno
def remover_aluno(nome):
    aluno = session.query(Aluno).filter_by(nome=nome).first()  # Busca o aluno pelo nome
    if aluno:
        session.delete(aluno)  # Deleta o aluno
        session.commit()  # Confirma a exclusão
        print(f'Aluno {nome} deletado com sucesso!')
    else:
        print(f'Aluno {nome} não encontrado.')

# Função para excluir uma turma e seus alunos
def remover_turma(nome):
    turmas = session.query(Turma).filter_by(nome=nome).first()
    if turmas:
        session.delete(turmas)  # Deleta a turma e seus alunos associados
        session.commit()
        print(f"Turma '{nome}' e seus alunos foram deletados com sucesso!")
    else:
        print(f"Turma '{nome}' não encontrada.")

# Função para adicionar um aluno na turma 
def adicionar_aluno_na_turma(nome, nova_turma):
    aluno = session.query(Aluno).filter_by(nome=nome).first() 
    if aluno:
        aluno.turma = nova_turma
        session.commit()
        print(f"Aluno {nome} movido para a turma '{nova_turma}' com sucesso!")
    else:
        print(f"Aluno {aluno} não encontrado.")


