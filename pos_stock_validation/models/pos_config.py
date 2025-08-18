from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_stock_validation = fields.Boolean(
        string='Enable Stock Validation',
        default=True,
        help='Enable stock validation before payment in POS'
    )
    
    min_stock_threshold = fields.Float(
        string='Minimum Stock Threshold',
        default=5.0,
        help='Minimum stock quantity required to allow payment'
    )

