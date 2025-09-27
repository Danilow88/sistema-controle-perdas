"""
Configurações para o Sistema de Monitoramento de Monitores
"""

class MonitorConfig:
    """Configurações centralizadas para monitores"""
    
    # Google Sheets - Sistema de Monitores
    MONITORS_SPREADSHEET_ID = '1hI6WWiH03AvXFxMCpPpYtIhQEU062C_k4utIE6YyctY'
    MONITORS_SHEET_NAME = 'Calendário de eventos - Monitores'
    MONITORS_SHEET_GID = '1469973439'
    
    # Status possíveis para eventos
    EVENT_STATUS = {
        'PENDENTE': 'Pendente',
        'CONFIRMADO': 'Confirmado', 
        'EXCEDENTE': 'Excedente',
        'CONCLUIDO': 'Concluído'
    }
    
    # Status de atendimento
    ATTENDANCE_STATUS = {
        'NAO_INICIADO': 'Não Iniciado',
        'EM_ANDAMENTO': 'Em Andamento',
        'CONCLUIDO': 'Concluído',
        'PENDENTE': 'Pendente'
    }
    
    # Mapeamento de colunas da planilha
    COLUMN_MAPPING = {
        'DATA_SOLICITACAO': 0,    # Coluna A
        'DATA_MONTAGEM': 1,       # Coluna B
        'SALA': 2,                # Coluna C
        'MONITORES': 3,           # Coluna D
        'DATA_DESMONTAGEM': 4,    # Coluna E
        'OBSERVACOES': 5,         # Coluna F
        'REPORTER': 6,            # Coluna G
        'KEY': 7,                 # Coluna H
        'STATUS': 8,              # Coluna I
        'STATUS_ATENDIMENTO': 9   # Coluna J
    }
    
    # Configurações de alertas
    ALERT_THRESHOLDS = {
        'MAX_PENDING_EVENTS': 5,
        'MAX_EXCEEDED_EVENTS': 3,
        'MAX_EVENTS_WITHOUT_REPORTER': 10,
        'DAYS_BEFORE_EXPIRY_WARNING': 7
    }
    
    # Configurações de interface
    UI_CONFIG = {
        'ITEMS_PER_PAGE': 10,
        'MAX_SEARCH_RESULTS': 100,
        'DEFAULT_DATE_FORMAT': 'DD/MM/YYYY',
        'REFRESH_INTERVAL_MINUTES': 30
    }
    
    # Cores do tema Nubank (fiel ao HTML original)
    THEME_COLORS = {
        'PRIMARY': '#8a05be',
        'PRIMARY_DARK': '#4500a0',
        'BACKGROUND': '#f5f5f7',
        'CARD_BACKGROUND': '#ffffff',
        'TEXT_PRIMARY': '#333333',
        'TEXT_SECONDARY': '#666666',
        'SUCCESS': '#2b8a3e',
        'WARNING': '#e67700', 
        'DANGER': '#c92a2a',
        'INFO': '#1971c2'
    }
    
    # Configurações de badges por status
    STATUS_BADGES = {
        'Pendente': {
            'color': '#e67700',
            'background': '#fff4e6',
            'icon': '⏳'
        },
        'Confirmado': {
            'color': '#2b8a3e',
            'background': '#d3f9d8',
            'icon': '✅'
        },
        'Excedente': {
            'color': '#c92a2a',
            'background': '#ffe3e3',
            'icon': '⚠️'
        },
        'Concluído': {
            'color': '#2b8a3e',
            'background': '#d3f9d8',
            'icon': '🏁'
        }
    }
    
    # Configurações de badges por status de atendimento
    ATTENDANCE_BADGES = {
        'Não Iniciado': {
            'color': '#6c757d',
            'background': '#f8f9fa',
            'icon': '⭕'
        },
        'Em Andamento': {
            'color': '#1971c2',
            'background': '#e7f5ff',
            'icon': '🔄'
        },
        'Concluído': {
            'color': '#2b8a3e',
            'background': '#d3f9d8',
            'icon': '✅'
        },
        'Pendente': {
            'color': '#e67700',
            'background': '#fff4e6',
            'icon': '⏸️'
        }
    }
    
    # Tipos de salas comuns
    COMMON_ROOMS = [
        'Sala A-201', 'Sala A-202', 'Sala A-203',
        'Sala B-301', 'Sala B-302', 'Sala B-303',
        'Sala C-101', 'Sala C-102', 'Sala C-103',
        'Auditório Principal', 'Auditório Secundário',
        'Sala de Treinamento 1', 'Sala de Treinamento 2',
        'Sala de Reunião Executiva', 'Sala de Videoconferência'
    ]
    
    # Limites de monitores por tipo de sala
    MONITOR_LIMITS = {
        'Sala pequena': {'min': 1, 'max': 3, 'optimal': 2},
        'Sala média': {'min': 2, 'max': 5, 'optimal': 3},
        'Sala grande': {'min': 3, 'max': 8, 'optimal': 5},
        'Auditório': {'min': 5, 'max': 15, 'optimal': 10},
        'Sala de treinamento': {'min': 2, 'max': 6, 'optimal': 4}
    }
    
    # Configurações de exportação
    EXPORT_CONFIG = {
        'CSV_DELIMITER': ',',
        'CSV_ENCODING': 'utf-8-sig',
        'DATE_FORMAT': '%d/%m/%Y',
        'FILENAME_FORMAT': 'monitores_export_%Y%m%d_%H%M%S.csv'
    }
    
    # Mensagens de sistema
    SYSTEM_MESSAGES = {
        'LOADING': 'Carregando dados da planilha...',
        'NO_DATA': 'Nenhum dado encontrado na planilha',
        'FILTER_NO_RESULTS': 'Nenhum resultado para os filtros aplicados',
        'EXPORT_SUCCESS': 'Dados exportados com sucesso!',
        'UPDATE_SUCCESS': 'Status atualizado com sucesso!',
        'ERROR_LOADING': 'Erro ao carregar dados da planilha',
        'ERROR_UPDATING': 'Erro ao atualizar status',
        'ERROR_EXPORTING': 'Erro ao exportar dados'
    }
    
    # Configurações de validação
    VALIDATION_RULES = {
        'MAX_MONITORS_PER_EVENT': 20,
        'MIN_MONITORS_PER_EVENT': 1,
        'MAX_ROOM_NAME_LENGTH': 100,
        'MAX_REPORTER_NAME_LENGTH': 100,
        'MAX_KEY_LENGTH': 50,
        'MAX_OBSERVATIONS_LENGTH': 500
    }
    
    # URLs e endpoints
    ENDPOINTS = {
        'GVIZ_BASE': 'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq',
        'CSV_EXPORT': 'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}',
        'SHEET_VIEW': 'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={gid}'
    }
    
    @classmethod
    def get_gviz_url(cls, query='SELECT *'):
        """Gera URL para consulta gviz"""
        base_url = cls.ENDPOINTS['GVIZ_BASE'].format(spreadsheet_id=cls.MONITORS_SPREADSHEET_ID)
        params = {
            'tqx': 'out:json',
            'sheet': cls.MONITORS_SHEET_NAME,
            'headers': '1',
            'tq': query
        }
        
        param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{param_string}"
    
    @classmethod
    def get_csv_url(cls):
        """Gera URL para export CSV"""
        return cls.ENDPOINTS['CSV_EXPORT'].format(
            spreadsheet_id=cls.MONITORS_SPREADSHEET_ID,
            gid=cls.MONITORS_SHEET_GID
        )
    
    @classmethod
    def get_sheet_url(cls):
        """Gera URL para visualizar planilha"""
        return cls.ENDPOINTS['SHEET_VIEW'].format(
            spreadsheet_id=cls.MONITORS_SPREADSHEET_ID,
            gid=cls.MONITORS_SHEET_GID
        )
    
    @classmethod
    def get_status_badge_config(cls, status):
        """Retorna configuração de badge para um status"""
        return cls.STATUS_BADGES.get(status, {
            'color': '#6c757d',
            'background': '#f8f9fa',
            'icon': '❓'
        })
    
    @classmethod
    def get_attendance_badge_config(cls, status):
        """Retorna configuração de badge para status de atendimento"""
        return cls.ATTENDANCE_BADGES.get(status, {
            'color': '#6c757d',
            'background': '#f8f9fa',
            'icon': '❓'
        })
    
    @classmethod
    def validate_event_data(cls, data):
        """Valida dados de um evento"""
        errors = []
        
        # Validar monitores
        monitores = data.get('monitores', 0)
        if monitores < cls.VALIDATION_RULES['MIN_MONITORS_PER_EVENT']:
            errors.append(f"Mínimo de {cls.VALIDATION_RULES['MIN_MONITORS_PER_EVENT']} monitor(es)")
        
        if monitores > cls.VALIDATION_RULES['MAX_MONITORS_PER_EVENT']:
            errors.append(f"Máximo de {cls.VALIDATION_RULES['MAX_MONITORS_PER_EVENT']} monitores")
        
        # Validar sala
        sala = data.get('sala', '')
        if len(sala) > cls.VALIDATION_RULES['MAX_ROOM_NAME_LENGTH']:
            errors.append(f"Nome da sala muito longo (máx. {cls.VALIDATION_RULES['MAX_ROOM_NAME_LENGTH']} chars)")
        
        # Validar reporter
        reporter = data.get('reporter', '')
        if len(reporter) > cls.VALIDATION_RULES['MAX_REPORTER_NAME_LENGTH']:
            errors.append(f"Nome do reporter muito longo (máx. {cls.VALIDATION_RULES['MAX_REPORTER_NAME_LENGTH']} chars)")
        
        # Validar key
        key = data.get('key', '')
        if len(key) > cls.VALIDATION_RULES['MAX_KEY_LENGTH']:
            errors.append(f"Key muito longa (máx. {cls.VALIDATION_RULES['MAX_KEY_LENGTH']} chars)")
        
        # Validar observações
        observacoes = data.get('observacoes', '')
        if len(observacoes) > cls.VALIDATION_RULES['MAX_OBSERVATIONS_LENGTH']:
            errors.append(f"Observações muito longas (máx. {cls.VALIDATION_RULES['MAX_OBSERVATIONS_LENGTH']} chars)")
        
        return errors
    
    @classmethod
    def get_room_type(cls, room_name):
        """Determina tipo da sala baseado no nome"""
        room_lower = room_name.lower()
        
        if 'auditório' in room_lower or 'auditorio' in room_lower:
            return 'Auditório'
        elif 'treinamento' in room_lower:
            return 'Sala de treinamento'
        elif any(size in room_lower for size in ['grande', 'principal']):
            return 'Sala grande'
        elif any(size in room_lower for size in ['pequena', 'pequeno']):
            return 'Sala pequena'
        else:
            return 'Sala média'
    
    @classmethod
    def get_monitor_recommendation(cls, room_name, requested_monitors):
        """Retorna recomendação de monitores para uma sala"""
        room_type = cls.get_room_type(room_name)
        limits = cls.MONITOR_LIMITS.get(room_type, cls.MONITOR_LIMITS['Sala média'])
        
        if requested_monitors < limits['min']:
            return {
                'status': 'below_minimum',
                'message': f"Recomendado mínimo {limits['min']} monitores para {room_type}",
                'recommended': limits['optimal']
            }
        elif requested_monitors > limits['max']:
            return {
                'status': 'above_maximum', 
                'message': f"Máximo recomendado {limits['max']} monitores para {room_type}",
                'recommended': limits['optimal']
            }
        elif requested_monitors == limits['optimal']:
            return {
                'status': 'optimal',
                'message': f"Quantidade ideal para {room_type}",
                'recommended': limits['optimal']
            }
        else:
            return {
                'status': 'acceptable',
                'message': f"Quantidade aceitável para {room_type}",
                'recommended': limits['optimal']
            }

# Instância global
monitor_config = MonitorConfig()
