from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def get_rop_products(self):
        """Get products with quantity less than 5"""
        products = self.env['product.template'].search([
            ('type', '=', 'product'),
            ('active', '=', True)
        ])
        
        rop_products = []
        for product in products:
            total_qty = sum(product.product_variant_ids.mapped('qty_available'))
            if total_qty < 5:
                rop_products.append({
                    'id': product.id,
                    'name': product.name,
                    'default_code': product.default_code or '',
                    'qty_available': total_qty,
                    'list_price': product.list_price,
                    'categ_id': product.categ_id.name,
                    'uom_name': product.uom_id.name,
                })
        
        return rop_products

    rop_qty_available = fields.Float(
        string='ROP Available Qty', 
        compute='_compute_rop_qty',
        help='Total quantity available for ROP calculation'
    )

    @api.depends('product_variant_ids.qty_available')
    def _compute_rop_qty(self):
        for product in self:
            product.rop_qty_available = sum(product.product_variant_ids.mapped('qty_available'))

    def action_open_quantity_wizard(self):
        """Open quantity update wizard"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Update Product Quantity',
            'res_model': 'product.quantity.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }
    
    @api.model
    def get_realtime_rop_products(self):
        """Get products with quantity greater than 5 for real-time view"""
        products = self.env['product.template'].search([
            ('type', '=', 'product'),
            ('active', '=', True)
        ])
        
        realtime_products = []
        for product in products:
            total_qty = sum(product.product_variant_ids.mapped('qty_available'))
            if total_qty > 5:
                realtime_products.append({
                    'id': product.id,
                    'name': product.name,
                    'default_code': product.default_code or '',
                    'qty_available': total_qty,
                    'list_price': product.list_price,
                    'categ_id': product.categ_id.name,
                    'uom_name': product.uom_id.name,
                    'last_updated': fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                })
        
        return realtime_products
    