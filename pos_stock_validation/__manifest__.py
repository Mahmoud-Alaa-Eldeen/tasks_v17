{
    'name': 'POS Stock Validation',
    'category': 'Point of Sale',
    'summary': 'Validate stock quantity before payment in POS',
    'description': """
        This module adds validation to the POS payment process to check if products
        have sufficient stock (> 5 units) before allowing payment. If stock is below
        the threshold, it shows a message "This product under of the Re-Order Point measure".
    """,
    'author': 'Custom Development',
    'depends': ['point_of_sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_config_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_stock_validation/static/src/js/models.js',
            'pos_stock_validation/static/src/js/payment_screen.js',
            'pos_stock_validation/static/src/js/product_screen.js',

        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

