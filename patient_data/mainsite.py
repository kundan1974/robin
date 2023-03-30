mainsite_query = """
SELECT DISTINCT s1_parent_main.crnumber, 
CONCAT(s1_parent_main.first_name, " ", s1_parent_main.last_name) AS PtName, s1_parent_main.age, 
s1_parent_main.gender, s1_parent_main.height, s1_parent_main.weight, s2_child_dx.c_t_id, 
s2_child_dx.c_n_id, s2_child_dx.c_m_id, s2_child_dx.c_stage_group_id, 
s2_child_dx.icd_topo_code_id, s2_child_dx.laterality, s3_child_cp.startdate, s4_child_cp_rt.rtstartdate,
s4_child_cp_rt.tech1, s4_child_cp_rt.rtdose1, s4_child_cp_rt.rtdose2, s5_child_cp_ch_protocol.chemo_protocol,
s6_child_cp_sx.sxdate, s7_child_as.parent_id, s7_child_as.as_date, s8_child_fup.visitdate, s8_child_fup.LRstatus,
s8_child_fup.RRstatus, s8_child_fup.DMstatus, s8_child_fup.Death
FROM s1_parent_main INNER JOIN s2_child_dx ON s1_parent_main.crnumber  = s2_child_dx.parent_id_id
INNER JOIN s3_child_cp ON s2_child_dx.s2_id  = s3_child_cp.s2_id
LEFT JOIN s4_child_cp_rt ON s3_child_cp.s3_id = s4_child_cp_rt.s3_id
LEFT JOIN s7_child_as ON s4_child_cp_rt.s4_id = s7_child_as.s4_id
LEFT JOIN s6_child_cp_sx ON s3_child_cp.s3_id = s6_child_cp_sx.s3_id
LEFT JOIN s5_child_cp_ch_protocol ON s3_child_cp.s3_id = s5_child_cp_ch_protocol.s3_id
LEFT JOIN s8_child_fup ON s3_child_cp.s3_id = s8_child_fup.s3_id
WHERE s2_child_dx.icd_main_topo_id LIKE %s ORDER BY s7_child_as.as_date, s8_child_fup.visitdate DESC;
"""

mainsite_subsite_query = """
SELECT DISTINCT s1_parent_main.crnumber, 
CONCAT(s1_parent_main.first_name, " ", s1_parent_main.last_name) AS PtName, s1_parent_main.age, 
s1_parent_main.gender, s1_parent_main.height, s1_parent_main.weight, s2_child_dx.c_t_id, 
s2_child_dx.c_n_id, s2_child_dx.c_m_id, s2_child_dx.c_stage_group_id, 
s2_child_dx.icd_topo_code_id, s2_child_dx.laterality, s3_child_cp.startdate, s4_child_cp_rt.rtstartdate,
s4_child_cp_rt.tech1, s4_child_cp_rt.rtdose1, s4_child_cp_rt.rtdose2, s5_child_cp_ch_protocol.chemo_protocol,
s6_child_cp_sx.sxdate, s7_child_as.parent_id, s7_child_as.as_date, s8_child_fup.visitdate, s8_child_fup.LRstatus,
s8_child_fup.RRstatus, s8_child_fup.DMstatus, s8_child_fup.Death
FROM s1_parent_main INNER JOIN s2_child_dx ON s1_parent_main.crnumber  = s2_child_dx.parent_id_id
INNER JOIN s3_child_cp ON s2_child_dx.s2_id  = s3_child_cp.s2_id
LEFT JOIN s4_child_cp_rt ON s3_child_cp.s3_id = s4_child_cp_rt.s3_id
LEFT JOIN s7_child_as ON s4_child_cp_rt.s4_id = s7_child_as.s4_id
LEFT JOIN s6_child_cp_sx ON s3_child_cp.s3_id = s6_child_cp_sx.s3_id
LEFT JOIN s5_child_cp_ch_protocol ON s3_child_cp.s3_id = s5_child_cp_ch_protocol.s3_id
LEFT JOIN s8_child_fup ON s3_child_cp.s3_id = s8_child_fup.s3_id
WHERE s2_child_dx.icd_main_topo_id LIKE %s AND s2_child_dx.icd_topo_code_id = %s ORDER BY s7_child_as.as_date, s8_child_fup.visitdate DESC;
"""