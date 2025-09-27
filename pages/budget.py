"""
Página de Orçamentos
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import logging

from services.inventory import inventory_service
from services.google_sheets import google_sheets_service
from utils.helpers import (
    show_success_message, show_error_message, show_info_message,
    show_loading_spinner, format_currency, format_number
)
from utils.charts import ChartGenerator
from config.settings import settings

logger = logging.getLogger(__name__)

def show():
    """Exibe a página de orçamentos"""
    
    st.title("💰 Gestão de Orçamentos")
    st.markdown("Gerencie orçamentos baseados em perdas e análise de custos")
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Gerar Orçamento",
        "📈 Análise de Custos",
        "💾 Orçamentos Salvos",
        "📋 Relatórios"
    ])
    
    with tab1:
        show_budget_generator()
    
    with tab2:
        show_cost_analysis()
    
    with tab3:
        show_saved_budgets()
    
    with tab4:
        show_budget_reports()

def show_budget_generator():
    """Exibe gerador de orçamentos"""
    st.subheader("📊 Gerador de Orçamentos Automático")
    
    st.markdown("""
    ### 💡 Como Funciona
    
    O sistema analisa as perdas históricas e gera sugestões de compra baseadas em:
    - **Histórico de perdas** por tipo de item
    - **Frequência de reposição** necessária
    - **Preços estimados** por categoria
    - **Análise por prédio** e localização
    """)
    
    # Configurações do orçamento
    with st.expander("⚙️ Configurações do Orçamento", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            budget_limit = st.number_input(
                "💰 Limite do Orçamento (R$)",
                min_value=1000.0,
                max_value=100000.0,
                value=25000.0,
                step=1000.0,
                help="Valor máximo para o orçamento"
            )
        
        with col2:
            period_analysis = st.selectbox(
                "📅 Período de Análise",
                ["monthly", "quarterly", "yearly"],
                format_func=lambda x: {
                    "monthly": "Mensal",
                    "quarterly": "Trimestral",
                    "yearly": "Anual"
                }[x],
                help="Período para análise de perdas"
            )
        
        with col3:
            building_focus = st.selectbox(
                "🏢 Foco por Prédio",
                ["Todos"] + settings.BUILDINGS,
                help="Concentrar orçamento em prédio específico"
            )
    
    # Botão para gerar orçamento
    if st.button("🚀 Gerar Orçamento Automático", type="primary", use_container_width=True):
        generate_automatic_budget(budget_limit, period_analysis, building_focus)

def generate_automatic_budget(budget_limit: float, period: str, building_focus: str):
    """Gera orçamento automático baseado em perdas"""
    
    with show_loading_spinner("Analisando perdas históricas..."):
        try:
            # Obter dados de perdas
            chart_data_result = inventory_service.get_chart_data_from_sheet(period)
            
            if not chart_data_result['success']:
                show_error_message("Erro ao obter dados de perdas para análise")
                return
            
            chart_data = chart_data_result['data']
            
            # Dados por tipo de item
            item_type_data = chart_data.get('byItemType', {'labels': [], 'values': []})
            building_data = chart_data.get('byBuilding', {'labels': [], 'values': []})
            
            if not item_type_data['labels']:
                show_info_message("Nenhum dado de perdas encontrado para gerar orçamento")
                return
            
            # Calcular sugestões de compra
            budget_items = calculate_budget_suggestions(
                item_type_data, 
                building_data, 
                budget_limit, 
                building_focus
            )
            
            # Exibir orçamento gerado
            display_generated_budget(budget_items, budget_limit, period, building_focus)
            
        except Exception as e:
            logger.error(f"Erro ao gerar orçamento: {e}")
            show_error_message("Erro ao gerar orçamento automático")

def calculate_budget_suggestions(item_type_data: dict, building_data: dict, 
                               budget_limit: float, building_focus: str) -> list:
    """Calcula sugestões de compra baseadas em perdas"""
    
    budget_items = []
    remaining_budget = budget_limit
    
    # Preços por tipo de item
    item_prices = settings.ITEM_PRICES
    
    # Processar cada tipo de item
    for i, item_type in enumerate(item_type_data['labels']):
        if i < len(item_type_data['values']):
            loss_quantity = item_type_data['values'][i]
            
            if loss_quantity > 0 and item_type in item_prices:
                unit_price = item_prices[item_type]
                
                # Calcular quantidade sugerida (baseada na perda + margem de segurança)
                safety_margin = 1.2  # 20% de margem de segurança
                suggested_quantity = int(loss_quantity * safety_margin)
                
                # Limitar quantidade máxima por item
                max_quantity_per_item = 50
                suggested_quantity = min(suggested_quantity, max_quantity_per_item)
                
                total_cost = suggested_quantity * unit_price
                
                # Verificar se cabe no orçamento
                if total_cost <= remaining_budget:
                    budget_items.append({
                        'item_type': item_type,
                        'suggested_quantity': suggested_quantity,
                        'unit_price': unit_price,
                        'total_cost': total_cost,
                        'loss_basis': loss_quantity,
                        'priority': 'Alta' if loss_quantity > 10 else 'Média' if loss_quantity > 5 else 'Baixa'
                    })
                    
                    remaining_budget -= total_cost
    
    # Ordenar por prioridade e custo
    budget_items.sort(key=lambda x: (x['priority'] == 'Alta', x['total_cost']), reverse=True)
    
    return budget_items

def display_generated_budget(budget_items: list, budget_limit: float, period: str, building_focus: str):
    """Exibe orçamento gerado"""
    
    st.success("✅ Orçamento gerado com sucesso!")
    
    # Resumo do orçamento
    total_cost = sum(item['total_cost'] for item in budget_items)
    total_items = sum(item['suggested_quantity'] for item in budget_items)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Custo Total", format_currency(total_cost))
    
    with col2:
        st.metric("🛒 Total de Itens", format_number(total_items))
    
    with col3:
        st.metric("📊 Tipos Diferentes", len(budget_items))
    
    with col4:
        remaining = budget_limit - total_cost
        st.metric("💵 Orçamento Restante", format_currency(remaining))
    
    # Tabela detalhada
    st.subheader("📋 Itens Sugeridos")
    
    if budget_items:
        df = pd.DataFrame(budget_items)
        
        # Formatar DataFrame para exibição
        display_df = pd.DataFrame({
            'Tipo de Item': df['item_type'],
            'Quantidade Sugerida': df['suggested_quantity'],
            'Preço Unitário': df['unit_price'].apply(format_currency),
            'Custo Total': df['total_cost'].apply(format_currency),
            'Base (Perdas)': df['loss_basis'].astype(int),
            'Prioridade': df['priority']
        })
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Gráfico de distribuição de custos
        st.subheader("📊 Distribuição de Custos")
        
        # Preparar dados para gráfico
        chart_data = {
            'labels': df['item_type'].tolist(),
            'values': df['total_cost'].tolist()
        }
        
        fig = ChartGenerator.create_pie_chart(chart_data, "Distribuição de Custos por Tipo")
        st.plotly_chart(fig, use_container_width=True)
        
        # Opções de ação
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Salvar Orçamento", use_container_width=True):
                save_budget(budget_items, total_cost, period, building_focus)
        
        with col2:
            # Download do orçamento como CSV
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV",
                data=csv_data,
                file_name=f"orcamento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            if st.button("🔄 Gerar Novo", use_container_width=True):
                st.rerun()
    
    else:
        show_info_message("Nenhum item sugerido com o orçamento atual")

def save_budget(budget_items: list, total_cost: float, period: str, building_focus: str):
    """Salva orçamento na planilha"""
    
    try:
        with show_loading_spinner("Salvando orçamento..."):
            # Calcular totais por tipo
            item_totals = {}
            for item in budget_items:
                item_type = item['item_type']
                quantity = item['suggested_quantity']
                item_totals[item_type] = item_totals.get(item_type, 0) + quantity
            
            # Preparar dados para salvar
            budget_data = {
                'building': building_focus,
                'periodo': period,
                'totalHeadsets': item_totals.get('Headsets', 0),
                'totalMouses': item_totals.get('Mouses', 0),
                'totalTeclados': item_totals.get('Teclados', 0),
                'totalAdaptadores': item_totals.get('Adaptadores', 0),
                'totalUsbGorila': item_totals.get('USB Gorila', 0),
                'valorTotal': total_cost
            }
            
            # Salvar na planilha (simulado)
            # Em uma implementação real, salvaria via Google Sheets
            success = save_budget_to_sheet(budget_data)
            
            if success:
                show_success_message("Orçamento salvo com sucesso!")
                st.balloons()
            else:
                show_error_message("Erro ao salvar orçamento")
                
    except Exception as e:
        logger.error(f"Erro ao salvar orçamento: {e}")
        show_error_message("Erro ao salvar orçamento")

def save_budget_to_sheet(budget_data: dict) -> bool:
    """Salva orçamento na planilha (simulado)"""
    try:
        # Em uma implementação real, usaria google_sheets_service
        # para salvar na aba "Orcamento"
        
        # Por enquanto, apenas simula o salvamento
        logger.info(f"Orçamento salvo: {budget_data}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao salvar na planilha: {e}")
        return False

def show_cost_analysis():
    """Exibe análise de custos"""
    st.subheader("📈 Análise de Custos")
    
    # Seleção do período para análise
    period = st.selectbox(
        "📅 Período para Análise",
        ["monthly", "quarterly", "yearly"],
        format_func=lambda x: {
            "monthly": "Mensal",
            "quarterly": "Trimestral",
            "yearly": "Anual"
        }[x]
    )
    
    with show_loading_spinner("Carregando análise de custos..."):
        try:
            # Obter dados de perdas
            chart_data_result = inventory_service.get_chart_data_from_sheet(period)
            
            if chart_data_result['success']:
                chart_data = chart_data_result['data']
                
                # Análise por período
                period_data = chart_data.get(period, {'labels': [], 'values': []})
                if period_data['labels']:
                    st.subheader(f"💰 Custos por Período - {period.title()}")
                    
                    # Converter para valores monetários
                    cost_data = {
                        'labels': period_data['labels'],
                        'values': [v * 150 for v in period_data['values']]  # Custo médio estimado
                    }
                    
                    fig = ChartGenerator.create_line_chart(
                        cost_data,
                        f"Evolução de Custos - {period.title()}",
                        "Período",
                        "Custo (R$)"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Análise por tipo de item
                item_type_data = chart_data.get('byItemType', {'labels': [], 'values': []})
                if item_type_data['labels']:
                    st.subheader("🔧 Custos por Tipo de Item")
                    
                    # Calcular custos reais por tipo
                    item_costs = []
                    for i, item_type in enumerate(item_type_data['labels']):
                        if i < len(item_type_data['values']):
                            quantity = item_type_data['values'][i]
                            unit_price = settings.ITEM_PRICES.get(item_type, 100)
                            total_cost = quantity * unit_price
                            item_costs.append(total_cost)
                    
                    cost_by_type = {
                        'labels': item_type_data['labels'],
                        'values': item_costs
                    }
                    
                    fig = ChartGenerator.create_bar_chart(
                        cost_by_type,
                        "Custos por Tipo de Item",
                        "Tipo de Item",
                        "Custo Total (R$)"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Análise por prédio
                building_data = chart_data.get('byBuilding', {'labels': [], 'values': []})
                if building_data['labels']:
                    st.subheader("🏢 Custos por Prédio")
                    
                    # Converter para custos
                    building_costs = [v * 150 for v in building_data['values']]
                    
                    cost_by_building = {
                        'labels': building_data['labels'],
                        'values': building_costs
                    }
                    
                    fig = ChartGenerator.create_pie_chart(
                        cost_by_building,
                        "Distribuição de Custos por Prédio"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Resumo de custos
                show_cost_summary(chart_data)
                
            else:
                show_error_message("Erro ao carregar dados para análise de custos")
                
        except Exception as e:
            logger.error(f"Erro na análise de custos: {e}")
            show_error_message("Erro ao realizar análise de custos")

def show_cost_summary(chart_data: dict):
    """Exibe resumo de custos"""
    st.subheader("📊 Resumo de Custos")
    
    try:
        # Calcular custos totais
        item_type_data = chart_data.get('byItemType', {'labels': [], 'values': []})
        
        total_cost = 0
        total_items = 0
        
        cost_breakdown = {}
        
        for i, item_type in enumerate(item_type_data['labels']):
            if i < len(item_type_data['values']):
                quantity = item_type_data['values'][i]
                unit_price = settings.ITEM_PRICES.get(item_type, 100)
                item_cost = quantity * unit_price
                
                cost_breakdown[item_type] = {
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_cost': item_cost
                }
                
                total_cost += item_cost
                total_items += quantity
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Custo Total", format_currency(total_cost))
        
        with col2:
            st.metric("📦 Total de Itens", format_number(total_items))
        
        with col3:
            avg_cost = total_cost / total_items if total_items > 0 else 0
            st.metric("📊 Custo Médio/Item", format_currency(avg_cost))
        
        with col4:
            most_expensive = max(cost_breakdown.items(), key=lambda x: x[1]['total_cost'])[0] if cost_breakdown else "N/A"
            st.metric("💸 Maior Custo", most_expensive)
        
        # Tabela detalhada
        if cost_breakdown:
            st.markdown("### 📋 Detalhamento por Tipo")
            
            breakdown_df = pd.DataFrame([
                {
                    'Tipo': item_type,
                    'Quantidade': data['quantity'],
                    'Preço Unitário': format_currency(data['unit_price']),
                    'Custo Total': format_currency(data['total_cost']),
                    '% do Total': f"{(data['total_cost'] / total_cost * 100):.1f}%" if total_cost > 0 else "0%"
                }
                for item_type, data in cost_breakdown.items()
            ])
            
            st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        logger.error(f"Erro no resumo de custos: {e}")
        show_error_message("Erro ao gerar resumo de custos")

def show_saved_budgets():
    """Exibe orçamentos salvos"""
    st.subheader("💾 Orçamentos Salvos")
    
    st.info("ℹ️ Funcionalidade de orçamentos salvos será implementada em versão futura")
    
    # Placeholder para orçamentos salvos
    sample_budgets = [
        {
            'Data': '15/01/2025',
            'Período': 'Mensal',
            'Prédio': 'HQ1',
            'Valor Total': 'R$ 25.000,00',
            'Status': 'Aprovado'
        },
        {
            'Data': '10/01/2025',
            'Período': 'Trimestral',
            'Prédio': 'Todos',
            'Valor Total': 'R$ 45.000,00',
            'Status': 'Pendente'
        },
        {
            'Data': '05/01/2025',
            'Período': 'Anual',
            'Prédio': 'HQ2',
            'Valor Total': 'R$ 30.000,00',
            'Status': 'Rejeitado'
        }
    ]
    
    df = pd.DataFrame(sample_budgets)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Filtros para orçamentos salvos
    with st.expander("🔍 Filtros", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.selectbox("Status", ["Todos", "Aprovado", "Pendente", "Rejeitado"])
        
        with col2:
            st.selectbox("Período", ["Todos", "Mensal", "Trimestral", "Anual"])
        
        with col3:
            st.date_input("Data Inicial")

def show_budget_reports():
    """Exibe relatórios de orçamento"""
    st.subheader("📋 Relatórios de Orçamento")
    
    # Tipos de relatório
    report_type = st.selectbox(
        "📊 Tipo de Relatório",
        [
            "Comparativo Mensal",
            "Eficiência de Orçamento",
            "ROI por Tipo de Item",
            "Previsão de Gastos"
        ]
    )
    
    if report_type == "Comparativo Mensal":
        show_monthly_comparison_report()
    elif report_type == "Eficiência de Orçamento":
        show_budget_efficiency_report()
    elif report_type == "ROI por Tipo de Item":
        show_roi_report()
    elif report_type == "Previsão de Gastos":
        show_spending_forecast_report()

def show_monthly_comparison_report():
    """Exibe relatório comparativo mensal"""
    st.markdown("### 📊 Comparativo Mensal de Orçamentos")
    
    # Dados de exemplo
    months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
    budgeted = [25000, 30000, 28000, 32000, 27000, 29000]
    actual = [23500, 31200, 26800, 33500, 28200, 27800]
    
    comparison_data = pd.DataFrame({
        'Mês': months,
        'Orçado (R$)': budgeted,
        'Real (R$)': actual,
        'Variação (R$)': [a - b for a, b in zip(actual, budgeted)],
        'Variação (%)': [f"{((a - b) / b * 100):.1f}%" for a, b in zip(actual, budgeted)]
    })
    
    st.dataframe(comparison_data, use_container_width=True, hide_index=True)
    
    # Gráfico comparativo
    chart_data = pd.DataFrame({
        'Mês': months,
        'Orçado': budgeted,
        'Realizado': actual
    })
    
    st.line_chart(chart_data.set_index('Mês'))

def show_budget_efficiency_report():
    """Exibe relatório de eficiência de orçamento"""
    st.markdown("### ⚡ Eficiência de Orçamento")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Eficiência Geral", "87%", "↑ 5%")
    
    with col2:
        st.metric("Economia Realizada", "R$ 12.500", "↑ R$ 2.300")
    
    with col3:
        st.metric("Precisão de Previsão", "92%", "↑ 3%")
    
    st.info("📊 Relatório detalhado de eficiência será implementado em versão futura")

def show_roi_report():
    """Exibe relatório de ROI por tipo de item"""
    st.markdown("### 💹 ROI por Tipo de Item")
    
    roi_data = pd.DataFrame({
        'Tipo de Item': ['Headsets', 'Mouses', 'Teclados', 'Adaptadores', 'USB Gorila'],
        'Investimento (R$)': [15000, 8000, 6000, 9000, 3500],
        'Economia (R$)': [18000, 9500, 6800, 10200, 4000],
        'ROI (%)': ['20%', '19%', '13%', '13%', '14%']
    })
    
    st.dataframe(roi_data, use_container_width=True, hide_index=True)
    
    st.info("📈 Análise detalhada de ROI será implementada em versão futura")

def show_spending_forecast_report():
    """Exibe relatório de previsão de gastos"""
    st.markdown("### 🔮 Previsão de Gastos")
    
    # Dados de previsão
    forecast_months = ['Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    predicted_spending = [28500, 31000, 29500, 33000, 30000, 32500]
    
    forecast_data = pd.DataFrame({
        'Mês': forecast_months,
        'Previsão (R$)': predicted_spending
    })
    
    st.line_chart(forecast_data.set_index('Mês'))
    
    # Resumo da previsão
    total_forecast = sum(predicted_spending)
    st.metric("💰 Previsão Total (Jul-Dez)", format_currency(total_forecast))
    
    st.info("🤖 Modelo de previsão baseado em machine learning será implementado em versão futura")
