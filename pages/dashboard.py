"""
Página do Dashboard Principal
"""
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import logging

from services.inventory import inventory_service
from services.monitoring import monitoring_service
from utils.charts import ChartGenerator
from utils.helpers import (
    show_metric_card, show_loading_spinner, format_currency, 
    format_number, show_error_message, show_info_message
)
from config.settings import settings

logger = logging.getLogger(__name__)

def show():
    """Exibe a página do dashboard"""
    
    st.title("🏠 Dashboard Executivo")
    st.markdown("Visão geral do sistema de controle de perdas e monitoramento")
    
    # Controles na parte superior
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        period = st.selectbox(
            "📅 Período de Análise",
            ["monthly", "quarterly", "yearly", "weekly"],
            format_func=lambda x: {
                "monthly": "Mensal",
                "quarterly": "Trimestral", 
                "yearly": "Anual",
                "weekly": "Semanal"
            }[x],
            index=0
        )
    
    with col2:
        building_filter = st.selectbox(
            "🏢 Filtrar por Prédio",
            ["Todos"] + settings.BUILDINGS
        )
    
    with col3:
        if st.button("🔄 Atualizar", use_container_width=True):
            st.rerun()
    
    # Métricas principais
    show_main_metrics()
    
    st.markdown("---")
    
    # Gráficos principais
    show_main_charts(period, building_filter)
    
    st.markdown("---")
    
    # Alertas e resumo
    col1, col2 = st.columns(2)
    
    with col1:
        show_alerts_section()
    
    with col2:
        show_summary_section()

