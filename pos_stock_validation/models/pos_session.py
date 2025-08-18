from odoo import models, fields, api


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """Override to include stock quantity in POS product data"""
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(['qty_available', 'virtual_available'])
        return result

    def _get_pos_ui_product_product(self, params):
        """Override to add stock information to products"""
        products = super()._get_pos_ui_product_product(params)
        
        # Add stock quantity information to each product
        for product in products:
            product_obj = self.env['product.product'].browse(product['id'])
            product['qty_available'] = product_obj.qty_available
            product['virtual_available'] = product_obj.virtual_available
            
        return products

