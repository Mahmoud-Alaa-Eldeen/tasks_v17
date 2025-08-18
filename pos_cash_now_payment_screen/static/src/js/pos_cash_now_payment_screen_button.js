/** @odoo-module */

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";


export class CashNow extends Component {
    static template = "point_of_sale.CashNow";

    setup() {
        this.pos = usePos();
    }
   async  click() {

    console.log("Cash now button clicked from Product Screen");

            const order = this.pos.get_order();

        // Check if there are items in the order
        if (order.get_orderlines().length === 0) {
            await this.pos.popup.add(ErrorPopup, {
                title: _t("Empty Order"),
                body: _t("Please add products to the order before proceeding."),
            });
            return;
        }

        try {

            // Find the 'admin' customer
            console.log('in try this',this);
            const allPartners = this.pos.partners;    
            let adminCustomer = allPartners[0];//.find(partner => partner.id === 3);//this.pos.db.get_partner_by_name("admin");
            console.log('adminCustomer',adminCustomer);
            if (!adminCustomer) {
                // Fallback: search for a partner named 'admin' (case-insensitive)
                adminCustomer = this.pos.db.partners.find(partner => 
                    partner.name && partner.name.toLowerCase() === 'Administrator'
                );
            }

            if (!adminCustomer) {
                await this.pos.popup.add(ErrorPopup, {
                    title: _t("Admin Customer Not Found"),
                    body: _t("The 'admin' customer could not be found. Please create an 'admin' customer in Odoo."),
                });
                return;
            }

            // Set the customer to admin
            console.log('adminCustomer before set',adminCustomer);
            order.set_partner(adminCustomer);

            // Navigate to the payment screen
            this.pos.showScreen("PaymentScreen");

            // Find the cash payment method
            const cashPaymentMethod = this.pos.payment_methods.find(method => 
                method.type === "cash" || method.name.toLowerCase().includes("cash")
            );

            if (!cashPaymentMethod) {
                await this.pos.popup.add(ErrorPopup, {
                    title: _t("Cash Payment Method Not Found"),
                    body: _t("No cash payment method is configured. Please configure a cash payment method in POS settings."),
                });
                return;
            }

            // Set the cash payment method as selected
            // This part might need to be handled on the PaymentScreen itself if direct selection is not possible here
            // For now, we just navigate and assume the user will select it or it's the default.
            // A more robust solution would involve patching PaymentScreen to auto-select cash.
            
            // To automatically select cash, we need to add a payment line with the cash method
            // However, this should ideally happen *after* navigating to the payment screen and ensuring it's ready.
            // For simplicity in this direct patch, we'll add it here, but it might be better to do it in a patched PaymentScreen.
            
            // Add a payment line with the cash method and set the amount to the total
            // This will effectively select the cash method and make the order paid if enough cash is added.
            if (order.get_total_with_tax() > 0) {
                order.add_paymentline(cashPaymentMethod);
                const paymentline = order.selected_paymentline;
                paymentline.set_amount(order.get_total_with_tax());
            }

        } catch (error) {
            console.error("Error in Cash now button:", error);
            await this.pos.popup.add(ErrorPopup, {
                title: _t("Error"),
                body: _t(`An unexpected error occurred: ${error.message}`),
            });
        }

    }
}

ProductScreen.addControlButton({
    component: CashNow,
    condition: function () {
        return true;
    },
});

/////////////////////////////////////
/*
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";

patch(ProductScreen.prototype, {
    async onClickCashNowPaymentScreen() {
        console.log("Cash now button clicked from Product Screen");

        const order = this.currentOrder;

        // Check if there are items in the order
        if (order.get_orderlines().length === 0) {
            await this.popup.add(ErrorPopup, {
                title: _t("Empty Order"),
                body: _t("Please add products to the order before proceeding."),
            });
            return;
        }

        try {
            // Find the 'admin' customer
            let adminCustomer = this.pos.db.get_partner_by_name("admin");
            if (!adminCustomer) {
                // Fallback: search for a partner named 'admin' (case-insensitive)
                adminCustomer = this.pos.db.partners.find(partner => 
                    partner.name && partner.name.toLowerCase() === 'admin'
                );
            }

            if (!adminCustomer) {
                await this.popup.add(ErrorPopup, {
                    title: _t("Admin Customer Not Found"),
                    body: _t("The 'admin' customer could not be found. Please create an 'admin' customer in Odoo."),
                });
                return;
            }

            // Set the customer to admin
            order.set_partner(adminCustomer);

            // Navigate to the payment screen
            this.showScreen("PaymentScreen");

            // Find the cash payment method
            const cashPaymentMethod = this.pos.payment_methods.find(method => 
                method.type === "cash" || method.name.toLowerCase().includes("cash")
            );

            if (!cashPaymentMethod) {
                await this.popup.add(ErrorPopup, {
                    title: _t("Cash Payment Method Not Found"),
                    body: _t("No cash payment method is configured. Please configure a cash payment method in POS settings."),
                });
                return;
            }

            // Set the cash payment method as selected
            // This part might need to be handled on the PaymentScreen itself if direct selection is not possible here
            // For now, we just navigate and assume the user will select it or it's the default.
            // A more robust solution would involve patching PaymentScreen to auto-select cash.
            
            // To automatically select cash, we need to add a payment line with the cash method
            // However, this should ideally happen *after* navigating to the payment screen and ensuring it's ready.
            // For simplicity in this direct patch, we'll add it here, but it might be better to do it in a patched PaymentScreen.
            
            // Add a payment line with the cash method and set the amount to the total
            // This will effectively select the cash method and make the order paid if enough cash is added.
            if (order.get_total_with_tax() > 0) {
                order.add_paymentline(cashPaymentMethod);
                const paymentline = order.selected_paymentline;
                paymentline.set_amount(order.get_total_with_tax());
            }

        } catch (error) {
            console.error("Error in Cash now button:", error);
            await this.popup.add(ErrorPopup, {
                title: _t("Error"),
                body: _t(`An unexpected error occurred: ${error.message}`),
            });
        }
    },
});


*/