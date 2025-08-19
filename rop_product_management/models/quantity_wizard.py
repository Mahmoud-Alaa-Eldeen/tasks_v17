from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductQuantityWizard(models.TransientModel):
    _name = 'product.quantity.wizard'
    _description = 'Product Quantity Update Wizard'

    product_id = fields.Many2one('product.template', string='Product', required=True)
    current_quantity = fields.Float(string='Current Quantity', readonly=True)
    new_quantity = fields.Float(string='New Quantity', required=True)
    reason = fields.Text(string='Reason for Update', help='Optional reason for the quantity update')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get('active_id'):
            product = self.env['product.template'].browse(self.env.context['active_id'])
            res.update({
                'product_id': product.id,
                'current_quantity': sum(product.product_variant_ids.mapped('qty_available')),
            })
        return res

    def action_update_quantity(self):
        """Update product quantity and send notifications"""
        self.ensure_one()
        
        if self.new_quantity < 0:
            raise UserError("Quantity cannot be negative!")

        # Get the main product variant
        product_variant = self.product_id.product_variant_ids[0] if self.product_id.product_variant_ids else False
        if not product_variant:
            raise UserError("No product variant found!")

        # Get or create stock quant
        location = self.env.ref('stock.stock_location_stock')
        quant = self.env['stock.quant'].search([
            ('product_id', '=', product_variant.id),
            ('location_id', '=', location.id),
        ], limit=1)

        old_qty = self.current_quantity
        qty_diff = self.new_quantity - old_qty

        if quant:
            # Update existing quant
            quant.quantity = self.new_quantity
        else:
            # Create new quant
            self.env['stock.quant'].create({
                'product_id': product_variant.id,
                'location_id': location.id,
                'quantity': self.new_quantity,
            })

        # Send notification to admin and warehouse users
        self._send_quantity_update_notification(old_qty, self.new_quantity, qty_diff)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success!',
                'message': f'Product quantity updated from {old_qty} to {self.new_quantity}',
                'type': 'success',
                'sticky': False,
            }
        }

    def _send_quantity_update_notification(self, old_qty, new_qty, qty_diff):
        """Send notification to admin and warehouse users"""
        
        # Get users to notify (Admin and Warehouse users)
        admin_users = self.env.ref('base.group_system').users
        warehouse_users = self.env.ref('stock.group_stock_manager').users
        stock_users = self.env.ref('stock.group_stock_user').users
        
        all_users = admin_users | warehouse_users | stock_users
        
        # Exclude current user from notification
        users_to_notify = all_users.filtered(lambda u: u.id != self.env.user.id)
        
        if users_to_notify:
            # Create notification message
            message = f"""
            Product Quantity Updated: {self.product_id.name}
            
            Updated by: {self.env.user.name}
            Old Quantity: {old_qty}
            New Quantity: {new_qty}
            Difference: {'+' if qty_diff > 0 else ''}{qty_diff}
            
            {f'Reason: {self.reason}' if self.reason else ''}
            """

            # Send notification to each user
            for user in users_to_notify:
                self.env['mail.thread'].message_notify(
                    partner_ids=[user.partner_id.id],
                    subject=f'Product Quantity Updated: {self.product_id.name}',
                    body=message,
                    email_from=self.env.user.email_formatted,
                )