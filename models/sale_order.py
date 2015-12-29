# -*- coding    : utf-8 -*-
from openerp import models, api, fields, _


class sale_order_line_extend(models.Model):
    _inherit = "sale.order.line"
    

    virtual_available2 = fields.Float(string='Saldo Stock', store=True, help="Este campo es solo informativo")
    warehouse_id = fields.Reference([('stock.warehouse', 'Warehouse')])
    
    @api.multi
    @api.onchange('product_id')
    def product_id_change_with_wh(
            self, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, warehouse_id=False,
            virtual_available2=False, order_id=False, context=None):
        """
        Se sobreescribe el metodo product_id_change_with_wh para agregar
        las cantidades en stock del producto
        """
        
        res = super(sale_order_line_extend, self).product_id_change_with_wh(
            pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos,
            name=name, partner_id=partner_id, lang=lang, update_tax=update_tax,
            date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag,
            warehouse_id=warehouse_id, context=context)
        
        product_obj = self.env['product.product']
        product = product_obj.browse(product)
        
        warning_msgs = ''
        if product and res['value']['product_uos_qty']:            
            if res['value']['product_uos_qty'] > product.qty_available:
                warn_msg = \
                    _('You plan to sell %.2f %s but you only have %.2f %s '
                      'available !\nThe real stock is %.2f %s. (without '
                      'reservations)') % \
                    (qty, product.uom_id.name,
                        max(0, product.virtual_available), product.uom_id.name,
                        max(0, product.qty_available), product.uom_id.name)
                warning_msgs += _("Not enough stock ! : ") + warn_msg + "\n\n"
                            
        lot_stock = self.env['stock.warehouse'].search_read([('id', '=', warehouse_id)], ['lot_stock_id'])
        for a in lot_stock:
            stock_quant = self.env['stock.quant'].search_read([('location_id', '=', a['lot_stock_id'][0])], ['location_id', 'product_id', 'qty'])
            for b in stock_quant:
                product_on_stock_id = b['product_id'][0]
                product_qty_stock = b['qty']
                if (product.id == product_on_stock_id) and (a['lot_stock_id'][0] == b['location_id'][0]):
                    if product_qty_stock < 0 or (a['lot_stock_id'][0] != b['location_id'][0]):
                        warn_msg = \
                            _('Ud. va a vender un producto que no tiene en stock! '
                              'Seleccione otro almacen')
                        warning_msgs += _("No disponible ! : ") + warn_msg + "\n\n"
                        res['value'].update({'virtual_available2': 0.0})
                    else:
                        res['value'].update({'virtual_available2': (product_qty_stock - qty)})
        
        if warning_msgs:
            warning = {
                'title': _('Configuration Error!'),
                'message': warning_msgs
            }
            res['warning'] = warning
            
        return res