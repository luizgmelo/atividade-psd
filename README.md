# 🚀 Socket Server Simples

Um servidor de socket básico em Python que escuta em uma porta específica e ecoa de volta as mensagens recebidas.

## 🛠️ Pré-requisitos

- Python 3.6 ou superior
- Acesso ao terminal/linha de comando

## 🚀 Como executar o servidor

1. **Clone o repositório** (se ainda não tiver feito):
   ```bash
   git clone <seu-repositorio>
   cd atividade-psd
   ```

2. **Ative o ambiente virtual (recomendado)**:
   ```bash
   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Instale as dependências** (se houver):
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie o servidor**:
   ```bash
   python server.py
   ```

   Você deverá ver a mensagem:
   ```
   Servidor escutando em 127.0.0.1:65432
   ```

## 🔌 Testando a conexão

Você pode testar o servidor usando o `netcat` (nc) ou `telnet` em outro terminal:

```bash
# Usando netcat
nc 127.0.0.1 65432

# Ou usando telnet
telnet 127.0.0.1 65432
```

Digite qualquer mensagem e pressione Enter. O servidor irá ecoar a mensagem de volta.

## ⚙️ Configuração

O servidor está configurado com os seguintes parâmetros padrão:
- **Host**: 127.0.0.1 (localhost)
- **Porta**: 65432

Para alterar essas configurações, edite as variáveis `HOST` e `PORT` no arquivo `server.py`.
