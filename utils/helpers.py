"""
Funções auxiliares gerais
"""
import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

def setup_page_config(page_title: str = "Sistema de Controle", layout: str = "wide"):
    """Configura a página do Streamlit"""
    st.set_page_config(
        page_title=page_title,
        page_icon="📊",
        layout=layout,
        initial_sidebar_state="expanded"
    )

def show_success_message(message: str):
    """Exibe mensagem de sucesso"""
    st.success(f"✅ {message}")

def show_error_message(message: str):
    """Exibe mensagem de erro"""
    st.error(f"❌ {message}")

def show_warning_message(message: str):
    """Exibe mensagem de aviso"""
    st.warning(f"⚠️ {message}")

def show_info_message(message: str):
    """Exibe mensagem informativa"""
    st.info(f"ℹ️ {message}")

def create_download_link(df: pd.DataFrame, filename: str, link_text: str = "Download CSV"):
    """Cria link para download de DataFrame como CSV"""
    try:
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label=link_text,
            data=csv,
            file_name=filename,
            mime='text/csv'
        )
    except Exception as e:
        logger.error(f"Erro ao criar link de download: {e}")
        show_error_message("Erro ao gerar arquivo para download")

def create_excel_download_link(df: pd.DataFrame, filename: str, link_text: str = "Download Excel"):
    """Cria link para download de DataFrame como Excel"""
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Dados')
        
        excel_data = output.getvalue()
        
        st.download_button(
            label=link_text,
            data=excel_data,
            file_name=filename,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        logger.error(f"Erro ao criar link de download Excel: {e}")
        show_error_message("Erro ao gerar arquivo Excel para download")

def format_number(value: float, decimals: int = 2) -> str:
    """Formata número com separadores brasileiros"""
    try:
        if decimals == 0:
            return f"{value:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        else:
            return f"{value:,.{decimals}f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return "0"

def format_currency(value: float) -> str:
    """Formata valor como moeda brasileira"""
    try:
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return "R$ 0,00"

def show_metric_card(title: str, value: str, delta: str = None, help_text: str = None):
    """Exibe card de métrica"""
    st.metric(
        label=title,
        value=value,
        delta=delta,
        help=help_text
    )

def create_sidebar_filters() -> Dict[str, Any]:
    """Cria filtros na barra lateral"""
    st.sidebar.header("🔍 Filtros")
    
    filters = {}
    
    # Filtro de período
    period_options = ['Semanal', 'Mensal', 'Trimestral', 'Anual']
    filters['period'] = st.sidebar.selectbox(
        "Período",
        period_options,
        index=1  # Mensal como padrão
    )
    
    # Filtro de prédio
    building_options = ['Todos', 'HQ1', 'HQ2', 'Spark']
    filters['building'] = st.sidebar.selectbox(
        "Prédio",
        building_options
    )
    
    # Filtro de data
    filters['date_range'] = st.sidebar.date_input(
        "Período de Data",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        max_value=datetime.now()
    )
    
    return filters

def show_loading_spinner(text: str = "Carregando..."):
    """Exibe spinner de carregamento"""
    return st.spinner(text)

def cache_data(ttl: int = 300):
    """Decorator para cache de dados"""
    return st.cache_data(ttl=ttl)

def display_dataframe_with_filters(df: pd.DataFrame, title: str = "Dados"):
    """Exibe DataFrame com filtros interativos"""
    if df.empty:
        show_info_message("Nenhum dado disponível")
        return
    
    st.subheader(title)
    
    # Filtros de coluna
    columns_to_filter = st.multiselect(
        "Selecione colunas para filtrar:",
        df.columns.tolist(),
        default=[]
    )
    
    filtered_df = df.copy()
    
    for col in columns_to_filter:
        if df[col].dtype == 'object':
            # Filtro para strings
            unique_values = df[col].unique()
            selected_values = st.multiselect(
                f"Filtrar {col}:",
                unique_values,
                default=unique_values.tolist()
            )
            filtered_df = filtered_df[filtered_df[col].isin(selected_values)]
        else:
            # Filtro para números
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            selected_range = st.slider(
                f"Filtrar {col}:",
                min_val,
                max_val,
                (min_val, max_val)
            )
            filtered_df = filtered_df[
                (filtered_df[col] >= selected_range[0]) & 
                (filtered_df[col] <= selected_range[1])
            ]
    
    # Exibir DataFrame filtrado
    st.dataframe(filtered_df, use_container_width=True)
    
    # Informações sobre o filtro
    if len(filtered_df) != len(df):
        st.info(f"Mostrando {len(filtered_df)} de {len(df)} registros")
    
    # Links de download
    col1, col2 = st.columns(2)
    with col1:
        create_download_link(filtered_df, f"{title.lower().replace(' ', '_')}.csv")
    with col2:
        create_excel_download_link(filtered_df, f"{title.lower().replace(' ', '_')}.xlsx")

def show_alert(alert_type: str, title: str, message: str, icon: str = None):
    """Exibe alerta formatado"""
    icons = {
        'success': '✅',
        'warning': '⚠️',
        'danger': '❌',
        'info': 'ℹ️'
    }
    
    alert_icon = icons.get(alert_type, icon or 'ℹ️')
    
    if alert_type == 'success':
        st.success(f"{alert_icon} **{title}**\n\n{message}")
    elif alert_type == 'warning':
        st.warning(f"{alert_icon} **{title}**\n\n{message}")
    elif alert_type == 'danger':
        st.error(f"{alert_icon} **{title}**\n\n{message}")
    else:
        st.info(f"{alert_icon} **{title}**\n\n{message}")

def create_tabs(tab_names: List[str]):
    """Cria abas do Streamlit"""
    return st.tabs(tab_names)

def show_progress_bar(progress: float, text: str = ""):
    """Exibe barra de progresso"""
    st.progress(progress, text)

def validate_uploaded_file(uploaded_file, allowed_types: List[str] = ['csv', 'xlsx']) -> bool:
    """Valida arquivo enviado"""
    if uploaded_file is None:
        return False
    
    file_extension = uploaded_file.name.split('.')[-1].lower()
    return file_extension in allowed_types

def parse_uploaded_csv(uploaded_file) -> pd.DataFrame:
    """Parseia arquivo CSV enviado"""
    try:
        return pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            return pd.read_csv(uploaded_file, encoding='latin1')
        except Exception as e:
            logger.error(f"Erro ao ler CSV: {e}")
            return pd.DataFrame()

def parse_uploaded_excel(uploaded_file, sheet_name: str = None) -> pd.DataFrame:
    """Parseia arquivo Excel enviado"""
    try:
        return pd.read_excel(uploaded_file, sheet_name=sheet_name)
    except Exception as e:
        logger.error(f"Erro ao ler Excel: {e}")
        return pd.DataFrame()

def create_expander(title: str, expanded: bool = False):
    """Cria expander do Streamlit"""
    return st.expander(title, expanded=expanded)

def show_json_data(data: Dict[str, Any], title: str = "Dados JSON"):
    """Exibe dados JSON formatados"""
    with st.expander(title):
        st.json(data)

def get_current_timestamp() -> str:
    """Retorna timestamp atual formatado"""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Divisão segura que evita divisão por zero"""
    try:
        return numerator / denominator if denominator != 0 else default
    except:
        return default

def truncate_text(text: str, max_length: int = 50) -> str:
    """Trunca texto com reticências"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
