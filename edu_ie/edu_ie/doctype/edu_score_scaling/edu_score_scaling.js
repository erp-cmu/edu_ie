// Copyright (c) 2026, IE and contributors
// For license information, please see license.txt

frappe.ui.form.on("EDU Score Scaling", {
	refresh(frm) {},
	scaling_method(frm) {
		if (frm.doc.scaling_method === "Threshold") {
			// Show the threshold fields and make them required
			frm.set_df_property("threshold_1", "hidden", 0);
			frm.set_df_property("threshold_2", "hidden", 0);
			frm.set_df_property("threshold_3", "hidden", 0);
			frm.set_df_property("threshold_4", "hidden", 0);
			// Make the threshold fields required
			frm.set_df_property("threshold_1", "reqd", 1);
			frm.set_df_property("threshold_2", "reqd", 1);
			frm.set_df_property("threshold_3", "reqd", 1);
			frm.set_df_property("threshold_4", "reqd", 1);
		} else if (frm.doc.scaling_method === "Linear") {
			// Hide the threshold fields and make them not required
			frm.set_df_property("threshold_1", "hidden", 1);
			frm.set_df_property("threshold_2", "hidden", 1);
			frm.set_df_property("threshold_3", "hidden", 1);
			frm.set_df_property("threshold_4", "hidden", 1);
			// Make the threshold fields not required
			frm.set_df_property("threshold_1", "reqd", 0);
			frm.set_df_property("threshold_2", "reqd", 0);
			frm.set_df_property("threshold_3", "reqd", 0);
			frm.set_df_property("threshold_4", "reqd", 0);
		} else {
			console.log("Unknown scaling method: " + frm.doc.scaling_method);
		}
	},
});
