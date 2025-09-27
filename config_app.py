"""
Configurações da aplicação
"""
import os

class AppConfig:
    """Configurações centralizadas"""
    
    # Google Sheets
    SPREADSHEET_ID = '1IMcXLIyOJOANhfxKfzYlwtBqtsXJfRMhCPmoKQdCtdY'
    INVENTORY_SHEET_NAME = 'Inventory'
    MONITORS_SHEET_NAME = 'agenda ts'
    
    # Dados do sistema
    ITEMS_BY_BUILDING = {
        'Spark': [
            'Headset-spk', 'Adaptadores usb c-spk', 'Mouse-spk', 'Teclado k120-spk',
            'Usb Gorila 5m1 lanspk', 'Usb Gorila 6m1 spk'
        ],
        'HQ1': [
            'Headset-hq1', 'Adaptadores usb c-hq1', 'Mouse-hq1', 'Teclado k120-hq1',
            'Usb Gorila 5m1 lan hq1', 'Usb Gorila 6m1 hq1'
        ],
        'HQ2': [
            'Headset-hq2', 'Adaptadores usb c-hq2', 'Mouse-hq2', 'Teclado k120-hq2',
            'Usb Gorila 5m1 lan hq2', 'Usb Gorila 6m1 hq2'
        ]
    }
    
    ITEM_NAMES = {
        'Headset-spk': 'Headset - Spark',
        'Adaptadores usb c-spk': 'Adaptador USB-C - Spark',
        'Mouse-spk': 'Mouse - Spark',
        'Teclado k120-spk': 'Teclado K120 - Spark',
        'Headset-hq1': 'Headset - HQ1',
        'Adaptadores usb c-hq1': 'Adaptador USB-C - HQ1',
        'Mouse-hq1': 'Mouse - HQ1',
        'Teclado k120-hq1': 'Teclado K120 - HQ1',
        'Headset-hq2': 'Headset - HQ2',
        'Adaptadores usb c-hq2': 'Adaptador USB-C - HQ2',
        'Mouse-hq2': 'Mouse - HQ2',
        'Teclado k120-hq2': 'Teclado K120 - HQ2',
        'Usb Gorila 5m1 lan hq1': 'USB Gorila 5-em-1 - HQ1',
        'Usb Gorila 5m1 lan hq2': 'USB Gorila 5-em-1 - HQ2',
        'Usb Gorila 5m1 lanspk': 'USB Gorila 5-em-1 - Spark',
        'Usb Gorila 6m1 hq1': 'USB Gorila 6-em-1 - HQ1',
        'Usb Gorila 6m1 hq2': 'USB Gorila 6-em-1 - HQ2',
        'Usb Gorila 6m1 spk': 'USB Gorila 6-em-1 - Spark'
    }
    
    BUILDING_FLOORS = {
        'HQ1': [
            "2° ANDAR L MAIOR", "2° ANDAR L MENOR", "4° ANDAR L MAIOR", "4° ANDAR L MENOR",
            "6° ANDAR L MAIOR", "6° ANDAR L MENOR", "8° ANDAR L MAIOR", "8° ANDAR L MENOR", "4° ANDAR"
        ],
        'HQ2': [
            "2° ANDAR L MAIOR", "2° ANDAR L MENOR", "4° ANDAR L MAIOR", "4° ANDAR L MENOR",
            "6° ANDAR L MAIOR", "6° ANDAR L MENOR", "8° ANDAR L MAIOR", "8° ANDAR L MENOR",
            "8° ANDAR", "12° ANDAR", "15° ANDAR"
        ],
        'Spark': [
            "1° ANDAR", "2° ANDAR", "3° ANDAR"
        ]
    }
    
    BUDGET_ITEMS = [
        {'id': 'headsets', 'name': 'Headsets', 'unitPrice': 260.00, 'priority': 1},
        {'id': 'adaptadores-gorila', 'name': 'Adaptadores Gorila', 'unitPrice': 112.00, 'priority': 1},
        {'id': 'teclados', 'name': 'Teclados', 'unitPrice': 90.00, 'priority': 3},
        {'id': 'mouses', 'name': 'Mouses', 'unitPrice': 31.90, 'priority': 4}
    ]
    
    # Quantidades para reposição (do HTML original)
    REPOSITION_QUANTITIES = {
        'HQ1 - Lado Maior': {'Teclados': 20, 'Headsets': 5, 'Mouses': 10, 'Adaptadores': 5},
        'HQ1 - Lado Menor': {'Teclados': 10, 'Headsets': 5, 'Mouses': 5, 'Adaptadores': 5},
        'HQ2': {'Teclados': 15, 'Headsets': 5, 'Mouses': 10, 'Adaptadores': 5},
        'Spark': {'Teclados': 15, 'Headsets': 10, 'Mouses': 15, 'Adaptadores': 10}
    }

# Instância global
config = AppConfig()
