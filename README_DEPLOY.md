# 🚀 Sistema de Controle de Perdas - Deploy Guide

## ✨ Sobre o Sistema

Sistema completo de controle de perdas e entradas de gadgets, convertido do HTML/JavaScript original para Streamlit com integração ao Google Sheets.

### 🎯 Funcionalidades Principais

- **📝 Registro de Perdas**: Formulário completo com validação
- **➕ Registro de Entradas**: Suporte a itens personalizados
- **📊 Dashboard Interativo**: Gráficos multi-período
- **💰 Orçamentos Inteligentes**: Geração baseada em prioridades
- **📦 Inventário Completo**: Histórico de movimentações
- **💾 Persistência de Dados**: Google Sheets + backup local
- **🎨 Interface Fiel**: Design idêntico ao HTML original

---

## 🛠️ Setup Rápido

### 1. **Deploy no Streamlit Cloud**

1. **Acesse**: [share.streamlit.io](https://share.streamlit.io)

2. **Configure**:
   - **Repository**: `Danilow88/sistema-controle-perdas`
   - **Branch**: `main`
   - **Main file**: `streamlit_app.py`

3. **Secrets** (opcional para Google Sheets):
   ```toml
   [google_sheets]
   type = "service_account"
   project_id = "seu-project-id"
   private_key_id = "sua-private-key-id"
   private_key = "-----BEGIN PRIVATE KEY-----\nsua-chave-privada\n-----END PRIVATE KEY-----\n"
   client_email = "seu-email@seu-project.iam.gserviceaccount.com"
   client_id = "seu-client-id"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/seu-email%40seu-project.iam.gserviceaccount.com"
   ```

4. **Deploy**: Clique em "Deploy!"

---

## 🔧 Setup Local (Desenvolvimento)

### 1. **Clone o Repositório**
```bash
git clone https://github.com/Danilow88/sistema-controle-perdas.git
cd sistema-controle-perdas
```

### 2. **Ambiente Virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. **Instalar Dependências**
```bash
pip install -r requirements.txt
```

### 4. **Configurar Google Sheets** (Opcional)
```bash
# Copiar template de credenciais
cp credentials_template.json credentials.json

# Editar com suas credenciais reais
nano credentials.json
```

### 5. **Executar Aplicação**
```bash
streamlit run streamlit_app.py
```

---

## 📊 Integração Google Sheets

### 1. **Criar Service Account**

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie novo projeto ou selecione existente
3. Ative a API do Google Sheets
4. Crie Service Account
5. Gere chave JSON

### 2. **Configurar Planilha**

1. **ID da Planilha**: `1IMcXLIyOJOANhfxKfzYlwtBqtsXJfRMhCPmoKQdCtdY`
2. **Aba**: `Inventory`
3. **Compartilhar** planilha com o email do Service Account

### 3. **Estrutura da Planilha**

| A | B | C | D | E | F | G | H | I | J | K | L |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Inventory ID | Item ID | DateTime | Amount | building | Email | Invoice | Sku | Andar | Tipod de movimentacao | Fornecedor | Prateleira |

---

## 🎨 Personalização

### **Cores e Tema**
- **Roxo Principal**: `#8A2BE2`
- **Roxo Secundário**: `#9370DB`
- **Gradiente**: `135deg, #8A2BE2 0%, #4B0082 100%`

### **Estrutura de Arquivos**
```
sistema-controle-perdas/
├── streamlit_app.py          # App principal
├── data_manager.py           # Gerenciador de dados
├── config_app.py             # Configurações
├── requirements.txt          # Dependências
├── credentials_template.json # Template de credenciais
├── .gitignore               # Arquivos ignorados
└── README_DEPLOY.md         # Este arquivo
```

---

## 🚨 Troubleshooting

### **Erro de Módulo**
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### **Erro Google Sheets**
1. Verificar credenciais em `credentials.json`
2. Confirmar compartilhamento da planilha
3. Validar ID da planilha

### **Erro de Permissão**
```bash
# Dar permissões de execução
chmod +x venv/bin/python
```

---

## 📈 Métricas e Monitoramento

### **Dados Salvos**
- ✅ **Local**: `inventory_data.json`
- ✅ **Google Sheets**: Planilha configurada
- ✅ **Session State**: Dados temporários

### **Estatísticas Disponíveis**
- Total de registros
- Entradas vs Perdas
- Itens únicos
- Prédios ativos
- Range de datas

---

## 🎯 Roadmap

- [x] ✅ Conversão HTML → Streamlit
- [x] ✅ Interface fiel ao original
- [x] ✅ Salvamento de dados
- [x] ✅ Integração Google Sheets
- [x] ✅ Dashboard interativo
- [x] ✅ Sistema de orçamentos
- [ ] 🔄 Relatórios avançados
- [ ] 🔄 Notificações automáticas
- [ ] 🔄 API REST

---

## 💡 Dicas de Uso

1. **Registro de Perdas**: Sempre informar prédio e andar
2. **Entradas**: Usar "ESTOQUE" como localização padrão
3. **Orçamentos**: Baseados em prioridades automáticas
4. **Backup**: Dados salvos localmente e no Google Sheets
5. **Filtros**: Usar modal de inventário para análises

---

## 📞 Suporte

- **GitHub**: [Danilow88/sistema-controle-perdas](https://github.com/Danilow88/sistema-controle-perdas)
- **Issues**: Reportar bugs e sugestões
- **Streamlit Cloud**: [Aplicação Online](https://share.streamlit.io)

---

**🎉 Sistema pronto para uso em produção!**

*Desenvolvido com ❤️ usando Streamlit, Python e Google Sheets*
