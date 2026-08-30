# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EDUEvalCollection(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from edu_ie.edu_ie.doctype.edu_eval_collection_table.edu_eval_collection_table import (
			EDUEvalCollectionTable,
		)

		amended_from: DF.Link | None
		clo: DF.Int
		course: DF.Link
		curriculum: DF.Link | None
		evaluation_year: DF.Link | None
		floor_c1: DF.Float
		floor_c2: DF.Float
		floor_c3: DF.Float
		floor_c4: DF.Float
		scores: DF.Table[EDUEvalCollectionTable]
	# end: auto-generated types

	def autoname(self):

		# TODO: Check if CLO actually exists in the evaluation of that year first
		name = f"{self.curriculum}-{self.evaluation_year}-{self.course}-CLO{self.clo}"

		if frappe.db.exists("EDU Eval Collection", name):
			frappe.throw(
				f"An evaluation collection for curriculum {self.curriculum}, evaluation year {self.evaluation_year}, course {self.course}, and CLO {self.clo} already exists."
			)
		self.name = name
