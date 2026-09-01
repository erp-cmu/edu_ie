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
		from edu_ie.edu_ie.doctype.edu_course_ci_clo.edu_course_ci_clo import EDUCourseCICLO
		from edu_ie.edu_ie.doctype.edu_course_ci_clo_pi_map.edu_course_ci_clo_pi_map import EDUCourseCICLOPIMap
		from edu_ie.edu_ie.doctype.edu_course_ci_eval.edu_course_ci_eval import EDUCourseCIEval
		from edu_ie.edu_ie.doctype.edu_course_ci_rubric.edu_course_ci_rubric import EDUCourseCIRubric
		from edu_ie.edu_ie.doctype.edu_section_link.edu_section_link import EDUSectionLink
		from frappe.types import DF

		abet1_file: DF.Attach | None
		abet2_file: DF.Attach | None
		amended_from: DF.Link | None
		clo_pi_mapping: DF.Table[EDUCourseCICLOPIMap]
		clo_table: DF.Table[EDUCourseCICLO]
		course: DF.Link
		cso_evaluation_table: DF.Table[EDUCourseCIEval]
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
		# Check if a document with the same course, evaluation year, and curriculum already exists
		num_existing = frappe.db.count(
			"EDU Course CI",
			{
				"course": self.course,
				"evaluation_year": self.evaluation_year,
				"curriculum": self.curriculum,
				"docstatus": ["in", [0, 1]],  # Count only Draft and Submitted documents
			},
		)
		if num_existing > 0:
			frappe.throw(
				f"An EDU Course CI document already exists for course '{self.course}', evaluation year '{self.evaluation_year}', and curriculum '{self.curriculum}'. Please check the existing documents."
			)
		self.name = f"{self.course}-{self.curriculum}-{self.evaluation_year}"

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
		table_clo_numbers = [item.get("clo_number", -1) for item in self.clo_table]  # [1,2]
		mapping_clo_numbers = [item.get("clo_number", -1) for item in self.clo_pi_mapping]  # [1,2]
		mapping_pis = [item.get("pi", -1) for item in self.clo_pi_mapping]  # ['PI-1', 'PI-2']

		# Check for uniqueness of CLO numbers in the CLO table.
		if len(table_clo_numbers) != len(set(table_clo_numbers)):
			frappe.throw(
				'Duplicate CLO numbers found in "CLO Entries" table. Each CLO should have a unique number.'
			)

		# Check for unmatched CLO numbers between the mapping and the table.
		for map_clo in mapping_clo_numbers:
			if map_clo not in table_clo_numbers:
				frappe.throw(
					f'CLO-{map_clo} in "CLO-PI Mapping" table was not found in "CLO Entries" table. Please check the mapping and entries tables.'
				)

		# Check for unmatched CLO numbers between the table and the mapping.
		for clo in table_clo_numbers:
			if clo not in mapping_clo_numbers:
				frappe.throw(
					f'There is no PI mapping found for CLO-{clo} in "CLO Entries" table. Please check the mapping and entries tables.'
				)

		msg = ""
		if len(mapping_clo_numbers) != len(set(mapping_clo_numbers)):
			msg = (
				msg
				+ '• Duplicate CLO numbers found in "CLO-PI Mapping" table. Each CLO should be mapped only once. Please check with the instructor(s).'
			)

		if len(mapping_pis) != len(set(mapping_pis)):
			msg = (
				msg
				+ '• Duplicate PI entries found in "CLO-PI Mapping" table. Each PI should be mapped to only one CLO. Please check with the instructor(s).'
			)

		if msg != "":
			frappe.msgprint(msg)

	def check_rubric(self):
		rubric_table = self.rubric_table

		if rubric_table:
			# Check for duplicates
			rubric_nos = [item.get("clo_number", -1) for item in rubric_table]  # [1,2]
			if len(rubric_nos) != len(set(rubric_nos)):
				frappe.throw(
					"Duplicate CLO numbers found in the rubric table. Each rubric entry should have a unique CLO number."
				)

			# Check if there is CLO number assigned for each rubric entry
			clo_numbers = [item.get("clo_number", -1) for item in self.clo_table]  # [1,2]
			for rubric in rubric_table:
				if rubric.clo_number not in clo_numbers:
					frappe.throw(
						f"Rubric number {rubric.clo_number} does not match any CLO number in the CLO table. Please ensure that each rubric entry corresponds to a valid CLO."
					)

	def before_save(self):
		self.calculate_average_score()
		self.change_filenames()
		self.check_cso_mapping()
		self.check_rubric()


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
