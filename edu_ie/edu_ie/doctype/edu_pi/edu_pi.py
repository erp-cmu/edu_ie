# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe


class EDUPI(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		curriculum: DF.Link
		description_en: DF.SmallText | None
		description_th: DF.SmallText | None
		pi_number: DF.Int
		po: DF.Link
		tk: DF.Link | None
	# end: auto-generated types

	def autoname(self):
		po_number = frappe.get_value("EDU PO", self.po, "po_number")
		tk = self.tk or ""
		if tk:
			tk_number = frappe.get_value("EDU TK", self.tk, "tk_number")
			name = f"PI {po_number}.{tk_number}"
		else:
			name = f"PI {po_number}"
		pi_number = self.pi_number
		if pi_number > 1:
			name = name + f" ({pi_number})"

		name = f"{self.curriculum}-{name}"

		# Check is this is already exists in the database
		if frappe.db.exists("EDU PI", name):
			frappe.throw(
				f"PI {po_number}.{tk_number} ({pi_number}) already exists. Please change the number."
			)
		self.name = name
