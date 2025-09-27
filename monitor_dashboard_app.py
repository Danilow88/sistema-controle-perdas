"""
Sistema de Monitoramento de Monitores - Streamlit
Baseado no HTML monitor_dashboard_fixed.html
Integração com Google Sheets para dados de eventos
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import gspread
from google.oauth2.service_account import Credentials
import json

# Configuração da página
st.set_page_config(
    page_title="Monitoramento de Monitores",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS fiel ao HTML original
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #f5f5f7;
    color: #333;
}

/* Nubank theme colors */
.nubank-bg {
    background: linear-gradient(135deg, #8a05be 0%, #4500a0 100%);
}

.main-header {
    background: linear-gradient(135deg, #8a05be 0%, #4500a0 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header-left {
    display: flex;
    align-items: center;
}

.header-icon {
    background: white;
    padding: 8px;
    border-radius: 50%;
    margin-right: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.header-title {
    font-size: 24px;
    font-weight: 700;
    margin: 0;
}

.header-subtitle {
    color: rgba(255,255,255,0.9);
    margin-top: 4px;
    font-size: 14px;
}

.nubank-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.nubank-card:hover {
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    transform: translateY(-2px);
}

.metric-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    padding: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.metric-content h3 {
    font-size: 24px;
    font-weight: 700;
    margin: 4px 0 0 0;
    color: #333;
}

.metric-content p {
    color: #666;
    font-size: 14px;
    margin: 0;
}

.metric-icon {
    padding: 12px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.icon-purple { background-color: rgba(138, 5, 190, 0.1); color: #8a05be; }
.icon-green { background-color: rgba(43, 138, 62, 0.1); color: #2b8a3e; }
.icon-yellow { background-color: rgba(230, 119, 0, 0.1); color: #e67700; }
.icon-blue { background-color: rgba(25, 113, 194, 0.1); color: #1971c2; }

.stButton > button {
    background: linear-gradient(135deg, #8a05be 0%, #4500a0 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 24px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(138, 5, 190, 0.3) !important;
}

.stSelectbox > div > div {
    background: #f8f9fa !important;
    border: 2px solid #e9ecef !important;
    border-radius: 24px !important;
    padding: 10px 16px !important;
}

.stSelectbox > div > div:focus-within {
    border-color: #8a05be !important;
    background: white !important;
    box-shadow: 0 0 0 3px rgba(138, 5, 190, 0.2) !important;
}

.stTextInput > div > div > input {
    background: #f8f9fa !important;
    border: 2px solid #e9ecef !important;
    border-radius: 24px !important;
    padding: 10px 16px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #8a05be !important;
    background: white !important;
    box-shadow: 0 0 0 3px rgba(138, 5, 190, 0.2) !important;
}

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 16px;
    font-size: 12px;
    font-weight: 600;
}

.badge-warning {
    background-color: #fff4e6;
    color: #e67700;
}

.badge-success {
    background-color: #d3f9d8;
    color: #2b8a3e;
}

.badge-danger {
    background-color: #ffe3e3;
    color: #c92a2a;
}

.badge-info {
    background-color: #e7f5ff;
    color: #1971c2;
}

.alert {
    border-left: 4px solid;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
}

.alert-danger {
    background-color: #fff5f5;
    border-left-color: #c92a2a;
    color: #c92a2a;
}

.alert-warning {
    background-color: #fff9db;
    border-left-color: #e67700;
    color: #e67700;
}

.alert-info {
    background-color: #e7f5ff;
    border-left-color: #1971c2;
    color: #1971c2;
}

.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
}

.status-pending { background-color: #fff4e6; color: #e67700; }
.status-confirmed { background-color: #d3f9d8; color: #2b8a3e; }
.status-exceeded { background-color: #ffe3e3; color: #c92a2a; }
.status-completed { background-color: #d3f9d8; color: #2b8a3e; }
</style>
""", unsafe_allow_html=True)

