# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EDUPO(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description_en: DF.SmallText | None
		description_th: DF.SmallText | None
		po_number: DF.Int
	# end: auto-generated types

	def autoname(self):
		self.name = f"PO-{self.po_number}"
