"""
Página de Monitoramento de Equipamentos
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import logging

from services.monitoring import monitoring_service
from utils.helpers import (
    show_success_message, show_error_message, show_info_message,
    show_loading_spinner, display_dataframe_with_filters, format_number
)
from config.settings import settings

logger = logging.getLogger(__name__)

def show():
    """Exibe a página de monitoramento"""
    
    st.title("🖥️ Monitoramento de Equipamentos")
    st.markdown("Acompanhe solicitações de monitores e equipamentos via JIRA")
    
    # Controles na parte superior
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        status_filter = st.selectbox(
            "📊 Filtrar por Status",
            ["Todos", "Pending", "In Progress", "Waiting for Support", "Done", "Resolved"]
        )
    
    with col2:
        building_filter = st.selectbox(
            "🏢 Filtrar por Localização",
            ["Todos", "HQ1", "HQ2", "Spark", "Outros"]
        )
    
    with col3:
        if st.button("🔄 Sincronizar JIRA", use_container_width=True):
            sync_jira_data()
    
    # Métricas principais
    show_monitoring_metrics()
    
    st.markdown("---")
    
    # Tabs principais
    tab1, tab2, tab3 = st.tabs([
        "📊 Dashboard",
        "📋 Solicitações",
        "🚨 Alertas"
    ])
    
    with tab1:
        show_monitoring_dashboard()
    
    with tab2:
        show_requests_table(status_filter, building_filter)
    
    with tab3:
        show_alerts_tab()

def show_monitoring_metrics():
    """Exibe métricas de monitoramento"""
    st.subheader("📊 Métricas de Monitoramento")
    
    with show_loading_spinner("Carregando métricas..."):
        try:
            stats = monitoring_service.get_summary_stats()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="📝 Total de Solicitações",
                    value=format_number(stats.get('totalSolicitacoes', 0)),
                    help="Total de solicitações de monitoramento"
                )
            
            with col2:
                st.metric(
                    label="🖥️ Total de Monitores",
                    value=format_number(stats.get('totalMonitores', 0)),
                    help="Total de monitores solicitados"
                )
            
            with col3:
                st.metric(
                    label="⏳ Pendentes",
                    value=format_number(stats.get('pendentes', 0)),
                    delta="-2 vs semana anterior",
                    delta_color="inverse",
                    help="Solicitações pendentes de atendimento"
                )
            
            with col4:
                st.metric(
                    label="🕒 Última Atualização",
                    value=stats.get('ultimaAtualizacao', 'N/A'),
                    help="Última sincronização com o JIRA"
                )
                
        except Exception as e:
            logger.error(f"Erro ao carregar métricas: {e}")
            show_error_message("Erro ao carregar métricas de monitoramento")

def show_monitoring_dashboard():
    """Exibe dashboard de monitoramento"""
    st.subheader("📊 Dashboard de Monitoramento")
    
    with show_loading_spinner("Carregando dados do dashboard..."):
        try:
            # Obter dados de monitoramento
            monitor_data = monitoring_service.get_monitor_data()
            
            if not monitor_data['success']:
                show_error_message("Erro ao carregar dados do JIRA")
                return
            
            data = monitor_data['data']
            
            if not data:
                show_info_message("Nenhuma solicitação encontrada")
                return
            
            # Converter para DataFrame para análise
            df = pd.DataFrame(data)
            
            # Gráficos de análise
            col1, col2 = st.columns(2)
            
            with col1:
                show_status_distribution_chart(df)
            
            with col2:
                show_priority_distribution_chart(df)
            
            # Análise temporal
            st.markdown("### 📈 Análise Temporal")
            show_temporal_analysis(df)
            
            # Top solicitantes
            st.markdown("### 👥 Top Solicitantes")
            show_top_requesters(df)
            
        except Exception as e:
            logger.error(f"Erro ao exibir dashboard: {e}")
            show_error_message("Erro ao carregar dashboard de monitoramento")

def show_status_distribution_chart(df: pd.DataFrame):
    """Exibe gráfico de distribuição por status"""
    try:
        if 'status' in df.columns:
            status_counts = df['status'].value_counts()
            
            # Criar gráfico de pizza simples com Streamlit
            st.subheader("📊 Distribuição por Status")
            
            # Usar o gráfico nativo do Streamlit
            chart_data = pd.DataFrame({
                'Status': status_counts.index,
                'Quantidade': status_counts.values
            })
            
            st.bar_chart(chart_data.set_index('Status'))
            
            # Tabela de detalhes
            with st.expander("📋 Detalhes por Status"):
                chart_data['Percentual'] = (chart_data['Quantidade'] / chart_data['Quantidade'].sum() * 100).round(1)
                chart_data['Percentual'] = chart_data['Percentual'].astype(str) + '%'
                st.dataframe(chart_data, hide_index=True, use_container_width=True)
        else:
            show_info_message("Dados de status não disponíveis")
            
    except Exception as e:
        logger.error(f"Erro ao criar gráfico de status: {e}")
        show_error_message("Erro ao criar gráfico de distribuição por status")

def show_priority_distribution_chart(df: pd.DataFrame):
    """Exibe gráfico de distribuição por prioridade"""
    try:
        if 'priority' in df.columns:
            priority_counts = df['priority'].value_counts()
            
            st.subheader("⚡ Distribuição por Prioridade")
            
            # Usar o gráfico nativo do Streamlit
            chart_data = pd.DataFrame({
                'Prioridade': priority_counts.index,
                'Quantidade': priority_counts.values
            })
            
            st.bar_chart(chart_data.set_index('Prioridade'))
            
            # Tabela de detalhes
            with st.expander("📋 Detalhes por Prioridade"):
                chart_data['Percentual'] = (chart_data['Quantidade'] / chart_data['Quantidade'].sum() * 100).round(1)
                chart_data['Percentual'] = chart_data['Percentual'].astype(str) + '%'
                st.dataframe(chart_data, hide_index=True, use_container_width=True)
        else:
            show_info_message("Dados de prioridade não disponíveis")
            
    except Exception as e:
        logger.error(f"Erro ao criar gráfico de prioridade: {e}")
        show_error_message("Erro ao criar gráfico de distribuição por prioridade")

def show_temporal_analysis(df: pd.DataFrame):
    """Exibe análise temporal"""
    try:
        if 'created' in df.columns:
            # Tentar converter datas
            df['created_date'] = pd.to_datetime(df['created'], errors='coerce')
            df_with_dates = df.dropna(subset=['created_date'])
            
            if not df_with_dates.empty:
                # Agrupar por mês
                df_with_dates['month'] = df_with_dates['created_date'].dt.to_period('M')
                monthly_counts = df_with_dates.groupby('month').size()
                
                # Criar gráfico de linha
                chart_data = pd.DataFrame({
                    'Mês': [str(m) for m in monthly_counts.index],
                    'Solicitações': monthly_counts.values
                })
                
                st.line_chart(chart_data.set_index('Mês'))
            else:
                show_info_message("Não foi possível processar as datas das solicitações")
        else:
            show_info_message("Dados de data de criação não disponíveis")
            
    except Exception as e:
        logger.error(f"Erro na análise temporal: {e}")
        show_info_message("Erro ao processar análise temporal")

def show_top_requesters(df: pd.DataFrame):
    """Exibe top solicitantes"""
    try:
        if 'reporter' in df.columns:
            reporter_counts = df['reporter'].value_counts().head(10)
            
            if not reporter_counts.empty:
                chart_data = pd.DataFrame({
                    'Solicitante': reporter_counts.index,
                    'Solicitações': reporter_counts.values
                })
                
                st.dataframe(chart_data, hide_index=True, use_container_width=True)
            else:
                show_info_message("Nenhum dado de solicitantes disponível")
        else:
            show_info_message("Dados de solicitantes não disponíveis")
            
    except Exception as e:
        logger.error(f"Erro ao mostrar top solicitantes: {e}")
        show_info_message("Erro ao processar dados de solicitantes")

def show_requests_table(status_filter: str, building_filter: str):
    """Exibe tabela de solicitações"""
    st.subheader("📋 Solicitações de Monitoramento")
    
    with show_loading_spinner("Carregando solicitações..."):
        try:
            # Obter dados de monitoramento
            monitor_data = monitoring_service.get_monitor_data()
            
            if not monitor_data['success']:
                show_error_message("Erro ao carregar dados do JIRA")
                return
            
            data = monitor_data['data']
            
            if not data:
                show_info_message("Nenhuma solicitação encontrada")
                return
            
            # Converter para DataFrame
            df = pd.DataFrame(data)
            
            # Aplicar filtros
            filtered_df = df.copy()
            
            if status_filter != "Todos":
                filtered_df = filtered_df[filtered_df['status'] == status_filter]
            
            if building_filter != "Todos":
                # Filtrar por localização (pode estar em diferentes campos)
                building_mask = (
                    filtered_df['officeLocation'].str.contains(building_filter, case=False, na=False) |
                    filtered_df['floor'].str.contains(building_filter, case=False, na=False) |
                    filtered_df['spaceArea'].str.contains(building_filter, case=False, na=False)
                )
                filtered_df = filtered_df[building_mask]
            
            if filtered_df.empty:
                show_info_message("Nenhuma solicitação encontrada com os filtros aplicados")
                return
            
            # Selecionar colunas para exibição
            display_columns = {
                'key': 'Key',
                'summary': 'Resumo',
                'status': 'Status',
                'priority': 'Prioridade',
                'reporter': 'Solicitante',
                'assignee': 'Responsável',
                'monitorPositions': 'Qtd Monitores',
                'created': 'Criado em',
                'updated': 'Atualizado em'
            }
            
            # Filtrar colunas existentes
            available_columns = [col for col in display_columns.keys() if col in filtered_df.columns]
            display_df = filtered_df[available_columns].copy()
            
            # Renomear colunas
            display_df = display_df.rename(columns={k: v for k, v in display_columns.items() if k in available_columns})
            
            # Formatação especial para algumas colunas
            if 'Qtd Monitores' in display_df.columns:
                display_df['Qtd Monitores'] = display_df['Qtd Monitores'].fillna(0).astype(int)
            
            # Adicionar coluna de ações
            if st.checkbox("🔧 Mostrar Ações", value=False):
                show_actions_column(filtered_df)
            
            # Exibir tabela
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Estatísticas da tabela filtrada
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📊 Total Filtrado", len(filtered_df))
            
            with col2:
                total_monitors = filtered_df['monitorPositions'].fillna(0).sum()
                st.metric("🖥️ Total Monitores", int(total_monitors))
            
            with col3:
                avg_monitors = filtered_df['monitorPositions'].fillna(0).mean()
                st.metric("📈 Média por Solicitação", f"{avg_monitors:.1f}")
            
        except Exception as e:
            logger.error(f"Erro ao exibir tabela de solicitações: {e}")
            show_error_message("Erro ao carregar tabela de solicitações")

def show_actions_column(df: pd.DataFrame):
    """Exibe coluna de ações para as solicitações"""
    st.subheader("🔧 Ações nas Solicitações")
    
    # Seletor de solicitação
    if 'key' in df.columns and 'summary' in df.columns:
        options = [f"{row['key']} - {row['summary'][:50]}..." for _, row in df.iterrows()]
        selected_option = st.selectbox("Selecione uma solicitação:", ["Nenhuma"] + options)
        
        if selected_option != "Nenhuma":
            selected_key = selected_option.split(" - ")[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_status = st.selectbox(
                    "Novo Status:",
                    ["Pending", "In Progress", "Waiting for Support", "Done", "Resolved"]
                )
            
            with col2:
                if st.button("✅ Atualizar Status", type="primary"):
                    update_request_status(selected_key, new_status)

def update_request_status(key: str, new_status: str):
    """Atualiza status de uma solicitação"""
    try:
        with show_loading_spinner(f"Atualizando status de {key}..."):
            success = monitoring_service.update_status(key, new_status)
            
            if success:
                show_success_message(f"Status de {key} atualizado para {new_status}")
                st.rerun()  # Recarregar página para mostrar mudanças
            else:
                show_error_message("Erro ao atualizar status")
                
    except Exception as e:
        logger.error(f"Erro ao atualizar status: {e}")
        show_error_message("Erro ao atualizar status da solicitação")

def show_alerts_tab():
    """Exibe tab de alertas"""
    st.subheader("🚨 Alertas e Notificações")
    
    with show_loading_spinner("Carregando alertas..."):
        try:
            # Obter dados para gerar alertas
            monitor_data = monitoring_service.get_monitor_data()
            
            if monitor_data['success']:
                alerts = monitoring_service.get_alerts_and_actions(monitor_data['data'])
                
                if alerts:
                    for alert in alerts:
                        alert_type = alert.get('type', 'info')
                        title = alert.get('title', 'Alerta')
                        message = alert.get('message', '')
                        
                        if alert_type == 'success':
                            st.success(f"✅ **{title}**\n\n{message}")
                        elif alert_type == 'warning':
                            st.warning(f"⚠️ **{title}**\n\n{message}")
                        elif alert_type == 'danger':
                            st.error(f"❌ **{title}**\n\n{message}")
                        else:
                            st.info(f"ℹ️ **{title}**\n\n{message}")
                else:
                    st.success("✅ **Tudo em dia!**\n\nNenhum alerta no momento.")
            else:
                show_error_message("Erro ao carregar dados para alertas")
                
        except Exception as e:
            logger.error(f"Erro ao carregar alertas: {e}")
            show_error_message("Erro ao carregar alertas")
    
    # Configurações de alertas
    st.markdown("---")
    st.subheader("⚙️ Configurações de Alertas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("📧 Alertas por Email", value=False, disabled=True)
        st.checkbox("📱 Notificações Push", value=False, disabled=True)
    
    with col2:
        st.number_input("⏰ Intervalo de Verificação (min)", min_value=5, max_value=60, value=15, disabled=True)
        st.selectbox("🔔 Nível de Alerta", ["Baixo", "Médio", "Alto"], index=1, disabled=True)
    
    st.info("ℹ️ Configurações de alertas serão implementadas em versão futura")

def sync_jira_data():
    """Sincroniza dados do JIRA"""
    try:
        with show_loading_spinner("Sincronizando dados do JIRA..."):
            # Atualizar planilha com dados do JIRA
            records_updated = monitoring_service.update_sheet_with_jira_data()
            
            if records_updated > 0:
                show_success_message(f"Sincronização concluída! {records_updated} registros atualizados.")
                st.rerun()  # Recarregar página
            else:
                show_info_message("Nenhum novo registro encontrado")
                
    except Exception as e:
        logger.error(f"Erro na sincronização: {e}")
        show_error_message("Erro ao sincronizar dados do JIRA")

# Função auxiliar para teste de conexão
def test_jira_connection():
    """Testa conexão com JIRA"""
    try:
        from services.jira_client import jira_client
        
        with show_loading_spinner("Testando conexão com JIRA..."):
            success = jira_client.test_connection()
            
            if success:
                show_success_message("Conexão com JIRA OK!")
            else:
                show_error_message("Falha na conexão com JIRA")
                
    except Exception as e:
        logger.error(f"Erro ao testar conexão JIRA: {e}")
        show_error_message("Erro ao testar conexão com JIRA")
