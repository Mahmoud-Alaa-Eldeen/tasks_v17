from odoo import http
from odoo.http import request

class ROPController(http.Controller):


    @http.route(['/shop/rop/update-quantity'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def update_product_quantity(self, **kwargs):
        """Handle quantity update from website form"""
        
        # Check access
        user = request.env.user
        has_access = (
            user.has_group('base.group_system') or
            user.has_group('stock.group_stock_manager') or
            user.has_group('stock.group_stock_user') or
            user.has_group('rop_product_management.group_rop_access')
        )
        
        if not has_access:
            return "You can't access this function"

        try:
            product_id = int(kwargs.get('product_id', 0))
            new_quantity = float(kwargs.get('new_quantity', 0))
            reason = kwargs.get('reason', '')

            if not product_id:
                raise UserError("Product ID is required")
            
            if new_quantity < 0:
                raise UserError("Quantity cannot be negative")

            # Create and execute wizard
            wizard = request.env['product.quantity.wizard'].create({
                'product_id': product_id,
                'new_quantity': new_quantity,
                'reason': reason,
            })
            
            wizard.action_update_quantity()
            
            # Success message
            product = request.env['product.template'].browse(product_id)
            message = f"Successfully updated {product.name} quantity to {new_quantity}"
            
            return request.render('rop_product_management.quantity_update_success', {
                'message': message
            })

        except Exception as e:
            # Error handling
            return request.render('rop_product_management.quantity_update_success', {
                'message': f"Error: {str(e)}"
            })

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
