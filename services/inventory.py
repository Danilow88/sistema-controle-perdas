"""
Página de Controle de Inventário
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import logging

from services.inventory import inventory_service
from utils.helpers import (
    show_success_message, show_error_message, show_info_message,
    show_loading_spinner, display_dataframe_with_filters,
    validate_uploaded_file, parse_uploaded_csv
)
from config.settings import settings

logger = logging.getLogger(__name__)

def show():
    """Exibe a página de inventário"""
    
    st.title("📦 Controle de Inventário")
    st.markdown("Gerencie entradas e saídas de equipamentos")
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Novo Registro",
        "📊 Visualizar Dados", 
        "📤 Upload CSV",
        "📈 Relatórios"
    ])
    
    with tab1:
        show_new_record_form()
    
    with tab2:
        show_inventory_data()
    
    with tab3:
        show_csv_upload()
    
    with tab4:
        show_reports()

def show_new_record_form():
    """Exibe formulário para novo registro"""
    st.subheader("➕ Registrar Nova Movimentação")
    
    with st.form("inventory_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            item_id = st.text_input(
                "🔧 Item ID *",
                placeholder="Ex: Headset-hq1, Mouse-hq2",
                help="Identificador único do item"
            )
            
            amount = st.number_input(
                "📊 Quantidade *",
                min_value=1,
                value=1,
                help="Quantidade de itens"
            )
            
            building = st.selectbox(
                "🏢 Prédio *",
                options=settings.BUILDINGS,
                help="Selecione o prédio"
            )
            
            location = st.text_input(
                "📍 Localização *",
                placeholder="Ex: 5º andar, Sala 501",
                help="Localização específica do item"
            )
            
            movement_type = st.selectbox(
                "🔄 Tipo de Movimentação *",
                options=["entrada", "perda"],
                format_func=lambda x: "📥 Entrada" if x == "entrada" else "📤 Perda"
            )
        
        with col2:
            email = st.text_input(
                "📧 Email do Responsável",
                placeholder="usuario@empresa.com"
            )
            
            invoice_number = st.text_input(
                "🧾 Número da Nota Fiscal",
                placeholder="NF-123456"
            )
            
            sku = st.text_input(
                "🏷️ SKU",
                placeholder="SKU do produto"
            )
            
            supplier = st.text_input(
                "🏪 Fornecedor",
                placeholder="Nome do fornecedor"
            )
            
            shelf_location = st.text_input(
                "📦 Localização na Prateleira",
                placeholder="Ex: A1-B2-C3"
            )
        
        # Botão de submit
        submitted = st.form_submit_button(
            "💾 Registrar Movimentação",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            # Validar campos obrigatórios
            if not all([item_id, amount, building, location, movement_type]):
                show_error_message("Por favor, preencha todos os campos obrigatórios marcados com *")
                return
            
            # Preparar dados para processamento
            form_data = {
                'itemId': item_id,
                'amount': amount,
                'building': building,
                'location': location,
                'type': movement_type,
                'email': email,
                'invoiceNumber': invoice_number,
                'sku': sku,
                'supplier': supplier,
                'shelfLocation': shelf_location
            }
            
            # Processar dados
            with show_loading_spinner("Registrando movimentação..."):
                result = inventory_service.process_form_data(form_data)
                
                if result['success']:
                    show_success_message(result['message'])
                    st.balloons()
                else:
                    show_error_message(result['message'])

def show_inventory_data():
    """Exibe dados do inventário"""
    st.subheader("📊 Dados do Inventário")
    
    # Filtros
    with st.expander("🔍 Filtros Avançados", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            building_filter = st.selectbox(
                "Filtrar por Prédio",
                options=["Todos"] + settings.BUILDINGS
            )
        
        with col2:
            item_filter = st.text_input(
                "Filtrar por Item ID",
                placeholder="Digite parte do ID do item"
            )
        
        with col3:
            supplier_filter = st.text_input(
                "Filtrar por Fornecedor",
                placeholder="Nome do fornecedor"
            )
    
    # Preparar filtros
    filters = {}
    if building_filter != "Todos":
        filters['building'] = building_filter
    if item_filter:
        filters['itemId'] = item_filter
    if supplier_filter:
        filters['supplier'] = supplier_filter
    
    # Carregar dados
    with show_loading_spinner("Carregando dados do inventário..."):
        try:
            result = inventory_service.get_inventory_entries(filters)
            
            if result['success']:
                data = result['data']
                
                if data:
                    # Converter para DataFrame
                    df = pd.DataFrame(data)
                    
                    # Formatar colunas para exibição
                    display_df = df.copy()
                    display_columns = {
                        'itemId': 'Item ID',
                        'dateTime': 'Data/Hora',
                        'amount': 'Quantidade',
                        'building': 'Prédio',
                        'floor': 'Andar',
                        'supplier': 'Fornecedor',
                        'invoice': 'Nota Fiscal',
                        'sku': 'SKU'
                    }
                    
                    # Selecionar e renomear colunas
                    available_columns = [col for col in display_columns.keys() if col in display_df.columns]
                    display_df = display_df[available_columns]
                    display_df = display_df.rename(columns=display_columns)
                    
                    # Exibir estatísticas
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total de Registros", len(data))
                    
                    with col2:
                        total_amount = sum(item.get('amount', 0) for item in data)
                        st.metric("Total de Itens", f"{total_amount:,.0f}")
                    
                    with col3:
                        unique_items = len(set(item.get('itemId', '') for item in data))
                        st.metric("Itens Únicos", unique_items)
                    
                    with col4:
                        unique_suppliers = len(set(item.get('supplier', '') for item in data if item.get('supplier')))
                        st.metric("Fornecedores", unique_suppliers)
                    
                    # Exibir DataFrame com filtros
                    st.markdown("---")
                    display_dataframe_with_filters(display_df, "Entradas de Inventário")
                    
                else:
                    show_info_message("Nenhum registro encontrado com os filtros aplicados")
                    
            else:
                show_error_message(f"Erro ao carregar dados: {result.get('error', 'Erro desconhecido')}")
                
        except Exception as e:
            logger.error(f"Erro ao exibir dados do inventário: {e}")
            show_error_message("Erro ao carregar dados do inventário")

def show_csv_upload():
    """Exibe interface para upload de CSV"""
    st.subheader("📤 Upload de Dados via CSV")
    
    st.markdown("""
    ### 📋 Formato do Arquivo CSV
    
    O arquivo CSV deve conter as seguintes colunas (na ordem):
    1. **Item ID** (obrigatório)
    2. **Data/Hora** (formato: DD/MM/AAAA HH:MM:SS)
    3. **Quantidade** (obrigatório)
    4. **Prédio**
    5. **Email**
    6. **Nota Fiscal**
    7. **SKU**
    8. **Localização**
    9. **Fornecedor**
    10. **Prateleira**
    """)
    
    # Upload do arquivo
    uploaded_file = st.file_uploader(
        "Selecione o arquivo CSV",
        type=['csv'],
        help="Arquivo CSV com dados de inventário"
    )
    
    if uploaded_file is not None:
        if validate_uploaded_file(uploaded_file, ['csv']):
            # Preview do arquivo
            with st.expander("👀 Preview do Arquivo", expanded=True):
                try:
                    df_preview = parse_uploaded_csv(uploaded_file)
                    
                    if not df_preview.empty:
                        st.dataframe(df_preview.head(10), use_container_width=True)
                        st.info(f"📊 Arquivo contém {len(df_preview)} linhas")
                        
                        # Botão para processar
                        if st.button("🚀 Processar Upload", type="primary"):
                            process_csv_upload(uploaded_file)
                    else:
                        show_error_message("Arquivo CSV vazio ou com formato inválido")
                        
                except Exception as e:
                    logger.error(f"Erro ao fazer preview do CSV: {e}")
                    show_error_message("Erro ao ler arquivo CSV")
        else:
            show_error_message("Formato de arquivo inválido. Use apenas arquivos CSV.")

def process_csv_upload(uploaded_file):
    """Processa upload de arquivo CSV"""
    try:
        # Ler conteúdo do arquivo
        csv_content = uploaded_file.getvalue().decode('utf-8')
        
        with show_loading_spinner("Processando arquivo CSV..."):
            result = inventory_service.process_csv_upload(csv_content, uploaded_file.name)
            
            if result['success']:
                show_success_message(result['message'])
                
                # Mostrar estatísticas do upload
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("✅ Sucessos", result.get('successCount', 0))
                
                with col2:
                    st.metric("📝 Total Processado", result.get('totalProcessed', 0))
                
                with col3:
                    error_count = len(result.get('errors', []))
                    st.metric("❌ Erros", error_count)
                
                # Mostrar erros se houver
                if result.get('errors'):
                    with st.expander("⚠️ Erros Encontrados", expanded=False):
                        for error in result['errors']:
                            st.error(error)
                
                st.balloons()
            else:
                show_error_message(result.get('error', 'Erro no processamento'))
                
                if result.get('errors'):
                    with st.expander("❌ Detalhes dos Erros", expanded=True):
                        for error in result['errors']:
                            st.error(error)
                            
    except Exception as e:
        logger.error(f"Erro ao processar upload de CSV: {e}")
        show_error_message("Erro ao processar arquivo CSV")

def show_reports():
    """Exibe relatórios de inventário"""
    st.subheader("📈 Relatórios de Inventário")
    
    # Seleção do tipo de relatório
    report_type = st.selectbox(
        "📊 Tipo de Relatório",
        [
            "Resumo Geral",
            "Por Prédio",
            "Por Tipo de Item",
            "Por Fornecedor",
            "Por Período"
        ]
    )
    
    # Filtros de data
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "📅 Data Inicial",
            value=datetime.now().replace(day=1)  # Primeiro dia do mês
        )
    
    with col2:
        end_date = st.date_input(
            "📅 Data Final",
            value=datetime.now()
        )
    
    if st.button("📊 Gerar Relatório", type="primary"):
        generate_report(report_type, start_date, end_date)

def generate_report(report_type: str, start_date, end_date):
    """Gera relatório específico"""
    with show_loading_spinner(f"Gerando relatório: {report_type}..."):
        try:
            # Obter dados do inventário
            result = inventory_service.get_inventory_entries()
            
            if not result['success']:
                show_error_message("Erro ao obter dados para relatório")
                return
            
            data = result['data']
            
            if not data:
                show_info_message("Nenhum dado disponível para o relatório")
                return
            
            # Converter para DataFrame
            df = pd.DataFrame(data)
            
            # Filtrar por data se possível
            if 'dateTime' in df.columns:
                try:
                    df['dateTime'] = pd.to_datetime(df['dateTime'], errors='coerce')
                    df = df.dropna(subset=['dateTime'])
                    
                    # Aplicar filtro de data
                    start_datetime = pd.to_datetime(start_date)
                    end_datetime = pd.to_datetime(end_date) + pd.Timedelta(days=1)
                    
                    df = df[(df['dateTime'] >= start_datetime) & (df['dateTime'] < end_datetime)]
                except Exception as e:
                    logger.warning(f"Erro ao filtrar por data: {e}")
            
            if df.empty:
                show_info_message("Nenhum dado encontrado no período selecionado")
                return
            
            # Gerar relatório baseado no tipo
            if report_type == "Resumo Geral":
                show_general_summary_report(df)
            elif report_type == "Por Prédio":
                show_building_report(df)
            elif report_type == "Por Tipo de Item":
                show_item_type_report(df)
            elif report_type == "Por Fornecedor":
                show_supplier_report(df)
            elif report_type == "Por Período":
                show_period_report(df)
                
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            show_error_message("Erro ao gerar relatório")

def show_general_summary_report(df: pd.DataFrame):
    """Exibe relatório resumo geral"""
    st.subheader("📊 Resumo Geral")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Registros", len(df))
    
    with col2:
        total_items = df['amount'].sum() if 'amount' in df.columns else 0
        st.metric("Total de Itens", f"{total_items:,.0f}")
    
    with col3:
        unique_items = df['itemId'].nunique() if 'itemId' in df.columns else 0
        st.metric("Itens Únicos", unique_items)
    
    with col4:
        unique_buildings = df['building'].nunique() if 'building' in df.columns else 0
        st.metric("Prédios", unique_buildings)
    
    # Tabela detalhada
    st.markdown("### 📋 Dados Detalhados")
    display_dataframe_with_filters(df, "Relatório Geral")

def show_building_report(df: pd.DataFrame):
    """Exibe relatório por prédio"""
    st.subheader("🏢 Relatório por Prédio")
    
    if 'building' in df.columns:
        building_summary = df.groupby('building').agg({
            'amount': 'sum',
            'itemId': 'count'
        }).reset_index()
        
        building_summary.columns = ['Prédio', 'Total Itens', 'Total Registros']
        
        st.dataframe(building_summary, use_container_width=True, hide_index=True)
    else:
        show_info_message("Coluna 'building' não encontrada nos dados")

def show_item_type_report(df: pd.DataFrame):
    """Exibe relatório por tipo de item"""
    st.subheader("🔧 Relatório por Tipo de Item")
    
    if 'itemId' in df.columns:
        # Categorizar itens
        df['itemType'] = df['itemId'].apply(lambda x: categorize_item_simple(x))
        
        item_summary = df.groupby('itemType').agg({
            'amount': 'sum',
            'itemId': 'count'
        }).reset_index()
        
        item_summary.columns = ['Tipo de Item', 'Total Itens', 'Total Registros']
        item_summary = item_summary.sort_values('Total Itens', ascending=False)
        
        st.dataframe(item_summary, use_container_width=True, hide_index=True)
    else:
        show_info_message("Coluna 'itemId' não encontrada nos dados")

def show_supplier_report(df: pd.DataFrame):
    """Exibe relatório por fornecedor"""
    st.subheader("🏪 Relatório por Fornecedor")
    
    if 'supplier' in df.columns:
        # Filtrar apenas registros com fornecedor
        df_with_supplier = df[df['supplier'].notna() & (df['supplier'] != '')]
        
        if not df_with_supplier.empty:
            supplier_summary = df_with_supplier.groupby('supplier').agg({
                'amount': 'sum',
                'itemId': 'count'
            }).reset_index()
            
            supplier_summary.columns = ['Fornecedor', 'Total Itens', 'Total Registros']
            supplier_summary = supplier_summary.sort_values('Total Itens', ascending=False)
            
            st.dataframe(supplier_summary, use_container_width=True, hide_index=True)
        else:
            show_info_message("Nenhum registro com fornecedor informado")
    else:
        show_info_message("Coluna 'supplier' não encontrada nos dados")

def show_period_report(df: pd.DataFrame):
    """Exibe relatório por período"""
    st.subheader("📅 Relatório por Período")
    
    if 'dateTime' in df.columns:
        try:
            df['dateTime'] = pd.to_datetime(df['dateTime'], errors='coerce')
            df = df.dropna(subset=['dateTime'])
            
            df['month'] = df['dateTime'].dt.to_period('M')
            
            period_summary = df.groupby('month').agg({
                'amount': 'sum',
                'itemId': 'count'
            }).reset_index()
            
            period_summary.columns = ['Período', 'Total Itens', 'Total Registros']
            period_summary = period_summary.sort_values('Período', ascending=False)
            
            st.dataframe(period_summary, use_container_width=True, hide_index=True)
        except Exception as e:
            logger.error(f"Erro ao processar relatório por período: {e}")
            show_error_message("Erro ao processar datas para relatório por período")
    else:
        show_info_message("Coluna 'dateTime' não encontrada nos dados")

def categorize_item_simple(item_id: str) -> str:
    """Categoriza item de forma simples"""
    if not item_id:
        return 'Outros'
    
    item_lower = item_id.lower()
    
    if 'headset' in item_lower:
        return 'Headsets'
    elif 'mouse' in item_lower:
        return 'Mouses'
    elif 'teclado' in item_lower:
        return 'Teclados'
    elif 'adaptador' in item_lower or 'usb c' in item_lower:
        return 'Adaptadores'
    elif 'usb gorila' in item_lower or 'gorila' in item_lower:
        return 'USB Gorila'
    else:
        return 'Outros'
