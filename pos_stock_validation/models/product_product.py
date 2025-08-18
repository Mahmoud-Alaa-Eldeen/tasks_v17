from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def check_stock_availability(self, product_id, required_qty=5):
        """
        Check if product has sufficient stock
        Returns True if stock is sufficient, False otherwise
        """
        product = self.browse(product_id)
        return product.qty_available > required_qty

    def get_stock_message(self):
        """
        Get stock validation message for POS
        """
        if self.qty_available <= 5:
            return "This product under of the Re-Order Point measure"
        return ""

