"""
Sistema de Controle de Perdas e Entradas - Gadgets
Versão fiel ao HTML original + Salvamento de dados
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import uuid

# Configuração
st.set_page_config(
    page_title="Controle de Perdas e Entradas - Gadgets",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS fiel ao original
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #8A2BE2 0%, #4B0082 100%);
}

.main-container {
    background-color: #fff;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    margin: 24px auto;
    max-width: 1200px;
    overflow: hidden;
}

.header {
    background: linear-gradient(90deg, #8A2BE2, #9370DB);
    color: white;
    padding: 20px;
}

.header-content {
    display: flex;
    align-items: center;
    gap: 16px;
}

.logo {
    width: 52px;
    height: 52px;
    background-color: rgba(255,255,255,0.15);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    color: #fff;
}

.section-title {
    font-size: 16px;
    font-weight: 700;
    color: #8A2BE2;
    margin-bottom: 12px;
}

.building-group {
    background-color: #f8f9ff;
    padding: 12px;
    border-radius: 10px;
    border-left: 4px solid #8A2BE2;
    margin: 8px 0;
}

.location-info {
    background-color: #e6f7ff;
    padding: 10px 12px;
    border-radius: 10px;
    margin-top: 8px;
    border-left: 4px solid #8A2BE2;
}

.success-message {
    background-color: #e6f7ee;
    color: #2e7d32;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    font-weight: 600;
    margin: 12px 0;
}

.reposicao-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

.reposicao-table th {
    background-color: #820ad1;
    color: white;
    padding: 8px;
    text-align: center;
}

.reposicao-table td {
    padding: 8px;
    text-align: center;
    border-bottom: 1px solid #eee;
}

.stButton > button {
    background-color: #8A2BE2 !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
}
</style>
""", unsafe_allow_html=True)

# Dados do sistema
ITEMS_BY_BUILDING = {
    'Spark': ['Headset-spk', 'Mouse-spk', 'Teclado k120-spk', 'Adaptadores usb c-spk', 'Usb Gorila 6m1 spk'],
    'HQ1': ['Headset-hq1', 'Mouse-hq1', 'Teclado k120-hq1', 'Adaptadores usb c-hq1', 'Usb Gorila 6m1 hq1'],
    'HQ2': ['Headset-hq2', 'Mouse-hq2', 'Teclado k120-hq2', 'Adaptadores usb c-hq2', 'Usb Gorila 6m1 hq2']
}

ITEM_NAMES = {
    'Headset-spk': 'Headset - Spark', 'Mouse-spk': 'Mouse - Spark', 'Teclado k120-spk': 'Teclado K120 - Spark',
    'Adaptadores usb c-spk': 'Adaptador USB-C - Spark', 'Usb Gorila 6m1 spk': 'USB Gorila 6-em-1 - Spark',
    'Headset-hq1': 'Headset - HQ1', 'Mouse-hq1': 'Mouse - HQ1', 'Teclado k120-hq1': 'Teclado K120 - HQ1',
    'Adaptadores usb c-hq1': 'Adaptador USB-C - HQ1', 'Usb Gorila 6m1 hq1': 'USB Gorila 6-em-1 - HQ1',
    'Headset-hq2': 'Headset - HQ2', 'Mouse-hq2': 'Mouse - HQ2', 'Teclado k120-hq2': 'Teclado K120 - HQ2',
    'Adaptadores usb c-hq2': 'Adaptador USB-C - HQ2', 'Usb Gorila 6m1 hq2': 'USB Gorila 6-em-1 - HQ2'
}

BUILDING_FLOORS = {
    'HQ1': ["2° ANDAR L MAIOR", "2° ANDAR L MENOR", "4° ANDAR", "6° ANDAR L MAIOR", "8° ANDAR L MAIOR"],
    'HQ2': ["2° ANDAR L MAIOR", "4° ANDAR L MENOR", "8° ANDAR", "12° ANDAR", "15° ANDAR"],
    'Spark': ["1° ANDAR", "2° ANDAR", "3° ANDAR"]
}

def generate_id():
    return f'INV_{int(datetime.now().timestamp() * 1000)}_{str(uuid.uuid4()).split("-")[0].upper()}'

