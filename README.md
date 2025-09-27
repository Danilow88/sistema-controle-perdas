# Sistema de Controle de Perdas e Monitoramento

## 📋 Sobre o Projeto

Sistema completo para controle de perdas de gadgets e monitoramento de equipamentos, desenvolvido em Python com interface Streamlit. Integra com Google Sheets e JIRA para automação completa do processo.

## 🚀 Funcionalidades

### 📊 Dashboard de Perdas
- Visualização de perdas por período (semanal, mensal, trimestral, anual)
- Gráficos por tipo de item (Headsets, Mouses, Teclados, Adaptadores, USB Gorila)
- Análise por prédio (HQ1, HQ2, Spark)
- Relatórios executivos

### 📦 Controle de Inventário
- Registro de entradas e saídas
- Upload de dados via CSV
- Controle por localização e fornecedor
- Histórico completo de movimentações

### 🖥️ Monitoramento de Monitores
- Integração com JIRA para tickets de monitores
- Dashboard de solicitações
- Controle de status de atendimento
- Relatórios de SLA

### 💰 Orçamentos
- Geração automática de orçamentos baseado em perdas
- Análise de custos por período
- Sugestões de compra inteligentes

## 🛠️ Tecnologias

- **Python 3.9+**
- **Streamlit** - Interface web
- **Pandas** - Manipulação de dados
- **Plotly** - Visualizações interativas
- **Google Sheets API** - Integração com planilhas
- **JIRA API** - Integração com tickets
- **gspread** - Cliente Google Sheets

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/sistema-controle-perdas.git
cd sistema-controle-perdas
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

4. Execute a aplicação:
```bash
streamlit run app.py
```

## ⚙️ Configuração

### Google Sheets API
1. Crie um projeto no Google Cloud Console
2. Ative a Google Sheets API
3. Crie credenciais de service account
4. Baixe o arquivo JSON e salve como `credentials.json`

### JIRA API
1. Obtenha seu token de API do JIRA
2. Configure as variáveis no arquivo `.env`:
```env
JIRA_BASE_URL=https://sua-instancia.atlassian.net
JIRA_EMAIL=seu-email@empresa.com
JIRA_API_TOKEN=seu-token-aqui
```

### Google Sheets
Configure os IDs das planilhas no `.env`:
```env
INVENTORY_SPREADSHEET_ID=seu-id-da-planilha-inventory
MONITORS_SPREADSHEET_ID=seu-id-da-planilha-monitores
```

## 📁 Estrutura do Projeto

```
sistema-controle-perdas/
├── app.py                 # Aplicação principal Streamlit
├── requirements.txt       # Dependências Python
├── README.md             # Este arquivo
├── .env.example          # Exemplo de variáveis de ambiente
├── credentials.json      # Credenciais Google (não versionado)
├── config/
│   ├── __init__.py
│   ├── settings.py       # Configurações globais
│   └── database.py       # Configuração de banco
├── services/
│   ├── __init__.py
│   ├── google_sheets.py  # Integração Google Sheets
│   ├── jira_client.py    # Cliente JIRA
│   ├── inventory.py      # Serviços de inventário
│   └── monitoring.py     # Serviços de monitoramento
├── utils/
│   ├── __init__.py
│   ├── data_processing.py # Processamento de dados
│   ├── charts.py         # Geração de gráficos
│   └── helpers.py        # Funções auxiliares
├── pages/
│   ├── __init__.py
│   ├── dashboard.py      # Dashboard principal
│   ├── inventory.py      # Página de inventário
│   ├── monitoring.py     # Página de monitoramento
│   └── budget.py         # Página de orçamentos
└── components/
    ├── __init__.py
    ├── sidebar.py        # Barra lateral
    ├── charts.py         # Componentes de gráficos
    └── forms.py          # Formulários
```

## 🔧 Uso

### Dashboard Principal
Acesse a página inicial para ver:
- Resumo executivo de perdas
- Gráficos interativos
- KPIs principais

### Inventário
- Registre novas entradas/saídas
- Faça upload de arquivos CSV
- Visualize histórico de movimentações

### Monitoramento
- Acompanhe tickets do JIRA
- Atualize status de atendimento
- Gere relatórios de SLA

### Orçamentos
- Gere orçamentos automáticos
- Analise custos por período
- Exporte relatórios

## 🚀 Deploy no Streamlit Cloud

1. Faça push do código para GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu repositório
4. Configure as secrets no painel:
   - Adicione as variáveis de ambiente
   - Faça upload do `credentials.json`

## 📊 Screenshots

### Dashboard Principal
![Dashboard](screenshots/dashboard.png)

### Controle de Inventário  
![Inventário](screenshots/inventory.png)

### Monitoramento de Monitores
![Monitoramento](screenshots/monitoring.png)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

Seu Nome - [@seu_twitter](https://twitter.com/seu_twitter) - seu.email@empresa.com

Link do Projeto: [https://github.com/seu-usuario/sistema-controle-perdas](https://github.com/seu-usuario/sistema-controle-perdas)

## 🙏 Agradecimentos

- [Streamlit](https://streamlit.io/) pela excelente framework
- [Plotly](https://plotly.com/) pelas visualizações
- [Google](https://developers.google.com/) pelas APIs
- [Atlassian](https://www.atlassian.com/) pela API do JIRA
