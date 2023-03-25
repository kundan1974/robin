CITI_CHOICES = [
    ('', ''),
    ('New Delhi', 'New Delhi.'),
    ('Lucknow', 'Lucknow.'),
    ('Hissar', 'Hissar.'),
    ('Sonipat', 'Sonipat.'),
]

GENDER = [
    ('', ''),
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
]

YES_NO = [
    ('', ''),
    ('No', 'No.'),
    ('Yes', 'Yes.'),
    ('Unknown', 'Unknown.')
]

SMOKE_TYPE = [
    ('', ''),
    ('Bidi', 'Bidi.'),
    ('cigarette', 'cigarette.'),
    ('Other', 'Other.')
]

SMOKE_FREQ = [
    ('', ''),
    ('<=1 pack/day', '<=1 pack/day'),
    ('>1 pack <=2 pack', '>1 pack <=2 pack'),
    ('>2 pack <=3 pack', '>2 pack <=3 pack'),
    ('>3 pack <=4 pack', '>3 pack <=4 pack'),
    ('>4 pack <=5 pack', '>4 pack <=5 pack'),
    ('>5 pack', '>5 pack')
]

SMOKE_DUR = [
    ('', ''),
    ('<5 years', '<5 years'),
    ('>5 & <=10 years', '>5 & <=10 years'),
    ('>10 & <=20 years', '>10 & <=20 years'),
    ('>20 & <=30 years', '>20 & <=30 years'),
    ('>30 & <=40 years', '>30 & <=40 years'),
    ('>40 & <=50 years', '>40 & <=50 years'),
    ('>50 years', '>50 years'),

]

PS = [
    ('', ''),
    ('PS 0', 'PS 0: Fully active, able to carry on all pre-disease performance without restriction'),
    ('PS 1',
     'PS 1: Restricted in physically strenuous activity but ambulatory and able to carry out work of a light or sedentary nature, e.g., light house work, office work'),
    ('PS 2',
     'PS 2: Ambulatory and capable of all selfcare but unable to carry out any work activities; up and about more than 50% of waking hours'),
    ('PS 3', 'PS 3: Capable of only limited selfcare; confined to bed or chair more than 50% of waking hours'),
    ('PS 4', 'PS 4: Completely disabled; cannot carry on any selfcare; totally confined to bed or chair'),
    ('PS 5', 'PS 5: Dead'),
]

REF_BY = [
    ('', ''),
    ('Internal Ref', 'Internal Ref'),
    ('Other Hospital', 'Other Hospital')
]

REG_DX = [
    ('', ''),
    ('NSCLC', 'NSCLC'),
    ('SCLC', 'SCLC')
]

DX_BY = [
    ('', ''),
    ('FNAC', 'FNAC'),
    ('Biopsy', 'Biopsy')
]

HPE = [
    ('', ''),
    ('SCC', 'SCC'),
    ('AdenoCa', 'AdenoCa'),
    ('NSCLC, NOS', 'NSCLC, NOS'),
    ('SCLC', 'SCLC'),
]

EGFR_STATUS = [
    ('', ''),
    ('Wild', 'Wild'),
    ('Mutant', 'Mutant'),
    ('QNS', 'QNS'),
    ('Not Needed', 'Not Needed'),
]

ALK_BY = [
    ('', ''),
    ('FISH', 'FISH'),
    ('IHC', 'IHC'),
]

ALK_STATUS = [
    ('', ''),
    ('Amplified', 'Amplified'),
    ('Not Amplified', 'Not Amplified'),
    ('QNS', 'QNS'),
    ('Not Needed', 'Not Needed'),
]

T_STAGE = [
    ('', ''),
    ('Tx', 'Tx'),
    ('Tis', 'Tis'),
    ('T1', 'T1'),
    ('T2', 'T2'),
    ('T3', 'T3'),
    ('T4', 'T4'),
]

N_STAGE = [
    ('', ''),
    ('Nx', 'Nx'),
    ('N0', 'N0'),
    ('N1', 'N1'),
    ('N2', 'N2'),
    ('N3', 'N3'),
]

M_STAGE = [
    ('', ''),
    ('Mx', 'Mx'),
    ('M0', 'M0'),
    ('M1', 'M1'),
    ('M2', 'M2'),
    ('M3', 'M3'),
]