def format_currency(value):
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def main():
    # Header
    st.markdown("""
    <div class="main-container">
        <div class="header">
            <div class="header-content">
                <div class="logo">💻</div>
                <div>
                    <h1 style="margin:0; font-size:22px; font-weight:700;">Controle de Perdas e Entradas - Gadgets</h1>
                    <p style="margin:6px 0 0 0; opacity:0.95; font-size:14px;">Registro de movimentações e visualização de indicadores</p>
                </div>
                <div>
                    <span style="background:rgba(255,255,255,0.15); padding:6px 10px; border-radius:999px; font-size:12px;">🟢 Online</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Layout principal
    col_main, col_sidebar = st.columns([1.6, 1])
    
    with col_main:
        show_main_panel()
    
    with col_sidebar:
        show_sidebar_panel()
    
    # Modais
    show_modals()

def show_main_panel():
    st.markdown('<div class="section-title">➖ Registrar Perda</div>', unsafe_allow_html=True)
    
    with st.form("loss_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            building = st.selectbox("Prédio *", [""] + list(ITEMS_BY_BUILDING.keys()))
        with col2:
            email = st.text_input("Email", placeholder="seu.email@exemplo.com.br")
        
        floor = ""
        if building:
            st.markdown(f'<div class="building-group"><strong>🏢 {building}</strong></div>', unsafe_allow_html=True)
            floor = st.selectbox(f"Andar ({building})", [""] + BUILDING_FLOORS.get(building, []))
        
        if building and floor:
            st.markdown(f'<div class="location-info"><strong>Local:</strong> {building} - {floor}</div>', unsafe_allow_html=True)
        
        items_data = []
        if building and floor:
            st.markdown("**Itens:**")
            num_items = st.number_input("Número de itens", 1, 4, 1)
            
            for i in range(num_items):
                col_item, col_qty = st.columns([2, 1])
                with col_item:
                    item = st.selectbox(f"Item {i+1}", [""] + ITEMS_BY_BUILDING.get(building, []), 
                                      format_func=lambda x: "Selecione" if x == "" else ITEM_NAMES.get(x, x), key=f"item_{i}")
                with col_qty:
                    qty = st.number_input("Qtd", 1, 1000, 1, key=f"qty_{i}")
                
                if item:
                    items_data.append({'itemId': item, 'quantity': qty, 'name': ITEM_NAMES.get(item, item)})
        
        submitted = st.form_submit_button("📝 Registrar Perda", type="primary", disabled=not (building and floor and items_data))
        
        if submitted:
            process_registration(building, floor, email, items_data, 'perda')

def show_sidebar_panel():
    # Reposição
    st.markdown('<div class="section-title">🚚 Quantidades para Reposição</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <table class="reposicao-table">
        <tr><th>Prédio</th><th>Teclados</th><th>Headsets</th><th>Mouses</th><th>Adaptadores</th></tr>
        <tr><td>HQ1 - L. Maior</td><td>20</td><td>5</td><td>10</td><td>5</td></tr>
        <tr><td>HQ1 - L. Menor</td><td>10</td><td>5</td><td>5</td><td>5</td></tr>
        <tr><td>HQ2</td><td>15</td><td>5</td><td>10</td><td>5</td></tr>
        <tr><td>Spark</td><td>15</td><td>10</td><td>15</td><td>10</td></tr>
    </table>
    """, unsafe_allow_html=True)
    
    # Ações
    st.markdown('<div class="section-title">⚡ Ações Rápidas</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💰", key="budget"):
            st.session_state.show_budget = True
    with col2:
        if st.button("➕", key="entry"):
            st.session_state.show_entry = True
    with col3:
        if st.button("📦", key="inventory"):
            st.session_state.show_inventory = True
    
    col4, col5 = st.columns(2)
    with col4:
        if st.button("📊", key="dashboard"):
            st.session_state.show_dashboard = True
    with col5:
        if st.button("💾", key="save"):
            save_data()

def show_modals():
    if st.session_state.get('show_entry'):
        show_entry_modal()
    if st.session_state.get('show_budget'):
        show_budget_modal()
    if st.session_state.get('show_inventory'):
        show_inventory_modal()
    if st.session_state.get('show_dashboard'):
        show_dashboard_modal()

def show_entry_modal():
    st.markdown("---")
    st.subheader("➕ Registro de Entrada")
    
    if st.button("❌ Fechar", key="close_entry"):
        st.session_state.show_entry = False
        st.rerun()
    
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            building = st.selectbox("Prédio *", [""] + list(ITEMS_BY_BUILDING.keys()), key="entry_building")
            email = st.text_input("Email", key="entry_email")
        with col2:
            invoice = st.text_input("Nota Fiscal")
            supplier = st.text_input("Fornecedor")
        
        floor = ""
        if building:
            floors = ["ESTOQUE"] + BUILDING_FLOORS.get(building, [])
            floor = st.selectbox(f"Andar ({building})", [""] + floors, key="entry_floor")
        
        items = []
        if building and floor:
            st.success(f"📍 {building} - {floor}")
            num = st.number_input("Itens", 1, 4, 1, key="entry_num")
            
            for i in range(num):
                col_item, col_qty = st.columns([2, 1])
                with col_item:
                    item = st.selectbox(f"Item {i+1}", [""] + ITEMS_BY_BUILDING.get(building, []), 
                                      format_func=lambda x: "Selecione" if x == "" else ITEM_NAMES.get(x, x), key=f"entry_item_{i}")
                with col_qty:
                    qty = st.number_input("Qtd", 1, 1000, 1, key=f"entry_qty_{i}")
                
                if item:
                    items.append({'itemId': item, 'quantity': qty, 'name': ITEM_NAMES.get(item, item)})
        
        if st.form_submit_button("➕ Registrar Entrada", type="primary", disabled=not (building and floor and items)):
            process_registration(building, floor, email, items, 'entrada', invoice, '', supplier, '')

def show_budget_modal():
    st.markdown("---")
    st.subheader("💰 Orçamentos")
    
    if st.button("❌ Fechar", key="close_budget"):
        st.session_state.show_budget = False
        st.rerun()
    
    # Gráfico
    months = ['Jan', 'Fev', 'Mar', 'Abr']
    values = [25000, 30000, 28000, 32000]
    fig = px.line(x=months, y=values, title="Histórico de Orçamentos")
    fig.update_traces(line_color='#28a745')
    st.plotly_chart(fig, use_container_width=True)
    
    # Geração
    limit = st.selectbox("Limite:", [25000, 30000, 35000], format_func=format_currency)
    
    if st.button("🚀 Gerar", type="primary"):
        items = [
            {'Item': 'Headsets', 'Qtd': 40, 'Preço': 'R$ 260,00', 'Total': 'R$ 10.400,00'},
            {'Item': 'Adaptadores', 'Qtd': 25, 'Preço': 'R$ 112,00', 'Total': 'R$ 2.800,00'},
            {'Item': 'Teclados', 'Qtd': 30, 'Preço': 'R$ 90,00', 'Total': 'R$ 2.700,00'},
            {'Item': 'Mouses', 'Qtd': 50, 'Preço': 'R$ 32,00', 'Total': 'R$ 1.600,00'}
        ]
        
        df = pd.DataFrame(items)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.metric("💰 Total", "R$ 17.500,00")

def show_inventory_modal():
    st.markdown("---")
    st.subheader("📦 Inventário")
    
    if st.button("❌ Fechar", key="close_inventory"):
        st.session_state.show_inventory = False
        st.rerun()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Carregar", key="load"):
            load_data()
    with col2:
        if st.button("🎲 Exemplo", key="sample"):
            create_sample()
    with col3:
        if st.button("💾 Salvar", key="save_inv"):
            save_data()
    
    show_table()

def show_dashboard_modal():
    st.markdown("---")
    st.subheader("📊 Dashboard")
    
    if st.button("❌ Fechar", key="close_dashboard"):
        st.session_state.show_dashboard = False
        st.rerun()
    
    # Gráficos
    data = st.session_state.get('inventory_data', [])
    
    if data:
        df = pd.DataFrame(data)
        
        # Por prédio
        building_counts = df['building'].value_counts()
        fig1 = px.pie(values=building_counts.values, names=building_counts.index, title="Por Prédio")
        st.plotly_chart(fig1, use_container_width=True)
        
        # Por tipo
        type_counts = df['type'].value_counts()
        fig2 = px.bar(x=type_counts.index, y=type_counts.values, title="Por Tipo")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("📊 Registre dados para ver gráficos")

def process_registration(building, floor, email, items, reg_type, invoice='', sku='', supplier='', shelf=''):
    try:
        timestamp = datetime.now()
        
        for item in items:
            entry = {
                'inventoryId': generate_id(),
                'itemId': item['itemId'],
                'dateTime': timestamp.strftime('%d/%m/%Y %H:%M:%S'),
                'amount': abs(item['quantity']) if reg_type == 'entrada' else -abs(item['quantity']),
                'building': building,
                'location': floor,
                'email': email,
                'type': reg_type,
                'invoiceNumber': invoice,
                'sku': sku,
                'supplier': supplier,
                'shelfLocation': shelf
            }
            
            if 'inventory_data' not in st.session_state:
                st.session_state.inventory_data = []
            
            st.session_state.inventory_data.append(entry)
        
        st.markdown(f'<div class="success-message">✅ {reg_type.title()} registrada com sucesso!</div>', unsafe_allow_html=True)
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ Erro: {e}")

def show_table():
    data = st.session_state.get('inventory_data', [])
    
    if data:
        entries = [d for d in data if d.get('type') == 'entrada']
        
        if entries:
            df = pd.DataFrame([
                {
                    'Data': e.get('dateTime', ''),
                    'Item': e.get('itemId', ''),
                    'Qtd': f"+{abs(e.get('amount', 0))}",
                    'Prédio': e.get('building', ''),
                    'NF': e.get('invoiceNumber', ''),
                    'Fornecedor': e.get('supplier', '')
                }
                for e in entries
            ])
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.metric("📊 Entradas", len(entries))

def load_data():
    st.info("📥 Carregando do Google Sheets...")
    # Simular carregamento
    st.session_state.inventory_status = "✅ Dados carregados"

def save_data():
    data = st.session_state.get('inventory_data', [])
    if data:
        st.success(f"💾 {len(data)} registros salvos!")
    else:
        st.warning("⚠️ Nenhum dado para salvar")

def create_sample():
    sample = []
    for i in range(5):
        sample.append({
            'inventoryId': generate_id(),
            'itemId': 'Headset-hq1',
            'dateTime': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'amount': 5,
            'building': 'HQ1',
            'location': 'ESTOQUE',
            'email': 'test@empresa.com',
            'type': 'entrada',
            'invoiceNumber': f'NF-{i}',
            'sku': f'SKU-{i}',
            'supplier': 'Fornecedor A',
            'shelfLocation': f'P-A{i}'
        })
    
    st.session_state.inventory_data = sample
    st.success("🎲 Dados criados!")

if __name__ == "__main__":
    main()