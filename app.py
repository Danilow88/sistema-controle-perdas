"""
Aplicação principal do Sistema de Controle de Perdas
"""
import streamlit as st
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Imports locais
from config.settings import settings
from utils.helpers import setup_page_config, show_error_message, show_info_message
from pages import dashboard, inventory, monitoring, budget

# Configuração da página
setup_page_config("Sistema de Controle de Perdas", "wide")

def main():
    """Função principal da aplicação"""
    
    # CSS personalizado
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #8a05be 0%, #4500a0 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #8a05be;
    }
    
    .sidebar-logo {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid #eee;
        margin-bottom: 1rem;
    }
    
    .alert-success {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    
    .alert-danger {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header principal
    st.markdown(f"""
    <div class="main-header">
        <h1>📊 {settings.APP_TITLE}</h1>
        <p>Sistema completo para controle de perdas de gadgets e monitoramento de equipamentos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar com navegação
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h2>🏢 Nubank</h2>
            <p>Sistema de Controle</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Menu de navegação
        page = st.selectbox(
            "📍 Navegação",
            [
                "🏠 Dashboard",
                "📦 Inventário",
                "🖥️ Monitoramento",
                "💰 Orçamentos"
            ]
        )
        
        # Informações do sistema
        st.markdown("---")
        st.markdown("### ℹ️ Informações")
        st.info(f"""
        **Última atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
        
        **Versão:** 1.0.0
        
        **Ambiente:** {'Debug' if settings.DEBUG else 'Produção'}
        """)
        
        # Status das configurações
        if settings.is_configured():
            st.success("✅ Configurações OK")
        else:
            st.error("❌ Configurações incompletas")
            st.warning("Verifique as variáveis de ambiente")
    
    # Roteamento de páginas
    try:
        if page == "🏠 Dashboard":
            dashboard.show()
        elif page == "📦 Inventário":
            inventory.show()
        elif page == "🖥️ Monitoramento":
            monitoring.show()
        elif page == "💰 Orçamentos":
            budget.show()
    except Exception as e:
        st.error(f"❌ Erro ao carregar página: {str(e)}")
        
        if settings.DEBUG:
            st.exception(e)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Sistema de Controle de Perdas - Desenvolvido com ❤️ usando Streamlit</p>
        <p>© 2025 Nubank - Todos os direitos reservados</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