STAGE_GROUP = [
    ('', ''),
    ('Stage0', 'Stage0'),
    ('Stage 1a', 'Stage 1a'),
    ('Stage 1b', 'Stage 1b'),
    ('Stage 2a', 'Stage 2a'),
    ('Stage 2b', 'Stage 2b'),
    ('Stage 3a', 'Stage 3a'),
    ('Stage 3b', 'Stage 3b'),
    ('Stage 3c', 'Stage 3c'),
    ('Stage 4a', 'Stage 4a'),
    ('Stage 4b', 'Stage 4b'),
]

REG_FINAL_STATUS = [
    ('', ''),
    ('Treatment Naive', 'Treatment Naive'),
    ('Treatment Just Started', 'Treatment Just Started'),
    ('On Treatment - Progression', 'On Treatment - Progression'),
    ('On Treatment - Stable Disease', 'On Treatment - Stable Disease'),
    ('On Treatment - Responding', 'On Treatment - Responding'),
    ('On Treatment - No Evaluation Done', 'No Evaluation Done '),
]

DX_STATUS = [
    ('', ''),
    ('Initial Dx', 'Initial Dx'),
    ('First Relapse', 'First Relapse'),
    ('First Progression', 'First Progression'),
    ('Second Progression', 'Second Progression'),
    ('Third Progression', 'Third Progression'),
    ('Fourth Progression', 'Fourth Progression'),
    ('Fifth Progression', 'Fifth Progression'),
    ('Sixth Progression', 'Sixth Progression'),
]

MX_STATUS = [
    ('', ''),
    ('First Line', 'First Line'),
    ('Second Line', 'Second Line'),
    ('Third Line', 'Third Line'),
    ('Maintenance', 'Maintenance'),
]

MX_TYPE = [
    ('', ''),
    ('Chemo', 'Chemo'),
    ('TKI', 'TKI'),
    ('Immunotherapy', 'Immunotherapy'),
    ('ChemoImmuno', 'ChemoImmuno'),
    ('CCRT', 'CCRT'),
]

FU_STATUS = [
    ('', ''),
    ('PD', 'PD'),
    ('SD', 'SD'),
    ('PR', 'PR'),
    ('CR', 'CR'),
    ('Not Assessed', 'Not Assessed'),
    ('Death', 'Death'),
]

CHEMO_PROTOCOL = [
    ('', ''),
    ('Cis-Pacli', 'Cis-Pacli'),
    ('Pem-Cis', 'Pem-Cis'),
    ('Cis-Gem', 'Cis-Gem'),
]

TKI_DRUGS = [
    ('', ''),
    ('Gefitinib', 'Gefitinib'),
    ('Erlotinib', 'Erlotinib'),
    ('Osimertinib', 'Osimertinib'),
]

IMMUNO_DRUGS = [
    ('', ''),
    ('Nivolumab', 'Nivolumab'),
    ('Pembrozolumab', 'Pembrozolumab'),
]

# Patient Data Module Choices for radonc DB

symp_type_choices = [
    ("", ""),
    ('Mild', 'Mild'),
    ('Moderate', 'Moderate'),
    ('Severe', 'Severe')
]

txstatus_choices = [("", ""),
                    ('Ongoing', 'Ongoing'),
                    ('Visit within 3 months of treatment completion', 'Visit within 3 months of treatment completion'),
                    ('First Day', 'First Day'),
                    ('Last Day', 'Last Day'),
                    ('Consultation', 'Consultation')]

toxicity_choices = [
    ("", ""),
    ('Grade0', 'Grade0'),
    ('Grade1', 'Grade1'),
    ('Grade2', 'Grade2'),
    ('Grade3', 'Grade3'),
    ('Grade4', 'Grade4'),
    ('Grade5', 'Grade5'),
]

visit_choices = [
    ("", ""),
    ('Second Opinion', 'Second Opinion'),
    ('On Workup Evaluation', 'On Workup Evaluation'),
    ('Follow-up on treatment', 'Follow-up on treatment'),
    ('Follow-up post treatment', 'Follow-up post treatment'),
]

visit_actions = [
    ("", ""),
    ('No-Diagnosis No-Careplan Workup Evaluation Continued', 'No-Diagnosis No-Careplan Workup Evaluation Continued'),
    ('Diagnosis with No-Careplan (Pending Tumor Board Decision)',
     'Diagnosis with No-Careplan (Pending Tumor Board Decision)'),
    ('Careplan-Continued', 'Careplan-Continued'),
    ('Change-Careplan', 'Change-Careplan'),
    ('Close Careplan (Death)', 'Close Careplan (Death)')
]

