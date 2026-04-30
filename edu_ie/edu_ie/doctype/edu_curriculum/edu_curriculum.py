# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EDUCurriculum(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		abbreviation: DF.Data | None
		curriculum_name_en: DF.Data | None
		revision_year: DF.Data | None
	# end: auto-generated types

	pass