# Configurações do Google Sheets
SPREADSHEET_ID = '1hI6WWiH03AvXFxMCpPpYtIhQEU062C_k4utIE6YyctY'
SHEET_NAME = 'Calendário de eventos - Monitores'
SHEET_GID = '1469973439'

class MonitorManager:
    """Gerenciador de dados de monitores com Google Sheets"""
    
    def __init__(self):
        self.gc = None
        
    def init_google_sheets(self):
        """Inicializa conexão com Google Sheets"""
        try:
            if hasattr(st, 'secrets') and 'google_sheets' in st.secrets:
                credentials_dict = dict(st.secrets['google_sheets'])
                credentials = Credentials.from_service_account_info(
                    credentials_dict,
                    scopes=[
                        'https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive'
                    ]
                )
            else:
                # Desenvolvimento local
                if os.path.exists('credentials.json'):
                    credentials = Credentials.from_service_account_file(
                        'credentials.json',
                        scopes=[
                            'https://www.googleapis.com/auth/spreadsheets',
                            'https://www.googleapis.com/auth/drive'
                        ]
                    )
                else:
                    return False
            
            self.gc = gspread.authorize(credentials)
            return True
            
        except Exception as e:
            st.error(f"❌ Erro ao conectar Google Sheets: {e}")
            return False
    
    def load_monitor_data(self):
        """Carrega dados de monitores do Google Sheets"""
        try:
            if not self.gc and not self.init_google_sheets():
                return self.get_sample_data()
            
            # Tentar múltiplos métodos de carregamento
            try:
                # Método 1: gviz com nome da aba
                gviz_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:json&sheet={SHEET_NAME}&headers=1&tq=SELECT%20*"
                
                import requests
                response = requests.get(gviz_url, headers={'Accept': 'application/json'})
                
                if response.status_code == 200:
                    text = response.text
                    # Extrair JSON do response gviz
                    import re
                    match = re.search(r'google\.visualization\.Query\.setResponse\((.*)\);', text, re.DOTALL)
                    
                    if match:
                        json_data = json.loads(match.group(1))
                        
                        if json_data.get('status') == 'ok':
                            cols = json_data.get('table', {}).get('cols', [])
                            rows = json_data.get('table', {}).get('rows', [])
                            
                            # Processar dados
                            data = []
                            for row in rows:
                                cells = row.get('c', [])
                                row_data = []
                                for cell in cells:
                                    if cell is None:
                                        row_data.append('')
                                    elif isinstance(cell, dict) and 'v' in cell:
                                        row_data.append(cell['v'])
                                    else:
                                        row_data.append(str(cell))
                                data.append(row_data)
                            
                            return self.process_monitor_data(data)
            
            except Exception as e:
                st.warning(f"Método gviz falhou: {e}")
            
            # Fallback: usar gspread diretamente
            try:
                spreadsheet = self.gc.open_by_key(SPREADSHEET_ID)
                worksheet = spreadsheet.worksheet(SHEET_NAME)
                data = worksheet.get_all_values()
                
                if data and len(data) > 1:
                    return self.process_monitor_data(data[1:])  # Pular header
                    
            except Exception as e:
                st.warning(f"Método gspread falhou: {e}")
            
            # Se tudo falhar, usar dados de exemplo
            return self.get_sample_data()
            
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            return self.get_sample_data()
    
    def process_monitor_data(self, raw_data):
        """Processa dados brutos em formato estruturado"""
        processed_data = []
        
        for row in raw_data:
            if len(row) >= 10:  # Garantir que temos dados suficientes
                try:
                    item = {
                        'data_solicitacao': row[0] if len(row) > 0 else '',
                        'data_montagem': row[1] if len(row) > 1 else '',
                        'sala': row[2] if len(row) > 2 else '',
                        'monitores': int(row[3]) if len(row) > 3 and row[3].isdigit() else 0,
                        'data_desmontagem': row[4] if len(row) > 4 else '',
                        'observacoes': row[5] if len(row) > 5 else '',
                        'reporter': row[6] if len(row) > 6 else '',
                        'key': row[7] if len(row) > 7 else '',
                        'status': row[8] if len(row) > 8 else 'Pendente',
                        'status_atendimento': row[9] if len(row) > 9 else 'Não Iniciado'
                    }
                    processed_data.append(item)
                except (ValueError, IndexError):
                    continue
        
        # Remover duplicatas por key
        unique_data = {}
        for item in processed_data:
            key = item['key']
            if key and key not in unique_data:
                unique_data[key] = item
        
        return list(unique_data.values())
    
    def get_sample_data(self):
        """Dados de exemplo para demonstração"""
        return [
            {
                'data_solicitacao': '15/03/2025',
                'data_montagem': '20/03/2025',
                'sala': 'Sala A-201',
                'monitores': 3,
                'data_desmontagem': '25/03/2025',
                'observacoes': 'Evento corporativo',
                'reporter': 'João Silva',
                'key': 'MON-001',
                'status': 'Confirmado',
                'status_atendimento': 'Em Andamento'
            },
            {
                'data_solicitacao': '18/03/2025',
                'data_montagem': '22/03/2025',
                'sala': 'Sala B-305',
                'monitores': 5,
                'data_desmontagem': '28/03/2025',
                'observacoes': 'Treinamento técnico',
                'reporter': 'Maria Santos',
                'key': 'MON-002',
                'status': 'Excedente',
                'status_atendimento': 'Pendente'
            },
            {
                'data_solicitacao': '20/03/2025',
                'data_montagem': '25/03/2025',
                'sala': 'Auditório Principal',
                'monitores': 8,
                'data_desmontagem': '30/03/2025',
                'observacoes': 'Apresentação executiva',
                'reporter': 'Carlos Lima',
                'key': 'MON-003',
                'status': 'Pendente',
                'status_atendimento': 'Não Iniciado'
            },
            {
                'data_solicitacao': '22/03/2025',
                'data_montagem': '27/03/2025',
                'sala': 'Sala C-102',
                'monitores': 2,
                'data_desmontagem': '29/03/2025',
                'observacoes': 'Workshop interno',
                'reporter': 'Ana Costa',
                'key': 'MON-004',
                'status': 'Concluído',
                'status_atendimento': 'Concluído'
            }
        ]
    
    def update_status(self, key, new_status):
        """Atualiza status de atendimento no Google Sheets"""
        try:
            if not self.gc and not self.init_google_sheets():
                st.warning("Conexão com Google Sheets não disponível")
                return False
            
            spreadsheet = self.gc.open_by_key(SPREADSHEET_ID)
            worksheet = spreadsheet.worksheet(SHEET_NAME)
            
            # Encontrar linha pela key
            all_values = worksheet.get_all_values()
            
            for i, row in enumerate(all_values):
                if len(row) > 7 and row[7] == key:  # Coluna 8 é a key (índice 7)
                    # Atualizar coluna de status de atendimento (coluna 10, índice 9)
                    worksheet.update_cell(i + 1, 10, new_status)
                    return True
            
            return False
            
        except Exception as e:
            st.error(f"Erro ao atualizar status: {e}")
            return False

