# -*- coding    : utf-8 -*-
from openerp import models, fields, api, osv

class sale_order_line_extend(models.Model):
    _inherit = "sale.order.line"
    
        
    virtual_available2 = fields.Float(string='Saldo Stock', store=True, help="Este campo es solo informativo")
    
    
    def product_id_change_with_wh(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, warehouse_id=False,
            virtual_available2=False, context=None):
        
        res = super(sale_order_line_extend, self).product_id_change_with_wh(
            cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, packaging, fiscal_position, flag,
            warehouse_id=warehouse_id, context=context)
        
        product_obj = self.pool.get('product.product')
        product_obj = product_obj.browse(cr, uid, product, context=context)
        
        res['value'].update({'virtual_available2': (product_obj.virtual_available - qty)})
        return res