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

## Phenotypes available for the Richards method gene associations (currently 10)
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

## Phenotypes available for the Magma gene associations (currently 145)
```
+---------------------+-------------------------------------------------------+-------------+
| phenotype_code      | phenotype                                             | tran_efo_id |
+---------------------+-------------------------------------------------------+-------------+
| AcAce               | Acetoacetate                                          | EFO:0010111 |
| Ace                 | Acetate                                               | EFO:0010112 |
| AD                  | Alzheimer's disease                                   | EFO:0000249 |
| Adiponectin         | Adiponectin                                           | EFO:0004502 |
| AF                  | Atrial fibrillation                                   | EFO:0000275 |
| AHI                 | Apnea-Hypopnea Index                                  | EFO:0007817 |
| AHIinNREM           | Apnea-Hypopnea Index in NREM sleep                    | EFO:0008456 |
| AHIinREM            | Apnea-Hypopnea Index in REM sleep                     | EFO:0008455 |
| AIR                 | Acute insulin response                                | EFO:0006831 |
| Ala                 | Alanine                                               | EFO:0009765 |
| Alb                 | Serum albumin                                         | EFO:0004535 |
| allDKD              | All diabetic kidney disease                           | EFO:0000401 |
| ALLOA               | Any osteoarthritis                                    | EFO:0002506 |
| ALP                 | Alkaline phosphatase                                  | EFO:0004533 |
| ALS                 | ALS                                                   | EFO:0000253 |
| ALT                 | Alanine transaminase                                  | EFO:0004735 |
| AMD                 | Age-related macular degeneration                      | EFO:0001365 |
| ApoA1               | Serum ApoA1                                           | EFO:0004614 |
| ApoB                | Serum ApoB                                            | EFO:0004615 |
| AST                 | Aspartate aminotransferase                            | EFO:0004736 |
| BFP                 | Body fat percentage                                   | EFO:0007800 |
| BILIRUBIN           | Bilirubin                                             | EFO:0004570 |
| BIP                 | Bipolar disorder                                      | EFO:0000289 |
| BMI                 | BMI                                                   | EFO:0004340 |
| bOHBut              | Beta-hydroxybutyric acid                              | EFO:0010465 |
| BUN                 | Blood urea nitrogen                                   | EFO:0004741 |
| Ca                  | Calcium                                               | EFO:0004838 |
| CAD                 | Coronary artery disease                               | EFO:0000378 |
| CD                  | Crohn's disease                                       | EFO:0000384 |
| CHOL                | Total cholesterol                                     | EFO:0004574 |
| Cit                 | Citrate                                               | EFO:0010114 |
| CK                  | Creatine kinase                                       | EFO:0004534 |
| CKD                 | Chronic kidney disease                                | EFO:0003884 |
| Cl                  | Chloride                                              | EFO:0009284 |
| COPD                | Chronic obstructive pulmonary disease                 | EFO:0000341 |
| Creatinine          | Creatinine                                            | EFO:0004518 |
| CRP                 | Plasma C-reactive protein                             | EFO:0004458 |
| DBP                 | Diastolic blood pressure                              | EFO:0006336 |
| DI                  | Disposition index                                     | EFO:0006832 |
| eBMD                | Estimated bone mineral density                        | EFO:0009270 |
| EtOH                | Alcohol consumption                                   | EFO:0007878 |
| FAw3                | Omega-3 fatty acids                                   | EFO:0010119 |
| FAw6                | Omega-6 fatty acids                                   | EFO:0005680 |
| Fbg                 | Fibrinogen                                            | EFO:0004623 |
| FEV1                | Forced expired volume in 1 second (FEV1)              | EFO:0004314 |
| FEV1toFVC           | FEV1 to FVC ratio                                     | EFO:0004713 |
| FG                  | Fasting glucose                                       | EFO:0004465 |
| FGadjBMI            | Fasting glucose adj BMI                               | EFO:0008036 |
| FGovertime          | Fasting glucose change over time                      | EFO:0010120 |
| FG_plus_diab        | Fasting plasma glucose in diabetics and non-diabetics | EFO:0004465 |
| FI                  | Fasting insulin                                       | EFO:0004466 |
| FIadjBMI            | Fasting insulin adj BMI                               | EFO:0008037 |
| FNarea              | Femoral neck area                                     | EFO:0010076 |
| Fracture            | Bone fracture                                         | EFO:0003931 |
| FVC                 | Forced vital capacity (FVC)                           | EFO:0004312 |
| GGT                 | Gamma-glutamyl transferase                            | EFO:0004532 |
| Gln                 | Glutamine                                             | EFO:0009768 |
| Glol                | Glycerol                                              | EFO:0010115 |
| Gly                 | Glycine                                               | EFO:0009767 |
| Gp                  | Glycoproteins                                         | EFO:0004555 |
| Hb                  | Hemoglobin                                            | EFO:0004509 |
| HBA1C               | HbA1c                                                 | EFO:0004541 |
| HDL                 | HDL cholesterol                                       | EFO:0004612 |
| HEIGHT              | Height                                                | EFO:0004339 |
| HF                  | Heart failure                                         | EFO:0003144 |
| HIPC                | Hip circumference                                     | EFO:0005093 |
| HIPCadjBMI          | Hip circumference adj BMI                             | EFO:0008039 |
| HIPOA               | Hip osteoarthritis                                    | EFO:1000786 |
| His                 | Histidine                                             | EFO:0009769 |
| HOMAB               | HOMA-B                                                | EFO:0004469 |
| HOMAIR              | HOMA-IR                                               | EFO:0004501 |
| HR                  | Heart rate                                            | EFO:0004326 |
| IBD                 | Inflammatory bowel disease                            | EFO:0003767 |
| IDLchol             | IDL cholesterol                                       | EFO:0008595 |
| IGI                 | Insulinogenic index                                   | EFO:0009961 |
| Ile                 | Isoleucine                                            | EFO:0009793 |
| IntertrochArea      | Intertrochanteric-shaft area                          | EFO:0010075 |
| ISen                | Insulin sensitivity                                   | EFO:0004471 |
| K                   | Potassium                                             | EFO:0009283 |
| KNEEOA              | Knee osteoarthritis                                   | EFO:0004616 |
| lateDKD             | Late diabetic kidney disease                          | EFO:0004997 |
| LDH                 | Lactate dehydrogenase                                 | EFO:0004808 |
| LDL                 | LDL cholesterol                                       | EFO:0004611 |
| LEP                 | Leptin                                                | EFO:0005000 |
| Leu                 | Leucine                                               | EFO:0009770 |
| LVEF                | Left ventricular ejection fraction                    | EFO:0008373 |
| MAP                 | Mean arterial pressure                                | EFO:0006340 |
| MDD                 | Major depressive disorder                             | EFO:0003761 |
| MeanSleepDuration   | Mean sleep duration                                   | EFO:0005271 |
| MeanSleepDurationRN | Mean sleep duration, rank-normalized                  | EFO:0005271 |
| Men                 | Menarche                                              | EFO:0004703 |
| MI                  | Myocardial infarction                                 | EFO:0000612 |
| MP                  | Menopause                                             | EFO:0004704 |
| n6FA182             | Linoleic acid                                         | EFO:0006807 |
| ND                  | Neovascular age-related macular degeneration          | EFO:0004683 |
| NeuropathyinT2D     | Neuropathy in type 2 diabetics                        | EFO:1000783 |
| NICM                | Nonischemic cardiomyopathy                            | EFO:0009881 |
| P                   | Phosphorus                                            | EFO:0004861 |
| PACG                | Primary angle closure glaucoma                        | EFO:1001506 |
| PEAK                | Peak insulin response                                 | EFO:0008000 |
| PEF                 | Peak expiratory flow                                  | EFO:0009718 |
| Phe                 | Phenylalanine                                         | EFO:0005001 |
| POAG                | Open-angle glaucoma                                   | EFO:0004190 |
| PRI                 | PR interval                                           | EFO:0004462 |
| PulsePress          | Pulse pressure                                        | EFO:0005763 |
| Pwave_duration      | P-wave duration                                       | EFO:0005094 |
| Pyr                 | Pyruvate                                              | EFO:0010117 |
| QRS                 | QRS interval                                          | EFO:0005055 |
| RedCount            | Red blood cell count                                  | EFO:0004305 |
| SBP                 | Systolic blood pressure                               | EFO:0006335 |
| SCZ                 | Schizophrenia                                         | EFO:0000692 |
| SleepChronotype     | Chronotype (morningness)                              | EFO:0008328 |
| SleepDuration       | Sleep duration                                        | EFO:0005271 |
| SleepEDS            | Excessive daytime sleepiness                          | EFO:0005246 |
| SleepInsomnia       | Frequent insomnia symptoms                            | EFO:0004698 |
| SleepNaps           | Naps                                                  | EFO:0007828 |
| SM                  | Sphingomyelins                                        | EFO:0010118 |
| Sodium              | Sodium                                                | EFO:0009282 |
| Stroke_deep         | Non-lobar intracranial hemorrhage                     | EFO:0010178 |
| Stroke_hemorrhagic  | All intracranial hemorrhage                           | EFO:0000551 |
| Stroke_lobar        | Lobar intracranial hemorrhage                         | EFO:0010177 |
| SVL                 | Stroke volume                                         | EFO:0010555 |
| T1D                 | Type 1 diabetes                                       | EFO:0001359 |
| T2D                 | Type 2 diabetes                                       | EFO:0001360 |
| TG                  | Triglycerides                                         | EFO:0004530 |
| TGtoHDL             | Triglyceride-to-HDL ratio                             | EFO:0007929 |
| Thyroid             | Hypothyroidism                                        | EFO:0004705 |
| TotCho              | Total cholines                                        | EFO:0010116 |
| TotHipArea          | Total hip area                                        | EFO:0004844 |
| TotPG               | Total phosphoglycerides                               | EFO:0007630 |
| TrochanterArea      | Trochanter area                                       | EFO:0010074 |
| Tyr                 | Tyrosine                                              | EFO:0005058 |
| UA                  | Uric acid                                             | EFO:0004761 |
| UACR                | Urinary albumin-to-creatinine ratio                   | EFO:0007778 |
| UACR_nonDM          | UACR in non-diabetics                                 | EFO:0007778 |
| UC                  | Ulcerative colitis                                    | EFO:0000729 |
| Val                 | Valine                                                | EFO:0009792 |
| VitD                | Vitamin D                                             | EFO:0004631 |
| WAIST               | Waist circumference                                   | EFO:0004342 |
| WAISTadjBMI         | Waist circumference adj BMI                           | EFO:0007789 |
| WEIGHT              | Weight                                                | EFO:0004338 |
| WHR                 | Waist-hip ratio                                       | EFO:0004343 |
| WHRadjBMI           | Waist-hip ratio adj BMI                               | EFO:0007788 |
| WMH                 | Cerebral white matter hyperintensity volume           | EFO:0005665 |
| XXLVLDLpart         | Chylomicrons and XXL-VLDL cholesterol                 | EFO:0008596 |
+---------------------+-------------------------------------------------------+-------------+
```

## Phenotypes available for the Magma pathway associations (currently 82)
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

## Phenotypes available for the Integrated Genetics method gene associations (currently 10)
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



