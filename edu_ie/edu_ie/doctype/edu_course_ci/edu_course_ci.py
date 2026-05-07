# Copyright (c) 2026, IE and contributors
# For license information, please see license.txt

# import frappe
import os
import random
import re
import shutil
import string

import frappe
from frappe.model.document import Document
from frappe.utils import get_site_path, getdate, now


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

		abet1_file: DF.Attach | None
		abet2_file: DF.Attach | None
		amended_from: DF.Link | None
		course: DF.Link
		cso_evaluation_table: DF.Table[EDUCourseCIEval]
		cso_so_mapping: DF.Table[EDUCourseCICSOSOMap]
		cso_table: DF.Table[EDUCourseCICSO]
		curriculum: DF.Link
		discussion_course: DF.LongText | None
		evaluation_year: DF.Link
		raw_score_1: DF.Attach | None
		raw_score_2: DF.Attach | None
		raw_score_3: DF.Attach | None
		raw_score_4: DF.Attach | None
		rubric_table: DF.Table[EDUCourseCIRubric]
		sections: DF.TableMultiSelect[EDUSectionLink]
		student_work_1: DF.Attach | None
		student_work_2: DF.Attach | None
		student_work_3: DF.Attach | None
		student_work_4: DF.Attach | None
		student_work_5: DF.Attach | None
		student_work_6: DF.Attach | None
	# end: auto-generated types

	def autoname(self):
		# Check existing documents with the same course and evaluation year
		existing_docs = frappe.db.get_all(
			"EDU Course CI",
			filters={
				"course": self.course,
				"evaluation_year": self.evaluation_year,
				"curriculum": self.curriculum,
			},
			fields=["name"],
		)
		num_existing = len(existing_docs)

		if self.course and self.evaluation_year:
			self.name = f"{self.course}-{self.curriculum}-{self.evaluation_year}-V{num_existing + 1}"

		else:
			frappe.throw("Course and Evaluation Year must be set to generate the document name.")

	# Calculate the average score based on the cso_evaluation_table
	def calculate_average_score(self):
		if self.cso_evaluation_table and len(self.cso_evaluation_table) > 0:
			for eval_item in self.cso_evaluation_table:
				item_total_student = (
					eval_item.number_student_score_0
					+ eval_item.number_student_score_1
					+ eval_item.number_student_score_2
					+ eval_item.number_student_score_3
					+ eval_item.number_student_score_4
				)
				item_total_weighted_score = (
					eval_item.number_student_score_0 * 0
					+ eval_item.number_student_score_1 * 1
					+ eval_item.number_student_score_2 * 2
					+ eval_item.number_student_score_3 * 3
					+ eval_item.number_student_score_4 * 4
				)
				if item_total_student == 0:
					frappe.throw(f"No students evaluated for item '{eval_item.eval_item}'.")

				eval_item.total_students = item_total_student
				eval_item.average_score = item_total_weighted_score / item_total_student

	def change_filenames(self):
		attachment_fields = [
			"abet1_file",
			"abet2_file",
			"raw_score_1",
			"raw_score_2",
			"raw_score_3",
			"raw_score_4",
			"student_work_1",
			"student_work_2",
			"student_work_3",
			"student_work_4",
			"student_work_5",
			"student_work_6",
		]

		for field in attachment_fields:
			if self.get(field):
				self.change_filename_field(field)

	def change_filename_field(self, field, folder="edu_ie"):
		cur_filepath = self.get(field) or None

		if cur_filepath and not is_already_renamed(cur_filepath):
			if not cur_filepath.startswith(("/private/files/", "/files/")):
				frappe.throw("File path is not valid")

			split = os.path.split(cur_filepath)
			# path_prefix with leading "/" but not trailing "/"
			path_prefix, cur_filename = split
			# Add folder and trailing "/" to align with the convention
			path_prefix = path_prefix + "/" + folder + "/"

			# Ensure the target directory exists
			site_path = get_site_path()  # './SITENAME'
			target_directory = f"{site_path}{path_prefix}"
			os.makedirs(target_directory, exist_ok=True)

			try:
				cur_file_doc = frappe.get_last_doc(
					"File",
					filters={"file_url": cur_filepath},
				)
				if cur_file_doc:
					new_filename = gen_filename(cur_filename, self.name, field)
					new_filepath = f"{path_prefix}{new_filename}"

					cur_filepath_site = (
						f"{site_path}{cur_filepath}"  # The cur_filepath already contains leading "/""
					)
					new_filepath_site = f"{site_path}{new_filepath}"
					shutil.copyfile(cur_filepath_site, new_filepath_site)
					os.remove(cur_filepath_site)

					cur_file_doc.file_url = new_filepath
					cur_file_doc.file_name = new_filename
					cur_file_doc.save()
					self.set(field, cur_file_doc.file_url)

				else:
					frappe.log_error("File not found.")
			except Exception as e:
				frappe.throw(
					f"Error handling attachment: {e!s}",
					"Attachment Handling Exception",
				)

	def check_cso_mapping(self):
		table_cso_numbers = [item.get("cso_number", -1) for item in self.cso_table]  # [1,2]
		mapping_cso_numbers = [item.get("cso_number", -1) for item in self.cso_so_mapping]  # [1,2]
		mapping_sos = [item.get("so", -1) for item in self.cso_so_mapping]  # ['SO-1', 'SO-2']

		# Check for uniqueness of CSO numbers in the cso table.
		if len(table_cso_numbers) != len(set(table_cso_numbers)):
			frappe.throw(
				'Duplicate CSO numbers found in "CSO Entries" table. Each CSO should have a unique number.'
			)

		# Check for unmatched CSO numbers between the mapping and the table.
		for map_cso in mapping_cso_numbers:
			if map_cso not in table_cso_numbers:
				frappe.throw(
					f'CSO-{map_cso} in "CSO-SO Mapping" table was not found in "CSO Entries" table. Please check the mapping and entries tables.'
				)

		# Check for unmatched CSO numbers between the table and the mapping.
		for cso in table_cso_numbers:
			if cso not in mapping_cso_numbers:
				frappe.throw(
					f'There is no SO mapping found for CSO-{cso} in "CSO Entries" table. Please check the mapping and entries tables.'
				)

		msg = ""
		if len(mapping_cso_numbers) != len(set(mapping_cso_numbers)):
			msg = (
				msg
				+ '• Duplicate CSO numbers found in "CSO-SO Mapping" table. Each CSO should be mapped only once. Please check with the instructor(s).'
			)

		if len(mapping_sos) != len(set(mapping_sos)):
			msg = (
				msg
				+ '• Duplicate SO entries found in "CSO-SO Mapping" table. Each SO should be mapped to only one CSO. Please check with the instructor(s).'
			)

		if msg != "":
			frappe.msgprint(msg)

	def before_save(self):
		self.calculate_average_score()
		self.change_filenames()
		self.check_cso_mapping()


def is_already_renamed(filepath):
	fname = os.path.basename(filepath)
	result = re.search(r"^EDU_", fname)
	return bool(result)


def gen_filename(filename, document_name, field):
	_, ext = os.path.splitext(filename)
	random_prefix = gen_random_prefix(4)
	new_filename = f"EDU_{document_name}_{field}_{random_prefix}{ext}"
	return new_filename


def gen_random_prefix(n):
	return "".join(random.choices(string.ascii_uppercase + string.digits, k=n)).lower()
