# # -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from datetime import datetime, timedelta

STATES = [('open','Open'), ('baut','BAUT'), ('bast','BAST'), ('close','Close'), ('cancel','Cancel')]

class bill_plan(models.Model):
	_name = 'vit_project_billplan.bill_plan'
	_inherit = "vit_project_billplan.bill_plan"

	no_bast = fields.Char(string="Nomor BAST", states={'bast': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'baut': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
	no_baut = fields.Char(string="Nomor BAUT", states={'baut': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'bast': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
	bast_date = fields.Date( string="BAST Date", help="", states={'bast': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'baut': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
	baut_date = fields.Date( string="BAUT Date", help="", states={'baut': [('readonly', False),('required', True)], 'open': [('readonly', True)], 'bast': [('readonly', True)], 'close': [('readonly', True)], 'cancel': [('readonly', True)]})
	description = fields.Text(string="Deskripsi Fase")
	state = fields.Selection(string="State", selection=STATES, required=True, readonly=True, default=STATES[0][0])

	@api.multi
	def action_baut(self):
		self.write({'state': STATES[1][0]})
	@api.multi
	def action_bast(self):
		self.write({'state': STATES[2][0]})
	@api.multi
	def action_close(self):
		self.write({'state': STATES[3][0]})
	@api.multi
	def action_cancel(self):
		self.write({'state': STATES[4][0]})

class bill_planxlsx(models.AbstractModel):
	_name = 'report.vit_report_aging_billplan.bill_plan_xlsx'
	_inherit = 'report.report_xlsx.abstract'

	bill_id = fields.Many2one(comodel_name="vit_project_billplan.bill_plan")
	
	def generate_xlsx_report(self, workbook, data, lines):
		print("lines", lines, data)
		format0 = workbook.add_format({'font_size':14,'align':'vcenter','bold':True})
		# format0.set_font_name('Report Billplan')
		format1 = workbook.add_format({'font_size':10,'align':'vcenter', 'bold':True})
		format2 = workbook.add_format({'font_size':10,'align':'vcenter'})
		date_1 = datetime.strftime(lines.date, '%Y-%m-%d')
		plan_date_1 = datetime.strftime(lines.plan_date, '%Y-%m-%d')
		baut_date_1 = datetime.strftime(lines.baut_date, '%Y-%m-%d')
		bast_date_1 = datetime.strftime(lines.bast_date, '%Y-%m-%d')
		y = lines.project_id.total_revenue
		x = lines.amount
		z = y-x
		bast_date_2 = str(lines.bast_date)
		date_2 = str(lines.date)
		baut_date_2 = str(lines.baut_date)
		start = datetime.strptime(bast_date_2, '%Y-%m-%d')
		sub = datetime.strptime(date_2, '%Y-%m-%d')
		receive_date = start-sub
		# lines = self.env['vit_project_billplan.bill_plan'].browse(self.id)
		sheet = workbook.add_worksheet('Report Billplan')
		sheet.write(0, 0, 'Report Billplan', format0)	
		sheet.write(4, 0, 'ID Project', format1)
		sheet.write(4, 1, 'Tanggal Periode', format1)
		sheet.write(4, 2, 'Unit', format1)
		sheet.write(4, 3, 'Wilayah', format1)
		sheet.write(4, 4, 'Bisnis', format1)
		sheet.write(4, 5, 'Jenis Project', format1)
		sheet.write(4, 6, 'Customer', format1)
		sheet.write(4, 7, 'Afiliasi', format1)
		sheet.write(4, 8, 'Nomor Billplan', format1)
		sheet.write(4, 9, 'Reference', format1)
		sheet.write(4, 10, 'Tanggal Billplan', format1)
		sheet.write(4, 11, 'Rencana Penagihan', format1)
		sheet.write(4, 12, 'Description Fase', format1)
		sheet.write(4, 13, 'Nilai Revenue', format1)
		sheet.write(4, 14, 'Nilai ID Project', format1)
		sheet.write(4, 15, 'Sisa ID Project', format1)
		sheet.write(4, 16, 'Nomor BAUT', format1)
		sheet.write(4, 17, 'Tanggal BAUT', format1)
		sheet.write(4, 18, 'Nomor BAST', format1)
		sheet.write(4, 19, 'Tanggal BAST', format1)
		sheet.write(4, 20, 'Status Fase', format1)
		sheet.write(4, 21, 'Umur Billplan(Days)', format1)
		# for row in lines:
		
		# for xi in range(0,22):
		sheet.write(5, 0, lines.name, format2)
		sheet.write(5, 1, date_1, format2)
		sheet.write(5, 2, lines.unit_id.name, format2)
		sheet.write(5, 3, lines.analytic_tag_ids.name, format2)
		sheet.write(5, 4, lines.analytic_tag_ids_b.name, format2)
		sheet.write(5, 5, lines.project_id.project_type_id.name, format2)
		sheet.write(5, 6, lines.project_id.partner_id.name, format2)
		if 'Telkomsel' in lines.project_id.partner_id.name or 'telkomsel' in lines.project_id.partner_id.name or 'TELKOMSEL' in lines.project_id.partner_id.name: 
			sheet.write(5, 7, 'Telkomsel', format2)
		else:
			sheet.write(5, 7, 'Non Telkomsel', format2)
		# if 'T'lines.project_id.partner_id.name != 'Telkomsel' and lines.project_id.partner_id.name != 'telkomsel' and lines.project_id.partner_id.name != 'TELKOMSEL':	
		# sheet.write(5, 8, '[' + lines.analytic_account_id.name + '] ' + lines.project_id.name '-' + lines.analytic_account_id.partner_id.name, format2)
		sheet.write(5, 8, f'[ {lines.analytic_account_id.name}] {lines.project_id.name}', format2)
		sheet.write(5, 9, lines.reference, format2)
		sheet.write(5, 10, date_1, format2)
		sheet.write(5, 11, plan_date_1, format2)
		sheet.write(5, 12, lines.description, format2)
		sheet.write(5, 13,f'Rp ' '{0:,.2f}'.format(x), format2)
		sheet.write(5, 14,f'Rp ' '{0:,.2f}'.format(y), format2)
		sheet.write(5, 15,f'Rp ' '{0:,.2f}'.format(z), format2)
		sheet.write(5, 16, lines.no_baut, format2)
		sheet.write(5, 17, baut_date_1, format2)
		sheet.write(5, 18, lines.no_bast, format2)
		sheet.write(5, 19, bast_date_1, format2)
		# @api.onchange('state')
		# def on_change_type(lines):
		if lines.state == 'open' and lines.no_baut == False:
			sheet.write(5, 20, 'Fase 1', format2)
		if lines.no_baut == False and lines.state == 'baut':
			sheet.write(5, 20, 'Fase 1', format2)
		if lines.no_baut == True:
			sheet.write(5, 20, 'Fase 2', format2)
		if lines.state == 'bast' and lines.no_bast == False:
			sheet.write(5, 20, 'Fase 2', format2)
		if lines.no_bast == True:
			sheet.write(5, 20, 'Fase 3', format2)
		if lines.state == 'close':
			sheet.write(5, 20, 'Fase 3', format2)
		if lines.no_bast == False:
			sheet.write(5, 21, 'BAST belum selesai', format2)
		else:	
			sheet.write(5, 21, receive_date, format2)