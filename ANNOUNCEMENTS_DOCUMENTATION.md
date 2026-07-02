# Sistema de Gerenciamento de Anúncios

## 📋 Resumo da Implementação

Sistema completo de gerenciamento de anúncios para a Mergington High School, controlado pelo banco de dados MongoDB, com interface amigável e autenticação obrigatória.

## ✨ Funcionalidades Implementadas

### Backend (Python/FastAPI)

#### 1. Modelo de Dados
- **Coleção MongoDB**: `announcements`
- **Campos**:
  - `_id`: ObjectId único
  - `title`: Título do anúncio (obrigatório)
  - `message`: Corpo do anúncio (obrigatório)
  - `start_date`: Data de início (opcional) - formato: YYYY-MM-DD
  - `expiration_date`: Data de expiração (obrigatório) - formato: YYYY-MM-DD
  - `created_by`: Usuário que criou (preenchido automaticamente)
  - `created_at`: Data de criação (timestamp automático)

#### 2. Endpoints da API

**GET `/announcements`**
- Lista anúncios ativos (não expirados e começados)
- Sem autenticação necessária
- Filtra por datas automaticamente
- Ordenação por data mais recente primeiro

**GET `/announcements/all`**
- Lista todos os anúncios incluindo expirados
- Sem autenticação (visível apenas para admins no frontend)
- Para gerenciamento completo

**POST `/announcements`**
- Criar novo anúncio
- Requer autenticação: `?teacher_username=<username>`
- Parâmetros: `title`, `message`, `expiration_date`, `start_date` (opcional)
- Validação: data de início não pode ser após expiração

**PUT `/announcements/{announcement_id}`**
- Atualizar anúncio existente
- Requer autenticação: `?teacher_username=<username>`
- Todos os campos são opcionais (apenas envia o que mudar)

**DELETE `/announcements/{announcement_id}`**
- Deletar anúncio
- Requer autenticação: `?teacher_username=<username>`

### Frontend (HTML/CSS/JavaScript)

#### 1. Interface do Usuário

**Banner Dinâmico**
- Container `#announcement-banner-container`
- Exibe anúncios ativos automaticamente
- Design atraente com animação de slide-down
- Atualiza em tempo real

**Botão de Gerenciamento**
- Localizado no header, ao lado do nome do usuário
- Ícone: ⚙️ + texto "Announcements"
- Visível apenas para usuários autenticados
- Hover effect para melhor UX

**Modal de Gerenciamento**
- Divide em dois painéis:
  - **Painel Esquerdo**: Formulário de criar/editar
  - **Painel Direito**: Lista de todos os anúncios

#### 2. Funcionalidades JavaScript

**Carregamento de Anúncios**
- Função `loadActiveAnnouncements()`: Carrega anúncios ativos
- Função `loadAllAnnouncements()`: Carrega todos para o admin
- Auto-refresh ao criar/editar/deletar

**Criar Anúncio**
- Formulário com campos: título, mensagem, data início, data expiração
- Validação de datas no frontend
- Feedback visual com mensagens de sucesso/erro

**Editar Anúncio**
- Clique no botão "Edit" em um anúncio existente
- Preenche o formulário automaticamente
- Muda o botão para "Update Announcement"
- Botão "Cancel" aparece para cancelar edição

**Deletar Anúncio**
- Clique no botão "Delete"
- Confirmação antes de deletar (não pode ser desfeito)
- Remove da lista imediatamente após confirmação

**Proteção de Segurança**
- Função `escapeHtml()`: Previne XSS
- Todos os inputs são sanitizados
- Autenticação obrigatória para CRUD
- Senhas não são enviadas para o frontend

#### 3. Responsividade

**Desktop**
- Layout lado-a-lado: formulário à esquerda, lista à direita
- Modal com max-width: 800px

**Mobile**
- Layout empilhado: formulário acima, lista abaixo
- Modal responsivo com padding adequado
- Toque e scroll funcionam normalmente

## 🎨 Design e UX

### Paleta de Cores
- Primária: #1a237e (azul escuro)
- Sucesso: #2e7d32 (verde)
- Erro: #c62828 (vermelho)
- Fundo: #f5f5f5 (cinza claro)

### Animações
- Slide-down ao aparecer banner
- Fade-in/fade-out do modal
- Hover effects em botões
- Transições suaves (0.2-0.3s)

### Tipografia
- Font: Arial, sans-serif
- Hierarquia visual clara
- Labels e placeholders descritivos

## 🔒 Segurança

### Autenticação
- Verifica usuário autenticado em todas as operações CRUD
- Usa `localStorage` para manter sessão
- Valida credenciais com banco de dados

### Validação de Dados
- Datas validadas em YYYY-MM-DD
- Expiração obrigatória, início opcional
- Validação lógica: início ≤ expiração
- Escapamento de HTML para prevenir XSS

### Banco de Dados
- ObjectId único para cada anúncio
- Timestamps automáticos
- Rastreamento de criador

## 📊 Dados Iniciais

Anúncio de exemplo criado na inicialização:
```json
{
  "title": "Activity registration is open!",
  "message": "Register now for our extracurricular activities. Limited spots available!",
  "start_date": null,
  "expiration_date": "2026-12-31"
}
```

## 🧪 Testes de API

Todos os endpoints foram testados com sucesso:
- ✅ GET anúncios ativos
- ✅ GET todos anúncios
- ✅ POST criar anúncio
- ✅ PUT atualizar anúncio
- ✅ DELETE deletar anúncio
- ✅ Validação de autenticação
- ✅ Validação de datas
- ✅ Filtragem de anúncios expirados

## 📁 Arquivos Modificados

1. `/src/backend/database.py` - Adiciona coleção e dados iniciais
2. `/src/backend/routers/announcements.py` - Novo arquivo com endpoints
3. `/src/backend/routers/__init__.py` - Importa novo router
4. `/src/app.py` - Registra novo router
5. `/src/static/index.html` - Adiciona modal e container de banner
6. `/src/static/styles.css` - Estilos para modal e banner
7. `/src/static/app.js` - Lógica de gerenciamento de anúncios

## 🚀 Como Usar

### Para Usuários Autenticados (Teachers)

1. Fazer login com credenciais
2. Clicar em "Announcements" no header
3. No modal:
   - **Criar**: Preencher formulário e clicar "Create Announcement"
   - **Editar**: Clicar "Edit" no anúncio e depois "Update Announcement"
   - **Deletar**: Clicar "Delete" e confirmar
4. Fechar modal com X ou clicando fora

### Para Todos os Usuários

- Ver anúncios ativos no banner dinâmico no topo
- Anúncios aparecem automaticamente quando não expirados

## 🔍 Troubleshooting

**Anúncio não aparece no banner:**
- Verificar se a data de início é <= hoje
- Verificar se a data de expiração é >= hoje
- Recarregar página para atualizar

**Erro ao criar anúncio:**
- Confirmar que está autenticado
- Verificar se a data de início é anterior à expiração
- Verificar console do navegador para mais detalhes

**Modal não abre:**
- Verificar se está autenticado
- Limpar cache do navegador
- Recarregar página
