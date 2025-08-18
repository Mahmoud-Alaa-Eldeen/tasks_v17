# POS Stock Validation Module for Odoo 17

## Overview

The POS Stock Validation module is a custom Odoo 17 extension that adds intelligent stock validation to the Point of Sale (POS) system. This module prevents payment processing when products in the cart have insufficient stock quantities, specifically when the available stock is 5 units or less. When validation fails, the system displays a clear message: "This product under of the Re-Order Point measure" to inform users about the stock shortage.

## Features

- **Real-time Stock Validation**: Automatically checks product stock levels before allowing payment processing
- **Configurable Threshold**: Set custom minimum stock thresholds through POS configuration
- **User-friendly Error Messages**: Clear, informative popup messages when validation fails
- **Seamless Integration**: Works seamlessly with existing Odoo 17 POS workflows
- **Backend Integration**: Extends both frontend JavaScript and backend Python models
- **Configuration Options**: Enable/disable validation and set custom thresholds per POS configuration

## Technical Architecture

### Backend Components

The module extends several core Odoo models to provide comprehensive stock validation functionality:

#### 1. POS Session Extension (`pos_session.py`)
- Extends `pos.session` model to include stock quantity data in POS product loading
- Adds `qty_available` and `virtual_available` fields to product data sent to frontend
- Ensures real-time stock information is available in the POS interface

#### 2. Product Extension (`product_product.py`)
- Extends `product.product` model with stock validation methods
- Provides `check_stock_availability()` method for backend validation
- Includes `get_stock_message()` method for consistent error messaging

#### 3. POS Configuration Extension (`pos_config.py`)
- Adds configuration fields to `pos.config` model
- `enable_stock_validation`: Boolean field to enable/disable validation
- `min_stock_threshold`: Float field to set minimum required stock quantity

### Frontend Components

#### 1. Models Extension (`models.js`)
- Extends the `Orderline` prototype with stock validation methods
- `hasValidStock()`: Checks if orderline product meets stock requirements
- `getStockValidationMessage()`: Returns appropriate error message
- `getCurrentStock()`: Retrieves current stock quantity for display

#### 2. Payment Screen Extension (`payment_screen.js`)
- Extends `PaymentScreen` to add validation before payment processing
- `validateStock()`: Asynchronous method that checks all orderlines
- Displays error popup with detailed stock information when validation fails
- Prevents payment processing when stock validation fails

## Installation Guide

### Prerequisites

Before installing the POS Stock Validation module, ensure you have:

1. **Odoo 17 Enterprise or Community Edition** properly installed and running
2. **Administrative access** to the Odoo instance
3. **Point of Sale module** installed and configured
4. **Inventory/Stock module** installed and configured
5. **File system access** to the Odoo addons directory

### Step 1: Download and Extract Module

1. Download the `pos_stock_validation` module files
2. Extract the module to your Odoo addons directory:
   ```bash
   # Navigate to your Odoo addons directory
   cd /path/to/odoo/addons
   
   # Copy the module directory
   cp -r /path/to/pos_stock_validation ./
   ```

### Step 2: Update Addons List

1. Access your Odoo instance as an administrator
2. Navigate to **Apps** menu
3. Click **Update Apps List** button
4. Confirm the update when prompted

### Step 3: Install the Module

1. In the **Apps** menu, search for "POS Stock Validation"
2. Click the **Install** button next to the module
3. Wait for the installation to complete
4. The system will automatically restart if required

### Step 4: Verify Installation

1. Navigate to **Point of Sale > Configuration > Point of Sale**
2. Open any POS configuration
3. Verify that the **Stock Validation** section appears in the form
4. Check that the following fields are visible:
   - Enable Stock Validation (toggle)
   - Minimum Stock Threshold (numeric field)

## Configuration Guide

### Basic Configuration

1. **Access POS Configuration**:
   - Navigate to **Point of Sale > Configuration > Point of Sale**
   - Select the POS configuration you want to modify

2. **Enable Stock Validation**:
   - Scroll to the **Stock Validation** section
   - Toggle **Enable Stock Validation** to ON
   - Set **Minimum Stock Threshold** to your desired value (default: 5)

3. **Save Configuration**:
   - Click **Save** to apply changes
   - Restart any active POS sessions for changes to take effect

### Advanced Configuration Options

#### Threshold Customization

The minimum stock threshold can be customized per POS configuration:

- **Default Value**: 5 units
- **Recommended Range**: 1-10 units for most businesses
- **Special Cases**: 
  - High-volume products: Consider higher thresholds (10-20 units)
  - Low-volume products: Lower thresholds (1-3 units) may be appropriate

#### Multi-Location Setup

For businesses with multiple locations:

1. Configure each POS separately with location-specific thresholds
2. Ensure stock quantities reflect the correct warehouse/location
3. Test validation with products from different stock locations

### Testing the Configuration

