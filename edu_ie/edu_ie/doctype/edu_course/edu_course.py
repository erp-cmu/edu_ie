# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EDUCourse(Document):
	def before_insert(self):
		self.course_number_abbreviation = (
			(self.course_number).strip() + " - " + (self.abbreviation).upper().strip()
		)

	def autoname(self):
		self.name = (self.course_number).strip() + " - " + (self.abbreviation).upper().strip()
