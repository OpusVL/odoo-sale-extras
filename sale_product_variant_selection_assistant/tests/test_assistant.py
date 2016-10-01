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



class AssistantTestCommon(common.TransactionCase):
    def setUp(self):
        super(AssistantTestCommon, self).setUp()
        Partner = self.env['res.partner']
        ProductTemplate = self.env['product.template']
        ProductProduct = self.env['product.product']
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
        self.setup_add_attribute('legs', ['Pedestal', 'Four Straight', 'Three Straight'])
        self.setup_add_attribute('maturity', ['Mild', 'Medium', 'Mature', 'Extra Mature'])
        self.setup_add_attribute('wood', ['Mahogany', 'Teak', 'MDF', 'Balsa', 'Oak'])
        self.products['table'] = ProductTemplate.create(dict(
            name='TEST Table',
            attribute_line_ids=[
                (0, False, dict(
                    attribute_id=self.attributes['legs'].id,
                    value_ids=[
                        (6, False, [v.id for v in self.attr_values['legs'].values()]),
                    ],
                )),
                (0, False, dict(
                    attribute_id=self.attributes['wood'].id,
                    value_ids=[
                        (6, False, [self.attr_values['wood'][n].id for n in ['Mahogany', 'Teak']]),
                    ],
                )),
            ],
        ))
        self.products['cheese'] = ProductTemplate.create(dict(
            name='Cheese',
            attribute_line_ids=[
                (0, False, dict(
                    attribute_id=self.attributes['maturity'].id,
                    value_ids=[
                        (6, False, [self.attr_values['maturity'][n].id for n in ['Mature', 'Extra Mature']]),
                    ]
                ))
            ],
        ))
        self.orders['FIRST'] = SaleOrder.create(dict(
            partner_id = self.partners['acme'].id,
        ))

    def setup_add_attribute(self, name, value_names):
        ProductAttribute = self.env['product.attribute']
        ProductAttributeValue = self.env['product.attribute.value']
        self.attributes[name] = attr = ProductAttribute.create(dict(name='TEST '+name))
        self.attr_values[name] = values = {}
        for val in value_names:
            values[val] = ProductAttributeValue.create(dict(name=val, attribute_id=attr.id))



class AvailableValuesTests(AssistantTestCommon):
    """Test the available values method: _assistant_available_values()
    """
    at_install = False
    post_install = True

    def create_line_with_template(self, order_name, template_name):
        order = self.orders[order_name]
        return self.env['sale.order.line'].create(dict(
            order_id=order.id,
            name='NOT NULL',
            variant_assistant_product_template_id=self.products[template_name].id,
        ))

    def test_create_line_with_template(self):
        result = self.create_line_with_template('FIRST', 'cheese')

        self.assertEqual(result.order_id, self.orders['FIRST'])
        self.assertEqual(result.variant_assistant_product_template_id, self.products['cheese'])
        

    def test_cheese_maturities(self):
        """cheese._assistant_available_values(maturity) -> Mature, Extra Mature
        """
        line = self.create_line_with_template('FIRST', 'cheese')
        
        result = line._assistant_available_values(self.attributes['maturity'])

        self.assertTrue(result)
        self.assertSetEqual(frozenset(result.mapped('name')), frozenset(['Mature', 'Extra Mature']))

        
    def test_cheese_legs(self):
        """cheese._assistant_available_values(legs) empty
        """
        line = self.create_line_with_template('FIRST', 'cheese')

        result = line._assistant_available_values(self.attributes['legs'])

        self.assertFalse(result, 'returned recordset should be empty')
    

