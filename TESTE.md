# 🧪 Guia de Testes do Sistema de Chat

## Cenários de Teste

### 1. Teste de Validação de Nickname Único

**Objetivo:** Verificar que não é possível conectar dois usuários com o mesmo nickname.

**Passos:**
1. Inicie o servidor: `python server.py`
2. Em um terminal, inicie o cliente 1: `python client.py`
3. Digite o nome "João" quando solicitado
4. Em outro terminal, inicie o cliente 2: `python client.py`
5. Digite o nome "João" novamente

**Resultado Esperado:**
- Cliente 1 conecta com sucesso
- Cliente 2 recebe: `ERRO: Usuário já conectado` e é desconectado

---

### 2. Teste de Criação e Gerenciamento de Grupos

**Objetivo:** Testar criação, listagem e entrada em grupos.

**Passos:**
1. Cliente 1 (João): `-criargrupo desenvolvedores`
2. Cliente 1: `-listargrupos`
3. Cliente 2 (Maria): `-entrargrupo desenvolvedores`
4. Cliente 1: `-listausrgrupo desenvolvedores`
5. Cliente 1: `-criargrupo desenvolvedores` (tentar duplicar)

**Resultado Esperado:**
- Grupo criado com sucesso
- Lista mostra "desenvolvedores"
- Maria entra no grupo
- Lista de membros mostra João e Maria
- Erro ao tentar criar grupo duplicado: `ERRO: Grupo 'desenvolvedores' já existente`

---

### 3. Teste de Mensagens Direcionadas para Usuário

**Objetivo:** Testar envio de mensagens diretas entre usuários.

**Passos:**
1. Cliente 1 (João): `-msg U Maria Olá Maria!`
2. Cliente 2 (Maria) deve receber a mensagem formatada

**Resultado Esperado:**
- Maria recebe: `(João, 23/11/2025 14:30:45) Olá Maria!`
- João recebe confirmação: `Mensagem enviada para Maria`

---

### 4. Teste de Mensagens para Grupo

**Objetivo:** Testar envio de mensagens para grupo.

**Passos:**
1. Cliente 1 (João): `-entrargrupo desenvolvedores`
2. Cliente 2 (Maria): `-entrargrupo desenvolvedores`
3. Cliente 1: `-msg G desenvolvedores Reunião às 15h!`

**Resultado Esperado:**
- Maria recebe: `(João, desenvolvedores, 23/11/2025 14:35:12) Reunião às 15h!`
- João recebe confirmação com contagem de membros

---

### 5. Teste de Mensagens Offline

**Objetivo:** Verificar armazenamento e entrega de mensagens offline.

**Passos:**
1. Cliente 1 (João) conectado
2. Cliente 2 (Maria) desconectado
3. Cliente 1: `-msg U Maria Mensagem importante!`
4. Cliente 2 (Maria) se conecta novamente

**Resultado Esperado:**
- João recebe: `Mensagem armazenada para Maria (offline)`
- Quando Maria conecta, recebe automaticamente: `(João, 23/11/2025 14:40:00) Mensagem importante!`

---

### 6. Teste de Broadcast Seletivo

**Objetivo:** Testar envio de mensagens para diferentes grupos de usuários.

**Passos:**
1. Cliente 1 (João) online
2. Cliente 2 (Maria) online
3. Cliente 3 (Pedro) offline
4. Cliente 1: `-msgt C Mensagem para online`
5. Cliente 1: `-msgt D Mensagem para offline`
6. Cliente 1: `-msgt T Mensagem para todos`

**Resultado Esperado:**
- `-msgt C`: Apenas Maria recebe
- `-msgt D`: Armazenada para Pedro
- `-msgt T`: Maria recebe imediatamente, Pedro recebe ao conectar

---

### 7. Teste de Comandos Inválidos

**Objetivo:** Verificar tratamento de erros.

**Passos:**
1. Cliente 1: `-comando_invalido`
2. Cliente 1: `-criargrupo` (sem nome)
3. Cliente 1: `-msg` (sem parâmetros)
4. Cliente 1: `-entrargrupo grupo_inexistente`
5. Cliente 1: `Olá` (mensagem sem comando)

**Resultado Esperado:**
- `ERRO: Comando inexistente`
- `ERRO: Comando inválido. Use: -criargrupo NOME_DO_GRUPO`
- `ERRO: Comando inválido. Use: -msg U/G NICK/GRUPO MENSAGEM`
- `ERRO: Grupo 'grupo_inexistente' não existe`
- `ERRO: Use -msg ou -msgt para enviar mensagens`

---

### 8. Teste de Listagem de Usuários

**Objetivo:** Verificar listagem de usuários online.

**Passos:**
1. Conectar 3 clientes: João, Maria, Pedro
2. Cliente 1: `-listarusuarios`

**Resultado Esperado:**
```
Usuários online:
- João
- Maria
- Pedro
```

---

### 9. Teste de Grupo Sem Membros

**Objetivo:** Verificar comportamento ao listar grupo vazio.

**Passos:**
1. Cliente 1: `-criargrupo vazio`
2. Cliente 1: `-listausrgrupo vazio`

**Resultado Esperado:**
- `Grupo 'vazio' não possui membros`

---

### 10. Teste de Envio para Grupo Sem Ser Membro

**Objetivo:** Verificar restrição de envio para grupos.

**Passos:**
1. Cliente 1 (João): `-criargrupo privado`
2. Cliente 2 (Maria): `-msg G privado Tentando enviar`

**Resultado Esperado:**
- `ERRO: Você não é membro do grupo 'privado'`

---

## Checklist de Validações Implementadas

- [x] Validação de nickname único
- [x] Validação de comandos inválidos
- [x] Validação de parâmetros obrigatórios
- [x] Validação de grupo existente/inexistente
- [x] Validação de usuário existente/inexistente
- [x] Validação de pertencimento a grupo
- [x] Formatação de mensagens com timestamp
- [x] Armazenamento de mensagens offline
- [x] Entrega automática de mensagens offline
- [x] Tratamento de erros com mensagens claras

## Como Executar os Testes

1. **Abra 4 terminais:**
   - Terminal 1: Servidor
   - Terminal 2: Cliente 1
   - Terminal 3: Cliente 2
   - Terminal 4: Cliente 3

2. **Execute os cenários na ordem sugerida**

3. **Observe os logs do servidor** para acompanhar as operações

4. **Verifique se todos os resultados esperados são obtidos**
