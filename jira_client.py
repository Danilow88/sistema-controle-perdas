"""
Cliente para integração com JIRA API
"""
import requests
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

from config.settings import settings

logger = logging.getLogger(__name__)

class JiraClient:
    """Cliente para interação com JIRA"""
    
    def __init__(self):
        self.base_url = settings.JIRA_BASE_URL
        self.email = settings.JIRA_EMAIL
        self.api_token = settings.JIRA_API_TOKEN
        self.project_key = settings.JIRA_PROJECT_KEY
        self.field_mapping = settings.JIRA_FIELD_MAPPING
        
        # Configurar autenticação
        auth_string = f"{self.email}:{self.api_token}"
        auth_bytes = auth_string.encode('ascii')
        self.auth_header = base64.b64encode(auth_bytes).decode('ascii')
        
        self.headers = {
            'Authorization': f'Basic {self.auth_header}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self) -> bool:
        """Testa a conexão com o JIRA"""
        try:
            url = f"{self.base_url}/rest/api/3/myself"
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                user_data = response.json()
                logger.info(f"Conexão bem-sucedida. Usuário: {user_data.get('displayName', 'N/A')}")
                return True
            else:
                logger.error(f"Falha na autenticação. Status: {response.status_code}")
                logger.error(f"Resposta: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao testar conexão com JIRA: {e}")
            return False
    
    def fetch_monitor_issues(self) -> List[Dict[str, Any]]:
        """Busca issues relacionadas a monitores"""
        try:
            logger.info("Iniciando busca de issues de monitores no JIRA")
            
            if not self.test_connection():
                raise Exception("Falha na autenticação com o JIRA")
            
            # JQL específica para Installation/Uninstallation Monitors
            jql = (
                '"Request Type" = "Installation/Uninstallation Monitors" '
                'AND priority = Medium '
                'AND "Support Level - ITOPS" = L3 '
                'AND status NOT IN ("Canceled", "Encerrado", "Done", "Resolved") '
                'ORDER BY created DESC'
            )
            
            # Campos para solicitar
            fields = [
                "issuetype", "reporter", "updated", "created", "status", 
                "summary", "priority", "assignee", "description"
            ]
            
            # Adicionar campos personalizados
            for field_id in self.field_mapping.values():
                if field_id and field_id not in fields:
                    fields.append(field_id)
            
            # Fazer requisição
            url = f"{self.base_url}/rest/api/3/search/jql"
            payload = {
                "jql": jql,
                "maxResults": 100,
                "fields": fields
            }
            
            logger.info(f"Fazendo requisição para: {url}")
            logger.info(f"JQL: {jql}")
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=60)
            
            if response.status_code != 200:
                # Tentar com payload simplificado
                logger.warning("Tentando com payload simplificado...")
                simple_payload = {"jql": jql}
                response = requests.post(url, json=simple_payload, headers=self.headers, timeout=60)
                
                if response.status_code != 200:
                    raise Exception(f"JIRA API error: {response.status_code} - {response.text}")
            
            data = response.json()
            issues = data.get('issues', [])
            
            logger.info(f"{data.get('total', 0)} issues encontradas no total")
            logger.info(f"Processando {len(issues)} issues retornadas...")
            
            return self._process_jira_issues(issues)
            
        except Exception as e:
            logger.error(f"Erro ao buscar dados do JIRA: {e}")
            raise
    
    def _process_jira_issues(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processa issues do JIRA para formato da aplicação"""
        processed_data = []
        
        if not issues:
            logger.info("Nenhum issue para processar")
            return processed_data
        
        logger.info(f"Processando {len(issues)} issues de monitores...")
        
        for index, issue in enumerate(issues):
            try:
                fields = issue.get('fields', {})
                
                # Obter valores dos campos personalizados
                custom_fields = {}
                for field_name, field_id in self.field_mapping.items():
                    custom_fields[field_name] = self._get_field_value(fields, field_id)
                
                processed_item = {
                    'issueType': fields.get('issuetype', {}).get('name', ''),
                    'reporter': fields.get('reporter', {}).get('displayName', ''),
                    'updated': self._format_date_for_sheet(fields.get('updated')),
                    'requestType': custom_fields.get('Request Type', ''),
                    'dateActivity': self._format_date_for_sheet(custom_fields.get('TC - Date of activity')),
                    'windowEnd': self._format_date_for_sheet(custom_fields.get('TC - Maintenance window End')),
                    'windowStart': self._format_date_for_sheet(custom_fields.get('TC - Maintenance window Start')),
                    'reason': custom_fields.get('TC - Reason for request monitor', ''),
                    'reinstallationDate': self._format_date_for_sheet(custom_fields.get('TC - Reinstallation date')),
                    'spaceArea': custom_fields.get('TC - Space/Area monitores', ''),
                    'installationType': custom_fields.get('TC - Type of Installation/Uninstallation', ''),
                    'monitorRequestType': custom_fields.get('TC - Type of Request Monitors', ''),
                    'floor': custom_fields.get('Floor - ITOPS', ''),
                    'monitorPositions': custom_fields.get('Number of monitor positions', 0),
                    'created': self._format_date_for_sheet(fields.get('created')),
                    'key': issue.get('key', ''),
                    'status': fields.get('status', {}).get('name', 'Pending'),
                    'summary': fields.get('summary', ''),
                    'priority': fields.get('priority', {}).get('name', 'Medium'),
                    'assignee': fields.get('assignee', {}).get('displayName', 'Não atribuído'),
                    'description': fields.get('description', 'Sem descrição'),
                    'url': f"{self.base_url}/browse/{issue.get('key', '')}",
                    'officeLocation': custom_fields.get('TC - Office Location', '')
                }
                
                processed_data.append(processed_item)
                
                # Log detalhado para cada issue
                logger.info(f"{index + 1}. {processed_item['key']} - {processed_item['summary']}")
                logger.info(f"   Status: {processed_item['status']} | Assignee: {processed_item['assignee']}")
                
            except Exception as error:
                logger.error(f"Erro ao processar issue {issue.get('key', 'unknown')}: {error}")
        
        # Log do resumo
        logger.info("=== RESUMO ===")
        logger.info(f"Total de issues processadas: {len(processed_data)}")
        
        # Agrupar por status
        status_count = {}
        for item in processed_data:
            status = item['status']
            status_count[status] = status_count.get(status, 0) + 1
        
        logger.info("Distribuição por status:")
        for status, count in status_count.items():
            logger.info(f"  {status}: {count}")
        
        return processed_data
    
    def _get_field_value(self, fields: Dict[str, Any], field_id: str) -> Any:
        """Obtém valor de um campo, tratando diferentes tipos"""
        if not field_id or field_id not in fields:
            return ''
        
        field_value = fields[field_id]
        
        if field_value is None:
            return ''
        
        if isinstance(field_value, dict):
            # Diferentes tipos de campos podem ter estruturas diferentes
            if 'value' in field_value:
                return field_value['value']
            elif 'name' in field_value:
                return field_value['name']
            elif 'displayName' in field_value:
                return field_value['displayName']
            else:
                return str(field_value)
        
        return field_value
    
    def _format_date_for_sheet(self, date_string: Optional[str]) -> str:
        """Formata data para a planilha"""
        if not date_string:
            return ''
        
        try:
            date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return date.strftime("%d/%m/%Y %H:%M")
        except Exception:
            return str(date_string)
    
    def update_issue_status(self, issue_key: str, new_status: str) -> bool:
        """Atualiza o status de um issue (se necessário)"""
        try:
            # Esta funcionalidade pode ser implementada se necessário
            logger.info(f"Solicitação para atualizar {issue_key} para status {new_status}")
            # Por enquanto, apenas log
            return True
        except Exception as e:
            logger.error(f"Erro ao atualizar status do issue: {e}")
            return False

# Instância global do cliente
jira_client = JiraClient()
