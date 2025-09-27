"""
Sistema de Controle de Perdas e Entradas - Gadgets
Versão completa convertida do HTML/JavaScript para Streamlit
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import uuid

# Configuração da página
st.set_page_config(
    page_title="Controle de Perdas e Entradas - Gadgets",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.main-header {
    background: linear-gradient(90deg, #8A2BE2, #9370DB);
    color: white;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.section-title {
    font-size: 16px;
    font-weight: 700;
    color: #8A2BE2;
    margin-bottom: 12px;
}

.building-card {
    background-color: #f8f9ff;
    padding: 12px;
    border-radius: 10px;
    border-left: 4px solid #8A2BE2;
    margin: 8px 0;
}

.reposicao-info {
    background-color: #f8f9ff;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #e6e6f7;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# Dados constantes
ITEMS_BY_BUILDING = {
    'Spark': ['Headset-spk', 'Adaptadores usb c-spk', 'Mouse-spk', 'Teclado k120-spk', 'Usb Gorila 5m1 lanspk', 'Usb Gorila 6m1 spk'],
    'HQ1': ['Headset-hq1', 'Adaptadores usb c-hq1', 'Mouse-hq1', 'Teclado k120-hq1', 'Usb Gorila 5m1 lan hq1', 'Usb Gorila 6m1 hq1'],
    'HQ2': ['Headset-hq2', 'Adaptadores usb c-hq2', 'Mouse-hq2', 'Teclado k120-hq2', 'Usb Gorila 5m1 lan hq2', 'Usb Gorila 6m1 hq2']
}

ITEM_NAMES = {
    'Headset-spk': 'Headset - Spark', 'Adaptadores usb c-spk': 'Adaptador USB-C - Spark', 'Mouse-spk': 'Mouse - Spark',
    'Teclado k120-spk': 'Teclado K120 - Spark', 'Headset-hq1': 'Headset - HQ1', 'Adaptadores usb c-hq1': 'Adaptador USB-C - HQ1',
    'Mouse-hq1': 'Mouse - HQ1', 'Teclado k120-hq1': 'Teclado K120 - HQ1', 'Headset-hq2': 'Headset - HQ2',
    'Adaptadores usb c-hq2': 'Adaptador USB-C - HQ2', 'Mouse-hq2': 'Mouse - HQ2', 'Teclado k120-hq2': 'Teclado K120 - HQ2',
    'Usb Gorila 5m1 lan hq1': 'USB Gorila 5-em-1 - HQ1', 'Usb Gorila 5m1 lan hq2': 'USB Gorila 5-em-1 - HQ2',
    'Usb Gorila 5m1 lanspk': 'USB Gorila 5-em-1 - Spark', 'Usb Gorila 6m1 hq1': 'USB Gorila 6-em-1 - HQ1',
    'Usb Gorila 6m1 hq2': 'USB Gorila 6-em-1 - HQ2', 'Usb Gorila 6m1 spk': 'USB Gorila 6-em-1 - Spark'
}

BUILDING_FLOORS = {
    'HQ1': ["2° ANDAR L MAIOR", "2° ANDAR L MENOR", "4° ANDAR L MAIOR", "4° ANDAR L MENOR", "6° ANDAR L MAIOR", "6° ANDAR L MENOR", "8° ANDAR L MAIOR", "8° ANDAR L MENOR", "4° ANDAR"],
    'HQ2': ["2° ANDAR L MAIOR", "2° ANDAR L MENOR", "4° ANDAR L MAIOR", "4° ANDAR L MENOR", "6° ANDAR L MAIOR", "6° ANDAR L MENOR", "8° ANDAR L MAIOR", "8° ANDAR L MENOR", "8° ANDAR", "12° ANDAR", "15° ANDAR"],
    'Spark': ["1° ANDAR", "2° ANDAR", "3° ANDAR"]
}

def generate_unique_id():
    return f'INV_{int(datetime.now().timestamp() * 1000)}_{str(uuid.uuid4()).split("-")[0].upper()}'

def format_currency(value):
    try:
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return "R$ 0,00"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>💻 Controle de Perdas e Entradas - Gadgets</h1>
        <p>Registro de movimentações e visualização de indicadores</p>
        <span style="background-color: rgba(255,255,255,0.15); color: #fff; padding: 6px 10px; border-radius: 999px; font-size: 12px;">🟢 Online</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Layout em abas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Registrar Perda",
        "➕ Registrar Entrada", 
        "📊 Dashboard",
        "💰 Orçamentos",
        "📦 Inventário"
    ])
    
    with tab1:
        show_loss_registration()
    
    with tab2:
        show_entry_registration()
    
    with tab3:
        show_dashboard()
    
    with tab4:
        show_budget_section()
    
    with tab5:
        show_inventory_section()

def show_loss_registration():
    """Aba de registro de perdas"""
    st.subheader("📝 Registrar Perda de Equipamentos")
    
    col_main, col_info = st.columns([2, 1])
    
    with col_main:
        with st.form("loss_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                building = st.selectbox("Prédio *", options=[""] + list(ITEMS_BY_BUILDING.keys()))
            
            with col2:
                email = st.text_input("Email", placeholder="seu.email@exemplo.com.br")
            
            floor = ""
            if building:
                st.markdown(f"**🏢 {building}**")
                floor = st.selectbox(f"Andar ({building})", options=[""] + BUILDING_FLOORS.get(building, []))
            
            if building and floor:
                st.success(f"📍 Local: {building} - {floor}")
                
                st.markdown("**Itens para registrar perda:**")
                num_items = st.number_input("Número de itens", min_value=1, max_value=4, value=1)
                
                items_data = []
                for i in range(num_items):
                    col_item, col_qty = st.columns([2, 1])
                    
                    with col_item:
                        item_id = st.selectbox(
                            f"Item {i+1}",
                            options=[""] + ITEMS_BY_BUILDING.get(building, []),
                            format_func=lambda x: "Selecione um item" if x == "" else ITEM_NAMES.get(x, x),
                            key=f"loss_item_{i}"
                        )
                    
                    with col_qty:
                        quantity = st.number_input(f"Qtd {i+1}", min_value=1, value=1, key=f"loss_qty_{i}")
                    
                    if item_id:
                        items_data.append({'itemId': item_id, 'quantity': quantity, 'name': ITEM_NAMES.get(item_id, item_id)})
            
            submitted = st.form_submit_button("📝 Registrar Perda", type="primary", disabled=not (building and floor and items_data))
            
            if submitted and building and floor and items_data:
                process_registration(building, floor, email, items_data, 'perda')
    
    with col_info:
        show_reposition_info()

def show_entry_registration():
    """Aba de registro de entradas"""
    st.subheader("➕ Registrar Entrada de Equipamentos")
    
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            building = st.selectbox("Prédio *", options=[""] + list(ITEMS_BY_BUILDING.keys()), key="entry_building")
            email = st.text_input("Email", key="entry_email")
            invoice = st.text_input("Nota Fiscal", placeholder="NF-123456")
        
        with col2:
            sku = st.text_input("SKU", placeholder="Código do produto")
            supplier = st.text_input("Fornecedor", placeholder="Nome do fornecedor")
            shelf = st.text_input("Prateleira", placeholder="Ex: P-A1")
        
        floor = ""
        if building:
            floor_options = ["ESTOQUE"] + BUILDING_FLOORS.get(building, [])
            floor = st.selectbox(f"Andar ({building})", options=[""] + floor_options, key="entry_floor")
        
        if building and floor:
            st.success(f"📍 Local: {building} - {floor}")
            
            st.markdown("**Itens para entrada:**")
            num_items = st.number_input("Número de itens", min_value=1, max_value=4, value=1, key="entry_num_items")
            
            items_data = []
            for i in range(num_items):
                col_item, col_qty = st.columns([2, 1])
                
                with col_item:
                    item_options = [""] + ITEMS_BY_BUILDING.get(building, []) + ["ITEM_PERSONALIZADO"]
                    item_id = st.selectbox(
                        f"Item {i+1}",
                        options=item_options,
                        format_func=lambda x: ("Selecione um item" if x == "" else 
                                             "🆕 Item Personalizado" if x == "ITEM_PERSONALIZADO" else 
                                             ITEM_NAMES.get(x, x)),
                        key=f"entry_item_{i}"
                    )
                
                with col_qty:
                    quantity = st.number_input(f"Qtd {i+1}", min_value=1, value=1, key=f"entry_qty_{i}")
                
                # Item personalizado
                if item_id == "ITEM_PERSONALIZADO":
                    st.markdown("**📦 Item Personalizado:**")
                    col_name, col_value = st.columns(2)
                    
                    with col_name:
                        custom_name = st.text_input("Nome do Item *", key=f"custom_name_{i}")
                    
                    with col_value:
                        custom_value = st.number_input("Valor (R$) *", min_value=0.0, step=0.01, key=f"custom_value_{i}")
                    
                    custom_supplier = st.text_input("Fornecedor *", key=f"custom_supplier_{i}")
                    
                    if custom_name and custom_value and custom_supplier:
                        items_data.append({
                            'itemId': f"CUSTOM_{custom_name.replace(' ', '_').upper()}",
                            'quantity': quantity,
                            'name': custom_name,
                            'isCustom': True,
                            'customData': {'name': custom_name, 'value': custom_value, 'supplier': custom_supplier}
                        })
                elif item_id:
                    items_data.append({
                        'itemId': item_id,
                        'quantity': quantity,
                        'name': ITEM_NAMES.get(item_id, item_id),
                        'isCustom': False
                    })
        
        submitted = st.form_submit_button("➕ Registrar Entrada", type="primary", disabled=not (building and floor and items_data))
        
        if submitted and building and floor and items_data:
            process_registration(building, floor, email, items_data, 'entrada', invoice, sku, supplier, shelf)

def show_dashboard():
    """Aba de dashboard"""
    st.subheader("📊 Dashboard Multi-Período")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    # Calcular métricas do histórico
    history = st.session_state.get('inventory_history', [])
    
    total_records = len(history)
    total_entries = len([h for h in history if h.get('type') == 'entrada'])
    total_losses = len([h for h in history if h.get('type') == 'perda'])
    total_value = sum([abs(h.get('amount', 0)) * 150 for h in history])  # Valor estimado
    
    with col1:
        st.metric("📦 Total Registros", total_records)
    
    with col2:
        st.metric("➕ Entradas", total_entries, f"+{total_entries}")
    
    with col3:
        st.metric("➖ Perdas", total_losses, f"-{total_losses}")
    
    with col4:
        st.metric("💰 Valor Estimado", format_currency(total_value))
    
    # Gráficos
    if history:
        create_dashboard_charts_from_history(history)
    else:
        create_sample_dashboard_charts()

def create_dashboard_charts_from_history(history):
    """Cria gráficos baseados no histórico real"""
    df = pd.DataFrame(history)
    
    # Gráfico temporal
    st.subheader("📈 Evolução Temporal")
    
    if not df.empty:
        df['dateTime'] = pd.to_datetime(df['dateTime'], format='%d/%m/%Y %H:%M:%S')
        df['date'] = df['dateTime'].dt.date
        
        daily_data = df.groupby('date').size().reset_index()
        daily_data.columns = ['Data', 'Registros']
        
        fig = px.line(daily_data, x='Data', y='Registros', title="Registros por Dia")
        fig.update_traces(line_color='#8A2BE2')
        st.plotly_chart(fig, use_container_width=True)
    
    # Gráficos por categoria
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏢 Por Prédio")
        if not df.empty:
            building_counts = df['building'].value_counts()
            fig = px.pie(values=building_counts.values, names=building_counts.index)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔄 Por Tipo")
        if not df.empty:
            type_counts = df['type'].value_counts()
            fig = px.bar(x=type_counts.index, y=type_counts.values)
            st.plotly_chart(fig, use_container_width=True)

def create_sample_dashboard_charts():
    """Cria gráficos de exemplo"""
    st.info("📊 Registre algumas movimentações para ver gráficos baseados em dados reais")
    
    # Dados de exemplo
    monthly_data = pd.DataFrame({
        'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
        'Perdas': [15000, 22000, 18000, 25000, 20000],
        'Entradas': [18000, 25000, 20000, 28000, 23000]
    })
    
    fig = px.line(monthly_data, x='Mês', y=['Perdas', 'Entradas'], title="Evolução Mensal (Exemplo)")
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        building_data = pd.DataFrame({
            'Prédio': ['HQ1', 'HQ2', 'Spark'],
            'Valor': [18000, 12000, 15000]
        })
        fig = px.pie(building_data, values='Valor', names='Prédio', title="Por Prédio (Exemplo)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        item_data = pd.DataFrame({
            'Tipo': ['Headsets', 'Mouses', 'Teclados', 'Adaptadores', 'USB Gorila'],
            'Quantidade': [25, 8, 5, 15, 7]
        })
        fig = px.bar(item_data, x='Tipo', y='Quantidade', title="Por Tipo (Exemplo)")
        st.plotly_chart(fig, use_container_width=True)

def show_budget_section():
    """Aba de orçamentos"""
    st.subheader("💰 Orçamentos Sugeridos")
    
    # Configurações
    col1, col2 = st.columns(2)
    
    with col1:
        budget_limit = st.selectbox(
            "Limite de orçamento:",
            options=[25000, 30000, 35000, 40000, 45000],
            format_func=lambda x: format_currency(x)
        )
    
    with col2:
        if st.button("➕ Item Personalizado"):
            st.info("Funcionalidade em desenvolvimento")
    
    if st.button("🚀 Gerar Orçamento", type="primary"):
        generate_budget(budget_limit)

def generate_budget(budget_limit):
    """Gera orçamento"""
    budget_items = [
        {'Item': 'Teclados', 'Preço': 90.00, 'Qtd': int(budget_limit * 0.25 / 90), 'Total': budget_limit * 0.25},
        {'Item': 'Mouses', 'Preço': 31.90, 'Qtd': int(budget_limit * 0.15 / 31.90), 'Total': budget_limit * 0.15},
        {'Item': 'Headsets', 'Preço': 260.00, 'Qtd': int(budget_limit * 0.35 / 260), 'Total': budget_limit * 0.35},
        {'Item': 'Adaptadores', 'Preço': 112.00, 'Qtd': int(budget_limit * 0.25 / 112), 'Total': budget_limit * 0.25}
    ]
    
    df = pd.DataFrame(budget_items)
    df['Preço Unitário'] = df['Preço'].apply(format_currency)
    df['Custo Total'] = df['Total'].apply(format_currency)
    df = df[['Item', 'Preço Unitário', 'Qtd', 'Custo Total']]
    
    st.success("✅ Orçamento gerado!")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    total = sum([item['Total'] for item in budget_items])
    st.metric("💰 Total", format_currency(total))
    
    # Gráfico
    fig = px.pie(values=[item['Total'] for item in budget_items], names=[item['Item'] for item in budget_items])
    st.plotly_chart(fig, use_container_width=True)

def show_inventory_section():
    """Aba de inventário"""
    st.subheader("📦 Inventário - Histórico de Movimentações")
    
    # Filtros
    with st.expander("🔍 Filtros", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_building = st.selectbox("Prédio", ["Todos"] + list(ITEMS_BY_BUILDING.keys()))
            filter_type = st.selectbox("Tipo", ["Todos", "entrada", "perda"])
        
        with col2:
            filter_item = st.text_input("Item ID")
            filter_supplier = st.text_input("Fornecedor")
        
        with col3:
            date_from = st.date_input("Data inicial", value=datetime.now() - timedelta(days=30))
            date_to = st.date_input("Data final", value=datetime.now())
    
    # Dados do inventário
    history = st.session_state.get('inventory_history', [])
    
    if history:
        df = pd.DataFrame(history)
        
        # Aplicar filtros
        if filter_building != "Todos":
            df = df[df['building'] == filter_building]
        
        if filter_type != "Todos":
            df = df[df['type'] == filter_type]
        
        if filter_item:
            df = df[df['itemId'].str.contains(filter_item, case=False, na=False)]
        
        if filter_supplier:
            df = df[df['supplier'].str.contains(filter_supplier, case=False, na=False)]
        
        # Preparar para exibição
        display_df = df.copy()
        display_df['Tipo'] = display_df['type'].apply(lambda x: '📥 Entrada' if x == 'entrada' else '📤 Perda')
        display_df['Quantidade'] = display_df['amount'].apply(lambda x: f"+{abs(x)}" if x > 0 else str(x))
        
        # Selecionar colunas
        columns = ['dateTime', 'itemId', 'Quantidade', 'building', 'location', 'Tipo', 'invoiceNumber', 'supplier']
        display_df = display_df[columns]
        display_df.columns = ['Data/Hora', 'Item ID', 'Quantidade', 'Prédio', 'Andar', 'Tipo', 'Nota Fiscal', 'Fornecedor']
        
        # Estatísticas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total", len(df))
        
        with col2:
            entries = len(df[df['type'] == 'entrada'])
            st.metric("📥 Entradas", entries)
        
        with col3:
            losses = len(df[df['type'] == 'perda'])
            st.metric("📤 Perdas", losses)
        
        with col4:
            unique_items = df['itemId'].nunique()
            st.metric("🔧 Itens Únicos", unique_items)
        
        # Tabela
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Download
        csv_data = display_df.to_csv(index=False)
        st.download_button(
            "📄 Download CSV",
            data=csv_data,
            file_name=f"inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("📝 Nenhum registro no histórico. Registre algumas movimentações primeiro!")
        
        # Botão para criar dados de exemplo
        if st.button("🎲 Criar Dados de Exemplo"):
            create_sample_data()

def create_sample_data():
    """Cria dados de exemplo"""
    sample_data = []
    
    # Perdas
    for i in range(5):
        sample_data.append({
            'inventoryId': generate_unique_id(),
            'itemId': np.random.choice(['Headset-hq1', 'Mouse-hq2', 'Teclado k120-spark']),
            'dateTime': (datetime.now() - timedelta(days=np.random.randint(1, 30))).strftime('%d/%m/%Y %H:%M:%S'),
            'amount': -np.random.randint(1, 5),
            'building': np.random.choice(['HQ1', 'HQ2', 'Spark']),
            'location': '5° ANDAR',
            'email': 'usuario@empresa.com',
            'type': 'perda',
            'invoiceNumber': '',
            'sku': '',
            'supplier': '',
            'shelfLocation': ''
        })
    
    # Entradas
    for i in range(3):
        sample_data.append({
            'inventoryId': generate_unique_id(),
            'itemId': np.random.choice(['Headset-hq1', 'Mouse-hq2', 'Adaptadores usb c-hq1']),
            'dateTime': (datetime.now() - timedelta(days=np.random.randint(1, 15))).strftime('%d/%m/%Y %H:%M:%S'),
            'amount': np.random.randint(5, 20),
            'building': np.random.choice(['HQ1', 'HQ2', 'Spark']),
            'location': 'ESTOQUE',
            'email': 'compras@empresa.com',
            'type': 'entrada',
            'invoiceNumber': f'NF-{np.random.randint(100000, 999999)}',
            'sku': f'SKU-{np.random.randint(1000, 9999)}',
            'supplier': np.random.choice(['Fornecedor A', 'Fornecedor B', 'Fornecedor C']),
            'shelfLocation': f'P-{np.random.choice(["A1", "B2", "C3"])}'
        })
    
    st.session_state.inventory_history = sample_data
    st.success("🎲 Dados de exemplo criados!")
    st.rerun()

def show_reposition_info():
    """Informações de reposição"""
    st.markdown("""
    <div class="reposicao-info">
        <div class="section-title">🚚 Quantidades para Reposição</div>
    </div>
    """, unsafe_allow_html=True)
    
    reposicao_data = {
        'Prédio': ['HQ1 - L. Maior', 'HQ1 - L. Menor', 'HQ2', 'Spark'],
        'Teclados': [20, 10, 15, 15],
        'Headsets': [5, 5, 5, 10],
        'Mouses': [10, 5, 10, 15],
        'Adaptadores': [5, 5, 5, 10]
    }
    
    st.dataframe(pd.DataFrame(reposicao_data), use_container_width=True, hide_index=True)

def process_registration(building, floor, email, items_data, reg_type, invoice='', sku='', supplier='', shelf=''):
    """Processa registro de movimentação"""
    try:
        with st.spinner(f"Processando registro de {reg_type}..."):
            import time
            time.sleep(1)
            
            timestamp = datetime.now()
            registered_items = []
            
            for item in items_data:
                entry = {
                    'inventoryId': generate_unique_id(),
                    'itemId': item['itemId'],
                    'dateTime': timestamp.strftime('%d/%m/%Y %H:%M:%S'),
                    'amount': abs(item['quantity']) if reg_type == 'entrada' else -abs(item['quantity']),
                    'building': building,
                    'location': floor,
                    'email': email,
                    'type': reg_type,
                    'invoiceNumber': invoice,
                    'sku': sku,
                    'supplier': item.get('customData', {}).get('supplier', supplier),
                    'shelfLocation': shelf
                }
                registered_items.append(entry)
            
            # Salvar no session state
            if 'inventory_history' not in st.session_state:
                st.session_state.inventory_history = []
            
            st.session_state.inventory_history.extend(registered_items)
            
            st.success(f"✅ {reg_type.title()} registrada com sucesso para {len(items_data)} item(ns)!")
            st.balloons()
            
            # Resumo
            with st.expander("📋 Resumo do Registro", expanded=True):
                summary_data = []
                for item in items_data:
                    summary_data.append({
                        'Item': item['name'],
                        'Quantidade': item['quantity'],
                        'Prédio': building,
                        'Andar': floor,
                        'Tipo': reg_type.title(),
                        'Data/Hora': timestamp.strftime('%d/%m/%Y %H:%M:%S')
                    })
                
                st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
    
    except Exception as e:
        st.error(f"❌ Erro ao registrar {reg_type}: {str(e)}")

if __name__ == "__main__":
    main()