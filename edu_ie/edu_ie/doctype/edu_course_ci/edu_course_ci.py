# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EDUCourseCI(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from edu_ie.edu_ie.doctype.edu_course_ci_cso.edu_course_ci_cso import EDUCourseCICSO
		from edu_ie.edu_ie.doctype.edu_course_ci_cso_so_map.edu_course_ci_cso_so_map import (
			EDUCourseCICSOSOMap,
		)
		from edu_ie.edu_ie.doctype.edu_course_ci_eval.edu_course_ci_eval import EDUCourseCIEval
		from edu_ie.edu_ie.doctype.edu_course_ci_rubric.edu_course_ci_rubric import EDUCourseCIRubric
		from edu_ie.edu_ie.doctype.edu_section_link.edu_section_link import EDUSectionLink

		amended_from: DF.Link | None
		course: DF.Link
		cso_evaluation_table: DF.Table[EDUCourseCIEval]
		cso_so_mapping: DF.Table[EDUCourseCICSOSOMap]
		cso_table: DF.Table[EDUCourseCICSO]
		curriculum: DF.Link
		evaluation_year: DF.Link | None
		rubric_table: DF.Table[EDUCourseCIRubric]
		sections: DF.TableMultiSelect[EDUSectionLink]
	# end: auto-generated types

	pass