deathcause_choices = [
    ("", ""),
    ("Due to present cancer", "Due to present cancer"),
    ("Due to other cancer", "Due to other cancer"),
    ("Cardiovascular", "Cardiovascular"),
    ("Diabetes mellitus", "Diabetes mellitus"),
    ("Ischemic heart disease", "Ischemic heart disease"),
    ("Hypertensive Disease", "Hypertensive Disease"),
    ("Pulmonary embolism", "Pulmonary embolism"),
    ("Chronic kidney disease", "Chronic kidney disease"),
    ("Acute pulmonary disease", "Acute pulmonary disease"),
    ("Other chronic disease", "Other chronic disease"),
    ("Tuberculosis", "Tuberculosis"),
    ("Autoimmune disorder", "Autoimmune disorder"),
    ("Meningitis", "Meningitis"),
    ("Hepatobiliary", "Hepatobiliary"),
    ("Treatment related complications", "Treatment related complications"),
    ("Other Causes", 'Other Causes')

]

frequency_choices = [
    ("", ""),
    ('BD', 'BD'),
    ('OD', 'OD'),
    ('QID', 'QID'),
    ('SOS', 'SOS'),
    ('HS', 'HS'),
    ('TDS', 'TDS'),
    ('Stat', 'Stat'),
]

unit_choices = [
    ("", ""),
    ('mg', 'mg'),
    ('ml', 'ml'),
    ('gm', 'gm'),
    ('Tab', 'Tab'),
    ('Drops', 'Drops'),
    ('mcg', 'mcg'),
    ('Cap', 'Cap'),
    ('tsf', 'tsf'),
]

route_choices = [
    ("", ""),
    ('Local', 'Local'),
    ('Oral', 'Oral'),
    ('Oral Rinse', 'Oral Rinse'),
    ('SC', 'SC'),
    ('Enema', 'Enema'),
]

drugs_choices = [
    ("", ""),
    ('Radiaguard', 'Radiaguard'),
    ('Natskin', 'Radiaguard'),
    ('Signoflam', 'Signoflam'),
    ('Emset', 'Emset'),
    ('Sucrafil-O gel', 'Sucrafil-O gel'),
    ('Wheycan Powder', 'Wheycan Powder'),
    ('Temozolamide', 'Temozolamide'),
    ('Emeset', 'Emeset'),
    ('Allegra', 'Allegra'),
    ('Dolo', 'Dolo'),
    ('PanD', 'PanD'),
    ('Levocitrizine', 'Levocitrizine'),
    ('CQMax', 'CQMax'),
    ('Candid Mouth Paint', 'Candid Mouth Paint'),
    ('Ulgel-O', 'Ulgel-O'),
    ('Mucaine', 'Mucaine'),
    ('Silverex', 'Silverex'),
    ('Cremaffin', 'Cremaffin'),
    ('Gentian Violet', 'Gentian Violet'),
    ('Ultracet', 'Ultracet'),
    ('Sucrcrafil-O gel', 'Sucrcrafil-O gel'),
    ('Practin', 'Practin'),
    ('Alex', 'Alex'),
    ('Dexona', 'Dexona'),
    ('Wysolone', 'Wysolone'),
    ('Mecobol', 'Mecobol'),
    ('Resource Hepatic', 'Resource Hepatic'),
    ('Curcon gel', 'Curcon gel'),
    ('Linid', 'Linid'),
    ('Looze', 'Looze'),
    ('Nitrest', 'Nitrest'),
    ('Mecobal', 'Mecobal'),
    ('Radiagard', 'Radiagard'),
    ('Isabgol husk', 'Isabgol husk'),
    ('medrol', 'medrol'),
    ('otrivin', 'otrivin'),
    ('Aksitaram EF', 'Aksitaram EF'),
    ('PenoDSR', 'PenoDSR'),
    ('Zolfresh', 'Zolfresh'),
    ('Pantop-D', 'Pantop-D'),
    ('Lyrica', 'Lyrica'),
    ('Nitrofurantoin', 'Nitrofurantoin'),
    ('levocet', 'levocet'),
    ('pan DSR', 'pan DSR'),
    ('Tranexa', 'Tranexa'),
    ('Sinarest', 'Sinarest'),
    ('OfloxOZ', 'OfloxOZ'),
    ('Augmentin', 'Augmentin'),
    ('Nasonix', 'Nasonix'),
    ('Temozolamide', 'Temozolamide'),
    ('Ondem', 'Ondem'),
    ('levoflox', 'levoflox'),
    ('Jelonat dressing', 'Jelonat dressing'),
    ('Pan40', 'Pan40'),
    ('Pantop', 'Pantop'),
    ('Becasule-Z', 'PenoDSR'),
    ('Dom-DT', 'Zolfresh'),
    ('Nefopam', 'Pantop-D'),
    ('Drotin', 'Lyrica'),
    ('Uvdyne', 'Nitrofurantoin'),
    ('SodaBicarb', 'levocet'),
    ('Ulgel', 'pan DSR'),
    ('Silverx', 'Tranexa'),
    ('Grafeel', 'Sinarest'),
    ('Morphin', 'OfloxOZ'),
    ('Codistar', 'Augmentin'),
    ('Codestar', 'Nasonix'),
    ('Dulcolax', 'Temozolamide'),
    ('Pantocid', 'Ondem'),
    ('Vertin', 'levoflox'),
    ('Zerodol', 'Jelonat dressing'),
    ('Econorm', 'Econorm'),
    ('Alprax', 'Pantop'),
    ('Oflox', 'Oflox'),
    ('Pan', 'Pan'),
    ('Buscogast', 'Buscogast'),
    ('Hifenac SR', 'Hifenac SR'),
    ('DomStal', 'DomStal'),
    ('chymoral Forte', 'chymoral Forte')
]

