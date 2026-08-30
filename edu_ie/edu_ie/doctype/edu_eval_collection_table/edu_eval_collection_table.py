# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EDUEvalCollectionTable(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		score_raw: DF.Float
		score_scaled: DF.Float
		section: DF.Link | None
		student_id: DF.Link
	# end: auto-generated types

	pass
