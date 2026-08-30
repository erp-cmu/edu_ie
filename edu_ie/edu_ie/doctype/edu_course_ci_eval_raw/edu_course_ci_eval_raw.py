# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EDUCourseCIEvalRaw(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from edu_ie.edu_ie.doctype.edu_section_link.edu_section_link import EDUSectionLink
		from frappe.types import DF

		amended_from: DF.Link | None
		course: DF.Link | None
		curriculum: DF.Link | None
		evaluation_year: DF.Link | None
		sections: DF.TableMultiSelect[EDUSectionLink]
	# end: auto-generated types

	pass
