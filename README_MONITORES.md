# 🖥️ Sistema de Monitoramento de Monitores

## 📋 Sobre o Sistema

Sistema completo de monitoramento de eventos de monitores, convertido do HTML original para Streamlit com integração ao Google Sheets e Google Apps Script.

### ✨ Funcionalidades Principais

- **📊 Dashboard em Tempo Real**: Métricas e indicadores atualizados
- **📋 Gestão de Eventos**: Controle completo de solicitações de monitores
- **🔄 Status Dinâmico**: Atualização de status de atendimento em tempo real
- **📈 Análises Avançadas**: Relatórios e gráficos interativos
- **📥 Export de Dados**: Exportação para CSV com dados completos
- **🚨 Sistema de Alertas**: Notificações automáticas para eventos críticos
- **🎨 Interface Fiel**: Design idêntico ao HTML original com tema Nubank

---

## 🏗️ Arquitetura do Sistema

### **📁 Estrutura de Arquivos:**

```
sistema-monitores/
├── monitor_dashboard_app.py    # 🎨 Aplicação Streamlit principal
├── monitor_code.gs             # ⚙️ Google Apps Script (backend)
├── monitor_config.py           # 📋 Configurações centralizadas
├── requirements.txt            # 📦 Dependências Python
└── README_MONITORES.md         # 📚 Esta documentação
```

### **🔧 Componentes:**

1. **Frontend (Streamlit)**: Interface web moderna e responsiva
2. **Backend (Google Apps Script)**: Lógica de negócio e integração
3. **Dados (Google Sheets)**: Armazenamento e sincronização
4. **Config**: Configurações centralizadas e validações

---

## 🚀 Setup e Instalação

### **1. Configuração do Google Sheets**

**📊 Planilha Principal:**
- **ID**: `1hI6WWiH03AvXFxMCpPpYtIhQEU062C_k4utIE6YyctY`
- **Aba**: `Calendário de eventos - Monitores`
- **GID**: `1469973439`

**📋 Estrutura de Colunas:**
| A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|
| Data Solicitação | Data Montagem | Sala | Monitores | Data Desmontagem | Observações | Reporter | Key | Status | Status Atendimento |

### **2. Google Apps Script**