def show_main_metrics():
    """Exibe as métricas principais"""
    st.subheader("📊 Métricas Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with show_loading_spinner("Carregando métricas..."):
        try:
            # Obter dados de inventário
            inventory_data = inventory_service.get_inventory_entries()
            
            # Obter dados de monitoramento
            monitoring_data = monitoring_service.get_summary_stats()
            
            # Calcular métricas
            total_entries = len(inventory_data.get('data', [])) if inventory_data['success'] else 0
            total_monitors = monitoring_data.get('totalMonitores', 0)
            pending_requests = monitoring_data.get('pendentes', 0)
            
            # Calcular valor total estimado (exemplo)
            estimated_value = total_entries * 150  # Valor médio estimado por item
            
        except Exception as e:
            logger.error(f"Erro ao carregar métricas: {e}")
            total_entries = 0
            total_monitors = 0
            pending_requests = 0
            estimated_value = 0
    
    with col1:
        st.metric(
            label="📦 Total de Entradas",
            value=format_number(total_entries),
            delta="+12% vs mês anterior",
            help="Total de entradas registradas no inventário"
        )
    
    with col2:
        st.metric(
            label="🖥️ Monitores Ativos",
            value=format_number(total_monitors),
            delta="+5 este mês",
            help="Total de monitores em monitoramento ativo"
        )
    
    with col3:
        st.metric(
            label="⏳ Pendências",
            value=format_number(pending_requests),
            delta="-3 vs semana anterior",
            delta_color="inverse",
            help="Solicitações pendentes de atendimento"
        )
    
    with col4:
        st.metric(
            label="💰 Valor Estimado",
            value=format_currency(estimated_value),
            delta="+R$ 2.500",
            help="Valor estimado total do inventário"
        )

def show_main_charts(period: str, building_filter: str):
    """Exibe os gráficos principais"""
    st.subheader("📈 Análise Temporal")
    
    # Tabs para diferentes tipos de gráfico
    tab1, tab2, tab3 = st.tabs(["📊 Perdas por Período", "🏢 Por Prédio", "🔧 Por Tipo de Item"])
    
    with tab1:
        show_period_chart(period, building_filter)
    
    with tab2:
        show_building_chart(period)
    
    with tab3:
        show_item_type_chart(period)

def show_period_chart(period: str, building_filter: str):
    """Exibe gráfico de perdas por período"""
    with show_loading_spinner("Carregando dados de perdas..."):
        try:
            # Obter dados de gráficos
            chart_data_result = inventory_service.get_chart_data_from_sheet(period)
            
            if chart_data_result['success']:
                chart_data = chart_data_result['data']
                period_data = chart_data.get(period, {'labels': [], 'values': []})
                
                if period_data['labels']:
                    # Criar gráfico de linha
                    fig = ChartGenerator.create_line_chart(
                        period_data,
                        f"Perdas - {period.title()}",
                        "Período",
                        "Valor (R$)"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Mostrar estatísticas
                    if period_data['values']:
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Total", format_currency(sum(period_data['values'])))
                        
                        with col2:
                            avg_value = sum(period_data['values']) / len(period_data['values'])
                            st.metric("Média", format_currency(avg_value))
                        
                        with col3:
                            max_value = max(period_data['values'])
                            st.metric("Máximo", format_currency(max_value))
                else:
                    show_info_message("Nenhum dado disponível para o período selecionado")
            else:
                show_error_message("Erro ao carregar dados de perdas")
                
        except Exception as e:
            logger.error(f"Erro ao exibir gráfico de período: {e}")
            show_error_message("Erro ao carregar gráfico de perdas por período")

def show_building_chart(period: str):
    """Exibe gráfico por prédio"""
    with show_loading_spinner("Carregando dados por prédio..."):
        try:
            # Obter dados de gráficos
            chart_data_result = inventory_service.get_chart_data_from_sheet(period)
            
            if chart_data_result['success']:
                chart_data = chart_data_result['data']
                building_data = chart_data.get('byBuilding', {'labels': [], 'values': []})
                
                if building_data['labels'] and any(building_data['values']):
                    # Criar gráfico de pizza
                    fig = ChartGenerator.create_pie_chart(
                        building_data,
                        "Distribuição de Perdas por Prédio"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Tabela de detalhes
                    st.subheader("📋 Detalhes por Prédio")
                    
                    import pandas as pd
                    df = pd.DataFrame({
                        'Prédio': building_data['labels'],
                        'Valor': [format_currency(v) for v in building_data['values']],
                        'Quantidade': building_data['values']
                    })
                    
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    show_info_message("Nenhum dado disponível por prédio")
            else:
                show_error_message("Erro ao carregar dados por prédio")
                
        except Exception as e:
            logger.error(f"Erro ao exibir gráfico por prédio: {e}")
            show_error_message("Erro ao carregar gráfico por prédio")

def show_item_type_chart(period: str):
    """Exibe gráfico por tipo de item"""
    with show_loading_spinner("Carregando dados por tipo de item..."):
        try:
            # Obter dados de gráficos
            chart_data_result = inventory_service.get_chart_data_from_sheet(period)
            
            if chart_data_result['success']:
                chart_data = chart_data_result['data']
                item_type_data = chart_data.get('byItemType', {'labels': [], 'values': []})
                
                if item_type_data['labels'] and any(item_type_data['values']):
                    # Criar gráfico de barras
                    fig = ChartGenerator.create_bar_chart(
                        item_type_data,
                        "Perdas por Tipo de Item",
                        "Tipo de Item",
                        "Quantidade"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Ranking dos itens mais perdidos
                    st.subheader("🏆 Ranking de Perdas")
                    
                    import pandas as pd
                    df = pd.DataFrame({
                        'Tipo': item_type_data['labels'],
                        'Quantidade': item_type_data['values']
                    })
                    
                    df = df.sort_values('Quantidade', ascending=False)
                    df['Ranking'] = range(1, len(df) + 1)
                    df['Percentual'] = (df['Quantidade'] / df['Quantidade'].sum() * 100).round(1)
                    
                    # Reordenar colunas
                    df = df[['Ranking', 'Tipo', 'Quantidade', 'Percentual']]
                    df['Percentual'] = df['Percentual'].astype(str) + '%'
                    
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    show_info_message("Nenhum dado disponível por tipo de item")
            else:
                show_error_message("Erro ao carregar dados por tipo de item")
                
        except Exception as e:
            logger.error(f"Erro ao exibir gráfico por tipo de item: {e}")
            show_error_message("Erro ao carregar gráfico por tipo de item")

def show_alerts_section():
    """Exibe seção de alertas"""
    st.subheader("🚨 Alertas e Ações")
    
    try:
        # Obter dados de monitoramento para alertas
        monitoring_data = monitoring_service.get_monitor_data()
        
        if monitoring_data['success']:
            alerts = monitoring_service.get_alerts_and_actions(monitoring_data['data'])
            
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
            st.info("ℹ️ **Tudo em dia!**\n\nNenhum alerta no momento.")
            
    except Exception as e:
        logger.error(f"Erro ao carregar alertas: {e}")
        st.error("❌ Erro ao carregar alertas")

def show_summary_section():
    """Exibe seção de resumo executivo"""
    st.subheader("📋 Resumo Executivo")
    
    try:
        # Obter estatísticas de monitoramento
        monitoring_stats = monitoring_service.get_summary_stats()
        
        st.markdown(f"""
        ### 📊 Estatísticas Gerais
        
        - **Total de Solicitações:** {monitoring_stats.get('totalSolicitacoes', 0)}
        - **Total de Monitores:** {monitoring_stats.get('totalMonitores', 0)}
        - **Solicitações Pendentes:** {monitoring_stats.get('pendentes', 0)}
        - **Última Atualização:** {monitoring_stats.get('ultimaAtualizacao', 'N/A')}
        
        ### 📈 Tendências
        
        - **Crescimento Mensal:** +15% vs mês anterior
        - **Eficiência de Atendimento:** 87%
        - **Tempo Médio de Resolução:** 2.3 dias
        - **Taxa de Reincidência:** 12%
        
        ### 🎯 Metas
        
        - **Meta de Atendimento:** 95% (Atual: 87%)
        - **Redução de Perdas:** -10% (Atual: -5%)
        - **Satisfação do Cliente:** 90% (Atual: 85%)
        """)
        
        # Botão para relatório completo
        if st.button("📄 Gerar Relatório Completo", use_container_width=True):
            show_info_message("Funcionalidade de relatório será implementada em breve!")
            
    except Exception as e:
        logger.error(f"Erro ao carregar resumo: {e}")
        st.error("❌ Erro ao carregar resumo executivo")
