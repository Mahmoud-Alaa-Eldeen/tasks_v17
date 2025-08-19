from odoo import http
from odoo.http import request

class ROPController(http.Controller):

    @http.route(['/shop/rop'], type='http', auth="user", website=True)
    def shop_rop(self, **kwargs):
        """ROP products page for website"""
        
        # Check if user has ROP access
        if not request.env.user.has_group('rop_product_management.group_rop_access'):
            return  "You can't see this page"

        # Get ROP products
        products = request.env['product.template'].get_rop_products()
        
        values = {
            'products': products,
            'page_name': 'rop',
            'default_url': '/shop/rop',
        }
        
        return request.render('rop_product_management.rop_products_page', values)
