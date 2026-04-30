# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EDUCourseCIRubric(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		cso_number: DF.Int
		description_score_0: DF.SmallText
		description_score_1: DF.SmallText
		description_score_2: DF.SmallText
		description_score_3: DF.SmallText
		description_score_4: DF.SmallText
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
