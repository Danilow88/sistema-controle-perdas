/**
 * Google Apps Script para Sistema de Monitoramento de Monitores
 * Baseado no monitor_dashboard_fixed.html
 * Integração com planilha de eventos de monitores
 */

// Configurações da planilha
const SPREADSHEET_ID = '1hI6WWiH03AvXFxMCpPpYtIhQEU062C_k4utIE6YyctY';
const SHEET_NAME = 'Calendário de eventos - Monitores';

/**
 * Função principal para carregar dados dos monitores
 * @return {Object} Dados processados dos monitores
 */
function loadMonitorData() {
  try {
    console.log('🔄 Iniciando carregamento dos dados de monitores...');
    
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      throw new Error(`Aba "${SHEET_NAME}" não encontrada na planilha`);
    }
    
    // Obter dados da planilha
    const data = sheet.getDataRange().getValues();
    
    if (data.length <= 1) {
      throw new Error('Nenhum dado encontrado na planilha');
    }
    
    const header = data[0];
    const rows = data.slice(1);
    
    console.log('📋 Header encontrado:', header);
    console.log('📋 Total de linhas:', rows.length);
    
    // Processar dados
    const processedData = processMonitorData(rows);
    
    // Calcular resumo
    const summary = calculateSummary(processedData);
    
    // Gerar alertas
    const alerts = generateAlerts(processedData);
    
    const result = {
      success: true,
      data: processedData,
      summary: summary,
      alerts: alerts,
      timestamp: new Date().toISOString(),
      totalRecords: processedData.length
    };
    
    console.log('✅ Dados carregados com sucesso:', result.totalRecords, 'registros');
    return result;
    
  } catch (error) {
    console.error('❌ Erro ao carregar dados:', error);
    return {
      success: false,
      error: error.toString(),
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Processa dados brutos da planilha
 * @param {Array} rows - Linhas da planilha
 * @return {Array} Dados processados
 */
function processMonitorData(rows) {
  const processedData = [];
  const uniqueKeys = new Set();
  
  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    
    try {
      // Mapear colunas conforme estrutura da planilha
      const item = {
        dataSolicitacao: formatDate(row[0]) || '',
        dataMontagem: formatDate(row[1]) || '',
        sala: (row[2] || '').toString().trim(),
        monitores: parseInt(row[3]) || 0,
        dataDesmontagem: formatDate(row[4]) || '',
        observacoes: (row[5] || '').toString().trim(),
        reporter: (row[6] || '').toString().trim(),
        key: (row[7] || '').toString().trim(),
        status: (row[8] || 'Pendente').toString().trim(),
        statusAtendimento: (row[9] || 'Não Iniciado').toString().trim(),
        rowIndex: i + 2 // +2 porque começamos na linha 2 (header + índice 0-based)
      };
      
      // Validar dados essenciais
      if (!item.key) {
        console.warn(`Linha ${i + 2}: Key vazia, pulando registro`);
        continue;
      }
      
      // Evitar duplicatas por key
      if (uniqueKeys.has(item.key)) {
        console.warn(`Linha ${i + 2}: Key duplicada "${item.key}", pulando registro`);
        continue;
      }
      
      uniqueKeys.add(item.key);
      processedData.push(item);
      
    } catch (error) {
      console.error(`Erro ao processar linha ${i + 2}:`, error);
      continue;
    }
  }
  
  return processedData;
}

/**
 * Formata data para exibição
 * @param {*} dateValue - Valor da data
 * @return {string} Data formatada
 */
function formatDate(dateValue) {
  if (!dateValue) return '';
  
  try {
    let date;
    
    if (dateValue instanceof Date) {
      date = dateValue;
    } else if (typeof dateValue === 'string') {
      // Tentar parsear string de data
      date = new Date(dateValue);
      if (isNaN(date.getTime())) {
        return dateValue; // Retornar string original se não conseguir parsear
      }
    } else {
      return dateValue.toString();
    }
    
    // Formatar como DD/MM/YYYY
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    
    return `${day}/${month}/${year}`;
    
  } catch (error) {
    console.error('Erro ao formatar data:', dateValue, error);
    return dateValue ? dateValue.toString() : '';
  }
}

/**
 * Calcula resumo dos dados
 * @param {Array} data - Dados processados
 * @return {Object} Resumo calculado
 */
function calculateSummary(data) {
  const summary = {
    totalMonitores: 0,
    dentroLimite: 0,
    excedente: 0,
    totalEventos: data.length,
    statusDistribution: {},
    atendimentoDistribution: {}
  };
  
  data.forEach(item => {
    // Total de monitores
    summary.totalMonitores += item.monitores;
    
    // Monitores dentro do limite (Confirmado ou Concluído)
    if (item.status === 'Confirmado' || item.status === 'Concluído') {
      summary.dentroLimite += item.monitores;
    }
    
    // Monitores excedentes
    if (item.status === 'Excedente') {
      summary.excedente += item.monitores;
    }
    
    // Distribuição por status
    const status = item.status || 'Pendente';
    summary.statusDistribution[status] = (summary.statusDistribution[status] || 0) + 1;
    
    // Distribuição por status de atendimento
    const atendimento = item.statusAtendimento || 'Não Iniciado';
    summary.atendimentoDistribution[atendimento] = (summary.atendimentoDistribution[atendimento] || 0) + 1;
  });
  
  return summary;
}

/**
 * Gera alertas baseados nos dados
 * @param {Array} data - Dados processados
 * @return {Array} Lista de alertas
 */
function generateAlerts(data) {
  const alerts = [];
  
  // Contar eventos por tipo
  const eventosPendentes = data.filter(item => item.status === 'Pendente').length;
  const eventosExcedentes = data.filter(item => item.status === 'Excedente').length;
  const eventosSemReporter = data.filter(item => !item.reporter || item.reporter.trim() === '').length;
  const eventosVencidos = data.filter(item => isEventExpired(item)).length;
  
  // Alerta para eventos pendentes
  if (eventosPendentes > 0) {
    alerts.push({
      type: 'warning',
      title: 'Eventos Pendentes',
      message: `Existem ${eventosPendentes} eventos com status "Pendente".`,
      count: eventosPendentes,
      action: 'review_pending'
    });
  }
  
  // Alerta para eventos excedentes
  if (eventosExcedentes > 0) {
    alerts.push({
      type: 'danger',
      title: 'Eventos Excedentes',
      message: `Existem ${eventosExcedentes} eventos com status "Excedente".`,
      count: eventosExcedentes,
      action: 'review_exceeded'
    });
  }
  
  // Alerta para eventos sem reporter
  if (eventosSemReporter > 0) {
    alerts.push({
      type: 'info',
      title: 'Eventos sem Reporter',
      message: `Existem ${eventosSemReporter} eventos sem reporter definido.`,
      count: eventosSemReporter,
      action: 'assign_reporter'
    });
  }
  
  // Alerta para eventos vencidos
  if (eventosVencidos > 0) {
    alerts.push({
      type: 'danger',
      title: 'Eventos Vencidos',
      message: `Existem ${eventosVencidos} eventos com data de montagem vencida.`,
      count: eventosVencidos,
      action: 'review_expired'
    });
  }
  
  return alerts;
}

/**
 * Verifica se um evento está vencido
 * @param {Object} item - Item do evento
 * @return {boolean} True se vencido
 */
function isEventExpired(item) {
  if (!item.dataMontagem) return false;
  
  try {
    const today = new Date();
    const montagemDate = new Date(item.dataMontagem);
    
    // Considerar vencido se a data de montagem já passou e status não é Concluído
    return montagemDate < today && item.status !== 'Concluído';
    
  } catch (error) {
    return false;
  }
}

/**
 * Atualiza status de atendimento de um evento
 * @param {string} key - Chave do evento
 * @param {string} newStatus - Novo status
 * @return {Object} Resultado da operação
 */
function updateEventStatus(key, newStatus) {
  try {
    console.log(`🔄 Atualizando status do evento ${key} para: ${newStatus}`);
    
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      throw new Error(`Aba "${SHEET_NAME}" não encontrada`);
    }
    
    // Encontrar linha pela key
    const data = sheet.getDataRange().getValues();
    const keyColumn = 7; // Coluna H (índice 7)
    const statusColumn = 9; // Coluna J (índice 9) - Status de Atendimento
    
    for (let i = 1; i < data.length; i++) { // Começar da linha 2 (índice 1)
      if (data[i][keyColumn] === key) {
        // Atualizar status de atendimento
        sheet.getRange(i + 1, statusColumn + 1).setValue(newStatus);
        
        console.log(`✅ Status atualizado com sucesso para evento ${key}`);
        
        return {
          success: true,
          message: `Status do evento ${key} atualizado para: ${newStatus}`,
          key: key,
          newStatus: newStatus,
          timestamp: new Date().toISOString()
        };
      }
    }
    
    throw new Error(`Evento com key "${key}" não encontrado`);
    
  } catch (error) {
    console.error('❌ Erro ao atualizar status:', error);
    return {
      success: false,
      error: error.toString(),
      key: key,
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Marca evento como concluído
 * @param {string} key - Chave do evento
 * @return {Object} Resultado da operação
 */
function markEventAsCompleted(key) {
  try {
    console.log(`🏁 Marcando evento ${key} como concluído`);
    
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      throw new Error(`Aba "${SHEET_NAME}" não encontrada`);
    }
    
    // Encontrar linha pela key
    const data = sheet.getDataRange().getValues();
    const keyColumn = 7; // Coluna H (índice 7)
    const statusColumn = 8; // Coluna I (índice 8) - Status
    const statusAtendimentoColumn = 9; // Coluna J (índice 9) - Status de Atendimento
    
    for (let i = 1; i < data.length; i++) {
      if (data[i][keyColumn] === key) {
        // Atualizar tanto status quanto status de atendimento
        sheet.getRange(i + 1, statusColumn + 1).setValue('Concluído');
        sheet.getRange(i + 1, statusAtendimentoColumn + 1).setValue('Concluído');
        
        console.log(`✅ Evento ${key} marcado como concluído`);
        
        return {
          success: true,
          message: `Evento ${key} marcado como concluído`,
          key: key,
          timestamp: new Date().toISOString()
        };
      }
    }
    
    throw new Error(`Evento com key "${key}" não encontrado`);
    
  } catch (error) {
    console.error('❌ Erro ao marcar como concluído:', error);
    return {
      success: false,
      error: error.toString(),
      key: key,
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Exporta dados para CSV
 * @return {Object} Dados para download
 */
function exportToCSV() {
  try {
    const result = loadMonitorData();
    
    if (!result.success) {
      throw new Error(result.error);
    }
    
    const data = result.data;
    
    // Cabeçalho CSV
    const headers = [
      'Data Solicitação',
      'Data Montagem',
      'Monitores',
      'Sala',
      'Reporter',
      'Key',
      'Status',
      'Status de Atendimento',
      'Observações'
    ];
    
    // Dados CSV
    const csvRows = [headers.join(',')];
    
    data.forEach(item => {
      const row = [
        item.dataSolicitacao || '',
        item.dataMontagem || '',
        item.monitores || 0,
        `"${(item.sala || '').replace(/"/g, '""')}"`, // Escapar aspas
        `"${(item.reporter || '').replace(/"/g, '""')}"`,
        item.key || '',
        item.status || '',
        item.statusAtendimento || '',
        `"${(item.observacoes || '').replace(/"/g, '""')}"`
      ];
      csvRows.push(row.join(','));
    });
    
    const csvContent = csvRows.join('\n');
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    const filename = `monitores_export_${timestamp}.csv`;
    
    return {
      success: true,
      filename: filename,
      content: csvContent,
      mimeType: 'text/csv',
      size: csvContent.length
    };
    
  } catch (error) {
    console.error('❌ Erro ao exportar CSV:', error);
    return {
      success: false,
      error: error.toString()
    };
  }
}

/**
 * Gera relatório detalhado
 * @return {Object} Relatório completo
 */
function generateDetailedReport() {
  try {
    const result = loadMonitorData();
    
    if (!result.success) {
      throw new Error(result.error);
    }
    
    const data = result.data;
    const summary = result.summary;
    
    // Análise por sala
    const salaAnalysis = {};
    data.forEach(item => {
      const sala = item.sala || 'Não informado';
      if (!salaAnalysis[sala]) {
        salaAnalysis[sala] = {
          eventos: 0,
          monitores: 0,
          status: {}
        };
      }
      
      salaAnalysis[sala].eventos++;
      salaAnalysis[sala].monitores += item.monitores;
      
      const status = item.status || 'Pendente';
      salaAnalysis[sala].status[status] = (salaAnalysis[sala].status[status] || 0) + 1;
    });
    
    // Análise por reporter
    const reporterAnalysis = {};
    data.forEach(item => {
      const reporter = item.reporter || 'Não informado';
      if (!reporterAnalysis[reporter]) {
        reporterAnalysis[reporter] = {
          eventos: 0,
          monitores: 0
        };
      }
      
      reporterAnalysis[reporter].eventos++;
      reporterAnalysis[reporter].monitores += item.monitores;
    });
    
    // Análise temporal (eventos por mês)
    const monthlyAnalysis = {};
    data.forEach(item => {
      if (item.dataMontagem) {
        try {
          const date = new Date(item.dataMontagem);
          const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
          
          if (!monthlyAnalysis[monthKey]) {
            monthlyAnalysis[monthKey] = {
              eventos: 0,
              monitores: 0
            };
          }
          
          monthlyAnalysis[monthKey].eventos++;
          monthlyAnalysis[monthKey].monitores += item.monitores;
        } catch (error) {
          // Ignorar datas inválidas
        }
      }
    });
    
    const report = {
      success: true,
      timestamp: new Date().toISOString(),
      summary: summary,
      analysis: {
        porSala: salaAnalysis,
        porReporter: reporterAnalysis,
        temporal: monthlyAnalysis
      },
      recommendations: generateRecommendations(data, summary)
    };
    
    return report;
    
  } catch (error) {
    console.error('❌ Erro ao gerar relatório:', error);
    return {
      success: false,
      error: error.toString()
    };
  }
}

/**
 * Gera recomendações baseadas nos dados
 * @param {Array} data - Dados dos eventos
 * @param {Object} summary - Resumo dos dados
 * @return {Array} Lista de recomendações
 */
function generateRecommendations(data, summary) {
  const recommendations = [];
  
  // Recomendação para eventos pendentes
  if (summary.statusDistribution['Pendente'] > 0) {
    recommendations.push({
      type: 'action',
      priority: 'high',
      title: 'Revisar Eventos Pendentes',
      description: `Existem ${summary.statusDistribution['Pendente']} eventos pendentes que precisam de atenção.`,
      action: 'review_pending_events'
    });
  }
  
  // Recomendação para otimização de recursos
  if (summary.excedente > summary.totalMonitores * 0.2) {
    recommendations.push({
      type: 'optimization',
      priority: 'medium',
      title: 'Otimizar Uso de Monitores',
      description: 'Alto número de monitores em status excedente. Considere redistribuir recursos.',
      action: 'optimize_monitor_allocation'
    });
  }
  
  // Recomendação para eventos sem reporter
  const semReporter = data.filter(item => !item.reporter || item.reporter.trim() === '').length;
  if (semReporter > 0) {
    recommendations.push({
      type: 'process',
      priority: 'medium',
      title: 'Atribuir Responsáveis',
      description: `${semReporter} eventos não possuem reporter definido.`,
      action: 'assign_reporters'
    });
  }
  
  return recommendations;
}

/**
 * Função de teste para validar o sistema
 */
function testMonitorSystem() {
  console.log('🧪 Iniciando testes do sistema de monitores...');
  
  try {
    // Teste 1: Carregar dados
    console.log('Teste 1: Carregando dados...');
    const loadResult = loadMonitorData();
    console.log('Resultado do carregamento:', loadResult.success ? '✅ Sucesso' : '❌ Falha');
    
    if (loadResult.success) {
      console.log(`📊 ${loadResult.totalRecords} registros carregados`);
      console.log(`🚨 ${loadResult.alerts.length} alertas gerados`);
    }
    
    // Teste 2: Gerar relatório
    console.log('Teste 2: Gerando relatório...');
    const reportResult = generateDetailedReport();
    console.log('Resultado do relatório:', reportResult.success ? '✅ Sucesso' : '❌ Falha');
    
    // Teste 3: Export CSV
    console.log('Teste 3: Exportando CSV...');
    const exportResult = exportToCSV();
    console.log('Resultado do export:', exportResult.success ? '✅ Sucesso' : '❌ Falha');
    
    console.log('🎉 Testes concluídos!');
    
  } catch (error) {
    console.error('❌ Erro durante os testes:', error);
  }
}

/**
 * Função para configurar triggers automáticos
 */
function setupTriggers() {
  // Remover triggers existentes
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'autoUpdateMonitorData') {
      ScriptApp.deleteTrigger(trigger);
    }
  });
  
  // Criar trigger para atualização automática a cada hora
  ScriptApp.newTimeTrigger('autoUpdateMonitorData')
    .everyHours(1)
    .create();
  
  console.log('✅ Triggers configurados com sucesso');
}

/**
 * Função executada automaticamente para atualizar dados
 */
function autoUpdateMonitorData() {
  console.log('🔄 Atualização automática iniciada...');
  
  try {
    const result = loadMonitorData();
    
    if (result.success) {
      console.log(`✅ Dados atualizados automaticamente: ${result.totalRecords} registros`);
      
      // Se houver alertas críticos, pode enviar email
      const criticalAlerts = result.alerts.filter(alert => alert.type === 'danger');
      if (criticalAlerts.length > 0) {
        console.log(`🚨 ${criticalAlerts.length} alertas críticos encontrados`);
        // Aqui você pode implementar envio de email se necessário
      }
    } else {
      console.error('❌ Falha na atualização automática:', result.error);
    }
    
  } catch (error) {
    console.error('❌ Erro na atualização automática:', error);
  }
}
