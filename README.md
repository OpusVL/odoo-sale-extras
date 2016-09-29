odoo-sale-extras
================

# sale\_template\_quotation

Allow quotations to be frozen for use as templates.

A new button is added to the Quotation screen, "Convert to Template", which
freezes the quotation preventing it from being edited or converted to a sales
order.

A new Quotation Reference field is also created which must be filled in
before conversion to a template.


# sale\_list\_client\_order\_ref

Display the client order reference (Reference/Description) field in sales order
and quotation list views, and allow searching on that field.

# sale\_printout\_split\_sku

Install this to print the product SKU in a separate `Code No` column on the left of Description,
instead of the usual format of `[SKU] Description`

This works very well with Odoo 8.0's stock sale order/quotation printout templates,
but if you customise the base template then your mileage may vary with this,
and you may wish to use the module `sale_order_split_sku_fields` instead and specify
the columns as you wish in your custom template.

# sale\_order\_split\_sku\_fields

This provides the fields on the `sale.order` model used by `sale_printout_split_sku`,
also allowing you to use those separated fields with your own custom sale order report
templates.

Provides the following fields on the `sale.order` model:

* `product_sku`
* `description_without_sku`

# sale\_customer\_specific

Customer-specific products.

Adds to the Product form's Sale tab a tickbox 'Is customer specific', which if ticked will only allow
the product to be added to sale orders for specific customers, listed in the 'Allowed customers' field.

# Copyright and License

Copyright (C) 2016 OpusVL

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

If you require assistance, support, or further development of this
software, please contact OpusVL using the details below:

* Telephone: +44 (0)1788 298 410
* Email: community@opusvl.com
* Web: http://opusvl.com
