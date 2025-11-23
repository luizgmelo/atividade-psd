# 💬 Sistema de Chat Avançado com Socket

Um servidor de chat em tempo real com sistema completo de comandos, grupos, mensagens direcionadas e armazenamento de mensagens offline.

## ✨ Funcionalidades

- ✅ Conexão de múltiplos clientes simultaneamente
- ✅ Validação de nickname único (impede usuários duplicados)
- ✅ Sistema completo de comandos
- ✅ Criação e gerenciamento de grupos
- ✅ Mensagens direcionadas para usuários ou grupos
- ✅ Mensagens broadcast seletivas (online/offline/todos)
- ✅ Armazenamento de mensagens offline
- ✅ Formatação automática com timestamp e remetente
- ✅ Interface de linha de comando amigável com ajuda integrada

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

### Comandos Disponíveis

#### 📋 Listagem
- `-listarusuarios` - Lista todos os usuários online
- `-listargrupos` - Lista todos os grupos disponíveis
- `-listausrgrupo NOME_DO_GRUPO` - Lista membros de um grupo específico

#### 👥 Gerenciamento de Grupos
- `-criargrupo NOME_DO_GRUPO` - Cria um novo grupo
- `-entrargrupo NOME_GRUPO` - Entra em um grupo existente
- `-sairgrupo NOME_GRUPO` - Sai de um grupo

#### 💬 Envio de Mensagens
- `-msg U NICKNAME MENSAGEM` - Envia mensagem para um usuário específico
- `-msg G GRUPO MENSAGEM` - Envia mensagem para um grupo (precisa ser membro)
- `-msgt C MENSAGEM` - Envia para todos os usuários online
- `-msgt D MENSAGEM` - Envia para todos os usuários offline
- `-msgt T MENSAGEM` - Envia para todos os usuários (online e offline)

#### ℹ️ Ajuda
- `-ajuda` ou `-help` - Exibe lista de comandos
- `exit` - Sai do chat

### Formato das Mensagens

Todas as mensagens recebidas são formatadas automaticamente:
- Mensagem direta: `(NICK, DATA/HORA) MENSAGEM`
- Mensagem de grupo: `(NICK, GRUPO, DATA/HORA) MENSAGEM`

### Mensagens Offline

Se você enviar uma mensagem para um usuário que está offline, ela será armazenada e entregue automaticamente quando o usuário se conectar novamente.

## ⚙️ Configuração

O servidor está configurado com os seguintes parâmetros padrão:
- **Host**: 127.0.0.1 (localhost)
- **Porta**: 65432

Para alterar essas configurações, edite as variáveis `HOST` e `PORT` no arquivo `server.py`.

## 📝 Notas Importantes

### Validações e Erros
- ✅ Nickname único: não é permitido conectar com um nome já em uso
- ✅ Comandos inválidos retornam mensagem de erro com formato correto
- ✅ Grupo duplicado: não é possível criar grupo com nome existente
- ✅ Grupo inexistente: validação ao tentar entrar, sair ou listar membros
- ✅ Usuário não membro: não pode enviar mensagem para grupo que não pertence
- ✅ Mensagens sem comando: retorna erro solicitando uso de -msg ou -msgt

### Características Técnicas
- 🔄 O servidor suporta múltiplas conexões simultâneas usando threads
- 💾 Mensagens offline são armazenadas em memória e entregues no login
- 🕐 Todas as mensagens incluem timestamp no formato DD/MM/YYYY HH:MM:SS
- 🔒 Validação de parâmetros em todos os comandos
- 📱 Interface limpa com feedback claro de todas as operações
- ⚡ Use Ctrl+C para encerrar o cliente ou servidor a qualquer momento

### Exemplos de Uso

```bash
# Criar e usar um grupo
>> -criargrupo desenvolvedores
>> -entrargrupo desenvolvedores
>> -msg G desenvolvedores Olá pessoal!

# Enviar mensagem direta
>> -msg U joao Oi João, tudo bem?

# Broadcast para todos online
>> -msgt C Servidor será reiniciado em 5 minutos

# Listar usuários e grupos
>> -listarusuarios
>> -listargrupos
>> -listausrgrupo desenvolvedores
```