RT_LATE_TOXICITY = [
    ("", ""),
    ("WBC", "WBC"),
    ("Platelets", "Platelets"),
    ("Hemoglobin", "Hemoglobin"),
    ("Granulocytes/Bands", "Granulocytes/Bands"),
    ("Lymphocytes", "Lymphocytes"),
    ("Hemorrhage", "Hemorrhage"),
    ("Infection", "Infection"),
    ("Nausea", "Nausea"),
    ("Vomiting", "Vomiting"),
    ("Diarrhea", "Diarrhea"),
    ("Stomatitis", "Stomatitis"),
    ("Bilirubin", "Bilirubin"),
    ("Transaminase (SGOT, SGPT)", "Transaminase (SGOT, SGPT)"),
    ("Alkaline Phosphatase or S'nucleotidase", "Alkaline Phosphatase or S'nucleotidase"),
    ("Liver/clinical", "Liver/clinical"),
    ("Creatinine", "Creatinine"),
    ("Proteinuria", "Proteinuria"),
    ("Hematuria", "Hematuria"),
    ("Alopecia", "Alopecia"),
    ("Pulmonary", "Pulmonary"),
    ("Cardiac dysrhythmias", "Cardiac dysrhythmias"),
    ("Cardiac function", "Cardiac function"),
    ("Cardiac/ ischemia", "Cardiac/ ischemia"),
    ("Cardiac/pericardial", "Cardiac/pericardial"),
    ("Hypertension", "Hypertension"),
    ("Hypotension", "Hypotension"),
    ("Neurological/ sensory", "Neurological/ sensory"),
    ("Neurological/ motor", "Neurological/ motor"),
    ("Neurological/ cortical", "Neurological/ cortical"),
    ("Neurological/ cerebellar", "Neurological/ cerebellar"),
    ("Neurological/ mood", "Neurological/ mood"),
    ("Neurological/ headache", "Neurological/ headache"),
    ("Neurological/ constipation", "Neurological/ constipation"),
    ("Neurological/hearing", "Neurological/hearing"),
    ("Neurological/vision", "Neurological/vision"),
    ("Acute Skin", "Acute Skin"),
    ("Allergy", "Allergy"),
    ("Fever in absence of infection", "Fever in absence of infection"),
    ("Local", "Local"),
    ("Weight gain/loss", "Weight gain/loss"),
    ("Hyperglycemia", "Hyperglycemia"),
    ("Hypoglycemia", "Hypoglycemia"),
    ("Amylase", "Amylase"),
    ("Hypercalcemia", "Hypercalcemia"),
    ("Hypocalcemia", "Hypocalcemia"),
    ("Hypomagnesemia", "Hypomagnesemia"),
    ("Fibrinogen", "Fibrinogen"),
    ("Prothrombin time", "Prothrombin time"),
    ("Partial thromboplastin time", "Partial thromboplastin time"),
    ("Late Skin", "Late Skin"),
    ("Late Subcutaneous Tissue", "Late Subcutaneous Tissue"),
    ("Late Mucous Membrane", "Late Mucous Membrane"),
    ("Late Salivary Gland", "Late Salivary Gland"),
    ("Late Spinal Cord", "Late Spinal Cord"),
    ("Late Brain", "Late Brain"),
    ("Late Eye", "Late Eye"),
    ("Late Larynx", "Late Larynx"),
    ("Late Lung", "Late Lung"),
    ("Late Heart", "Late Heart"),
    ("Late Esophagus", "Late Esophagus"),
    ("Late Small Large Intestine", "Late Small Large Intestine"),
    ("Late Liver", "Late Liver"),
    ("Late Kidney", "Late Kidney"),
    ("Late Bladder", "Late Bladder"),
    ("Late Bone", "Late Bone"),
    ("Late Joint", "Late Joint"),
    ("No Toxicity", "No Toxicity"),
]

