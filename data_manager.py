"""
Gerenciador de dados para o Sistema de Controle de Perdas
Salvamento local e integração com Google Sheets
"""
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

class DataManager:
    """Gerenciador de dados com múltiplas opções de persistência"""
    
    def __init__(self):
        self.local_file = "inventory_data.json"
        self.spreadsheet_id = '1IMcXLIyOJOANhfxKfzYlwtBqtsXJfRMhCPmoKQdCtdY'
        self.sheet_name = 'Inventory'
        self.gc = None
        
    def init_google_sheets(self):
        """Inicializa conexão com Google Sheets"""
        try:
            if hasattr(st, 'secrets') and 'google_sheets' in st.secrets:
                # Produção - usar secrets do Streamlit
                credentials_dict = dict(st.secrets['google_sheets'])
                credentials = Credentials.from_service_account_info(
                    credentials_dict,
                    scopes=[
                        'https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive'
                    ]
                )
            else:
                # Desenvolvimento - usar arquivo local
                if os.path.exists('credentials.json'):
                    credentials = Credentials.from_service_account_file(
                        'credentials.json',
                        scopes=[
                            'https://www.googleapis.com/auth/spreadsheets',
                            'https://www.googleapis.com/auth/drive'
                        ]
                    )
                else:
                    return False
            
            self.gc = gspread.authorize(credentials)
            return True
            
        except Exception as e:
            st.error(f"❌ Erro ao conectar Google Sheets: {e}")
            return False
    
    def save_to_local(self, data):
        """Salva dados localmente"""
        try:
            # Carregar dados existentes
            existing_data = self.load_from_local()
            
            # Adicionar novos dados
            if isinstance(data, list):
                existing_data.extend(data)
            else:
                existing_data.append(data)
            
            # Salvar arquivo
            with open(self.local_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2, default=str)
            
            return True
            
        except Exception as e:
            st.error(f"❌ Erro ao salvar localmente: {e}")
            return False
    
    def load_from_local(self):
        """Carrega dados locais"""
        try:
            if os.path.exists(self.local_file):
                with open(self.local_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            st.error(f"❌ Erro ao carregar dados locais: {e}")
            return []
    
    def save_to_sheets(self, data):
        """Salva dados no Google Sheets"""
        try:
            if not self.gc and not self.init_google_sheets():
                return False
            
            spreadsheet = self.gc.open_by_key(self.spreadsheet_id)
            worksheet = spreadsheet.worksheet(self.sheet_name)
            
            # Preparar dados para inserção
            if isinstance(data, list):
                # Múltiplos registros
                rows_data = []
                for item in data:
                    row = self._prepare_row_data(item)
                    rows_data.append(row)
                
                # Inserir múltiplas linhas
                worksheet.append_rows(rows_data)
            else:
                # Registro único
                row_data = self._prepare_row_data(data)
                worksheet.append_row(row_data)
            
            return True
            
        except Exception as e:
            st.error(f"❌ Erro ao salvar no Google Sheets: {e}")
            return False
    
    def load_from_sheets(self, filter_entries_only=False):
        """Carrega dados do Google Sheets"""
        try:
            if not self.gc and not self.init_google_sheets():
                return []
            
            spreadsheet = self.gc.open_by_key(self.spreadsheet_id)
            worksheet = spreadsheet.worksheet(self.sheet_name)
            
            # Obter todos os registros
            records = worksheet.get_all_records()
            
            # Converter para formato padrão
            converted_data = []
            for record in records:
                entry = {
                    'inventoryId': record.get('Inventory ID', ''),
                    'itemId': record.get('Item ID', ''),
                    'dateTime': record.get('DateTime', ''),
                    'amount': float(record.get('Amount', 0)),
                    'building': record.get('building', ''),
                    'email': record.get('Email', ''),
                    'invoiceNumber': record.get('Invoice', ''),
                    'sku': record.get('Sku', ''),
                    'location': record.get('Andar', ''),
                    'type': record.get('Tipod de movimentacao', ''),
                    'supplier': record.get('Fornecedor', ''),
                    'shelfLocation': record.get('Prateleira', '')
                }
                
                # Filtrar apenas entradas se solicitado
                if filter_entries_only:
                    if entry['type'].lower() == 'entrada':
                        converted_data.append(entry)
                else:
                    converted_data.append(entry)
            
            return converted_data
            
        except Exception as e:
            st.error(f"❌ Erro ao carregar do Google Sheets: {e}")
            return []
    
    def _prepare_row_data(self, data):
        """Prepara dados para inserção na planilha"""
        return [
            data.get('inventoryId', ''),      # A - Inventory ID
            data.get('itemId', ''),           # B - Item ID  
            data.get('dateTime', ''),         # C - DateTime
            data.get('amount', 0),            # D - Amount
            data.get('building', ''),         # E - building
            data.get('email', ''),            # F - Email
            data.get('invoiceNumber', ''),    # G - Invoice
            data.get('sku', ''),              # H - Sku
            data.get('location', ''),         # I - Andar
            data.get('type', ''),             # J - Tipo de movimentação
            data.get('supplier', ''),         # K - Fornecedor
            data.get('shelfLocation', '')     # L - Prateleira
        ]
    
    def save_data(self, data, method='both'):
        """Salva dados usando método especificado"""
        success_local = False
        success_sheets = False
        
        if method in ['local', 'both']:
            success_local = self.save_to_local(data)
        
        if method in ['sheets', 'both']:
            success_sheets = self.save_to_sheets(data)
        
        return {
            'local': success_local,
            'sheets': success_sheets,
            'any_success': success_local or success_sheets
        }
    
    def load_data(self, source='both', filter_entries_only=False):
        """Carrega dados da fonte especificada"""
        data = []
        
        if source in ['local', 'both']:
            local_data = self.load_from_local()
            if local_data:
                data.extend(local_data)
        
        if source in ['sheets', 'both'] and not data:
            sheets_data = self.load_from_sheets(filter_entries_only)
            if sheets_data:
                data.extend(sheets_data)
        
        return data
    
    def get_statistics(self):
        """Obtém estatísticas dos dados"""
        data = st.session_state.get('inventory_data', [])
        
        if not data:
            return {
                'total_records': 0,
                'total_entries': 0,
                'total_losses': 0,
                'unique_items': 0,
                'unique_buildings': 0,
                'date_range': 'N/A'
            }
        
        df = pd.DataFrame(data)
        
        entries = df[df['type'] == 'entrada'] if 'type' in df.columns else pd.DataFrame()
        losses = df[df['type'] == 'perda'] if 'type' in df.columns else pd.DataFrame()
        
        # Calcular estatísticas
        stats = {
            'total_records': len(df),
            'total_entries': len(entries),
            'total_losses': len(losses),
            'unique_items': df['itemId'].nunique() if 'itemId' in df.columns else 0,
            'unique_buildings': df['building'].nunique() if 'building' in df.columns else 0,
            'date_range': 'N/A'
        }
        
        # Calcular range de datas
        if 'dateTime' in df.columns and not df.empty:
            try:
                df['dateTime_parsed'] = pd.to_datetime(df['dateTime'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
                df_with_dates = df.dropna(subset=['dateTime_parsed'])
                
                if not df_with_dates.empty:
                    min_date = df_with_dates['dateTime_parsed'].min().strftime('%d/%m/%Y')
                    max_date = df_with_dates['dateTime_parsed'].max().strftime('%d/%m/%Y')
                    stats['date_range'] = f"{min_date} a {max_date}"
            except:
                pass
        
        return stats
    
    def export_to_csv(self, data=None, filename=None):
        """Exporta dados para CSV"""
        if data is None:
            data = st.session_state.get('inventory_data', [])
        
        if not data:
            return None
        
        df = pd.DataFrame(data)
        
        # Formatar para exibição
        if not df.empty:
            display_df = df.copy()
            
            # Renomear colunas
            column_mapping = {
                'inventoryId': 'ID Inventário',
                'itemId': 'Item ID',
                'dateTime': 'Data/Hora',
                'amount': 'Quantidade',
                'building': 'Prédio',
                'location': 'Localização',
                'email': 'Email',
                'type': 'Tipo',
                'invoiceNumber': 'Nota Fiscal',
                'sku': 'SKU',
                'supplier': 'Fornecedor',
                'shelfLocation': 'Prateleira'
            }
            
            # Aplicar renomeação apenas para colunas existentes
            existing_columns = {k: v for k, v in column_mapping.items() if k in display_df.columns}
            display_df = display_df.rename(columns=existing_columns)
            
            # Formatar quantidade
            if 'Quantidade' in display_df.columns:
                display_df['Quantidade'] = display_df['Quantidade'].apply(
                    lambda x: f"+{abs(x)}" if x > 0 else str(x)
                )
            
            # Formatar tipo
            if 'Tipo' in display_df.columns:
                display_df['Tipo'] = display_df['Tipo'].apply(
                    lambda x: '📥 Entrada' if x == 'entrada' else '📤 Perda'
                )
        
        # Gerar CSV
        csv_data = display_df.to_csv(index=False, encoding='utf-8-sig')
        
        if filename is None:
            filename = f"inventario_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return csv_data, filename
    
    def clear_all_data(self):
        """Limpa todos os dados"""
        # Limpar session state
        if 'inventory_data' in st.session_state:
            del st.session_state['inventory_data']
        
        if 'budget_history' in st.session_state:
            del st.session_state['budget_history']
        
        # Remover arquivo local
        if os.path.exists(self.local_file):
            os.remove(self.local_file)
        
        return True

# Instância global
data_manager = DataManager()
