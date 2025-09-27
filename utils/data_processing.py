"""
Utilitários para processamento de dados
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Classe para processamento de dados"""
    
    @staticmethod
    def format_currency(value: float) -> str:
        """Formata valor como moeda brasileira"""
        try:
            return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except:
            return "R$ 0,00"
    
    @staticmethod
    def format_date_brazilian(date_value: Any) -> str:
        """Formata data no formato brasileiro"""
        if not date_value or date_value == '-':
            return '-'
        
        try:
            if isinstance(date_value, datetime):
                return date_value.strftime("%d/%m/%Y")
            elif isinstance(date_value, str):
                # Tentar parsear diferentes formatos
                for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%d/%m/%Y']:
                    try:
                        date_obj = datetime.strptime(date_value, fmt)
                        return date_obj.strftime("%d/%m/%Y")
                    except:
                        continue
                return date_value
            else:
                return str(date_value)
        except:
            return '-'
    
    @staticmethod
    def format_datetime_brazilian(date_value: Any) -> str:
        """Formata data e hora no formato brasileiro"""
        if not date_value or date_value == '-':
            return '-'
        
        try:
            if isinstance(date_value, datetime):
                return date_value.strftime("%d/%m/%Y %H:%M")
            elif isinstance(date_value, str):
                # Tentar parsear diferentes formatos
                for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M']:
                    try:
                        date_obj = datetime.strptime(date_value, fmt)
                        return date_obj.strftime("%d/%m/%Y %H:%M")
                    except:
                        continue
                return date_value
            else:
                return str(date_value)
        except:
            return '-'
    
    @staticmethod
    def safe_float(value: Any, default: float = 0.0) -> float:
        """Converte valor para float de forma segura"""
        try:
            if value is None or value == '':
                return default
            return float(value)
        except:
            return default
    
    @staticmethod
    def safe_int(value: Any, default: int = 0) -> int:
        """Converte valor para int de forma segura"""
        try:
            if value is None or value == '':
                return default
            return int(float(value))
        except:
            return default
    
    @staticmethod
    def categorize_item_type(item_id: str) -> str:
        """Categoriza tipo de item baseado no ID"""
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
    
    @staticmethod
    def get_week_number(date: datetime) -> int:
        """Obtém número da semana no ano"""
        return date.isocalendar()[1]
    
    @staticmethod
    def get_quarter(date: datetime) -> int:
        """Obtém trimestre da data"""
        return (date.month - 1) // 3 + 1
    
    @staticmethod
    def aggregate_by_period(df: pd.DataFrame, period: str, date_column: str, value_column: str) -> Dict[str, Any]:
        """Agrega dados por período"""
        try:
            if df.empty:
                return {'labels': [], 'values': []}
            
            # Converter coluna de data
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
            df = df.dropna(subset=[date_column])
            
            if period == 'weekly':
                df['period'] = df[date_column].dt.strftime('%Y-W%U')
                df['label'] = df[date_column].apply(lambda x: f"Sem {x.isocalendar()[1]}/{x.year}")
            elif period == 'monthly':
                df['period'] = df[date_column].dt.strftime('%Y-%m')
                df['label'] = df[date_column].dt.strftime('%b/%Y')
            elif period == 'quarterly':
                df['quarter'] = df[date_column].apply(lambda x: DataProcessor.get_quarter(x))
                df['period'] = df[date_column].dt.year.astype(str) + '-Q' + df['quarter'].astype(str)
                df['label'] = 'Q' + df['quarter'].astype(str) + '/' + df[date_column].dt.year.astype(str)
            elif period == 'yearly':
                df['period'] = df[date_column].dt.year.astype(str)
                df['label'] = df[date_column].dt.year.astype(str)
            else:
                return {'labels': [], 'values': []}
            
            # Agrupar por período
            grouped = df.groupby(['period', 'label'])[value_column].sum().reset_index()
            grouped = grouped.sort_values('period')
            
            return {
                'labels': grouped['label'].tolist(),
                'values': grouped[value_column].tolist()
            }
            
        except Exception as e:
            logger.error(f"Erro ao agregar por período: {e}")
            return {'labels': [], 'values': []}
    
    @staticmethod
    def filter_dataframe(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Aplica filtros a um DataFrame"""
        try:
            filtered_df = df.copy()
            
            for column, value in filters.items():
                if column in filtered_df.columns and value:
                    if isinstance(value, str):
                        # Filtro por substring (case insensitive)
                        filtered_df = filtered_df[
                            filtered_df[column].astype(str).str.contains(value, case=False, na=False)
                        ]
                    else:
                        # Filtro por valor exato
                        filtered_df = filtered_df[filtered_df[column] == value]
            
            return filtered_df
            
        except Exception as e:
            logger.error(f"Erro ao filtrar DataFrame: {e}")
            return df
    
    @staticmethod
    def calculate_statistics(df: pd.DataFrame, value_column: str) -> Dict[str, float]:
        """Calcula estatísticas básicas de uma coluna"""
        try:
            if df.empty or value_column not in df.columns:
                return {
                    'total': 0,
                    'mean': 0,
                    'median': 0,
                    'std': 0,
                    'min': 0,
                    'max': 0
                }
            
            values = pd.to_numeric(df[value_column], errors='coerce').dropna()
            
            return {
                'total': float(values.sum()),
                'mean': float(values.mean()),
                'median': float(values.median()),
                'std': float(values.std()),
                'min': float(values.min()),
                'max': float(values.max())
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {e}")
            return {
                'total': 0,
                'mean': 0,
                'median': 0,
                'std': 0,
                'min': 0,
                'max': 0
            }
    
    @staticmethod
    def validate_form_data(data: Dict[str, Any], required_fields: List[str]) -> Tuple[bool, str]:
        """Valida dados de formulário"""
        try:
            missing_fields = []
            
            for field in required_fields:
                if field not in data or not data[field]:
                    missing_fields.append(field)
            
            if missing_fields:
                return False, f"Campos obrigatórios faltando: {', '.join(missing_fields)}"
            
            return True, "Validação bem-sucedida"
            
        except Exception as e:
            return False, f"Erro na validação: {str(e)}"
    
    @staticmethod
    def clean_string(value: Any) -> str:
        """Limpa e normaliza string"""
        if value is None:
            return ''
        
        try:
            return str(value).strip()
        except:
            return ''
    
    @staticmethod
    def parse_csv_line(line: str) -> List[str]:
        """Parseia linha CSV considerando aspas"""
        result = []
        current = ''
        in_quotes = False
        
        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                result.append(current.strip())
                current = ''
            else:
                current += char
        
        result.append(current.strip())
        return result
    
    @staticmethod
    def generate_summary_report(data: List[Dict[str, Any]], title: str) -> Dict[str, Any]:
        """Gera relatório resumo dos dados"""
        try:
            if not data:
                return {
                    'title': title,
                    'total_records': 0,
                    'summary': 'Nenhum dado disponível'
                }
            
            total_records = len(data)
            
            # Estatísticas básicas
            summary = f"Total de registros: {total_records}"
            
            # Se há campo de data, mostrar período
            if data[0].get('dateTime') or data[0].get('created'):
                dates = []
                for item in data:
                    date_str = item.get('dateTime') or item.get('created', '')
                    if date_str:
                        try:
                            date_obj = pd.to_datetime(date_str)
                            dates.append(date_obj)
                        except:
                            continue
                
                if dates:
                    min_date = min(dates).strftime("%d/%m/%Y")
                    max_date = max(dates).strftime("%d/%m/%Y")
                    summary += f"\nPeríodo: {min_date} a {max_date}"
            
            return {
                'title': title,
                'total_records': total_records,
                'summary': summary,
                'last_updated': datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório resumo: {e}")
            return {
                'title': title,
                'total_records': 0,
                'summary': f'Erro ao gerar resumo: {str(e)}'
            }
