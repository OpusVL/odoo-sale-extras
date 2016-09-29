# -*- coding: utf-8 -*-

##############################################################################
#
# Sale - Product Variant Selection Assistant
# Copyright (C) 2016 OpusVL (<http://opusvl.com/>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    variant_assistant_product_template_id = fields.Many2one(
        string='Product Template',
        comodel_name='product.template',
        help='To use the variant assistant, select the top-level product template here',
    )

    variant_assistant_attribute_choice_ids = fields.One2many(
        comodel_name='sale.order.line.assistant.attribute.choice',
        foreign_field='sale_order_line_id',
        string='Choose attributes',
        invisible=[('variant_assistant_attribute_choice_ids', '=', False)],
        help='Now select the attribute values.  Once you select enough attributes to uniquely identify the product, it will be entered in the Product field',
    )

class SaleOrderLineAssistantAttributeChoice(models.Model):
    _name = 'sale.order.line.assistant.attribute.choice'

    sale_order_line_id = fields.Many2one(
        string='Sale Order Line',
        comodel_name='sale.order.line',
    )
    product_template_id = fields.Many2one(
        string='Product Template',
        invisible=True,
        related='sale_order_line_id.variant_assistant_product_template_id',
    )
    attribute_id = fields.Many2one(
        string='Attribute',
        comodel_name='product.attribute',
    )
    attribute_line_id = fields.Many2one(
        string='Attribute Line',
        comodel_name='product.attribute.line',
    )
    value_id = fields.Many2one(
        string='Value',
        comodel_name='product.attribute.value',
    )

    @api.one
    @api.constrains('product_template_id', 'attribute_id', 'attribute_line_id', 'value_id')
    def _check_attributes(self):
        if self.attribute_line_id.product_tmpl_id != self.product_template_id:
            raise ValidationError('Attribute line must match product template')
        if self.attribute_line_id.attribute_id != self.attribute_id:
            raise ValidationError('Attribute line must match attribute')
        if self.value_id.attribute_id != self.attribute_id:
            raise ValidationError('Attribute value must match attribute')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
