# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EDUCourse(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		abbreviation: DF.Data
		course_name_en: DF.Data
		course_name_th: DF.Data | None
		course_number: DF.Int
		course_number_abbreviation: DF.Data | None
	# end: auto-generated types

	def before_insert(self):
		self.abbreviation = self.abbreviation.upper().strip()
		self.course_number_abbreviation = str(self.course_number) + "-" + self.abbreviation

	def autoname(self):
		# self.name = (self.course_number).strip() + "-" + (self.abbreviation).upper().strip()
		self.name = str(self.course_number)
