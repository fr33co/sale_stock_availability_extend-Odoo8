# -*- coding: utf-8 -*-

{
    'name': 'Stock availability in sales order line improve and extend',
    'version': '8.0.0.1.0',
    'category': 'Tools',
    'description': """
    Incorpora modificaciones para el modulo sale_stock_availability
    """,
    'author': 'Angel A. Guadarrama B.',
    'website': 'https://github.com/fr33co',
    'depends': [
        'sale_stock_availability',
    ],
    'data': [
        'views/sale_view.xml',
        'views/product_view.xml',
        ],
    'installable': True,
}
