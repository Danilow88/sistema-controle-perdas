"""
Serviço para integração com Google Sheets
"""
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from typing import List, Dict, Any, Optional
import streamlit as st
from datetime import datetime
import logging

from config.settings import settings

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    """Serviço para interação com Google Sheets"""
    
    def __init__(self):
        self.gc = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa o cliente do Google Sheets"""
        try:
            # Tentar usar credenciais do Streamlit secrets primeiro
            if hasattr(st, 'secrets') and 'google_sheets' in st.secrets:
                credentials_dict = dict(st.secrets['google_sheets'])
                credentials = Credentials.from_service_account_info(
                    credentials_dict,
                    scopes=[
                        'https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive'
                    ]
                )
            else:
                # Fallback para arquivo local
                credentials = Credentials.from_service_account_file(
                    settings.GOOGLE_CREDENTIALS_FILE,
                    scopes=[
                        'https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive'
                    ]
                )
            
            self.gc = gspread.authorize(credentials)
            logger.info("Google Sheets client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets client: {e}")
            self.gc = None
    
    def get_worksheet(self, spreadsheet_id: str, sheet_name: str):
        """Obtém uma worksheet específica"""
        if not self.gc:
            raise Exception("Google Sheets client not initialized")
        
        try:
            spreadsheet = self.gc.open_by_key(spreadsheet_id)
            worksheet = spreadsheet.worksheet(sheet_name)
            return worksheet
        except Exception as e:
            logger.error(f"Failed to get worksheet {sheet_name}: {e}")
            raise
    
    def read_sheet_data(self, spreadsheet_id: str, sheet_name: str) -> pd.DataFrame:
        """Lê dados de uma planilha e retorna como DataFrame"""
        try:
            worksheet = self.get_worksheet(spreadsheet_id, sheet_name)
            data = worksheet.get_all_records()
            
            if not data:
                return pd.DataFrame()
            
            df = pd.DataFrame(data)
            logger.info(f"Successfully read {len(df)} rows from {sheet_name}")
            return df
            
        except Exception as e:
            logger.error(f"Failed to read sheet data: {e}")
            return pd.DataFrame()
    
    def append_row(self, spreadsheet_id: str, sheet_name: str, row_data: List[Any]):
        """Adiciona uma nova linha à planilha"""
        try:
            worksheet = self.get_worksheet(spreadsheet_id, sheet_name)
            worksheet.append_row(row_data)
            logger.info(f"Successfully appended row to {sheet_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to append row: {e}")
            return False
    
    def update_cell(self, spreadsheet_id: str, sheet_name: str, row: int, col: int, value: Any):
        """Atualiza uma célula específica"""
        try:
            worksheet = self.get_worksheet(spreadsheet_id, sheet_name)
            worksheet.update_cell(row, col, value)
            logger.info(f"Successfully updated cell ({row}, {col}) in {sheet_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update cell: {e}")
            return False
    
    def clear_sheet(self, spreadsheet_id: str, sheet_name: str):
        """Limpa todo o conteúdo de uma planilha"""
        try:
            worksheet = self.get_worksheet(spreadsheet_id, sheet_name)
            worksheet.clear()
            logger.info(f"Successfully cleared {sheet_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear sheet: {e}")
            return False
    
    def batch_update(self, spreadsheet_id: str, sheet_name: str, data: List[List[Any]], start_cell: str = 'A1'):
        """Atualiza múltiplas células de uma vez"""
        try:
            worksheet = self.get_worksheet(spreadsheet_id, sheet_name)
            worksheet.update(start_cell, data)
            logger.info(f"Successfully batch updated {len(data)} rows in {sheet_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to batch update: {e}")
            return False
    
    def create_sheet(self, spreadsheet_id: str, sheet_name: str):
        """Cria uma nova aba na planilha"""
        try:
            spreadsheet = self.gc.open_by_key(spreadsheet_id)
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="20")
            logger.info(f"Successfully created sheet {sheet_name}")
            return worksheet
            
        except Exception as e:
            logger.error(f"Failed to create sheet: {e}")
            return None
    
    def sheet_exists(self, spreadsheet_id: str, sheet_name: str) -> bool:
        """Verifica se uma aba existe na planilha"""
        try:
            spreadsheet = self.gc.open_by_key(spreadsheet_id)
            sheet_names = [ws.title for ws in spreadsheet.worksheets()]
            return sheet_name in sheet_names
            
        except Exception as e:
            logger.error(f"Failed to check if sheet exists: {e}")
            return False

# Instância global do serviço
google_sheets_service = GoogleSheetsService()
