# -*- coding    : utf-8 -*-
from openerp import models, api, fields, _
from openerp.addons import decimal_precision as dp


class product_template_extend(models.Model):
	_inherit = 'product.template'
	
	
	@api.one
	@api.depends('warehouse_id')
	def _stock_usable_qty(self):
		product_id = self.env['product.product'].search_read([('product_tmpl_id', '=', self.id)], ['id'])
		warehouse_id = self.env.context.get('warehouse_id', False)
		lot_stock = self.env['stock.warehouse'].search_read([('id', '=', warehouse_id)], ['lot_stock_id'])
		for a in lot_stock:
			stock_quant = self.env['stock.quant'].search_read([('location_id', '=', a['lot_stock_id'][0])], ['location_id', 'product_id', 'qty'])
			for b in stock_quant:
				product_on_stock_id = b['product_id'][0]
				product_qty_stock = b['qty']
				if (product_id[0]['id'] == product_on_stock_id) and (a['lot_stock_id'][0] == b['location_id'][0]):
					self.qty_available_stock = product_qty_stock

	warehouse_id = fields.Reference([('stock.warehouse', 'Warehouse')])
	qty_available_stock = fields.Float(compute='_stock_usable_qty', string='Saldo Stock')



