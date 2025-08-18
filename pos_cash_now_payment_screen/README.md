# POS Cash Now to Payment Screen Button Module

## Overview

The POS Cash Now to Payment Screen Button module enhances the Odoo 17 Point of Sale Product Screen by adding a dedicated "Cash now" button. This button streamlines the checkout process for cash transactions by automatically navigating to the payment screen, selecting the cash payment method, and assigning the customer to 'administrator'.

## Features

- **Quick Navigation**: Instantly moves from the Product Screen to the Payment Screen.
- **Automatic Cash Method Selection**: Automatically selects the cash payment method, reducing manual steps.
- **Default Customer Assignment**: Sets the customer for the order to 'administrator' by default, ideal for quick sales where customer tracking is not immediately required.
- **Strategic Button Placement**: The "Cash now" button is strategically placed next to the existing "Refund" button for easy access and intuitive workflow.
- **Empty Order Prevention**: Prevents navigation to the payment screen if the order is empty, prompting the user to add products first.
- **Cash Method Configuration Check**: Validates if a cash payment method is configured in POS settings and alerts the user if not.

## Installation

### Prerequisites

- Odoo 17.0 or later
- Point of Sale module installed and configured
- At least one cash payment method configured in POS settings
- An 'admin' customer (partner) should ideally exist in your Odoo database. If not, the module will prompt you to create one.

### Installation Steps

1. **Download the Module**
   - Extract the `pos_cash_now_payment_screen` module to your Odoo addons directory.

2. **Update Apps List**
   - Login to Odoo as Administrator.
   - Go to the **Apps** menu.
   - Click **Update Apps List**.

3. **Install the Module**
   - Search for "POS Cash Now to Payment Screen".
   - Click **Install**.

4. **Configure POS**
   - Ensure you have a cash payment method configured and enabled for your POS configuration.
   - Restart your POS sessions for changes to take effect.

## Usage

### Using the Cash Now Button

1. **Add Products to Order**
   - Add one or more products to the current POS order on the Product Screen.

2. **Click "Cash now"**
   - Locate and click the "Cash now" button. It is positioned next to the "Refund" button.

3. **Automatic Actions**
   - The system will automatically set the customer to 'administrator'.
   - You will be navigated to the Payment Screen.
   - The cash payment method will be automatically selected, and the total amount will be added to the cash payment line.

4. **Finalize Payment**
   - On the Payment Screen, you can then finalize the cash payment.

### Button Location

The "Cash now" button is specifically placed next to the "Refund" button within the control buttons area of the Product Screen.

## Technical Details

### Frontend Components

#### XML Template (`pos_cash_now_payment_screen_button.xml`)
- Extends the `ProductScreen` template.
- Uses an `xpath` expression to position the "Cash now" button `after` the `refund-button` within the `control-buttons` div.
- Uses Font Awesome money icon (`fa fa-money`) for visual identification.

#### JavaScript Logic (`pos_cash_now_payment_screen_button.js`)
- Implements the `onClickCashNowPaymentScreen` method, which is triggered when the button is clicked.
- **Order Validation**: Checks if the current order has any orderlines before proceeding.
- **Customer Assignment**: 
    - Attempts to find an existing customer named "admin" (case-insensitive).
    - If found, sets this customer as the partner for the current order.
    - If not found, displays an error popup, prompting the user to create an 'admin' customer.
- **Screen Navigation**: Uses `this.showScreen("PaymentScreen")` to navigate to the payment screen.
- **Cash Method Selection**: 
    - Finds the first available cash payment method configured in the POS.
    - If a cash method is found and the order total is greater than 0, it adds a payment line with the cash method and sets its amount to the order's total.
    - Displays an error popup if no cash payment method is configured.
- **Error Handling**: Includes `try-catch` blocks and `ErrorPopup` for user-friendly error messages.

### Backend Components

This module primarily focuses on frontend interactions. No specific backend Python models are introduced for this functionality, as the actions (setting customer, navigating, selecting payment method) are handled directly within the POS frontend logic.

### Key Methods

#### `onClickCashNowPaymentScreen()`
- The main method responsible for orchestrating the button's functionality.
- Handles the flow from product screen to payment screen with pre-selected options.

## Configuration

### Payment Method Requirements

For this module to function correctly, you must have at least one cash payment method configured in your Odoo POS settings:

1. Go to **Point of Sale > Configuration > Payment Methods**.
2. Ensure you have a payment method with `type` set to "Cash" or whose `name` includes "cash" (case-insensitive).
3. Make sure this payment method is enabled for your specific POS configuration.

### Customer Configuration

The module attempts to find a customer named "admin". It is highly recommended to have a partner record with the name "admin" in your Odoo database to ensure smooth operation. If such a partner does not exist, an error message will be displayed.

## Error Handling

The module includes error handling for common scenarios:

### Empty Order
- **Error**: "Empty Order"
- **Cause**: The "Cash now" button was clicked when there were no products in the order.
- **Solution**: Add products to the order before clicking the button.

### Admin Customer Not Found
- **Error**: "Admin Customer Not Found"
- **Cause**: A customer (partner) with the name "admin" could not be found in your Odoo database.
- **Solution**: Create a new customer record in Odoo and name it "admin".

### Cash Payment Method Not Found
- **Error**: "Cash Payment Method Not Found"
- **Cause**: No cash payment method is configured or enabled for your POS.
- **Solution**: Configure and enable at least one cash payment method in your POS settings.

### Unexpected Errors
- **Error**: "An unexpected error occurred: [error message]"
- **Cause**: A general JavaScript error occurred during the process.
- **Solution**: Check the browser's developer console for more detailed error messages and ensure all module dependencies are correctly loaded.

## Troubleshooting

### Button Not Appearing
1. **Module Installation**: Verify that the `pos_cash_now_payment_screen` module is installed and enabled in Odoo.
2. **Cache**: Clear your browser's cache and restart your POS session.
3. **XML Syntax**: Double-check the `pos_cash_now_payment_screen_button.xml` file for any syntax errors, especially in the `xpath` expression.
4. **Assets Loading**: Ensure that `point_of_sale._assets_pos` is correctly defined in your module's `__manifest__.py` and includes the core POS assets (`pos.xml`, `pos.js`) before your custom assets.

### Automatic Actions Not Working (e.g., Customer Not Set, Cash Not Selected)
1. **JavaScript Errors**: Check the browser's developer console for any JavaScript errors. These can prevent the script from executing fully.
2. **Customer Name**: Ensure the 'admin' customer's name is exactly "admin" (case-insensitive check is implemented, but exact match is best).
3. **Payment Method Name/Type**: Verify that your cash payment method is correctly configured with `type: 'cash'` or its name contains "cash".

## Compatibility

- **Odoo Version**: 17.0+
- **Dependencies**: `point_of_sale`
- **Browser Compatibility**: Modern web browsers supporting ES6+.
- **Mobile Compatibility**: Designed to be responsive and work on tablet POS systems.

## License

This module is licensed under LGPL-3, consistent with Odoo's licensing terms.