def main():
    """Função principal"""
    
    # Header fiel ao HTML original
    st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="header-left">
                <div class="header-icon">
                    <span style="color: #8a05be; font-size: 24px;">🖥️</span>
                </div>
                <div>
                    <h1 class="header-title">Monitoramento de Monitores</h1>
                    <p class="header-subtitle">Visualização dos dados da planilha de eventos</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar gerenciador
    if 'monitor_manager' not in st.session_state:
        st.session_state.monitor_manager = MonitorManager()
    
    # Botões de ação no topo
    col1, col2, col3 = st.columns([1, 1, 8])
    
    with col1:
        if st.button("🔄 Atualizar", key="refresh_btn"):
            st.session_state.monitor_data = None  # Force reload
            st.rerun()
    
    with col2:
        if st.button("📥 Exportar", key="export_btn"):
            export_data()
    
    # Carregar dados
    if 'monitor_data' not in st.session_state or st.session_state.monitor_data is None:
        with st.spinner("Carregando dados da planilha..."):
            st.session_state.monitor_data = st.session_state.monitor_manager.load_monitor_data()
    
    data = st.session_state.monitor_data
    
    # Cards de resumo (fiel ao HTML original)
    show_summary_cards(data)
    
    # Tabela de eventos
    show_events_table(data)
    
    # Alertas
    show_alerts(data)