INTENT_CHOICES = [
    ('', ''),
    ('Curative', 'Curative'),
    ('Palliative', 'Palliative')]

CP_CHOICES = [('', ''),
              ('Primary', 'Primary'),
              ('Salvage', 'Salvage'),
              ('Neoadjuvant', 'Neoadjuvant'),
              ('Adjuvant', 'Adjuvant'),
              ('Maintenance', 'Maintenance'),
              ('Palliative', 'Palliative'),
              ('Consolidation', 'Consolidation'),
              ('Sequential', 'Sequential'),
              ('Concurrent', 'Concurrent'),
              ('Prophylactic', 'Prophylactic'),
              ('Not Planned', 'Not Planned'),
              ]

DOC_TYPE_CHOICES = [('------', '------'),
                    ('Aadhar', 'Aadhar'),
                    ('PAN', 'PAN'),
                    ('Passport', 'Passport'),
                    ('Voter ID', 'Voter ID'),
                    ('Other', 'Other')
                    ]

LAB_NAME = [('', ''),
            ('InHouse', 'InHouse'),
            ('Outside(unspecified)', 'Outside(unspecified)'),
            ]

PROCEDURE_TYPE = [('', ''),
                  ('Block/Slide Review', 'Block/Slide Review'),
                  ('FNAC', 'FNAC'),
                  ('Biopsy', 'Biopsy'),
                  ('CSF', 'CSF'),
                  ('Ascitic Fluid', 'Ascitic Fluid'),
                  ('Pleural Fluid', 'Pleural Fluid'),
                  ('Pap Smear', 'Pap Smear')]

GUIDED_BY = [('', ''),
             ('None', 'None'),
             ('CT', 'CT'),
             ('USG', 'USG'),
             ('MR', 'MR'),
             ('EUS', 'EUS'),
             ('EBUS', 'EBUS'),
             ('UGIE', 'UGIE'),
             ('ProctoSigmoidoScopy', 'ProctoSigmoidoScopy'),
             ('Fluro', 'Fluro')
             ]

MOLECULAR_STATUS = [
    ("", ""),
    ('Report Awaited', 'Report Awaited'),
    ('Reported', 'Reported'),
]

MOLECULAR_TYPE = [
    ("", ""),
    ('EGFR', 'EGFR'),
    ('ALK', 'ALK'),
    ('ROS', 'ROS'),
    ('BRAF', 'BRAF'),
    ('ER', 'ER'),
    ('PR', 'PR'),
    ('HER2Neu', 'HER2Neu'),
    ('BRACA1', 'BRACA1'),
    ('BRACA2', 'BRACA2'),
    ('PDL1', 'PDL1'),
    ('Ki67', 'Ki67')
]

MOLECULAR_RESULT = [
    ("", ""),
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Unknown Significance', 'Unknown Significance'),
]

MOLECULAR_UNIT = [
    ("", ""),
    ('%', '%'),
]

