"""
Página de Monitoramento de Equipamentos
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import logging

def show():
    """Exibe a página de monitoramento"""
    
    st.title("🖥️ Monitoramento de Equipamentos")
    st.markdown("Acompanhe solicitações de monitores e equipamentos")
    
    # Controles na parte superior
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        status_filter = st.selectbox(
            "📊 Filtrar por Status",
            ["Todos", "Pending", "In Progress", "Done"]
        )
    
    with col2:
        building_filter = st.selectbox(
            "🏢 Filtrar por Localização",
            ["Todos", "HQ1", "HQ2", "Spark"]
        )
    
    with col3:
        if st.button("🔄 Atualizar", use_container_width=True):
            st.rerun()
    
    # Métricas principais
    st.subheader("📊 Métricas de Monitoramento")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Solicitações", "25", "+3")
    
    with col2:
        st.metric("🖥️ Monitores", "45", "+5")
    
    with col3:
        st.metric("⏳ Pendentes", "8", "-2")
    
    with col4:
        st.metric("🕒 Última Sync", "10:30")
    
    st.markdown("---")
    
    # Tabs principais
    tab1, tab2, tab3 = st.tabs([
        "📊 Dashboard",
        "📋 Solicitações",
        "🚨 Alertas"
    ])
    
    with tab1:
        st.subheader("📊 Dashboard de Monitoramento")
        
        # Dados de exemplo para gráfico
        chart_data = pd.DataFrame({
            'Status': ['Pending', 'In Progress', 'Done', 'Cancelled'],
            'Quantidade': [8, 12, 15, 2]
        })
        
        st.bar_chart(chart_data.set_index('Status'))
        
        # Análise temporal
        st.subheader("📈 Análise Temporal")
        
        temporal_data = pd.DataFrame({
            'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
            'Solicitações': [20, 25, 18, 30, 25]
        })
        
        st.line_chart(temporal_data.set_index('Mês'))
    
    with tab2:
        st.subheader("📋 Solicitações de Monitoramento")
        
        # Dados de exemplo
        sample_requests = {
            'Key': ['TS-1001', 'TS-1002', 'TS-1003', 'TS-1004'],
            'Resumo': ['Monitor Sala 501', 'Setup HQ2', 'Manutenção Spark', 'Nova instalação'],
            'Status': ['Pending', 'In Progress', 'Done', 'Pending'],
            'Prioridade': ['Medium', 'High', 'Low', 'Medium'],
            'Solicitante': ['João Silva', 'Maria Santos', 'Pedro Lima', 'Ana Costa'],
            'Criado em': ['01/01/2025', '02/01/2025', '03/01/2025', '04/01/2025']
        }
        
        df = pd.DataFrame(sample_requests)
        
        # Aplicar filtros
        if status_filter != "Todos":
            df = df[df['Status'] == status_filter]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Estatísticas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Total Filtrado", len(df))
        
        with col2:
            pending_count = len(df[df['Status'] == 'Pending'])
            st.metric("⏳ Pendentes", pending_count)
        
        with col3:
            done_count = len(df[df['Status'] == 'Done'])
            st.metric("✅ Concluídas", done_count)
    
    with tab3:
        st.subheader("🚨 Alertas e Notificações")
        
        # Alertas de exemplo
        st.warning("⚠️ **Eventos Pendentes**\n\nExistem 8 eventos com status 'Pendente'.")
        st.info("ℹ️ **Eventos sem Reporter**\n\nExistem 2 eventos sem reporter definido.")
        st.success("✅ **Tudo em dia!**\n\nNenhum alerta crítico no momento.")
        
        # Configurações de alertas
        st.markdown("---")
        st.subheader("⚙️ Configurações de Alertas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("📧 Alertas por Email", value=False, disabled=True)
            st.checkbox("📱 Notificações Push", value=False, disabled=True)
        
        with col2:
            st.number_input("⏰ Intervalo (min)", min_value=5, max_value=60, value=15, disabled=True)
            st.selectbox("🔔 Nível", ["Baixo", "Médio", "Alto"], index=1, disabled=True)
        
        st.info("ℹ️ Configurações de alertas serão implementadas em versão futura")
