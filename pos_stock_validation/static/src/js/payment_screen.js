/* @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";

// Extend the PaymentScreen to add stock validation before payment
patch(PaymentScreen.prototype, {
    
    /**
     * Validate stock before processing payment
     * @returns {boolean} true if validation passes, false otherwise
     */
    async validateStock() {
        const order = this.currentOrder;
        const orderlines = order.get_orderlines();
        
        // Check if stock validation is enabled
        if (!this.pos.config.enable_stock_validation) {
            return true;
        }
        
        // Check each orderline for sufficient stock
        for (const line of orderlines) {
            if (!line.hasValidStock()) {
                const message = line.getStockValidationMessage();
                const productName = line.product.display_name;
                const currentStock = line.getCurrentStock();
                const minThreshold = this.pos.config.min_stock_threshold || 5;
                
                // Send notification to warehouse admin
                try {
                    await this.sendStockNotification(line.product.id, currentStock, minThreshold);
                } catch (error) {
                    console.error('Failed to send stock notification:', error);
                }
                
                // Show error popup with stock validation message
                await this.popup.add(ErrorPopup, {
                    title: _t("Stock Validation Error"),
                    body: _t(`${productName}\n\n${message}\n\nCurrent Stock: ${currentStock}\nRequired: > ${minThreshold}\n\nWarehouse admin has been notified.`),
                });
                
                return false;
            }
        }
        
        return true;
    },
    
    /**
     * Override the validateOrder method to include stock validation
     */
    async validateOrder(isForceValidate) {
        // First validate stock
        const stockValid = await this.validateStock();
        if (!stockValid) {
            return false;
        }
        
        // If stock validation passes, proceed with original validation
        return await super.validateOrder(isForceValidate);
    },
    
    /**
     * Override the _isOrderValid method to include stock validation
     */
    _isOrderValid(isForceValidate) {
        // First check original validation
        const originalValid = super._isOrderValid(isForceValidate);
        if (!originalValid) {
            return false;
        }
        
        // Check stock validation (synchronous check)
        const order = this.currentOrder;
        const orderlines = order.get_orderlines();
        
        // Check if stock validation is enabled
        if (!this.pos.config.enable_stock_validation) {
            return true;
        }
        
        // Check each orderline for sufficient stock
        for (const line of orderlines) {
            if (!line.hasValidStock()) {
                return false;
            }
        }
        
        return true;
    },

    /**
     * Send notification to warehouse admin about low stock
     * @param {number} productId - Product ID
     * @param {number} currentStock - Current stock quantity
     * @param {number} threshold - Minimum threshold
     */
    async sendStockNotification(productId, currentStock, threshold) {
        try {
            const result = await this.orm.call(
                'stock.notification',
                'send_stock_notification',
                [productId, currentStock, threshold, this.pos.pos_session.id]
            );
            
            if (result.success) {
                console.log('Stock notification sent successfully:', result.message);
            } else {
                console.error('Failed to send stock notification:', result.message);
            }
            
            return result;
        } catch (error) {
            console.error('Error sending stock notification:', error);
            throw error;
        }
    },
});

