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

from openerp.tests import common
from openerp.exceptions import ValidationError

class ValidationTests(common.TransactionCase):
    """Test validation of models.
    """
    at_install = False
    post_install = True

    def setUp(self):
        super(ValidationTests, self).setUp()
        Partner = self.env['res.partner']
        ProductTemplate = self.env['product.template']
        ProductProduct = self.env['product.product']
        ProductAttribute = self.env['product.attribute']
        ProductAttributeValue = self.env['product.attribute.value']
        ProductAttributeLine = self.env['product.attribute.line']
        SaleOrder = self.env['sale.order']
        self.partners = {}
        self.products = {}
        self.attributes = {}
        self.attr_values = {}
        self.orders = {}
        
        self.partners['acme'] = Partner.create(dict(
            name='TEST ACME',
            is_company=True,
            customer=True,
            supplier=False,
        ))
        self.attributes['legs'] = ProductAttribute.create(dict(name='TEST Legs'))
        self.attr_values['legs'] = {}
        for name in ['Pedestal', 'Four Straight', 'Three Straight']:
            self.attr_values[name] = ProductAttributeValue.create(dict(name=name, attribute_id=self.attributes['legs'].id))
        self.products['table'] = ProductTemplate.create(dict(
            name='TEST Table',
            attribute_line_ids=[
                (0, False, dict(
                    attribute_id=self.attributes['legs'].id,
                    value_ids=[
                        (6, False, [v.id for v in self.attr_values['legs'].values()]),
                    ],
                )),
            ],
        ))
        self.products['cheese'] = ProductTemplate.create(dict(
            name='Cheese',
        ))
        self.orders['FIRST'] = SaleOrder.create(dict(
            partner_id = self.partners['acme'].id,
        ))
        #import pdb ; pdb.set_trace()

    def test_cheese_with_pedestal_legs(self):
        with self.assertRaisesRegexp(ValidationError, r"Attribute line must match product template"):
            cheese = self.products['cheese']
            self.orders['FIRST'].write(dict(
                order_line=[(0, False, dict(
                    product_id=cheese.product_variant_ids[0].id,
                ))],
            ))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
