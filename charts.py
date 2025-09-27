"""
Utilitários para geração de gráficos com Plotly
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ChartGenerator:
    """Gerador de gráficos com Plotly"""
    
    # Cores do tema Nubank
    NUBANK_COLORS = {
        'primary': '#8A05BE',
        'secondary': '#4500A0',
        'success': '#2B8A3E',
        'warning': '#E67700',
        'danger': '#C92A2A',
        'info': '#1971C2',
        'light': '#F8F9FA',
        'dark': '#343A40'
    }
    
    COLOR_PALETTE = [
        '#8A05BE', '#4500A0', '#2B8A3E', '#E67700', '#C92A2A',
        '#1971C2', '#7048E8', '#FD7E14', '#20C997', '#6F42C1'
    ]
    
    @classmethod
    def create_line_chart(cls, data: Dict[str, Any], title: str, x_label: str = '', y_label: str = '') -> go.Figure:
        """Cria gráfico de linha"""
        try:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=data.get('labels', []),
                y=data.get('values', []),
                mode='lines+markers',
                line=dict(color=cls.NUBANK_COLORS['primary'], width=3),
                marker=dict(size=8, color=cls.NUBANK_COLORS['primary']),
                name=title
            ))
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=20, color=cls.NUBANK_COLORS['dark'])
                ),
                xaxis_title=x_label,
                yaxis_title=y_label,
                template='plotly_white',
                hovermode='x unified',
                showlegend=False
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de linha: {e}")
            return go.Figure()
    
    @classmethod
    def create_bar_chart(cls, data: Dict[str, Any], title: str, x_label: str = '', y_label: str = '') -> go.Figure:
        """Cria gráfico de barras"""
        try:
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=data.get('labels', []),
                y=data.get('values', []),
                marker_color=cls.COLOR_PALETTE[:len(data.get('labels', []))],
                name=title
            ))
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=20, color=cls.NUBANK_COLORS['dark'])
                ),
                xaxis_title=x_label,
                yaxis_title=y_label,
                template='plotly_white',
                showlegend=False
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de barras: {e}")
            return go.Figure()
    
    @classmethod
    def create_pie_chart(cls, data: Dict[str, Any], title: str) -> go.Figure:
        """Cria gráfico de pizza"""
        try:
            fig = go.Figure()
            
            fig.add_trace(go.Pie(
                labels=data.get('labels', []),
                values=data.get('values', []),
                hole=0.3,
                marker=dict(colors=cls.COLOR_PALETTE[:len(data.get('labels', []))]),
                textinfo='label+percent',
                textposition='outside'
            ))
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=20, color=cls.NUBANK_COLORS['dark'])
                ),
                template='plotly_white',
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.01
                )
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de pizza: {e}")
            return go.Figure()
    
    @classmethod
    def create_multi_period_chart(cls, data: Dict[str, Any], title: str) -> go.Figure:
        """Cria gráfico com múltiplos períodos"""
        try:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Mensal', 'Trimestral', 'Anual', 'Por Prédio'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"type": "pie"}]]
            )
            
            # Gráfico mensal
            if 'monthly' in data and data['monthly']['labels']:
                fig.add_trace(
                    go.Scatter(
                        x=data['monthly']['labels'],
                        y=data['monthly']['values'],
                        mode='lines+markers',
                        name='Mensal',
                        line=dict(color=cls.NUBANK_COLORS['primary'])
                    ),
                    row=1, col=1
                )
            
            # Gráfico trimestral
            if 'quarterly' in data and data['quarterly']['labels']:
                fig.add_trace(
                    go.Bar(
                        x=data['quarterly']['labels'],
                        y=data['quarterly']['values'],
                        name='Trimestral',
                        marker_color=cls.NUBANK_COLORS['secondary']
                    ),
                    row=1, col=2
                )
            
            # Gráfico anual
            if 'yearly' in data and data['yearly']['labels']:
                fig.add_trace(
                    go.Bar(
                        x=data['yearly']['labels'],
                        y=data['yearly']['values'],
                        name='Anual',
                        marker_color=cls.NUBANK_COLORS['success']
                    ),
                    row=2, col=1
                )
            
            # Gráfico por prédio (pizza)
            if 'byBuilding' in data and data['byBuilding']['labels']:
                fig.add_trace(
                    go.Pie(
                        labels=data['byBuilding']['labels'],
                        values=data['byBuilding']['values'],
                        name='Por Prédio',
                        marker=dict(colors=cls.COLOR_PALETTE[:len(data['byBuilding']['labels'])])
                    ),
                    row=2, col=2
                )
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=24, color=cls.NUBANK_COLORS['dark'])
                ),
                template='plotly_white',
                showlegend=False,
                height=800
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico multi-período: {e}")
            return go.Figure()
    
    @classmethod
    def create_comparison_chart(cls, data1: Dict[str, Any], data2: Dict[str, Any], 
                               title: str, label1: str, label2: str) -> go.Figure:
        """Cria gráfico de comparação"""
        try:
            fig = go.Figure()
            
            # Primeira série
            fig.add_trace(go.Bar(
                name=label1,
                x=data1.get('labels', []),
                y=data1.get('values', []),
                marker_color=cls.NUBANK_COLORS['primary']
            ))
            
            # Segunda série
            fig.add_trace(go.Bar(
                name=label2,
                x=data2.get('labels', []),
                y=data2.get('values', []),
                marker_color=cls.NUBANK_COLORS['secondary']
            ))
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=20, color=cls.NUBANK_COLORS['dark'])
                ),
                barmode='group',
                template='plotly_white',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de comparação: {e}")
            return go.Figure()
    
    @classmethod
    def create_gauge_chart(cls, value: float, max_value: float, title: str, 
                          threshold_good: float = None, threshold_warning: float = None) -> go.Figure:
        """Cria gráfico de gauge (velocímetro)"""
        try:
            # Definir cores baseadas nos thresholds
            if threshold_good and threshold_warning:
                if value <= threshold_good:
                    color = cls.NUBANK_COLORS['success']
                elif value <= threshold_warning:
                    color = cls.NUBANK_COLORS['warning']
                else:
                    color = cls.NUBANK_COLORS['danger']
            else:
                color = cls.NUBANK_COLORS['primary']
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = value,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': title, 'font': {'size': 20}},
                delta = {'reference': max_value * 0.8},
                gauge = {
                    'axis': {'range': [None, max_value]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, max_value * 0.5], 'color': "lightgray"},
                        {'range': [max_value * 0.5, max_value * 0.8], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': max_value * 0.9
                    }
                }
            ))
            
            fig.update_layout(
                template='plotly_white',
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico gauge: {e}")
            return go.Figure()
    
    @classmethod
    def create_heatmap(cls, data: pd.DataFrame, x_col: str, y_col: str, 
                      value_col: str, title: str) -> go.Figure:
        """Cria mapa de calor"""
        try:
            # Criar pivot table
            pivot_data = data.pivot_table(
                values=value_col,
                index=y_col,
                columns=x_col,
                aggfunc='sum',
                fill_value=0
            )
            
            fig = go.Figure(data=go.Heatmap(
                z=pivot_data.values,
                x=pivot_data.columns,
                y=pivot_data.index,
                colorscale='Viridis',
                hoverongaps=False
            ))
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=20, color=cls.NUBANK_COLORS['dark'])
                ),
                template='plotly_white'
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar heatmap: {e}")
            return go.Figure()
    
    @classmethod
    def create_timeline_chart(cls, data: List[Dict[str, Any]], title: str) -> go.Figure:
        """Cria gráfico de timeline"""
        try:
            fig = go.Figure()
            
            for i, item in enumerate(data):
                fig.add_trace(go.Scatter(
                    x=[item.get('start_date'), item.get('end_date')],
                    y=[i, i],
                    mode='lines+markers',
                    name=item.get('name', f'Item {i}'),
                    line=dict(width=8, color=cls.COLOR_PALETTE[i % len(cls.COLOR_PALETTE)]),
                    marker=dict(size=10)
                ))
            
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=20, color=cls.NUBANK_COLORS['dark'])
                ),
                template='plotly_white',
                showlegend=True,
                yaxis=dict(
                    tickmode='array',
                    tickvals=list(range(len(data))),
                    ticktext=[item.get('name', f'Item {i}') for i, item in enumerate(data)]
                )
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico timeline: {e}")
            return go.Figure()
    
    @classmethod
    def create_empty_chart(cls, message: str = "Nenhum dado disponível") -> go.Figure:
        """Cria gráfico vazio com mensagem"""
        fig = go.Figure()
        
        fig.add_annotation(
            text=message,
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color=cls.NUBANK_COLORS['dark'])
        )
        
        fig.update_layout(
            template='plotly_white',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=400
        )
        
        return fig
