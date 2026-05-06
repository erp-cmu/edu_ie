# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EDUSO(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description_en: DF.SmallText | None
		description_th: DF.SmallText | None
		so_number: DF.Int
	# end: auto-generated types

	def autoname(self):
		self.name = f"SO-{self.so_number}"
