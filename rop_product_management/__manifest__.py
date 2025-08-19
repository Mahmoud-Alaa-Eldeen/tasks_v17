{
    'name': 'ROP Product Management',
    'version': '17.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Reorder Point View for Low Stock Products',
    'description': '''
        This module provides:
        - Website shop functionality
        - ROP view for products with quantity < 5
        - Restricted access to admin, warehouse admin, and users
    ''',
    'author': 'Your Company',
    'depends': [
        'base',
        'stock',
        'website',
        'website_sale',
        'sale_management',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/product_rop_views.xml',
        'views/website_templates.xml',
        'views/quantity_wizard_views.xml',
        'views/menu.xml',
        'data/website_data.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
