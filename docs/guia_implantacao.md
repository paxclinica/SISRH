# Guia de Implantação - Sistema de Controle de Treinamentos Pax Clínica

Este guia contém instruções passo a passo para implantar o Sistema de Controle de Treinamentos da Pax Clínica em um ambiente de produção.

## Passo 1: Preparação do Ambiente

### Requisitos de Sistema:
- Python 3.8 ou superior
- MySQL 5.7 ou superior
- Servidor web (opcional para produção: Nginx ou Apache)

### Instalação de Dependências:

```bash
# Instalar Python (caso não esteja instalado)
# Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL:
sudo yum install python3 python3-pip

# Instalar MySQL (caso não esteja instalado)
# Ubuntu/Debian:
sudo apt install mysql-server

# CentOS/RHEL:
sudo yum install mysql-server
sudo systemctl start mysqld
sudo systemctl enable mysqld
```

## Passo 2: Configuração do Banco de Dados

```bash
# Acessar o MySQL
mysql -u root -p

# Criar banco de dados
CREATE DATABASE pax_clinica_db;

# Criar usuário para a aplicação
CREATE USER 'pax_user'@'localhost' IDENTIFIED BY 'senha_segura';

# Conceder privilégios
GRANT ALL PRIVILEGES ON pax_clinica_db.* TO 'pax_user'@'localhost';
FLUSH PRIVILEGES;

# Sair do MySQL
EXIT;
```

## Passo 3: Configuração da Aplicação

1. Extraia os arquivos do projeto para o diretório desejado:
```bash
unzip pax_clinica_app.zip -d /caminho/para/aplicacao
cd /caminho/para/aplicacao/pax_clinica_app
```

2. Crie e ative um ambiente virtual Python:
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure a conexão com o banco de dados:
   - Edite o arquivo `src/main.py`
   - Atualize a string de conexão:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://pax_user:senha_segura@localhost:3306/pax_clinica_db"
   ```

5. Configure a chave secreta:
   - Edite o arquivo `src/main.py`
   - Atualize a chave secreta para uma string aleatória e segura:
   ```python
   app.config['SECRET_KEY'] = 'sua_chave_secreta_aleatoria'
   ```

## Passo 4: Inicialização do Banco de Dados

```bash
# Certifique-se de estar no diretório da aplicação com o ambiente virtual ativado
cd /caminho/para/aplicacao/pax_clinica_app
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Execute a aplicação para criar as tabelas
cd src
python main.py
```

## Passo 5: Execução em Ambiente de Desenvolvimento

Para testar a aplicação em ambiente de desenvolvimento:

```bash
# No diretório src da aplicação
python main.py
```

A aplicação estará disponível em `http://localhost:5000`

## Passo 6: Implantação em Ambiente de Produção

### Opção 1: Usando Gunicorn (recomendado para produção)

1. Instale o Gunicorn:
```bash
pip install gunicorn
```

2. Execute a aplicação com Gunicorn:
```bash
cd /caminho/para/aplicacao/pax_clinica_app
gunicorn --chdir src --bind 0.0.0.0:8000 "main:app"
```

3. Configure um servidor web (Nginx ou Apache) como proxy reverso.

### Opção 2: Usando o servidor de desenvolvimento Flask (não recomendado para produção)

```bash
cd /caminho/para/aplicacao/pax_clinica_app/src
python main.py
```

## Passo 7: Configuração do Servidor Web (Nginx)

Exemplo de configuração para Nginx:

```nginx
server {
    listen 80;
    server_name seu_dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /caminho/para/aplicacao/pax_clinica_app/src/static;
    }
}
```

## Passo 8: Configuração de Serviço Systemd (para execução automática)

Crie um arquivo de serviço systemd:

```bash
sudo nano /etc/systemd/system/pax_clinica.service
```

Adicione o seguinte conteúdo:

```
[Unit]
Description=Pax Clinica - Sistema de Controle de Treinamentos
After=network.target

[Service]
User=seu_usuario
Group=seu_grupo
WorkingDirectory=/caminho/para/aplicacao/pax_clinica_app
Environment="PATH=/caminho/para/aplicacao/pax_clinica_app/venv/bin"
ExecStart=/caminho/para/aplicacao/pax_clinica_app/venv/bin/gunicorn --chdir src --bind 0.0.0.0:8000 "main:app"
Restart=always

[Install]
WantedBy=multi-user.target
```

Ative e inicie o serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl enable pax_clinica
sudo systemctl start pax_clinica
```

## Passo 9: Verificação da Implantação

1. Verifique o status do serviço:
```bash
sudo systemctl status pax_clinica
```

2. Acesse a aplicação através do navegador:
```
http://seu_dominio.com
```

3. Crie um usuário inicial e teste as funcionalidades.

## Passo 10: Manutenção e Backup

### Backup do Banco de Dados:
```bash
mysqldump -u pax_user -p pax_clinica_db > backup_pax_clinica_$(date +%Y%m%d).sql
```

### Backup de Arquivos:
```bash
tar -czf backup_pax_clinica_files_$(date +%Y%m%d).tar.gz /caminho/para/aplicacao/pax_clinica_app/src/static/uploads
```

### Atualização da Aplicação:
```bash
# Pare o serviço
sudo systemctl stop pax_clinica

# Atualize os arquivos
# ...

# Ative o ambiente virtual e atualize dependências se necessário
cd /caminho/para/aplicacao/pax_clinica_app
source venv/bin/activate
pip install -r requirements.txt

# Reinicie o serviço
sudo systemctl start pax_clinica
```

## Suporte

Em caso de problemas durante a implantação, consulte a documentação completa ou entre em contato com o suporte técnico.
