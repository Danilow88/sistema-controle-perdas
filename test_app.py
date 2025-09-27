"""
Script de teste para verificar se a aplicação carrega corretamente
"""
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testa se todos os imports funcionam"""
    print("🔍 Testando imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit OK")
    except ImportError as e:
        print(f"❌ Streamlit: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas OK")
    except ImportError as e:
        print(f"❌ Pandas: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✅ Plotly OK")
    except ImportError as e:
        print(f"❌ Plotly: {e}")
        return False
    
    try:
        from config.settings import settings
        print("✅ Config OK")
    except ImportError as e:
        print(f"❌ Config: {e}")
        return False
    
    try:
        from services.inventory import inventory_service
        print("✅ Inventory Service OK")
    except ImportError as e:
        print(f"❌ Inventory Service: {e}")
        return False
    
    try:
        from services.monitoring import monitoring_service
        print("✅ Monitoring Service OK")
    except ImportError as e:
        print(f"❌ Monitoring Service: {e}")
        return False
    
    try:
        from utils.helpers import format_currency
        print("✅ Utils OK")
    except ImportError as e:
        print(f"❌ Utils: {e}")
        return False
    
    print("✅ Todos os imports funcionaram!")
    return True

def test_config():
    """Testa configurações"""
    print("\n🔧 Testando configurações...")
    
    try:
        from config.settings import settings
        
        print(f"📊 Inventory Spreadsheet ID: {settings.INVENTORY_SPREADSHEET_ID}")
        print(f"🖥️ Monitors Spreadsheet ID: {settings.MONITORS_SPREADSHEET_ID}")
        print(f"🏢 JIRA Base URL: {settings.JIRA_BASE_URL}")
        print(f"📧 JIRA Email: {settings.JIRA_EMAIL}")
        print(f"🔑 JIRA Token configurado: {'Sim' if settings.JIRA_API_TOKEN else 'Não'}")
        print(f"⚙️ Configurações válidas: {'Sim' if settings.is_configured() else 'Não'}")
        
        return True
    except Exception as e:
        print(f"❌ Erro nas configurações: {e}")
        return False

def test_structure():
    """Testa estrutura de arquivos"""
    print("\n📁 Testando estrutura de arquivos...")
    
    required_files = [
        'app.py',
        'streamlit_app.py',
        'requirements.txt',
        'config/settings.py',
        'services/google_sheets.py',
        'services/inventory.py',
        'services/monitoring.py',
        'services/jira_client.py',
        'pages/dashboard.py',
        'pages/inventory.py',
        'pages/monitoring.py',
        'pages/budget.py',
        'utils/helpers.py',
        'utils/charts.py',
        'utils/data_processing.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Arquivos faltando: {len(missing_files)}")
        return False
    else:
        print("\n✅ Todos os arquivos necessários estão presentes!")
        return True

def main():
    """Função principal de teste"""
    print("🧪 TESTE DO SISTEMA DE CONTROLE DE PERDAS")
    print("=" * 50)
    
    # Teste 1: Estrutura de arquivos
    structure_ok = test_structure()
    
    # Teste 2: Imports
    imports_ok = test_imports()
    
    # Teste 3: Configurações
    config_ok = test_config()
    
    # Resumo
    print("\n📊 RESUMO DOS TESTES:")
    print(f"📁 Estrutura: {'✅ OK' if structure_ok else '❌ FALHA'}")
    print(f"📦 Imports: {'✅ OK' if imports_ok else '❌ FALHA'}")
    print(f"⚙️ Configurações: {'✅ OK' if config_ok else '❌ FALHA'}")
    
    if all([structure_ok, imports_ok, config_ok]):
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("🚀 Sistema pronto para executar!")
        print("\n💡 Próximos passos:")
        print("1. Configure suas credenciais Google reais no arquivo credentials.json")
        print("2. Execute: source venv/bin/activate && streamlit run app.py")
        return True
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
        print("🔧 Corrija os problemas antes de executar o sistema")
        return False

if __name__ == "__main__":
    main()
