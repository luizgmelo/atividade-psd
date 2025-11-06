# 💬 Chat em Tempo Real com Socket

Um servidor de chat em tempo real que permite múltiplos clientes se conectarem e trocarem mensagens entre si, com identificação de usuários.

## ✨ Funcionalidades

- Conexão de múltiplos clientes simultaneamente
- Identificação de usuários por nome
- Transmissão de mensagens para todos os clientes conectados
- Notificações de entrada/saída de usuários
- Interface de linha de comando amigável

## 🛠️ Pré-requisitos

- Python 3.6 ou superior
- Acesso ao terminal/linha de comando

## 🚀 Como executar

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

3. **Inicie o servidor**:
   ```bash
   python server.py
   ```
   Você verá a mensagem:
   ```
   Chat server is running on 127.0.0.1:65432
   Waiting for connections...
   ```

4. **Conecte múltiplos clientes**:
   Em terminais separados, execute:
   ```bash
   python client.py
   ```
   Cada cliente será solicitado a inserir um nome de usuário.

## 💡 Como usar

- Ao iniciar o cliente, digite seu nome de usuário
- Digite sua mensagem e pressione Enter para enviar
- Digite 'exit' para sair do chat
- As mensagens são exibidas no formato: `nome: mensagem`
- Notificações são exibidas quando usuários entram ou saem do chat

## ⚙️ Configuração

O servidor está configurado com os seguintes parâmetros padrão:
- **Host**: 127.0.0.1 (localhost)
- **Porta**: 65432

Para alterar essas configurações, edite as variáveis `HOST` e `PORT` no arquivo `server.py`.

## 📝 Notas

- O servidor suporta múltiplas conexões simultâneas
- As mensagens são transmitidas para todos os clientes conectados
- A interface do cliente é limpa automaticamente para melhor legibilidade
- Use Ctrl+C para encerrar o cliente ou servidor a qualquer momento
