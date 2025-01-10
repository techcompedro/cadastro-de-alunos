from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# Configuração do banco de dados
engine = create_engine("sqlite:///C:/Users/pedro/OneDrive/Documentos/projetos/cadastro-de-alunos/codigo basico/escola_jiu_jitsu.db", echo=True)

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
    data_nascimento = Column(Date, nullable=True)  # Data de nascimento
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
    turma = session.query(Turma).filter_by(nome=nome_turma).first()
    if not turma:
        print(f"Turma '{nome_turma}' não encontrada. Criando turma...")
        adicionar_turma(nome_turma)  # Cria a turma se não existir
        turma = session.query(Turma).filter_by(nome=nome_turma).first()
    
    novo_aluno = Aluno(
        nome=nome,
        idade=idade,
        faixa=faixa,
        foto_perfil=foto_perfil,
        numero=numero,
        data_nascimento=data_nascimento,  # Correção para data de nascimento
        turma=turma  # Relaciona o aluno com a turma
    )
    session.add(novo_aluno)
    session.commit()
    print(f"Aluno '{nome}' adicionado à turma '{nome_turma}' com sucesso!")

# Função para listar todos os alunos
def listar_alunos():
    alunos = session.query(Aluno).all()
    for aluno in alunos:
        print(f"ID: {aluno.id}, Nome: {aluno.nome}, Idade: {aluno.idade}, Faixa: {aluno.faixa}, Número: {aluno.numero}, Data de Nascimento: {aluno.data_nascimento}, Turma: {aluno.turma.nome}")

# Função para listar todas as turmas
def listar_turma():
    turmas = session.query(Turma).all()
    for turma in turmas:
        print(f"ID: {turma.id}, Nome: {turma.nome}")

# Função para filtrar alunos por nome
def filtrar_alunos_por_nome(nome):
    alunos = session.query(Aluno).filter(Aluno.nome.ilike(f"{nome}")).all()
    if alunos:
        for aluno in alunos:
            print(f"ID: {aluno.id}, Nome: {aluno.nome}, Idade: {aluno.idade}, Faixa: {aluno.faixa}, Número: {aluno.numero}, Data de Nascimento: {aluno.data_nascimento}, Turma: {aluno.turma.nome}")
    else:
        print(f"Nenhum aluno encontrado com o nome '{nome}'.")

# Função para filtrar alunos por turma
def filtrar_alunos_por_turma(turma):
    alunos = session.query(Aluno).join(Turma).filter(Turma.nome.ilike(f"{turma}")).all()
    if alunos:
        for aluno in alunos:
            print(f"ID: {aluno.id}, Nome: {aluno.nome}, Idade: {aluno.idade}, Faixa: {aluno.faixa}, Número: {aluno.numero}, Data de Nascimento: {aluno.data_nascimento}, Turma: {aluno.turma.nome}")
    else:
        print(f"Nenhum aluno encontrado na turma '{turma}'.")

# Função para atualizar dados de um aluno
def atualizar_aluno(aluno_id, novo_nome=None, nova_idade=None, nova_faixa=None, nova_foto=None, novo_numero=None, nova_data_nascimento=None, nova_turma=None):
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
            aluno.data_nascimento = nova_data_nascimento
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
def remover_turma(nome_turma):
    turma = session.query(Turma).filter_by(nome=nome_turma).first()
    if turma:
        session.delete(turma)  # Deleta a turma e seus alunos associados
        session.commit()
        print(f"Turma '{nome_turma}' e seus alunos foram deletados com sucesso!")
    else:
        print(f"Turma '{nome_turma}' não encontrada.")

# Função para adicionar um aluno na turma 
def adicionar_aluno_na_turma(nome, nova_turma):
    aluno = session.query(Aluno).filter_by(nome=nome).first() 
    if aluno:
        aluno.turma = nova_turma
        session.commit()
        print(f"Aluno {nome} movido para a turma '{nova_turma}' com sucesso!")
    else:
        print(f"Aluno {aluno} não encontrado.")