def show_summary_cards(data):
    """Exibe cards de resumo fiel ao HTML original"""
    
    # Calcular métricas
    total_monitores = sum(item['monitores'] for item in data)
    dentro_limite = sum(item['monitores'] for item in data if item['status'] in ['Confirmado', 'Concluído'])
    excedente = sum(item['monitores'] for item in data if item['status'] == 'Excedente')
    ultima_atualizacao = datetime.now().strftime('%H:%M:%S')
    
    # Grid de cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <p>Total de Monitores</p>
                <h3>{total_monitores}</h3>
            </div>
            <div class="metric-icon icon-purple">
                🖥️
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <p>Dentro do Limite</p>
                <h3>{dentro_limite}</h3>
            </div>
            <div class="metric-icon icon-green">
                ✅
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <p>Excedente</p>
                <h3>{excedente}</h3>
            </div>
            <div class="metric-icon icon-yellow">
                ⚠️
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <p>Última Atualização</p>
                <h3>{ultima_atualizacao}</h3>
            </div>
            <div class="metric-icon icon-blue">
                🕐
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_events_table(data):
    """Exibe tabela de eventos com filtros"""
    
    st.markdown('<div class="nubank-card">', unsafe_allow_html=True)
    st.subheader("📋 Eventos de Monitor")
    
    # Filtros
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Buscar...", placeholder="Digite para buscar")
    
    with col2:
        status_options = ['Todos'] + list(set(item['status'] for item in data))
        status_filter = st.selectbox("Status", status_options)
    
    with col3:
        atendimento_options = ['Todos'] + list(set(item['status_atendimento'] for item in data))
        atendimento_filter = st.selectbox("Status Atendimento", atendimento_options)
    
    # Aplicar filtros
    filtered_data = data.copy()
    
    if search_term:
        filtered_data = [
            item for item in filtered_data
            if search_term.lower() in str(item).lower()
        ]
    
    if status_filter != 'Todos':
        filtered_data = [
            item for item in filtered_data
            if item['status'] == status_filter
        ]
    
    if atendimento_filter != 'Todos':
        filtered_data = [
            item for item in filtered_data
            if item['status_atendimento'] == atendimento_filter
        ]
    
    # Tabela interativa
    if filtered_data:
        # Converter para DataFrame
        df = pd.DataFrame(filtered_data)
        
        # Renomear colunas para exibição
        df_display = df.copy()
        df_display = df_display.rename(columns={
            'data_solicitacao': 'Data Solicitação',
            'data_montagem': 'Data Montagem',
            'sala': 'Sala',
            'monitores': 'Monitores',
            'reporter': 'Reporter',
            'key': 'Key',
            'status': 'Status',
            'status_atendimento': 'Status Atendimento'
        })
        
        # Selecionar colunas para exibição
        columns_to_show = [
            'Data Solicitação', 'Data Montagem', 'Monitores', 
            'Sala', 'Reporter', 'Key', 'Status', 'Status Atendimento'
        ]
        
        df_display = df_display[columns_to_show]
        
        # Exibir tabela
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Status": st.column_config.TextColumn(
                    "Status",
                    help="Status do evento"
                ),
                "Status Atendimento": st.column_config.SelectboxColumn(
                    "Status Atendimento",
                    help="Status de atendimento",
                    options=['Não Iniciado', 'Em Andamento', 'Concluído', 'Pendente'],
                    required=True
                )
            }
        )
        
        # Informações de paginação
        st.info(f"📊 Mostrando {len(filtered_data)} de {len(data)} registros")
        
        # Seção de ações rápidas
        st.markdown("### ⚡ Ações Rápidas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Atualizar status em lote
            if st.button("✅ Marcar Selecionados como Concluído"):
                # Em uma implementação real, você permitiria seleção múltipla
                st.success("Funcionalidade de atualização em lote")
        
        with col2:
            # Gerar relatório
            if st.button("📊 Gerar Relatório"):
                generate_report(filtered_data)
    
    else:
        st.info("Nenhum evento encontrado com os filtros aplicados")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_alerts(data):
    """Exibe alertas baseados nos dados"""
    
    st.markdown('<div class="nubank-card">', unsafe_allow_html=True)
    st.subheader("🚨 Alertas e Ações")
    
    # Calcular alertas
    eventos_pendentes = len([item for item in data if item['status'] == 'Pendente'])
    eventos_excedentes = len([item for item in data if item['status'] == 'Excedente'])
    eventos_sem_reporter = len([item for item in data if not item['reporter'] or item['reporter'].strip() == ''])
    
    alerts_shown = False
    
    if eventos_pendentes > 0:
        st.markdown(f"""
        <div class="alert alert-warning">
            <strong>⚠️ Eventos Pendentes</strong><br>
            Existem {eventos_pendentes} eventos com status "Pendente".
        </div>
        """, unsafe_allow_html=True)
        alerts_shown = True
    
    if eventos_excedentes > 0:
        st.markdown(f"""
        <div class="alert alert-danger">
            <strong>🚫 Eventos Excedentes</strong><br>
            Existem {eventos_excedentes} eventos com status "Excedente".
        </div>
        """, unsafe_allow_html=True)
        alerts_shown = True
    
    if eventos_sem_reporter > 0:
        st.markdown(f"""
        <div class="alert alert-info">
            <strong>ℹ️ Eventos sem Reporter</strong><br>
            Existem {eventos_sem_reporter} eventos sem reporter definido.
        </div>
        """, unsafe_allow_html=True)
        alerts_shown = True
    
    if not alerts_shown:
        st.success("✅ Nenhum alerta no momento. Todos os eventos estão em dia!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def generate_report(data):
    """Gera relatório dos dados"""
    
    # Análise por status
    status_counts = {}
    for item in data:
        status = item['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Gráfico de status
    if status_counts:
        fig_status = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Distribuição por Status",
            color_discrete_sequence=['#8a05be', '#4500a0', '#e67700', '#2b8a3e']
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Análise por monitores
    monitores_por_sala = {}
    for item in data:
        sala = item['sala']
        monitores = item['monitores']
        if sala not in monitores_por_sala:
            monitores_por_sala[sala] = 0
        monitores_por_sala[sala] += monitores
    
    if monitores_por_sala:
        fig_monitores = px.bar(
            x=list(monitores_por_sala.keys()),
            y=list(monitores_por_sala.values()),
            title="Monitores por Sala",
            color_discrete_sequence=['#8a05be']
        )
        fig_monitores.update_layout(
            xaxis_title="Sala",
            yaxis_title="Quantidade de Monitores"
        )
        st.plotly_chart(fig_monitores, use_container_width=True)

def export_data():
    """Exporta dados para CSV"""
    data = st.session_state.get('monitor_data', [])
    
    if not data:
        st.warning("Nenhum dado disponível para exportar")
        return
    
    # Converter para DataFrame
    df = pd.DataFrame(data)
    
    # Renomear colunas
    df = df.rename(columns={
        'data_solicitacao': 'Data Solicitação',
        'data_montagem': 'Data Montagem',
        'sala': 'Sala',
        'monitores': 'Monitores',
        'data_desmontagem': 'Data Desmontagem',
        'observacoes': 'Observações',
        'reporter': 'Reporter',
        'key': 'Key',
        'status': 'Status',
        'status_atendimento': 'Status Atendimento'
    })
    
    # Gerar CSV
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    
    # Download
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"monitores_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    st.success("✅ Dados exportados com sucesso!")

if __name__ == "__main__":
    main()
