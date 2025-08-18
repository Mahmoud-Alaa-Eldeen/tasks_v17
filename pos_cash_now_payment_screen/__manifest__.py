{
    'name': 'POS Cash Now to Payment Screen',
    'version': '17.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Adds a "Cash now" button to the POS Product Screen to navigate to payment screen with cash method and admin customer.',
    'description': """
        This module adds a 'Cash now' button to the Odoo 17 Point of Sale Product Screen.
        Clicking this button will:
        - Navigate to the payment screen.
        - Automatically select the cash payment method.
        - Automatically set the customer to 'administrator'.
        
    """,
    'author': 'Custom Development',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_config_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'point_of_sale/static/src/xml/pos.xml',
            'point_of_sale/static/src/js/pos.js',
            'pos_cash_now_payment_screen/static/src/xml/pos_cash_now_payment_screen_button.xml',
            'pos_cash_now_payment_screen/static/src/js/pos_cash_now_payment_screen_button.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

