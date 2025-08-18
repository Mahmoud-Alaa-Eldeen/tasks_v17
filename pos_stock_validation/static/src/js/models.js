/* @odoo-module */

import { Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

// Extend the Orderline model to include stock validation
patch(Orderline.prototype, {
    
    /**
     * Check if the product has sufficient stock
     * @returns {boolean} true if stock is sufficient, false otherwise
     */
    hasValidStock() {
        const product = this.product;
        const minThreshold = this.pos.config.min_stock_threshold || 5;
        
        // Check if stock validation is enabled
        if (!this.pos.config.enable_stock_validation) {
            return true;
        }
        
        // Check if product has sufficient stock
        return product.qty_available > minThreshold;
    },
    
    /**
     * Get stock validation message
     * @returns {string} validation message if stock is insufficient
     */
    getStockValidationMessage() {
        if (!this.hasValidStock()) {
            return "This product under of the Re-Order Point measure";
        }
        return "";
    },
    
    /**
     * Get current stock quantity
     * @returns {number} current stock quantity
     */
    getCurrentStock() {
        return this.product.qty_available || 0;
    }
});

