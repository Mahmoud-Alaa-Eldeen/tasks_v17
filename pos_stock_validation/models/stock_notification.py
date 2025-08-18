from odoo import models, fields, api
from odoo.exceptions import UserError


class StockNotification(models.Model):
    _name = 'stock.notification'
    _description = 'Stock Notification Management'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    current_stock = fields.Float(string='Current Stock', required=True)
    threshold = fields.Float(string='Threshold', required=True)
    notification_date = fields.Datetime(string='Notification Date', default=fields.Datetime.now)
    pos_session_id = fields.Many2one('pos.session', string='POS Session')
    notified_users = fields.Many2many('res.users', string='Notified Users')

    @api.model
    def send_stock_notification(self, product_id, current_stock, threshold, pos_session_id=None):
        """
        Send notification to warehouse admin when stock is below threshold
        """
        try:
            # Get the product
            product = self.env['product.product'].browse(product_id)
            if not product.exists():
                return {'success': False, 'message': 'Product not found'}

            # Find warehouse admin users (users with inventory manager rights)
            warehouse_admins = self.env['res.users'].search([
                ('groups_id', 'in', self.env.ref('stock.group_stock_manager').id)
            ])

            if not warehouse_admins:
                # Fallback to users with inventory user rights
                warehouse_admins = self.env['res.users'].search([
                    ('groups_id', 'in', self.env.ref('stock.group_stock_user').id)
                ])

            if not warehouse_admins:
                return {'success': False, 'message': 'No warehouse admin users found'}

            # Create notification record
            notification = self.create({
                'product_id': product_id,
                'current_stock': current_stock,
                'threshold': threshold,
                'pos_session_id': pos_session_id,
                'notified_users': [(6, 0, warehouse_admins.ids)]
            })

            # Send message to each warehouse admin
            for admin in warehouse_admins:
                # Create a message in the user's inbox
                self.env['mail.message'].create({
                    'subject': f'Stock Alert: {product.name} Below Re-Order Point',
                    'body': f"""
                        <p><strong>Stock Alert</strong></p>
                        <p>Product: <strong>{product.name}</strong></p>
                        <p>Current Stock: <strong>{current_stock}</strong></p>
                        <p>Re-Order Point: <strong>{threshold}</strong></p>
                        <p>This product is under the Re-Order Point measure and requires immediate attention.</p>
                        <p>Please check the inventory and consider restocking.</p>
                    """,
                    'message_type': 'notification',
                    'model': 'res.users',
                    'res_id': admin.id,
                    'partner_ids': [(4, admin.partner_id.id)],
                    # 'needaction_partner_ids': [(4, admin.partner_id.id)],
                })

            # Also post to the product's chatter if it has one
            if hasattr(product, 'message_post'):
                product.message_post(
                    subject=f'Stock Alert: Below Re-Order Point',
                    body=f"""
                        <p><strong>Stock Alert from POS</strong></p>
                        <p>Current Stock: <strong>{current_stock}</strong></p>
                        <p>Re-Order Point: <strong>{threshold}</strong></p>
                        <p>This product is under the Re-Order Point measure.</p>
                    """,
                    message_type='notification',
                    partner_ids=warehouse_admins.mapped('partner_id').ids
                )

            return {
                'success': True, 
                'message': f'Notification sent to {len(warehouse_admins)} warehouse admin(s)',
                'notification_id': notification.id
            }

        except Exception as e:
            return {'success': False, 'message': str(e)}

    @api.model
    def get_warehouse_admins(self):
        """
        Get list of warehouse admin users
        """
        try:
            warehouse_admins = self.env['res.users'].search([
                ('groups_id', 'in', self.env.ref('stock.group_stock_manager').id)
            ])
            
            if not warehouse_admins:
                warehouse_admins = self.env['res.users'].search([
                    ('groups_id', 'in', self.env.ref('stock.group_stock_user').id)
                ])

            return {
                'success': True,
                'admins': [{'id': admin.id, 'name': admin.name, 'email': admin.email} for admin in warehouse_admins]
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}

