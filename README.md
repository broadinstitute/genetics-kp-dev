# Genetics Knowledge API
Code repository for the maintenance of the Translator API for the Broad Institute's Genetics Team comprising members of the [Flannick Lab](http://www.flannicklab.org/).

# Data Available
The Genetics KP provides the following data

## Currently Available
* Magma gene/phenotype associations and Magma pathway/phenotype associations
  * de Leeuw CA, et al. MAGMA: generalized gene-set analysis of GWAS data. PLoS Comput Biol. 2015 Apr 17;11(4):e1004219. doi: 10.1371/journal.pcbi.1004219.
        PMID: 25885710
        [paper](https://ctg.cncr.nl/software/magma)

* Experimental Integrated Genetics method (Flannick Lab); under development

## Available by 12/16/2020
* Richards method gene/phenotype associations
  * Forgetta V, Jiang L, Vulpescu NA, et al. An Effector Index to Predict Causal Genes at GWAS Loci. Submitted for publication, 2020.
        [BioRxiv](https://www.biorxiv.org/content/10.1101/2020.06.28.171561v1)

* ABC method gene to phenotype associations
  * Fulco JP, Nasser J., et al. Activity-by-contact model of enhancer-promoter regulation from thousands of CRISPR perturbations. 
    Nat Genet. 2019 Dec;51(12):1664-1669.     
    doi: 10.1038/s41588-019-0538-0.
    PMID: 31784727

## Available by 01/16/2021
  * An extra 15 phenotypes added to the magma gene associations (from 145 to 160)
  * An extra 15 phenotypes added to the magma pathway associations (from 82 to 95)

# Phenotypes currently available for each method

## Phenotypes available for the Richards method gene associations (currently 10)
```
+--------------------------------+-------------+
| phenotype                      | efo_id      |
+--------------------------------+-------------+
| Calcium                        | EFO:0004838 |
| Diastolic blood pressure       | EFO:0006336 |
| Estimated bone mineral density | EFO:0009270 |
| Height                         | EFO:0004339 |
| Hypothyroidism                 | EFO:0004705 |
| LDL cholesterol                | EFO:0004611 |
| Red blood cell count           | EFO:0004305 |
| Systolic blood pressure        | EFO:0006335 |
| Triglycerides                  | EFO:0004530 |
| Type 2 diabetes                | EFO:0001360 |
+--------------------------------+-------------+
```

## Phenotypes available for the Magma gene associations (currently 145)
```
+-------------------------------------------------------+-------------+
| phenotype                                             | efo_id      |
+-------------------------------------------------------+-------------+
| Acetate                                               | EFO:0010112 |
| Acetoacetate                                          | EFO:0010111 |
| Acute insulin response                                | EFO:0006831 |
| Adiponectin                                           | EFO:0004502 |
| Age-related macular degeneration                      | EFO:0001365 |
| Alanine                                               | EFO:0009765 |
| Alanine transaminase                                  | EFO:0004735 |
| Alcohol consumption                                   | EFO:0007878 |
| Alkaline phosphatase                                  | EFO:0004533 |
| All diabetic kidney disease                           | EFO:0000401 |
| All intracranial hemorrhage                           | EFO:0000551 |
| ALS                                                   | EFO:0000253 |
| Alzheimer's disease                                   | EFO:0000249 |
| Any osteoarthritis                                    | EFO:0002506 |
| Apnea-Hypopnea Index                                  | EFO:0007817 |
| Apnea-Hypopnea Index in NREM sleep                    | EFO:0008456 |
| Apnea-Hypopnea Index in REM sleep                     | EFO:0008455 |
| Aspartate aminotransferase                            | EFO:0004736 |
| Atrial fibrillation                                   | EFO:0000275 |
| Beta-hydroxybutyric acid                              | EFO:0010465 |
| Bilirubin                                             | EFO:0004570 |
| Bipolar disorder                                      | EFO:0000289 |
| Blood urea nitrogen                                   | EFO:0004741 |
| BMI                                                   | EFO:0004340 |
| Body fat percentage                                   | EFO:0007800 |
| Bone fracture                                         | EFO:0003931 |
| Calcium                                               | EFO:0004838 |
| Cerebral white matter hyperintensity volume           | EFO:0005665 |
| Chloride                                              | EFO:0009284 |
| Chronic kidney disease                                | EFO:0003884 |
| Chronic obstructive pulmonary disease                 | EFO:0000341 |
| Chronotype (morningness)                              | EFO:0008328 |
| Chylomicrons and XXL-VLDL cholesterol                 | EFO:0008596 |
| Citrate                                               | EFO:0010114 |
| Coronary artery disease                               | EFO:0000378 |
| Creatine kinase                                       | EFO:0004534 |
| Creatinine                                            | EFO:0004518 |
| Crohn's disease                                       | EFO:0000384 |
| Diastolic blood pressure                              | EFO:0006336 |
| Disposition index                                     | EFO:0006832 |
| Estimated bone mineral density                        | EFO:0009270 |
| Excessive daytime sleepiness                          | EFO:0005246 |
| Fasting glucose                                       | EFO:0004465 |
| Fasting glucose adj BMI                               | EFO:0008036 |
| Fasting glucose change over time                      | EFO:0010120 |
| Fasting insulin                                       | EFO:0004466 |
| Fasting insulin adj BMI                               | EFO:0008037 |
| Fasting plasma glucose in diabetics and non-diabetics | EFO:0004465 |
| Femoral neck area                                     | EFO:0010076 |
| FEV1 to FVC ratio                                     | EFO:0004713 |
| Fibrinogen                                            | EFO:0004623 |
| Forced expired volume in 1 second (FEV1)              | EFO:0004314 |
| Forced vital capacity (FVC)                           | EFO:0004312 |
| Frequent insomnia symptoms                            | EFO:0004698 |
| Gamma-glutamyl transferase                            | EFO:0004532 |
| Glutamine                                             | EFO:0009768 |
| Glycerol                                              | EFO:0010115 |
| Glycine                                               | EFO:0009767 |
| Glycoproteins                                         | EFO:0004555 |
| HbA1c                                                 | EFO:0004541 |
| HDL cholesterol                                       | EFO:0004612 |
| Heart failure                                         | EFO:0003144 |
| Heart rate                                            | EFO:0004326 |
| Height                                                | EFO:0004339 |
| Hemoglobin                                            | EFO:0004509 |
| Hip circumference                                     | EFO:0005093 |
| Hip circumference adj BMI                             | EFO:0008039 |
| Hip osteoarthritis                                    | EFO:1000786 |
| Histidine                                             | EFO:0009769 |
| HOMA-B                                                | EFO:0004469 |
| HOMA-IR                                               | EFO:0004501 |
| Hypothyroidism                                        | EFO:0004705 |
| IDL cholesterol                                       | EFO:0008595 |
| Inflammatory bowel disease                            | EFO:0003767 |
| Insulin sensitivity                                   | EFO:0004471 |
| Insulinogenic index                                   | EFO:0009961 |
| Intertrochanteric-shaft area                          | EFO:0010075 |
| Isoleucine                                            | EFO:0009793 |
| Knee osteoarthritis                                   | EFO:0004616 |
| Lactate dehydrogenase                                 | EFO:0004808 |
| Late diabetic kidney disease                          | EFO:0004997 |
| LDL cholesterol                                       | EFO:0004611 |
| Left ventricular ejection fraction                    | EFO:0008373 |
| Leptin                                                | EFO:0005000 |
| Leucine                                               | EFO:0009770 |
| Linoleic acid                                         | EFO:0006807 |
| Lobar intracranial hemorrhage                         | EFO:0010177 |
| Major depressive disorder                             | EFO:0003761 |
| Mean arterial pressure                                | EFO:0006340 |
| Mean sleep duration                                   | EFO:0005271 |
| Mean sleep duration, rank-normalized                  | EFO:0005271 |
| Menarche                                              | EFO:0004703 |
| Menopause                                             | EFO:0004704 |
| Myocardial infarction                                 | EFO:0000612 |
| Naps                                                  | EFO:0007828 |
| Neovascular age-related macular degeneration          | EFO:0004683 |
| Neuropathy in type 2 diabetics                        | EFO:1000783 |
| Non-lobar intracranial hemorrhage                     | EFO:0010178 |
| Nonischemic cardiomyopathy                            | EFO:0009881 |
| Omega-3 fatty acids                                   | EFO:0010119 |
| Omega-6 fatty acids                                   | EFO:0005680 |
| Open-angle glaucoma                                   | EFO:0004190 |
| P-wave duration                                       | EFO:0005094 |
| Peak expiratory flow                                  | EFO:0009718 |
| Peak insulin response                                 | EFO:0008000 |
| Phenylalanine                                         | EFO:0005001 |
| Phosphorus                                            | EFO:0004861 |
| Plasma C-reactive protein                             | EFO:0004458 |
| Potassium                                             | EFO:0009283 |
| PR interval                                           | EFO:0004462 |
| Primary angle closure glaucoma                        | EFO:1001506 |
| Pulse pressure                                        | EFO:0005763 |
| Pyruvate                                              | EFO:0010117 |
| QRS interval                                          | EFO:0005055 |
| Red blood cell count                                  | EFO:0004305 |
| Schizophrenia                                         | EFO:0000692 |
| Serum albumin                                         | EFO:0004535 |
| Serum ApoA1                                           | EFO:0004614 |
| Serum ApoB                                            | EFO:0004615 |
| Sleep duration                                        | EFO:0005271 |
| Sodium                                                | EFO:0009282 |
| Sphingomyelins                                        | EFO:0010118 |
| Stroke volume                                         | EFO:0010555 |
| Systolic blood pressure                               | EFO:0006335 |
| Total cholesterol                                     | EFO:0004574 |
| Total cholines                                        | EFO:0010116 |
| Total hip area                                        | EFO:0004844 |
| Total phosphoglycerides                               | EFO:0007630 |
| Triglyceride-to-HDL ratio                             | EFO:0007929 |
| Triglycerides                                         | EFO:0004530 |
| Trochanter area                                       | EFO:0010074 |
| Type 1 diabetes                                       | EFO:0001359 |
| Type 2 diabetes                                       | EFO:0001360 |
| Tyrosine                                              | EFO:0005058 |
| UACR in non-diabetics                                 | EFO:0007778 |
| Ulcerative colitis                                    | EFO:0000729 |
| Uric acid                                             | EFO:0004761 |
| Urinary albumin-to-creatinine ratio                   | EFO:0007778 |
| Valine                                                | EFO:0009792 |
| Vitamin D                                             | EFO:0004631 |
| Waist circumference                                   | EFO:0004342 |
| Waist circumference adj BMI                           | EFO:0007789 |
| Waist-hip ratio                                       | EFO:0004343 |
| Waist-hip ratio adj BMI                               | EFO:0007788 |
| Weight                                                | EFO:0004338 |
+-------------------------------------------------------+-------------+
```

## Phenotypes available for the Magma pathway associations (currently 82)
```
+-------------------------------------------------------+-------------+
| phenotype                                             | efo_id      |
+-------------------------------------------------------+-------------+
| Adiponectin                                           | EFO:0004502 |
| Alanine transaminase                                  | EFO:0004735 |
| Alkaline phosphatase                                  | EFO:0004533 |
| All diabetic kidney disease                           | EFO:0000401 |
| ALS                                                   | EFO:0000253 |
| Alzheimer's disease                                   | EFO:0000249 |
| Any stroke                                            | EFO:0000712 |
| Apnea-Hypopnea Index                                  | EFO:0007817 |
| Apnea-Hypopnea Index in NREM sleep                    | EFO:0008456 |
| Apnea-Hypopnea Index in REM sleep                     | EFO:0008455 |
| Aspartate aminotransferase                            | EFO:0004736 |
| Atrial fibrillation                                   | EFO:0000275 |
| Bipolar disorder                                      | EFO:0000289 |
| BMI                                                   | EFO:0004340 |
| Body fat percentage                                   | EFO:0007800 |
| Bone fracture                                         | EFO:0003931 |
| Cerebral white matter hyperintensity volume           | EFO:0005665 |
| Chronic kidney disease                                | EFO:0003884 |
| Chronic obstructive pulmonary disease                 | EFO:0000341 |
| Chronotype (morningness)                              | EFO:0008328 |
| Coronary artery disease                               | EFO:0000378 |
| Creatinine                                            | EFO:0004518 |
| Crohn's disease                                       | EFO:0000384 |
| Diastolic blood pressure                              | EFO:0006336 |
| Dihomo-gamma-linoleic acid                            | EFO:0008356 |
| Disposition index                                     | EFO:0006832 |
| Estimated bone mineral density                        | EFO:0009270 |
| Excessive daytime sleepiness                          | EFO:0005246 |
| Fasting glucose                                       | EFO:0004465 |
| Fasting glucose adj BMI                               | EFO:0008036 |
| Fasting insulin                                       | EFO:0004466 |
| Fasting insulin adj BMI                               | EFO:0008037 |
| Fasting plasma glucose in diabetics and non-diabetics | EFO:0004465 |
| Frequent insomnia symptoms                            | EFO:0004698 |
| Gamma-glutamyl transferase                            | EFO:0004532 |
| Gamma-linolenic acid                                  | EFO:0007762 |
| HbA1c                                                 | EFO:0004541 |
| HDL cholesterol                                       | EFO:0004612 |
| Heart failure                                         | EFO:0003144 |
| Heart rate                                            | EFO:0004326 |
| Height                                                | EFO:0004339 |
| Hip circumference                                     | EFO:0005093 |
| Hip circumference adj BMI                             | EFO:0008039 |
| HOMA-B                                                | EFO:0004469 |
| HOMA-IR                                               | EFO:0004501 |
| Inflammatory bowel disease                            | EFO:0003767 |
| Insulin sensitivity                                   | EFO:0004471 |
| Insulinogenic index                                   | EFO:0009961 |
| Late diabetic kidney disease                          | EFO:0004997 |
| LDL cholesterol                                       | EFO:0004611 |
| Leptin                                                | EFO:0005000 |
| Linoleic acid                                         | EFO:0006807 |
| Lobar intracranial hemorrhage                         | EFO:0010177 |
| Major depressive disorder                             | EFO:0003761 |
| Mean sleep duration                                   | EFO:0005271 |
| Mean sleep duration, rank-normalized                  | EFO:0005271 |
| Naps                                                  | EFO:0007828 |
| Neuropathy in type 2 diabetics                        | EFO:1000783 |
| Non-HDL cholesterol                                   | EFO:0005689 |
| Non-lobar intracranial hemorrhage                     | EFO:0010178 |
| Nonischemic cardiomyopathy                            | EFO:0009881 |
| Oleic acid                                            | EFO:0006810 |
| P-wave duration                                       | EFO:0005094 |
| P-wave terminal force                                 | EFO:0008379 |
| Palmitoleic acid                                      | EFO:0007973 |
| Pericardial adipose tissue volume                     | EFO:0007890 |
| Ratio visceral-subcutaneous adipose tissue volume     | EFO:0004767 |
| Schizophrenia                                         | EFO:0000692 |
| Sleep duration                                        | EFO:0005271 |
| Subcutaneous adipose tissue volume                    | EFO:0004766 |
| Systolic blood pressure                               | EFO:0006335 |
| Total cholesterol                                     | EFO:0004574 |
| Triglycerides                                         | EFO:0004530 |
| Type 2 diabetes                                       | EFO:0001360 |
| UACR in non-diabetics                                 | EFO:0007778 |
| Ulcerative colitis                                    | EFO:0000729 |
| Urinary albumin-to-creatinine ratio                   | EFO:0007778 |
| Visceral adipose tissue volume                        | EFO:0004765 |
| Waist circumference                                   | EFO:0004342 |
| Waist circumference adj BMI                           | EFO:0007789 |
| Waist-hip ratio                                       | EFO:0004343 |
| Waist-hip ratio adj BMI                               | EFO:0007788 |
+-------------------------------------------------------+-------------+
```

## Phenotypes available for the ABC method gene associations (currently 65)
```
+-------------------------------------------------------+-------------+
| phenotype                                             | efo_id      |
+-------------------------------------------------------+-------------+
| Acute insulin response                                | EFO:0006831 |
| Adiponectin                                           | EFO:0004502 |
| Albuminuria                                           | EFO:0004285 |
| Alzheimer's disease                                   | EFO:0000249 |
| Atrial fibrillation                                   | EFO:0000275 |
| Bipolar disorder                                      | EFO:0000289 |
| Blood urea nitrogen                                   | EFO:0004741 |
| BMI                                                   | EFO:0004340 |
| Chronic kidney disease                                | EFO:0003884 |
| Chylomicrons and XXL-VLDL cholesterol                 | EFO:0008596 |
| Coronary artery disease                               | EFO:0000378 |
| Creatine kinase                                       | EFO:0004534 |
| Creatinine                                            | EFO:0004518 |
| Crohn's disease                                       | EFO:0000384 |
| Diastolic blood pressure                              | EFO:0006336 |
| Dihomo-gamma-linoleic acid                            | EFO:0008356 |
| Fasting glucose                                       | EFO:0004465 |
| Fasting glucose adj BMI                               | EFO:0008036 |
| Fasting insulin                                       | EFO:0004466 |
| Fasting plasma glucose in diabetics and non-diabetics | EFO:0004465 |
| Gamma-linolenic acid                                  | EFO:0007762 |
| HbA1c                                                 | EFO:0004541 |
| HDL cholesterol                                       | EFO:0004612 |
| Heart failure                                         | EFO:0003144 |
| Heart rate                                            | EFO:0004326 |
| Height                                                | EFO:0004339 |
| Hip circumference                                     | EFO:0005093 |
| Hip circumference adj BMI                             | EFO:0008039 |
| HOMA-B                                                | EFO:0004469 |
| Hypertension                                          | EFO:0000537 |
| IDL cholesterol                                       | EFO:0008595 |
| Inflammatory bowel disease                            | EFO:0003767 |
| LDL cholesterol                                       | EFO:0004611 |
| Left ventricular ejection fraction                    | EFO:0008373 |
| Leptin                                                | EFO:0005000 |
| Linoleic acid                                         | EFO:0006807 |
| Mean arterial pressure                                | EFO:0006340 |
| Non-HDL cholesterol                                   | EFO:0005689 |
| Nonischemic cardiomyopathy                            | EFO:0009881 |
| Oleic acid                                            | EFO:0006810 |
| Omega-3 fatty acids                                   | EFO:0010119 |
| Palmitoleic acid                                      | EFO:0007973 |
| Peak insulin response                                 | EFO:0008000 |
| Plasma C-reactive protein                             | EFO:0004458 |
| Proinsulin levels                                     | EFO:0010814 |
| Pulse pressure                                        | EFO:0005763 |
| Remnant cholesterol                                   | EFO:0010815 |
| Schizophrenia                                         | EFO:0000692 |
| Serum ApoA1                                           | EFO:0004614 |
| Serum ApoB                                            | EFO:0004615 |
| Stroke volume                                         | EFO:0010555 |
| Systolic blood pressure                               | EFO:0006335 |
| Total cholesterol                                     | EFO:0004574 |
| Triglyceride-to-HDL ratio                             | EFO:0007929 |
| Triglycerides                                         | EFO:0004530 |
| Type 1 diabetes                                       | EFO:0001359 |
| Type 2 diabetes                                       | EFO:0001360 |
| UACR in non-diabetics                                 | EFO:0007778 |
| Ulcerative colitis                                    | EFO:0000729 |
| Uric acid                                             | EFO:0004761 |
| Urinary albumin-to-creatinine ratio                   | EFO:0007778 |
| Waist circumference                                   | EFO:0004342 |
| Waist circumference adj BMI                           | EFO:0007789 |
| Waist-hip ratio                                       | EFO:0004343 |
| Waist-hip ratio adj BMI                               | EFO:0007788 |
+-------------------------------------------------------+-------------+
```

## Phenotypes available for the Integrated Genetics method gene associations (currently 10)
```
+-------------------------------------------------------+-------------+
| phenotype                                             | efo_id      |
+-------------------------------------------------------+-------------+
| Atrial fibrillation                                   | EFO:0000275 |
| Chronic kidney disease                                | EFO:0003884 |
| Coronary artery disease                               | EFO:0000378 |
| Fasting glucose                                       | EFO:0004465 |
| Fasting insulin                                       | EFO:0004466 |
| Fasting plasma glucose in diabetics and non-diabetics | EFO:0004465 |
| HbA1c                                                 | EFO:0004541 |
| HDL cholesterol                                       | EFO:0004612 |
| LDL cholesterol                                       | EFO:0004611 |
| Type 2 diabetes                                       | EFO:0001360 |
+-------------------------------------------------------+-------------+
```



