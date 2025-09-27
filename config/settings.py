"""
Configurações globais da aplicação
"""
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Settings:
    """Configurações da aplicação"""
    
    # Google Sheets
    INVENTORY_SPREADSHEET_ID = os.getenv('INVENTORY_SPREADSHEET_ID', '1IMcXLIyOJOANhfxKfzYlwtBqtsXJfRMhCPmoKQdCtdY')
    MONITORS_SPREADSHEET_ID = os.getenv('MONITORS_SPREADSHEET_ID', '1hI6WWiH03AvXFxMCpPpYtIhQEU062C_k4utIE6YyctY')
    GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
    
    # JIRA
    JIRA_BASE_URL = os.getenv('JIRA_BASE_URL', 'https://nubank.atlassian.net')
    JIRA_EMAIL = os.getenv('JIRA_EMAIL', '')
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN', '')
    JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY', 'TS')
    
    # Aplicação
    APP_TITLE = os.getenv('APP_TITLE', 'Sistema de Controle de Perdas')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TIMEZONE = os.getenv('TIMEZONE', 'America/Sao_Paulo')
    
    # Cache
    CACHE_TTL = int(os.getenv('CACHE_TTL', '300'))
    
    # Sheets names
    INVENTORY_SHEET_NAME = 'Inventory'
    MONITORS_SHEET_NAME = 'agenda ts'
    RESUMO_MENSAL_SHEET_NAME = 'Resumo Mensal'
    RESUMO_ANUAL_SHEET_NAME = 'Resumo Anual'
    ORCAMENTO_SHEET_NAME = 'Orcamento'
    
    # Mapeamento de campos JIRA
    JIRA_FIELD_MAPPING = {
        'Request Type': 'customfield_10010',
        'TC - Date of activity': 'customfield_44449',
        'TC - Maintenance window End': 'customfield_44451',
        'TC - Maintenance window Start': 'customfield_44450',
        'TC - Reason for request monitor': 'customfield_44475',
        'TC - Reinstallation date': 'customfield_44452',
        'TC - Space/Area monitores': 'customfield_44476',
        'TC - Type of Installation/Uninstallation': 'customfield_43375',
        'TC - Type of Request Monitors': 'customfield_43371',
        'Floor - ITOPS': 'customfield_12969',
        'Number of monitor positions': 'customfield_44455',
        'TC - Office Location': 'customfield_43376'
    }
    
    # Configurações de preços (para orçamentos)
    ITEM_PRICES = {
        'Headsets': 250.0,
        'Mouses': 80.0,
        'Teclados': 150.0,
        'Adaptadores': 45.0,
        'USB Gorila': 35.0
    }
    
    # Prédios
    BUILDINGS = ['HQ1', 'HQ2', 'Spark']
    
    # Tipos de item
    ITEM_TYPES = ['Headsets', 'Mouses', 'Teclados', 'Adaptadores', 'USB Gorila']
    
    @classmethod
    def get_jira_auth(cls):
        """Retorna tupla com email e token para autenticação JIRA"""
        return (cls.JIRA_EMAIL, cls.JIRA_API_TOKEN)
    
    @classmethod
    def is_configured(cls):
        """Verifica se as configurações essenciais estão definidas"""
        return bool(cls.JIRA_EMAIL and cls.JIRA_API_TOKEN)

# Instância global das configurações
settings = Settings()
