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
		number: DF.Int
		po: DF.Link
		tk: DF.Link | None
	# end: auto-generated types

	def autoname(self):
		po = self.po 
		tk = self.tk or ""
		if tk:
			name = f"PI {po}.{tk}"
		else:
			name = f"PI {po}"
		number = self.number 
		if number > 1:
			name = name + f" ({number})"

		# Check is this is already exists in the database
		if frappe.db.exists("EDUPI", name):
			frappe.throw(f"PI {po}.{tk} ({number}) already exists. Please change the number.")
		self.name = name
