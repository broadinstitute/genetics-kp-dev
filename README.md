# Genetics Knowledge API
Code repository for the maintenance of the Translator API for the Broad Institute's Genetics Team comprising members of the [Flannick Lab](http://www.flannicklab.org/).


# Data Available
The Genetics KP provides the following data

* Richards method gene/phenotype associations
  * Forgetta V, Jiang L, Vulpescu NA, et al. An Effector Index to Predict Causal Genes at GWAS Loci. Submitted for publication, 2020.
        [BioRxiv](https://www.biorxiv.org/content/10.1101/2020.06.28.171561v1)

* Magma gene/phenotype associations and Magma pathway/phenotype associations
  * de Leeuw CA, et al. MAGMA: generalized gene-set analysis of GWAS data. PLoS Comput Biol. 2015 Apr 17;11(4):e1004219. doi: 10.1371/journal.pcbi.1004219.
        PMID: 25885710
        [paper](https://ctg.cncr.nl/software/magma)

* ABC method gene to phenotype associations
  * Fulco JP, Nasser J., et al. Activity-by-contact model of enhancer-promoter regulation from thousands of CRISPR perturbations. 
    Nat Genet. 2019 Dec;51(12):1664-1669.     
    doi: 10.1038/s41588-019-0538-0.
    PMID: 31784727

* Experimental Integrated Genetics method (Flannick Lab); under development

## The available phenotypes currently available for searching are listed below

# Phenotypes available for the Richards method gene associations (currently 10)
```
+----------------+--------------------------------+
| phenotype_code | phenotype                      |
+----------------+--------------------------------+
| Ca             | Calcium                        |
| DBP            | Diastolic blood pressure       |
| eBMD           | Estimated bone mineral density |
| HEIGHT         | Height                         |
| LDL            | LDL cholesterol                |
| RedCount       | Red blood cell count           |
| SBP            | Systolic blood pressure        |
| T2D            | Type 2 diabetes                |
| TG             | Triglycerides                  |
| Thyroid        | Hypothyroidism                 |
+----------------+--------------------------------+
```

# Phenotypes available for the Magma gene associations (currently 145)
```
+---------------------+-------------------------------------------------------+
| phenotype_code      | phenotype                                             |
+---------------------+-------------------------------------------------------+
| AcAce               | Acetoacetate                                          |
| Ace                 | Acetate                                               |
| AD                  | Alzheimer's disease                                   |
| Adiponectin         | Adiponectin                                           |
| AF                  | Atrial fibrillation                                   |
| AHI                 | Apnea-Hypopnea Index                                  |
| AHIinNREM           | Apnea-Hypopnea Index in NREM sleep                    |
| AHIinREM            | Apnea-Hypopnea Index in REM sleep                     |
| AIR                 | Acute insulin response                                |
| Ala                 | Alanine                                               |
| Alb                 | Serum albumin                                         |
| allDKD              | All diabetic kidney disease                           |
| ALLOA               | Any osteoarthritis                                    |
| ALP                 | Alkaline phosphatase                                  |
| ALS                 | ALS                                                   |
| ALT                 | Alanine transaminase                                  |
| AMD                 | Age-related macular degeneration                      |
| ApoA1               | Serum ApoA1                                           |
| ApoB                | Serum ApoB                                            |
| AST                 | Aspartate aminotransferase                            |
| BFP                 | Body fat percentage                                   |
| BILIRUBIN           | Bilirubin                                             |
| BIP                 | Bipolar disorder                                      |
| BMI                 | BMI                                                   |
| bOHBut              | Beta-hydroxybutyric acid                              |
| BUN                 | Blood urea nitrogen                                   |
| Ca                  | Calcium                                               |
| CAD                 | Coronary artery disease                               |
| CD                  | Crohn's disease                                       |
| CHOL                | Total cholesterol                                     |
| Cit                 | Citrate                                               |
| CK                  | Creatine kinase                                       |
| CKD                 | Chronic kidney disease                                |
| Cl                  | Chloride                                              |
| COPD                | Chronic obstructive pulmonary disease                 |
| Creatinine          | Creatinine                                            |
| CRP                 | Plasma C-reactive protein                             |
| DBP                 | Diastolic blood pressure                              |
| DI                  | Disposition index                                     |
| eBMD                | Estimated bone mineral density                        |
| EtOH                | Alcohol consumption                                   |
| FAw3                | Omega-3 fatty acids                                   |
| FAw6                | Omega-6 fatty acids                                   |
| Fbg                 | Fibrinogen                                            |
| FEV1                | Forced expired volume in 1 second (FEV1)              |
| FEV1toFVC           | FEV1 to FVC ratio                                     |
| FG                  | Fasting glucose                                       |
| FGadjBMI            | Fasting glucose adj BMI                               |
| FGovertime          | Fasting glucose change over time                      |
| FG_plus_diab        | Fasting plasma glucose in diabetics and non-diabetics |
| FI                  | Fasting insulin                                       |
| FIadjBMI            | Fasting insulin adj BMI                               |
| FNarea              | Femoral neck area                                     |
| Fracture            | Bone fracture                                         |
| FVC                 | Forced vital capacity (FVC)                           |
| GGT                 | Gamma-glutamyl transferase                            |
| Gln                 | Glutamine                                             |
| Glol                | Glycerol                                              |
| Gly                 | Glycine                                               |
| Gp                  | Glycoproteins                                         |
| Hb                  | Hemoglobin                                            |
| HBA1C               | HbA1c                                                 |
| HDL                 | HDL cholesterol                                       |
| HEIGHT              | Height                                                |
| HF                  | Heart failure                                         |
| HIPC                | Hip circumference                                     |
| HIPCadjBMI          | Hip circumference adj BMI                             |
| HIPOA               | Hip osteoarthritis                                    |
| His                 | Histidine                                             |
| HOMAB               | HOMA-B                                                |
| HOMAIR              | HOMA-IR                                               |
| HR                  | Heart rate                                            |
| IBD                 | Inflammatory bowel disease                            |
| IDLchol             | IDL cholesterol                                       |
| IGI                 | Insulinogenic index                                   |
| Ile                 | Isoleucine                                            |
| IntertrochArea      | Intertrochanteric-shaft area                          |
| ISen                | Insulin sensitivity                                   |
| K                   | Potassium                                             |
| KNEEOA              | Knee osteoarthritis                                   |
| lateDKD             | Late diabetic kidney disease                          |
| LDH                 | Lactate dehydrogenase                                 |
| LDL                 | LDL cholesterol                                       |
| LEP                 | Leptin                                                |
| Leu                 | Leucine                                               |
| LVEF                | Left ventricular ejection fraction                    |
| MAP                 | Mean arterial pressure                                |
| MDD                 | Major depressive disorder                             |
| MeanSleepDuration   | Mean sleep duration                                   |
| MeanSleepDurationRN | Mean sleep duration, rank-normalized                  |
| Men                 | Menarche                                              |
| MI                  | Myocardial infarction                                 |
| MP                  | Menopause                                             |
| n6FA182             | Linoleic acid                                         |
| ND                  | Neovascular age-related macular degeneration          |
| NeuropathyinT2D     | Neuropathy in type 2 diabetics                        |
| NICM                | Nonischemic cardiomyopathy                            |
| P                   | Phosphorus                                            |
| PACG                | Primary angle closure glaucoma                        |
| PEAK                | Peak insulin response                                 |
| PEF                 | Peak expiratory flow                                  |
| Phe                 | Phenylalanine                                         |
| POAG                | Open-angle glaucoma                                   |
| PRI                 | PR interval                                           |
| PulsePress          | Pulse pressure                                        |
| Pwave_duration      | P-wave duration                                       |
| Pyr                 | Pyruvate                                              |
| QRS                 | QRS interval                                          |
| RedCount            | Red blood cell count                                  |
| SBP                 | Systolic blood pressure                               |
| SCZ                 | Schizophrenia                                         |
| SleepChronotype     | Chronotype (morningness)                              |
| SleepDuration       | Sleep duration                                        |
| SleepEDS            | Excessive daytime sleepiness                          |
| SleepInsomnia       | Frequent insomnia symptoms                            |
| SleepNaps           | Naps                                                  |
| SM                  | Sphingomyelins                                        |
| Sodium              | Sodium                                                |
| Stroke_deep         | Non-lobar intracranial hemorrhage                     |
| Stroke_hemorrhagic  | All intracranial hemorrhage                           |
| Stroke_lobar        | Lobar intracranial hemorrhage                         |
| SVL                 | Stroke volume                                         |
| T1D                 | Type 1 diabetes                                       |
| T2D                 | Type 2 diabetes                                       |
| TG                  | Triglycerides                                         |
| TGtoHDL             | Triglyceride-to-HDL ratio                             |
| Thyroid             | Hypothyroidism                                        |
| TotCho              | Total cholines                                        |
| TotHipArea          | Total hip area                                        |
| TotPG               | Total phosphoglycerides                               |
| TrochanterArea      | Trochanter area                                       |
| Tyr                 | Tyrosine                                              |
| UA                  | Uric acid                                             |
| UACR                | Urinary albumin-to-creatinine ratio                   |
| UACR_nonDM          | UACR in non-diabetics                                 |
| UC                  | Ulcerative colitis                                    |
| Val                 | Valine                                                |
| VitD                | Vitamin D                                             |
| WAIST               | Waist circumference                                   |
| WAISTadjBMI         | Waist circumference adj BMI                           |
| WEIGHT              | Weight                                                |
| WHR                 | Waist-hip ratio                                       |
| WHRadjBMI           | Waist-hip ratio adj BMI                               |
| WMH                 | Cerebral white matter hyperintensity volume           |
| XXLVLDLpart         | Chylomicrons and XXL-VLDL cholesterol                 |
+---------------------+-------------------------------------------------------+
```

# Phenotypes available for the Magma pathway associations (currently 82)
```
+---------------------+-------------------------------------------------------+
| phenotype_code      | phenotype                                             |
+---------------------+-------------------------------------------------------+
| AD                  | Alzheimer's disease                                   |
| Adiponectin         | Adiponectin                                           |
| AF                  | Atrial fibrillation                                   |
| AHI                 | Apnea-Hypopnea Index                                  |
| AHIinNREM           | Apnea-Hypopnea Index in NREM sleep                    |
| AHIinREM            | Apnea-Hypopnea Index in REM sleep                     |
| allDKD              | All diabetic kidney disease                           |
| ALP                 | Alkaline phosphatase                                  |
| ALS                 | ALS                                                   |
| ALT                 | Alanine transaminase                                  |
| AST                 | Aspartate aminotransferase                            |
| BFP                 | Body fat percentage                                   |
| BIP                 | Bipolar disorder                                      |
| BMI                 | BMI                                                   |
| CAD                 | Coronary artery disease                               |
| CD                  | Crohn's disease                                       |
| CHOL                | Total cholesterol                                     |
| CHOLnoHDL           | Non-HDL cholesterol                                   |
| CKD                 | Chronic kidney disease                                |
| COPD                | Chronic obstructive pulmonary disease                 |
| Creatinine          | Creatinine                                            |
| DBP                 | Diastolic blood pressure                              |
| DI                  | Disposition index                                     |
| eBMD                | Estimated bone mineral density                        |
| FA180               | Palmitoleic acid                                      |
| FA181n9             | Oleic acid                                            |
| FG                  | Fasting glucose                                       |
| FGadjBMI            | Fasting glucose adj BMI                               |
| FG_plus_diab        | Fasting plasma glucose in diabetics and non-diabetics |
| FI                  | Fasting insulin                                       |
| FIadjBMI            | Fasting insulin adj BMI                               |
| Fracture            | Bone fracture                                         |
| GGT                 | Gamma-glutamyl transferase                            |
| HBA1C               | HbA1c                                                 |
| HDL                 | HDL cholesterol                                       |
| HEIGHT              | Height                                                |
| HF                  | Heart failure                                         |
| HIPC                | Hip circumference                                     |
| HIPCadjBMI          | Hip circumference adj BMI                             |
| HOMAB               | HOMA-B                                                |
| HOMAIR              | HOMA-IR                                               |
| HR                  | Heart rate                                            |
| IBD                 | Inflammatory bowel disease                            |
| IGI                 | Insulinogenic index                                   |
| ISen                | Insulin sensitivity                                   |
| lateDKD             | Late diabetic kidney disease                          |
| LDL                 | LDL cholesterol                                       |
| LEP                 | Leptin                                                |
| MDD                 | Major depressive disorder                             |
| MeanSleepDuration   | Mean sleep duration                                   |
| MeanSleepDurationRN | Mean sleep duration, rank-normalized                  |
| n6FA182             | Linoleic acid                                         |
| n6FA183             | Gamma-linolenic acid                                  |
| n6FA203             | Dihomo-gamma-linoleic acid                            |
| NeuropathyinT2D     | Neuropathy in type 2 diabetics                        |
| NICM                | Nonischemic cardiomyopathy                            |
| PAT                 | Pericardial adipose tissue volume                     |
| Ptforce             | P-wave terminal force                                 |
| Pwave_duration      | P-wave duration                                       |
| SAT                 | Subcutaneous adipose tissue volume                    |
| SBP                 | Systolic blood pressure                               |
| SCZ                 | Schizophrenia                                         |
| SleepChronotype     | Chronotype (morningness)                              |
| SleepDuration       | Sleep duration                                        |
| SleepEDS            | Excessive daytime sleepiness                          |
| SleepInsomnia       | Frequent insomnia symptoms                            |
| SleepNaps           | Naps                                                  |
| Stroke_all          | Any stroke                                            |
| Stroke_deep         | Non-lobar intracranial hemorrhage                     |
| Stroke_lobar        | Lobar intracranial hemorrhage                         |
| T2D                 | Type 2 diabetes                                       |
| TG                  | Triglycerides                                         |
| UACR                | Urinary albumin-to-creatinine ratio                   |
| UACR_nonDM          | UACR in non-diabetics                                 |
| UC                  | Ulcerative colitis                                    |
| VAT                 | Visceral adipose tissue volume                        |
| VATSAT              | Ratio visceral-subcutaneous adipose tissue volume     |
| WAIST               | Waist circumference                                   |
| WAISTadjBMI         | Waist circumference adj BMI                           |
| WHR                 | Waist-hip ratio                                       |
| WHRadjBMI           | Waist-hip ratio adj BMI                               |
| WMH                 | Cerebral white matter hyperintensity volume           |
+---------------------+-------------------------------------------------------+
```

# Phenotypes available for the Integrated Genetics method gene associations (currently 10)
```
+----------------+-------------------------------------------------------+
| phenotype_code | phenotype                                             |
+----------------+-------------------------------------------------------+
| AF             | Atrial fibrillation                                   |
| CAD            | Coronary artery disease                               |
| CKD            | Chronic kidney disease                                |
| FG             | Fasting glucose                                       |
| FG_plus_diab   | Fasting plasma glucose in diabetics and non-diabetics |
| FI             | Fasting insulin                                       |
| HBA1C          | HbA1c                                                 |
| HDL            | HDL cholesterol                                       |
| LDL            | LDL cholesterol                                       |
| T2D            | Type 2 diabetes                                       |
+----------------+-------------------------------------------------------+
```



