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
from openerp.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    variant_assistant_product_template_id = fields.Many2one(
        string='Product Template',
        comodel_name='product.template',
        help='To use the variant assistant, select the top-level product template here',
    )

    variant_assistant_attribute_choice_ids = fields.One2many(
        comodel_name='sale.order.line.assistant.attribute.choice',
        inverse_name='sale_order_line_id',
        string='Choose attributes',
        invisible=[('variant_assistant_attribute_choice_ids', '=', False)],
        help='Now select the attribute values.  Once you select enough attributes to uniquely identify the product, it will be entered in the Product field',
    )

    
    @api.returns('product.attribute')
    def _assistant_attributes(self):
        """Return the attributes available on the chosen product template.
        """
        return self.variant_assistant_product_template_id.attribute_line_ids.mapped('attribute_id')

    
    @api.returns('product.attribute.value')
    def _assistant_available_values(self, attribute):
        """Return the values available for the given attribute on the chosen product template.
        """
        template = self.variant_assistant_product_template_id
        return attribute.value_ids.filtered(lambda v: v in template.attribute_line_ids.mapped('value_ids'))


    def _chosen_values(self):
        """Return the values the user has chosen.
        """
        choices = self.variant_assistant_attribute_choice_ids.filtered(lambda c: c.value_id)
        return choices.mapped('value_id')
        

    def _assistant_resolve_variant(self):
        """Return a unique variant matching chosen template and attribute choices.
        """
        empty_variants = self.env['product.product']
        template = self.variant_assistant_product_template_id
        if not template:
            return empty_variants
        values = self._chosen_values()
        domain = [('sale_ok', '=', True), ('product_tmpl_id', '=', template.id)]
        domain.extend([('attribute_value_ids', '=', v) for v in values.ids])
        variants = empty_variants.search(domain)
        #variants = template.product_variant_ids.filtered(lambda v: v.attribute_value_ids >= values)
        if len(variants) != 1:
            return empty_variants
        return variants

    
    @api.onchange('variant_assistant_product_template_id')
    def _onchange_variant_assistant_product_template_id(self):
        """Populate the choices table with options appropriate to chosen template.
        """
        changes = [(2, i, False) for i in self.variant_assistant_attribute_choice_ids.ids]
        attrs = self._assistant_attributes()
        for attr in attrs:
            choice_data = {"attribute_id": attr.id}
            options = self._assistant_available_values(attr)
            if len(options) == 1:
                choice_data['value_id'] = options.id
            changes.append((0, False, choice_data))
        self.update({'variant_assistant_attribute_choice_ids': changes})


    @api.onchange('variant_assistant_attribute_choice_ids')
    def _onchange_variant_assistant_attribute_choice_ids(self):
        """Resolve the variant when updates to choices have been completed.
        """
        self.product_id = self._assistant_resolve_variant()



class SaleOrderLineAssistantAttributeChoice(models.Model):
    _name = 'sale.order.line.assistant.attribute.choice'

    sale_order_line_id = fields.Many2one(
        string='Sale Order Line',
        comodel_name='sale.order.line',
    )
    
    product_template_id = fields.Many2one(
        string='Product Template',
        readonly=True,
        related='sale_order_line_id.variant_assistant_product_template_id',
    )
    
    attribute_id = fields.Many2one(
        string='Attribute',
        comodel_name='product.attribute',
        required=True,
    )

    value_id = fields.Many2one(
        string='Value',
        comodel_name='product.attribute.value',
    )

    
    @api.one
    @api.constrains('product_template_id', 'attribute_id', 'value_id')
    def _check_attributes(self):
        """Make sure the attributes choices list is sane.

        This is largely to catch errors let through by any holes there
        might be in the domain filtering.  In general, if these are producing
        errors to the user, the domain filtering probably needs adjusting.

        It also guards against users trying to force garbage through, and
        errors in records altered via API calls and tests.
        """
        if self.attribute_id not in self.product_template_id.attribute_line_ids.mapped('attribute_id'):
            raise ValidationError('Attribute must match product template')
        if self.value_id.attribute_id != self.attribute_id:
            raise ValidationError('Value must match attribute')
        if self.value_id not in self.product_template_id.attribute_line_ids.mapped('value_ids'):
            raise ValidationError("Value must match product")





# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
