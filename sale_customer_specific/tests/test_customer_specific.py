# -*- coding: utf-8 -*-

##############################################################################
#
# Customer-specific products
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

class CustomerSpecificTestCommon(common.TransactionCase):
    """Common arrangement and helpers for testing the customer unique logic.

    products['cheese'] is configured to be customer specific but to have no valid customers.

    products['table'] is configured to be customer specific, with only partners['acme_anvils'] able to buy

    products['chicken'] is configured as not customer-specific.
    """
    def setUp(self):
        super(CustomerSpecificTestCommon, self).setUp()
        Partner = self.env['res.partner']
        ProductTemplate = self.env['product.template']
        ProductProduct = self.env['product.product']
        SaleOrder = self.env['sale.order']
        self.partners = {}
        self.products = {}
        self.attributes = {}
        self.attr_values = {}
        self.orders = {}
        
        self.partners['acme_anvils'] = Partner.create(dict(
            name='TEST ACME ANVILS',
            is_company=True,
            customer=True,
            supplier=False,
        ))
        self.partners['acme_tunnels'] = Partner.create(dict(
            name='TEST ACME INSTANT TUNNELS',
            is_company=True,
            customer=True,
            supplier=False,
        ))
        self.setup_add_attribute('legs', ['Pedestal', 'Four Straight', 'Three Straight'])
        self.setup_add_attribute('maturity', ['Mild', 'Medium', 'Mature', 'Extra Mature'])
        self.setup_add_attribute('wood', ['Mahogany', 'Teak', 'MDF', 'Balsa', 'Oak'])
        self.setup_add_attribute('upbringing', ['Free Range', 'Battery'])
        self.products['table'] = ProductTemplate.create(dict(
            name='TEST Table',
            is_customer_specific=True,
            specific_customer_ids=[(6, False, [self.partners['acme_anvils'].id])],
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
            is_customer_specific=True,
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
            partner_id = self.partners['acme_anvils'].id,
        ))
        self.products['chicken'] = ProductTemplate.create(dict(
            name='Chicken',
            attribute_line_ids=[
                (0, False, dict(
                    attribute_id=self.attributes['maturity'].id,
                    value_ids=[
                        (6, False, [self.attr_values['maturity'][n].id for n in ['Mature', 'Extra Mature']]),
                    ]
                ))
            ],
        ))


    def setup_add_attribute(self, name, value_names):
        """Add an attribute and its values to the database.

        'TEST ' is prepended to name.

        The attribute object is added to self.attributes[name]

        For each val_name in value_names, an attribute value is created with val_name,
        attached to self.attributes[name], and registered under self.attr_values[name][val_name]
        for use in tests.
        """
        ProductAttribute = self.env['product.attribute']
        ProductAttributeValue = self.env['product.attribute.value']
        self.attributes[name] = attr = ProductAttribute.create(dict(name='TEST '+name))
        self.attr_values[name] = values = {}
        for val in value_names:
            values[val] = ProductAttributeValue.create(dict(name=val, attribute_id=attr.id))



class ProductTemplateCustomerSpecificTests(CustomerSpecificTestCommon):
    at_install = False
    post_install = True


    def test_chicken_is_not_customer_specific(self):
        """Chicken is not customer specific (i.e. the default is correct)"""
        result = self.products['chicken'].is_customer_specific

        self.assertFalse(result)
        

    def test_chicken_may_be_sold_to_acme_tunnels(self):
        """chicken may be sold to acme_tunnels

        Chicken is not marked as company-specific.
        """
        result = self.products['chicken'].may_be_sold_to_customer(self.partners['acme_tunnels'])

        self.assertTrue(result)


    def test_chicken_may_be_sold_to_acme_anvils(self):
        """chicken may be sold to acme_anvils

        Chicken is not marked as company-specific.
        """
        result = self.products['chicken'].may_be_sold_to_customer(self.partners['acme_anvils'])

        self.assertTrue(result)


    def test_cheese_is_customer_specific(self):
        """Cheese is customer specific, with no permitted customers."""
        result = self.products['cheese']

        self.assertTrue(result.is_customer_specific, "is_customer_specific is True")
        self.assertEqual(len(result.specific_customer_ids), 0, "specific_customer_ids is empty")


    def test_cheese_may_not_be_sold_to_acme_anvils(self):
        """Cheese cannot be sold to ACME Anvils """
        result = self.products['cheese'].may_be_sold_to_customer(self.partners['acme_anvils'])

        self.assertFalse(result)


    def test_cheese_may_not_be_sold_to_acme_tunnels(self):
        """Cheese cannot be sold to ACME Instant Tunnels"""
        result = self.products['cheese'].may_be_sold_to_customer(self.partners['acme_tunnels'])

        self.assertFalse(result)


    def test_table_is_customer_specific(self):
        """Table is specific to acme_anvils only.
        """
        result = self.products['table']

        self.assertTrue(result.is_customer_specific)
        self.assertEqual(result.specific_customer_ids, self.partners['acme_anvils'])


    def test_table_may_be_sold_to_acme_anvils(self):
        """Table can be sold to ACME Anvils"""

        result = self.products['table'].may_be_sold_to_customer(self.partners['acme_anvils'])

        self.assertTrue(result)


    def test_table_may_not_be_sold_to_acme_tunnels(self):
        """Table can be sold to ACME Anvils"""

        result = self.products['table'].may_be_sold_to_customer(self.partners['acme_tunnels'])

        self.assertFalse(result)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
