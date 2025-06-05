# Documentação do Sistema de Controle de Treinamentos - Pax Clínica

## Sumário
1. [Visão Geral](#visão-geral)
2. [Requisitos do Sistema](#requisitos-do-sistema)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Instalação e Configuração](#instalação-e-configuração)
5. [Funcionalidades](#funcionalidades)
6. [Guia do Usuário](#guia-do-usuário)
7. [Manutenção](#manutenção)
8. [Suporte](#suporte)

## Visão Geral

O Sistema de Controle de Treinamentos da Pax Clínica é uma aplicação web desenvolvida para gerenciar os treinamentos realizados pelos funcionários da clínica. O sistema permite o cadastro de pessoas (funcionários), registro de treinamentos, vinculação de participantes aos treinamentos, upload de atas e consulta de treinamentos por pessoa.

### Principais Funcionalidades:
- Autenticação de usuários (login e cadastro)
- Cadastro de pessoas (funcionários) com dados de admissão/demissão
- Cadastro de treinamentos com informações detalhadas
- Vinculação de participantes aos treinamentos
- Upload de atas de treinamento
- Consulta de treinamentos por pessoa

## Requisitos do Sistema

### Requisitos de Software:
- Python 3.8 ou superior
- MySQL 5.7 ou superior
- Pip (gerenciador de pacotes Python)
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

### Requisitos de Hardware:
- Processador: 1 GHz ou superior
- Memória RAM: 2 GB ou superior
- Espaço em disco: 500 MB para a aplicação

## Estrutura do Projeto

```
pax_clinica_app/
├── venv/                      # Ambiente virtual Python
├── src/                       # Código-fonte da aplicação
│   ├── models/                # Modelos de dados
│   │   ├── __init__.py        # Inicialização do SQLAlchemy
│   │   ├── usuario.py         # Modelo de Usuário
│   │   ├── pessoa.py          # Modelo de Pessoa
│   │   ├── treinamento.py     # Modelo de Treinamento
│   │   └── participacao.py    # Modelo de Participação
│   ├── routes/                # Rotas da aplicação
│   │   ├── __init__.py        # Inicialização das rotas
│   │   ├── auth.py            # Rotas de autenticação
│   │   ├── main.py            # Rotas principais
│   │   ├── pessoas.py         # Rotas de pessoas
│   │   ├── treinamentos.py    # Rotas de treinamentos
│   │   └── consultas.py       # Rotas de consultas
│   ├── static/                # Arquivos estáticos
│   │   ├── css/               # Estilos CSS
│   │   ├── js/                # Scripts JavaScript
│   │   └── uploads/           # Uploads de arquivos
│   │       └── atas/          # Atas de treinamentos
│   ├── templates/             # Templates HTML
│   │   ├── auth/              # Templates de autenticação
│   │   ├── main/              # Templates principais
│   │   ├── pessoas/           # Templates de pessoas
│   │   ├── treinamentos/      # Templates de treinamentos
│   │   ├── consultas/         # Templates de consultas
│   │   └── base.html          # Template base
│   └── main.py                # Arquivo principal da aplicação
└── requirements.txt           # Dependências do projeto
```

## Instalação e Configuração

### Pré-requisitos:
1. Instalar Python 3.8 ou superior
2. Instalar MySQL 5.7 ou superior
3. Criar um banco de dados MySQL para a aplicação

### Passos para Instalação:

1. **Clone o repositório ou extraia os arquivos do projeto:**
   ```bash
   git clone <url-do-repositorio> pax_clinica_app
   cd pax_clinica_app
   ```

2. **Crie e ative um ambiente virtual Python:**
   ```bash
   python -m venv venv
   
   # No Windows:
   venv\Scripts\activate
   
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências do projeto:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados:**
   
   Edite o arquivo `src/main.py` e atualize as configurações do banco de dados:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://usuario:senha@localhost:3306/nome_do_banco"
   ```

5. **Inicialize o banco de dados:**
   ```bash
   # Acesse o diretório src
   cd src
   
   # Execute o aplicativo para criar as tabelas
   python main.py
   ```

6. **Execute a aplicação:**
   ```bash
   python main.py
   ```

7. **Acesse a aplicação:**
   Abra um navegador e acesse `http://localhost:5000`

## Funcionalidades

### 1. Autenticação de Usuários
- Cadastro de novos usuários
- Login de usuários existentes
- Logout de usuários

### 2. Cadastro de Pessoas
- Adicionar novos funcionários
- Editar dados de funcionários existentes
- Visualizar lista de funcionários
- Excluir funcionários

### 3. Cadastro de Treinamentos
- Adicionar novos treinamentos
- Editar treinamentos existentes
- Visualizar lista de treinamentos
- Excluir treinamentos

### 4. Vinculação de Participantes
- Selecionar participantes para treinamentos
- Visualizar participantes de cada treinamento

### 5. Upload de Atas
- Anexar atas de treinamentos em formato PDF
- Visualizar atas anexadas

### 6. Consulta de Treinamentos por Pessoa
- Buscar treinamentos realizados por um funcionário específico
- Visualizar detalhes dos treinamentos

## Guia do Usuário

### Primeiro Acesso
1. Acesse a aplicação através do navegador
2. Clique em "Cadastre-se" na tela de login
3. Preencha os dados de cadastro e clique em "Cadastrar"
4. Faça login com as credenciais cadastradas

### Cadastro de Pessoas
1. No menu lateral, clique em "Pessoas"
2. Clique no botão "Nova Pessoa"
3. Preencha os dados do funcionário e clique em "Salvar"

### Cadastro de Treinamentos
1. No menu lateral, clique em "Treinamentos"
2. Clique no botão "Novo Treinamento"
3. Preencha os dados do treinamento
4. Selecione os participantes
5. Anexe a ata do treinamento (opcional)
6. Clique em "Salvar"

### Consulta de Treinamentos por Pessoa
1. No menu lateral, clique em "Consultas"
2. Selecione a pessoa desejada
3. Clique em "Consultar"
4. Visualize os treinamentos realizados pela pessoa

## Manutenção

### Backup do Banco de Dados
Recomenda-se realizar backups periódicos do banco de dados para evitar perda de dados:

```bash
# Backup do banco de dados
mysqldump -u usuario -p nome_do_banco > backup_pax_clinica.sql

# Restauração do banco de dados
mysql -u usuario -p nome_do_banco < backup_pax_clinica.sql
```

### Backup de Arquivos
Recomenda-se realizar backups periódicos dos arquivos de atas:

```bash
# Backup dos arquivos de atas
cp -r src/static/uploads/atas/ backup_atas/
```

## Suporte

Em caso de dúvidas ou problemas, entre em contato com o suporte técnico:

- Email: suporte@paxclinica.com.br
- Telefone: (XX) XXXX-XXXX