LAB_TEST_NAME = [
    ("", ""),
    ("Hb", "Hb"),
    ("TLC", "Total Leukocyte Count"),
    ("ANC", "Absolute Neutrophil Count"),
    ("ALC", "Absolute Lymphocyte Count"),
    ("AMC", "Absolute Monocyte Count"),
    ("AEC", "Absolute Eosinophil Count"),
    ("Plt", "Platelet Count"),
    ("S.Urea", "S.Urea"),
    ("S.Creat", "S.Creatinine"),
    ("Creat Clearance", "Creatinine Clearance"),
    ("GFR", "Glomular Filtration Rate(GFR)"),
    ("CEA", "CEA"),
    ("CA-125", "Cancer antigen 125 (CA 125)"),
    ("CA 15-3", "Cancer antigen 15-3 (CA 15-3)"),
    ("CA 19-9", "Cancer antigen 19-9 (CA 19-9)"),
    ("AFP", "Alpha-Fetoprotein (AFP)"),
    ("B-hCG", "Beta-Human Chorionic Gonadotropin (B-hCG)"),
    ("Chromogranin A", "Chromogranin A"),
    ("Synaptophysin", "Synaptophysin"),
    ("PSA", "Prostate-Specific Antigen (PSA)"),
    ("Testosterone", "Testosterone"),
    ("Estrogen", "Estrogen"),
    ("Progesterone", "Progesterone"),
    ("Na", "Sodium"),
    ("K", "Potassium"),
    ("Mg", "Magnesium"),
    ("Chl", "Chloride"),
    ("Ca", "Calcium"),
    ("Ca+", "Ionized Calcium"),
    ("RBS", "Random Blood Sugar"),
    ("FBS", "Fasting Blood Sugar"),
    ("HbA1C", "Hemoglobin A1C"),
    ("SGPT", "SGPT"),
    ("SGOT", "SGOT"),
    ("ALP", "Alkaline Phosphatase"),
    ("T.Bil", "Total Bilrubin"),
    ("Direct Bilirubin", "Conjugated(Direct) Bilrubin"),
    ("Indirect Bilirubin", "UnConjugated(Indirect) Bilrubin"),
    ("B12", "B12"),
    ("CRP", "C-Reactive Protein (CRP)"),
    ("PT", "Prothrombin Time (PT)"),
    ("PTT", "Partial Thromboplastin Time (PTT)"),
    ("INR", "INR"),
    ("Iron", "Iron"),
    ("TIBC", "Total Iron-Binding Capacity (TIBC)"),
    ("Folic Acid", "Folic Acid"),
    ("TSH", "Thyroid Stimulating Hormone"),
    ("T3", "T3"),
    ("T4", "T4"),
    ("ANA", "Antinuclear Antibody (ANA)"),
    ("HIV", "Human Immunodeficiency Virus (HIV) Test"),
    ("OBC", "Occult Blood Stool"),
    ("Ferritin", "Ferritin"),
]

LAB_TEST_UNITS = [
    ("", ""),
    ("%", "Percent (%)"),
    ("g/dL", "Grams per deciliter (g/dL)"),
    ("mg/dL", "Milligrams per deciliter (mg/dL)"),
    ("μg/dL", "Micrograms per deciliter (μg/dL)"),
    ("μg/L", " Micrograms per liter (μg/L)"),
    ("ng/mL", "Nanograms per milliliter (ng/mL)"),
    ("pg/dL", "Picograms per deciliter (pg/dL)"),
    ("mmol/L", "Millimoles per liter (mmol/L)"),
    ("nmol/L", "Nanomoles per liter (nmol/L)"),
    ("U/L", " Units per liter (U/L)"),
    ("U/mL", " Units per milliliter (U/mL)"),
    ("μU/mL", "Microunits per liter (μU/mL)"),
    ("IU/L", "International units per liter (IU/L)"),
    ("mL/min", "Milliliters per minute (mL/min)"),
    ("s", "Seconds (s)"),
    ("P", "Present"),
    ("A", "Absent"),
    ("Pos", "Positive"),
    ("N", "Negative"),
    ('units/cumm', 'Units per cumm')
]

DIBH_DAYS = [
    ("", ""),
    ("Day1", "Day1"),
    ("Day2", "Day2"),
    ("Day3", "Day3"),
    ("Day4", "Day4"),
    ("Day5", "Day5"),
    ("Day6", "Day6"),
    ("Day7", "Day7"),
    ("Day8", "Day8"),
    ("Day9", "Day9"),
    ("Day10", "Day10"),
]