1. **Criar Projeto**: [script.google.com](https://script.google.com)
2. **Colar Código**: Conteúdo do arquivo `monitor_code.gs`
3. **Configurar Triggers**: Executar função `setupTriggers()`
4. **Testar Sistema**: Executar função `testMonitorSystem()`

### **3. Aplicação Streamlit**

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run monitor_dashboard_app.py
```

### **4. Deploy no Streamlit Cloud**

1. **Repository**: Upload dos arquivos para GitHub
2. **App Configuration**:
   - **Main file**: `monitor_dashboard_app.py`
   - **Python version**: 3.8+
3. **Secrets** (opcional):
   ```toml
   [google_sheets]
   # Credenciais do Google Sheets (se necessário)
   ```

---

## 📊 Funcionalidades Detalhadas

### **🎯 Dashboard Principal**

**📈 Cards de Resumo:**
- **Total de Monitores**: Soma de todos os monitores solicitados
- **Dentro do Limite**: Monitores confirmados e concluídos
- **Excedente**: Monitores em status excedente
- **Última Atualização**: Timestamp da última sincronização

**🔍 Filtros Avançados:**
- Busca textual em todos os campos
- Filtro por status do evento
- Filtro por status de atendimento
- Paginação automática

### **📋 Gestão de Eventos**

**📝 Campos de Evento:**
- **Data Solicitação**: Quando foi solicitado
- **Data Montagem**: Quando será montado
- **Sala**: Local do evento
- **Monitores**: Quantidade solicitada
- **Reporter**: Responsável pela solicitação
- **Key**: Identificador único
- **Status**: Pendente, Confirmado, Excedente, Concluído
- **Status Atendimento**: Não Iniciado, Em Andamento, Concluído, Pendente

**⚡ Ações Rápidas:**
- Atualização de status em tempo real
- Marcação como concluído
- Exportação de dados
- Geração de relatórios

### **🚨 Sistema de Alertas**

**📊 Tipos de Alertas:**
- **⚠️ Eventos Pendentes**: Requer ação imediata
- **🚫 Eventos Excedentes**: Acima da capacidade
- **ℹ️ Eventos sem Reporter**: Falta responsável
- **⏰ Eventos Vencidos**: Data de montagem passou

### **📈 Análises e Relatórios**

**📊 Gráficos Disponíveis:**
- Distribuição por status (pizza)
- Monitores por sala (barras)
- Evolução temporal (linhas)
- Análise por reporter

**📋 Relatórios:**
- Resumo executivo
- Análise por sala
- Análise por responsável
- Recomendações automáticas

---

## ⚙️ Configurações

### **🎨 Tema Visual**

```python
THEME_COLORS = {
    'PRIMARY': '#8a05be',        # Roxo Nubank
    'PRIMARY_DARK': '#4500a0',   # Roxo escuro
    'SUCCESS': '#2b8a3e',        # Verde sucesso
    'WARNING': '#e67700',        # Laranja aviso
    'DANGER': '#c92a2a',         # Vermelho perigo
    'INFO': '#1971c2'            # Azul informação
}
```

### **📋 Status de Eventos**

```python
EVENT_STATUS = {
    'PENDENTE': 'Pendente',      # Aguardando confirmação
    'CONFIRMADO': 'Confirmado',  # Aprovado
    'EXCEDENTE': 'Excedente',    # Acima do limite
    'CONCLUIDO': 'Concluído'     # Finalizado
}
```

### **🔧 Limites de Monitores**

```python
MONITOR_LIMITS = {
    'Sala pequena': {'min': 1, 'max': 3, 'optimal': 2},
    'Sala média': {'min': 2, 'max': 5, 'optimal': 3},
    'Sala grande': {'min': 3, 'max': 8, 'optimal': 5},
    'Auditório': {'min': 5, 'max': 15, 'optimal': 10}
}
```

---

## 🔌 Integração Google Apps Script

### **🚀 Funções Principais:**

```javascript
// Carregar dados da planilha
loadMonitorData()

// Atualizar status de evento
updateEventStatus(key, newStatus)

// Marcar como concluído
markEventAsCompleted(key)

// Exportar para CSV
exportToCSV()

// Gerar relatório detalhado
generateDetailedReport()
```

### **⏰ Triggers Automáticos:**

```javascript
// Configurar atualização automática
setupTriggers()

// Função executada a cada hora
autoUpdateMonitorData()
```

---

## 📊 APIs e Endpoints

### **🔗 Google Sheets URLs:**

```python
# Consulta gviz
GVIZ_URL = 'https://docs.google.com/spreadsheets/d/{id}/gviz/tq'

# Export CSV
CSV_URL = 'https://docs.google.com/spreadsheets/d/{id}/export?format=csv'

# Visualizar planilha
SHEET_URL = 'https://docs.google.com/spreadsheets/d/{id}/edit'
```

### **📋 Parâmetros de Consulta:**

```python
params = {
    'tqx': 'out:json',           # Formato JSON
    'sheet': 'Nome da Aba',      # Aba específica
    'headers': '1',              # Incluir cabeçalho
    'tq': 'SELECT *'             # Query SQL-like
}
```

---

## 🛠️ Manutenção e Monitoramento

### **📊 Logs e Debug:**

```python
# Ativar logs detalhados
console.log('🔄 Carregando dados...')
console.log('✅ Dados carregados:', result.totalRecords)
console.error('❌ Erro:', error.message)
```

### **🧪 Testes:**

```python
# Executar no Google Apps Script
testMonitorSystem()
```

### **🔄 Atualização Automática:**

- **Frequência**: A cada hora
- **Trigger**: `autoUpdateMonitorData()`
- **Alertas**: Email para eventos críticos

---

## 🚨 Troubleshooting

### **❌ Problemas Comuns:**

1. **Erro de Permissão**:
   - Verificar compartilhamento da planilha
   - Validar credenciais do Google Sheets

2. **Dados Não Carregam**:
   - Confirmar ID da planilha
   - Verificar nome da aba
   - Testar URLs de API

3. **Status Não Atualiza**:
   - Verificar triggers do Apps Script
   - Confirmar permissões de escrita

### **🔧 Comandos de Debug:**

```bash
# Testar conexão
streamlit run monitor_dashboard_app.py --logger.level=debug

# Verificar dependências
pip list | grep -E "(streamlit|gspread|plotly)"

# Validar configurações
python -c "from monitor_config import monitor_config; print(monitor_config.get_sheet_url())"
```

---

## 📈 Roadmap e Melhorias

### **🎯 Próximas Funcionalidades:**

- [ ] 📱 **App Mobile**: Interface responsiva para dispositivos móveis
- [ ] 🔔 **Notificações Push**: Alertas em tempo real
- [ ] 📧 **Email Automático**: Relatórios periódicos por email
- [ ] 🤖 **IA Predictiva**: Previsão de demanda de monitores
- [ ] 📊 **Dashboard Executivo**: Visão estratégica para gestores
- [ ] 🔄 **Sincronização Bidirecional**: Edição direta na interface
- [ ] 📋 **Formulário de Solicitação**: Interface para novos pedidos
- [ ] 🗓️ **Integração Calendário**: Sincronização com Google Calendar

### **🛠️ Melhorias Técnicas:**

- [ ] ⚡ **Cache Inteligente**: Otimização de performance
- [ ] 🔒 **Autenticação**: Sistema de login e permissões
- [ ] 📊 **Métricas Avançadas**: KPIs e indicadores personalizados
- [ ] 🔍 **Busca Avançada**: Filtros complexos e busca fuzzy
- [ ] 📱 **PWA**: Progressive Web App para instalação
- [ ] 🌐 **Multi-idioma**: Suporte para português e inglês

---

## 👥 Suporte e Contribuição

### **📞 Contatos:**

- **GitHub**: [Sistema de Monitores](https://github.com/usuario/sistema-monitores)
- **Issues**: Reportar bugs e sugestões
- **Documentação**: README e código comentado

### **🤝 Como Contribuir:**

1. **Fork** do repositório
2. **Branch** para nova funcionalidade
3. **Commit** com mensagens claras
4. **Pull Request** com descrição detalhada

---

**🎉 Sistema de Monitoramento de Monitores - Pronto para Produção!**

*Desenvolvido com ❤️ usando Streamlit, Google Apps Script e Google Sheets*

---

## 📊 **Status do Projeto: ✅ COMPLETO E FUNCIONAL**

- ✅ Interface fiel ao HTML original
- ✅ Integração Google Sheets completa
- ✅ Google Apps Script implementado
- ✅ Sistema de alertas funcionando
- ✅ Exportação de dados
- ✅ Relatórios interativos
- ✅ Documentação completa
- ✅ Pronto para deploy