class AvailableAttributesTests(AssistantTestCommon):
    """Test the available attributes method: _assistant_attributes()
    """
    at_install = False
    post_install = True

    def test_assistant_clear_by_default(self):
        order = self.orders['FIRST']
        
        line = self.env['sale.order.line'].create(dict(
            order_id=order.id,
            name='NOT NULL',
        ))

        self.assertFalse(line.variant_assistant_product_template_id)
        self.assertFalse(line.variant_assistant_attribute_choice_ids)

        
    def test_cheese_attributes(self):
        """_assistant_attributes() yields correct attributes for cheese
        """
        line = self.env['sale.order.line'].create(dict(
            order_id=self.orders['FIRST'].id,
            name='NOT NULL',
            variant_assistant_product_template_id=self.products['cheese'].id,
        ))

        result = line._assistant_attributes()

        self.assertSetEqual(frozenset(result.mapped('name')), frozenset(['TEST maturity']),
                            "Maturity is the only valid attribute of Cheese")

        
    def test_table_attributes(self):
        """_assistant_attributes() yields correct attributes for table
        """
        line = self.env['sale.order.line'].create(dict(
            order_id=self.orders['FIRST'].id,
            name='NOT NULL',
            variant_assistant_product_template_id=self.products['table'].id,
        ))
        
        result = line._assistant_attributes()

        self.assertSetEqual(frozenset(result.mapped('name')), frozenset(['TEST legs', 'TEST wood']))

        
    def test_blank_attributes(self):
        """_assistant_attributes() yields empty set if template not set.
        """
        line = self.env['sale.order.line'].create(dict(
            order_id=self.orders['FIRST'].id,
            name='NOT NULL',
        ))

        result = line._assistant_attributes()

        self.assertEqual(result, self.env['product.attribute'])



class ValidationTests(AssistantTestCommon):
    """Test validation of variant choice assistant models.

    The validation is there to help catch bugs - onupdate methods will be dealing with this.
    """
    at_install = False
    post_install = True

    def test_cheese_with_legs_option(self):
        with self.assertRaisesRegexp(ValidationError, r"Attribute must match product template"):
            cheese = self.products['cheese']
            self.orders['FIRST'].write(dict(
                order_line=[(0, False, dict(
                    name='NOT NULL',
                    variant_assistant_product_template_id=cheese.id,
                    variant_assistant_attribute_choice_ids=[
                        (0, False, dict(attribute_id=self.attributes['legs'].id)),
                    ],
                ))],
            ))

    def test_table_with_mature_legs(self):
        with self.assertRaisesRegexp(ValidationError, r"Value must match attribute"):
            table = self.products['table']
            legs = self.attributes['legs']
            mature = self.attr_values['maturity']['Mature']
            self.orders['FIRST'].write(dict(
                order_line=[(0, False, dict(
                    name='NOT NULL',
                    variant_assistant_product_template_id=table.id,
                    variant_assistant_attribute_choice_ids=[
                        (0, False, dict(attribute_id=legs.id,
                                        value_id=mature.id)),
                    ],
                ))],
            ))

    def test_mild_cheese(self):
        """Picking mild cheese raises ValidationError.

        This is because Mild, although a valid Maturity, is not valid for this cheese.
        """
        with self.assertRaisesRegexp(ValidationError, r"Value must match product"):
            cheese = self.products['cheese']
            maturity = self.attributes['maturity']
            mild = self.attr_values['maturity']['Mild']
            self.orders['FIRST'].write(dict(
                order_line=[(0, False, dict(
                    name='NOT NULL',
                    variant_assistant_product_template_id=cheese.id,
                    variant_assistant_attribute_choice_ids=[
                        (0, False, dict(attribute_id=maturity.id, value_id=mild.id)),
                    ],
                ))]
            ))

    def test_assistant_is_optional(self):
        """It is still OK to create an order line without filling in the assistant fields.
        """
        self.orders['FIRST'].write(dict(
            order_line=[(0, False, dict(product_id=self.products['table'].product_variant_ids[0].id))],
        ))

    def test_table_with_pedestal_legs(self):
        """It is OK to choose mature cheese.
        """
        table = self.products['table']
        legs = self.attributes['legs']
        pedestal = self.attr_values['legs']['Pedestal']
        self.orders['FIRST'].write(dict(
            order_line=[(0, False, dict(
                name='NOT NULL',   # This won't matter while we're doing the onupdate
                variant_assistant_product_template_id=table.id,
                variant_assistant_attribute_choice_ids=[
                    (0, False, dict(attribute_id=legs.id, value_id=pedestal.id)),
                ],
            ))],
        ))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
