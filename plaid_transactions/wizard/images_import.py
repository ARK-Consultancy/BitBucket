from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import UserError


class PlaidAccount(models.TransientModel):
    _name = 'product.image'
    _description = 'Import Product Images'

    file_name = fields.Binary("File Name")
    
    def import_images(self):
	    try:
		book = xlrd.open_workbook(filename=self.file_name)
	    except FileNotFoundError:
		raise UserError('No such file or directory found. \n%s.' % self.file_name)
	    except xlrd.biffh.XLRDError:
		raise UserError('Only excel files are supported.')
	    for sheet in book.sheets():
		try:
		    line_vals = []
		    if sheet.name == 'Sheet1':
		        for row in range(sheet.nrows):
		            if row >= 1:
		                row_values = sheet.row_values(row)
		                vals = self._create_journal_entry(row_values)
		                line_vals.append((0, 0, vals))
		    if line_vals:
		        date = self.date
		        ref = self.jv_ref
		        self.env['account.move'].create({
		            'date': date,
		            'ref': ref,
		            'journal_id': self.jv_journal_id.id,
		            'line_ids': line_vals
		        })
		except IndexError:
		    pass
