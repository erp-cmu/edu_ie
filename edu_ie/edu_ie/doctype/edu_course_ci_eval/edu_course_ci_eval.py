# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EDUCourseCIEval(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		assessment_tool: DF.Link
		average_score: DF.Float
		cso_number: DF.Int
		number_student_score_0: DF.Int
		number_student_score_1: DF.Int
		number_student_score_2: DF.Int
		number_student_score_3: DF.Int
		number_student_score_4: DF.Int
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		question: DF.Data | None
	# end: auto-generated types

	pass
