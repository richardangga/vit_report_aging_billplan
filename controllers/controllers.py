# -*- coding: utf-8 -*-
from odoo import http

# class VitReportAgingBillplan(http.Controller):
#     @http.route('/vit_report_aging_billplan/vit_report_aging_billplan/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_report_aging_billplan/vit_report_aging_billplan/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_report_aging_billplan.listing', {
#             'root': '/vit_report_aging_billplan/vit_report_aging_billplan',
#             'objects': http.request.env['vit_report_aging_billplan.vit_report_aging_billplan'].search([]),
#         })

#     @http.route('/vit_report_aging_billplan/vit_report_aging_billplan/objects/<model("vit_report_aging_billplan.vit_report_aging_billplan"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_report_aging_billplan.object', {
#             'object': obj
#         })