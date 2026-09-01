# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
import re

import frappe
from frappe.model.document import Document


class EDUStudent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		curriculum: DF.Link
		firstname_en: DF.Data | None
		firstname_th: DF.Data
		lastname_en: DF.Data | None
		lastname_th: DF.Data
		student_id: DF.Data
	# end: auto-generated types

	def autoname(self):
		# Validate student_id format (9-digit number starting with 6 or 7)
		student_id_pattern = r"^[6|7]\d{8}$"
		if not re.match(student_id_pattern, self.student_id):
			frappe.throw("Invalid Student ID format. Please enter a 9-digit number.")

		# Set name as student_id
		if frappe.db.exists("EDU Student", self.student_id):
			frappe.throw(f"Student ID '{self.student_id}' already exists.")
		self.name = self.student_id
