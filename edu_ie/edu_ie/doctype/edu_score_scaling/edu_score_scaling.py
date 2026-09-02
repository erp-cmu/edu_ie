# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EDUScoreScaling(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		scaling_method: DF.Literal["Threshold", "Linear"]
		score_max: DF.Float
		score_min: DF.Float
		scoring_name: DF.Data
		threshold_1: DF.Float
		threshold_2: DF.Float
		threshold_3: DF.Float
		threshold_4: DF.Float
	# end: auto-generated types

	def autoname(self):

		tmp = f"{self.scoring_name.strip()} - {self.scaling_method.strip()}"
		count = frappe.db.count("EDU Score Scaling", {"name": tmp})
		if count > 0:
			self.name = f"{tmp}-{count + 1}"
			frappe.msgprint(
				f"Score Scaling with the name '{self.scoring_name}' and scaling method '{self.scaling_method}' already exists. The new name will be '{self.name}'."
			)
		else:
			self.name = f"{tmp}"

	def before_save(self):
		check_scaling_consistency(
			self.scaling_method,
			self.score_max,
			self.score_min,
			self.threshold_1,
			self.threshold_2,
			self.threshold_3,
			self.threshold_4,
		)


def check_scaling_consistency(
	scaling_method, score_max, score_min, threshold_1, threshold_2, threshold_3, threshold_4
):
	# Validate that score_min is less than score_max
	if score_min >= score_max:
		frappe.throw("score_min must be less than score_max.")

	# Validate that threshold values are in ascending order if scaling_method is "Threshold"
	if scaling_method == "Threshold":
		if not all(
			[
				threshold_1 is not None,
				threshold_2 is not None,
				threshold_3 is not None,
				threshold_4 is not None,
			]
		):
			frappe.throw("All threshold values must be provided for Threshold scaling method.")

		if threshold_4 <= threshold_3 or threshold_3 <= threshold_2 or threshold_2 <= threshold_1:
			frappe.throw(
				"Threshold values must be in ascending order: threshold_1 < threshold_2 < threshold_3 < threshold_4."
			)
	elif scaling_method == "Linear":
		threshold_1 = 0.0
		threshold_2 = 0.0
		threshold_3 = 0.0
		threshold_4 = 0.0
	else:
		frappe.throw("Unknown scaling method.")