1. **Create Test Scenario**:
   - Identify a product with stock quantity ≤ 5 units
   - Add the product to a POS order
   - Attempt to process payment

2. **Expected Behavior**:
   - Payment should be blocked
   - Error popup should display: "This product under of the Re-Order Point measure"
   - Popup should show current stock and required threshold

3. **Verify Success**:
   - Increase product stock to > 5 units
   - Retry payment processing
   - Payment should proceed normally

## Usage Instructions

### For POS Users

#### Normal Operation

When stock validation is enabled, the POS system will automatically check stock levels during payment processing. Users don't need to take any special actions during normal operation.

#### When Validation Fails

If a product has insufficient stock:

1. **Error Display**: A popup will appear with the message "This product under of the Re-Order Point measure"
2. **Stock Information**: The popup shows current stock and required threshold
3. **Resolution Options**:
   - Remove the product from the order
   - Reduce the quantity to available stock
   - Contact management to increase stock levels

#### Best Practices for Users

- **Check Stock Regularly**: Monitor product availability during busy periods
- **Communicate Issues**: Report recurring stock shortages to management
- **Alternative Products**: Suggest similar products when stock is unavailable

### For Administrators

#### Monitoring and Maintenance

1. **Regular Stock Reviews**:
   - Monitor products that frequently trigger validation errors
   - Adjust reorder points based on validation patterns
   - Review threshold settings periodically

2. **Performance Monitoring**:
   - Check POS session logs for validation-related issues
   - Monitor system performance during peak usage
   - Ensure stock data synchronization is working correctly

3. **User Training**:
   - Train POS users on new validation behavior
   - Provide guidelines for handling validation errors
   - Create standard procedures for stock shortage situations

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Validation Not Working

**Symptoms**: Payment proceeds despite low stock
**Possible Causes**:
- Stock validation disabled in POS configuration
- Module not properly installed
- POS session not restarted after configuration changes

**Solutions**:
1. Verify **Enable Stock Validation** is toggled ON
2. Restart the POS session
3. Check module installation status
4. Review browser console for JavaScript errors

#### Issue 2: Incorrect Stock Quantities

**Symptoms**: Validation shows wrong stock numbers
**Possible Causes**:
- Stock data not synchronized
- Multiple warehouse configurations
- Pending stock moves not processed

**Solutions**:
1. Run inventory synchronization
2. Check warehouse settings in POS configuration
3. Process pending stock moves
4. Verify product stock location settings

#### Issue 3: Performance Issues

**Symptoms**: Slow payment processing
**Possible Causes**:
- Large product catalogs
- Complex stock calculations
- Network latency

**Solutions**:
1. Optimize product loading parameters
2. Consider caching stock data
3. Review network configuration
4. Monitor database performance

### Error Messages and Meanings

| Error Message | Meaning | Resolution |
|---------------|---------|------------|
| "This product under of the Re-Order Point measure" | Product stock ≤ threshold | Increase stock or remove product |
| "Stock Validation Error" | General validation failure | Check configuration and stock data |
| JavaScript console errors | Frontend validation issues | Check browser compatibility and module assets |

### Debugging Steps

1. **Check Module Status**:
   ```bash
   # In Odoo shell
   self.env['ir.module.module'].search([('name', '=', 'pos_stock_validation')])
   ```

2. **Verify Configuration**:
   ```python
   # Check POS config settings
   pos_config = self.env['pos.config'].browse(config_id)
   print(pos_config.enable_stock_validation)
   print(pos_config.min_stock_threshold)
   ```

3. **Test Stock Data**:
   ```python
   # Check product stock
   product = self.env['product.product'].browse(product_id)
   print(product.qty_available)
   ```

## Support and Maintenance

### Getting Help

For technical support and assistance:

1. **Documentation**: Refer to this README and inline code comments
2. **Community Forums**: Post questions on Odoo community forums
3. **Professional Support**: Contact Odoo partners for enterprise support

### Updates and Upgrades

#### Version Compatibility

- **Current Version**: 17.0.1.0.0
- **Odoo Compatibility**: Odoo 17.0 Community and Enterprise
- **Dependencies**: point_of_sale, stock modules

#### Future Enhancements

Planned features for future versions:
- Multi-threshold support per product category
- Advanced stock reservation during POS sessions
- Integration with procurement automation
- Enhanced reporting and analytics

### Contributing

To contribute to the module development:

1. Fork the repository
2. Create feature branches for new functionality
3. Follow Odoo development guidelines
4. Submit pull requests with detailed descriptions
5. Include test cases for new features

## License and Legal

This module is released under the LGPL-3 license, consistent with Odoo's licensing model. Users are free to modify and distribute the module according to the license terms.

### Disclaimer

This module is provided "as is" without warranty of any kind. Users should thoroughly test the module in a development environment before deploying to production systems.

---

**Author**: Custom Development Team  
**Version**: 17.0.1.0.0  
**Last Updated**: August 2025  
**Odoo Version**: 17.0

