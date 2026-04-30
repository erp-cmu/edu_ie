# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
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
		revision_year: DF.Data
	# end: auto-generated types

	def validate(self):
		if self.revision_year:
			revision_year_int = int(self.revision_year)
			if (revision_year_int < 2500) or (revision_year_int >= 2600):  # Check Thai Year
				frappe.throw("Revision Year should be in Thai year (25XX format).")

	def autoname(self):
		# Check Thai Year
		if self.revision_year:
			try:
				revision_year_int = int(self.revision_year)
				if revision_year_int > 2500:
					self.revision_year = str(revision_year_int - 543)
			except ValueError:
				pass
		if self.abbreviation and self.revision_year:
			self.name = f"{self.abbreviation} - {self.revision_year}"
