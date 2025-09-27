# 🚀 Guia de Deploy no Streamlit Cloud

## 📋 Pré-requisitos

1. **Conta no GitHub** - para hospedar o código
2. **Conta no Streamlit Cloud** - [share.streamlit.io](https://share.streamlit.io)
3. **Credenciais do Google Sheets** - service account JSON
4. **Token do JIRA** - para integração com tickets

## 🛠️ Passo a Passo

### 1. Preparar o Repositório

```bash
# 1. Criar repositório no GitHub
git init
git add .
git commit -m "Initial commit: Sistema de Controle de Perdas"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/sistema-controle-perdas.git
git push -u origin main
```

### 2. Configurar Credenciais do Google

1. **Google Cloud Console:**
   - Acesse [console.cloud.google.com](https://console.cloud.google.com)
   - Crie um novo projeto ou use existente
   - Ative a Google Sheets API
   - Vá em "IAM & Admin" > "Service Accounts"
   - Crie uma nova service account
   - Baixe o arquivo JSON das credenciais

2. **Compartilhar Planilhas:**
   ```
   Compartilhe suas planilhas com o email da service account:
   - Planilha de Inventário: 1IMcXLIyOJOANhfxKfzYlwtBqtsXJfRMhCPmoKQdCtdY
   - Planilha de Monitores: 1hI6WWiH03AvXFxMCpPpYtIhQEU062C_k4utIE6YyctY
   ```

### 3. Configurar JIRA

1. **Obter Token de API:**
   - Acesse [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
   - Crie um novo token de API
   - Guarde o token com segurança

### 4. Deploy no Streamlit Cloud

1. **Acessar Streamlit Cloud:**
   - Vá para [share.streamlit.io](https://share.streamlit.io)
   - Faça login com GitHub

2. **Criar Nova App:**
   - Clique em "New app"
   - Selecione seu repositório
   - Branch: `main`
   - Main file path: `streamlit_app.py`

3. **Configurar Secrets:**
   
   No painel de configuração da app, adicione os secrets:

   ```toml
   # Google Sheets Service Account
   [google_sheets]
   type = "service_account"
   project_id = "seu-project-id"
   private_key_id = "sua-private-key-id"
   private_key = "-----BEGIN PRIVATE KEY-----\nsua-private-key-completa\n-----END PRIVATE KEY-----\n"
   client_email = "seu-service-account@projeto.iam.gserviceaccount.com"
   client_id = "seu-client-id"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "sua-cert-url"

   # IDs das Planilhas
   INVENTORY_SPREADSHEET_ID = "1IMcXLIyOJOANhfxKfzYlwtBqtsXJfRMhCPmoKQdCtdY"
   MONITORS_SPREADSHEET_ID = "1hI6WWiH03AvXFxMCpPpYtIhQEU062C_k4utIE6YyctY"

   # JIRA
   JIRA_BASE_URL = "https://nubank.atlassian.net"
   JIRA_EMAIL = "seu-email@nubank.com.br"
   JIRA_API_TOKEN = "seu-token-jira"
   JIRA_PROJECT_KEY = "TS"

   # Configurações da App
   APP_TITLE = "Sistema de Controle de Perdas"
   DEBUG = false
   TIMEZONE = "America/Sao_Paulo"
   CACHE_TTL = 300
   ```

4. **Deploy:**
   - Clique em "Deploy"
   - Aguarde o build completar
   - Acesse sua aplicação na URL fornecida

## 🔧 Configurações Avançadas

### Variáveis de Ambiente Opcionais

```toml
# Cache e Performance
CACHE_TTL = 300
MAX_RECORDS_DISPLAY = 1000

# Configurações de UI
THEME_PRIMARY_COLOR = "#8A05BE"
THEME_BACKGROUND_COLOR = "#FFFFFF"

# Configurações de Logging
LOG_LEVEL = "INFO"
```

### Configuração de Domínio Customizado

1. **Configurar CNAME:**
   ```
   CNAME: seu-dominio.com -> shares.streamlit.io
   ```

2. **Configurar no Streamlit Cloud:**
   - Vá em Settings > General
   - Adicione seu domínio customizado

## 🚨 Troubleshooting

### Problemas Comuns

1. **Erro de Credenciais Google:**
   ```
   ❌ Erro: "Insufficient permissions"
   ✅ Solução: Verificar se a service account tem acesso às planilhas
   ```

2. **Erro de JIRA:**
   ```
   ❌ Erro: "Authentication failed"
   ✅ Solução: Verificar email e token do JIRA
   ```

3. **Erro de Import:**
   ```
   ❌ Erro: "ModuleNotFoundError"
   ✅ Solução: Verificar requirements.txt
   ```

4. **Erro de Secrets:**
   ```
   ❌ Erro: "KeyError: secrets"
   ✅ Solução: Verificar formatação do secrets.toml
   ```

### Logs e Debug

- Acesse os logs da aplicação no painel do Streamlit Cloud
- Use `st.write()` para debug temporário
- Configure `DEBUG = true` nos secrets para mais informações

## 📊 Monitoramento

### Métricas Importantes

- **Uptime da aplicação**
- **Tempo de resposta das APIs**
- **Uso de recursos (CPU/Memory)**
- **Número de usuários ativos**

### Alertas

Configure alertas para:
- Falhas de autenticação
- Timeouts de API
- Erros críticos na aplicação

## 🔄 Atualizações

### Deploy Automático

O Streamlit Cloud faz deploy automático quando você faz push para a branch `main`:

```bash
git add .
git commit -m "feat: nova funcionalidade"
git push origin main
```

### Rollback

Para fazer rollback:
1. Acesse o painel do Streamlit Cloud
2. Vá em "Manage app"
3. Selecione um commit anterior
4. Clique em "Reboot"

## 📞 Suporte

- **Documentação Streamlit:** [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum:** [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues:** Para bugs específicos do projeto

## ✅ Checklist de Deploy

- [ ] Repositório criado no GitHub
- [ ] Credenciais do Google configuradas
- [ ] Token do JIRA obtido
- [ ] Planilhas compartilhadas com service account
- [ ] App criada no Streamlit Cloud
- [ ] Secrets configurados corretamente
- [ ] Primeira execução testada
- [ ] Funcionalidades principais validadas
- [ ] Documentação atualizada
- [ ] Usuários notificados da nova URL
