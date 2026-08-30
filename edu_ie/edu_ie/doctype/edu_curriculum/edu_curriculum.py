# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EDUCurriculum(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		abbreviation: DF.Data
		curriculum_name_en: DF.Data
		revision_year_en: DF.Int
		revision_year_th: DF.Int
	# end: auto-generated types

	def autoname(self):
		# Check Thai Year
		if self.revision_year_th:
			revision_year_th_int = int(self.revision_year_th)
			if (revision_year_th_int < 2500) or (revision_year_th_int >= 2700):  # Check Thai Year
				frappe.throw("Revision Year should be in Thai year (25XX format).")
			else:
				# Convert Thai Year to English Year
				self.revision_year_en = str(revision_year_th_int - 543)

		# Set name as abbreviation and revision year
		if self.abbreviation and self.revision_year_th:
			self.name = f"{self.abbreviation}-{self.revision_year_en}"
