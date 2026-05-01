# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document


class EDUEvaluationYear(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		evaluation_year_en: DF.Int
		evaluation_year_th: DF.Int
	# end: auto-generated types

	def autoname(self):
		# Check Thai Year
		if self.evaluation_year_th is None or self.evaluation_year_th == "" or self.evaluation_year_th == 0:
			frappe.throw("Evaluation Year (Thai) must be set.")
			return

		evaluation_year_th_int = int(self.evaluation_year_th)
		if (evaluation_year_th_int < 2500) or (evaluation_year_th_int >= 2700):  # Check Thai Year
			frappe.throw("Evaluation Year should be in Thai year (25XX format).")
		else:
			# Convert Thai Year to English Year
			self.evaluation_year_en = evaluation_year_th_int - 543

		self.name = str(self.evaluation_year_en)
