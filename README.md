# Genetics Knowledge API
Code repository for the maintenance of the Translator API for the Broad Institute's Genetics Team comprising members of the [Flannick Lab](http://www.flannicklab.org/).

# Docker Deployment Instructions
To deploy a dockerized version of this service, follow the following steps:
* checkout the master branch of this directory
* cd into the newly checked out directory; the two main files are
  * Dockerfile - provides the commands to build the docker image
  * build_docker.txt - provides the command options to build the docker image
* modify the build_docker.txt script (or a copy of it) to set the following docker variables which are used by the Dockerfile
  * fl_port - the network port that the application services
  * db_host - the Mysql database host
  * db_user - the Mysql database user name
  * db_passwd - the Mysql database user password
  * db_schema - the Mysql database schema for the application
  * db_cache_schema - the Mysql database schema for the application cache (default is the same as the regular schema)
  * db_results_limit - the maximum limit of how many results the service will send back (default is 150)
  * tran_log_file - the location of the log file the application will log its messages to
  * tran_max_query_size - this indicates how big a query size the service will accept (recommended default is 100000)
  * tran_url_normalizer - the URL of the NCATS node normalizer service (default is https://nodenormalization-sri.renci.org/get_normalized_nodes)
* build the docker image using the build_docker.txt file (. ./build_docker.txt)
* deploy the docker image

# Data Available
The Genetics KP provides the following data

## Currently Available
* Richards method gene/phenotype associations
  * Forgetta V, Jiang L, Vulpescu NA, et al. An Effector Index to Predict Causal Genes at GWAS Loci. Submitted for publication, 2020.
        [BioRxiv](https://www.biorxiv.org/content/10.1101/2020.06.28.171561v1)

* Magma gene/phenotype associations and Magma pathway/phenotype associations
  * de Leeuw CA, et al. MAGMA: generalized gene-set analysis of GWAS data. PLoS Comput Biol. 2015 Apr 17;11(4):e1004219. doi: 10.1371/journal.pcbi.1004219.
        PMID: 25885710
        [software](https://ctg.cncr.nl/software/magma),
        [paper](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1004219)

* ABC method gene to phenotype associations
  * Fulco JP, Nasser J., et al. Activity-by-contact model of enhancer-promoter regulation from thousands of CRISPR perturbations. 
      Nat Genet. 2019 Dec;51(12):1664-1669.     
      doi: 10.1038/s41588-019-0538-0.
      PMID: 31784727
      [paper](https://www.nature.com/articles/s41588-019-0538-0?proof=t)

* Experimental Integrated Genetics method (Flannick Lab); under development

## Added on 01/16/2021
  * An extra 41 phenotypes added to the magma gene associations (from 145 to 186)
  * Upgraded the API to be trapi v1.0 compatible

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

## Phenotypes available for the Magma gene associations (currently 186)
```
+--------------------------------------------------+-----------------------+
| phenotype                                        | phenotype_ontology_id |
+--------------------------------------------------+-----------------------+
| acetate measurement                              | EFO:0010112           |
| acetoaetate measurement                          | EFO:0010111           |
| acquired aneurysmal subarachnoid hemorrhage      | MONDO:0019543         |
| acute insulin response measurement               | EFO:0006831           |
| adiponectin measurement                          | EFO:0004502           |
| age at menarche                                  | EFO:0004703           |
| age at menopause                                 | EFO:0004704           |
| age-related macular degeneration                 | EFO:0001365           |
| alanine measurement                              | EFO:0009765           |
| alcohol consumption measurement                  | EFO:0007878           |
| alkaline phosphatase measurement                 | EFO:0004533           |
| Alzheimer's disease                              | EFO:0000249           |
| amyotrophic lateral sclerosis                    | EFO:0000253           |
| apolipoprotein A 1 measurement                   | EFO:0004614           |
| apolipoprotein measurement                       | EFO:0004615           |
| appendicular lean mass                           | EFO:0004980           |
| aspartate aminotransferase measurement           | EFO:0004736           |
| atrial fibrillation                              | EFO:0000275           |
| atrial fibrillation (disease)                    | MONDO:0004981         |
| atrophic macular degeneration                    | EFO:1001492           |
| beta-hydroxybutyric acid measurement             | EFO:0010465           |
| bilirubin measurement                            | EFO:0004570           |
| bipolar disorder                                 | EFO:0000289           |
| blood urea nitrogen measurement                  | EFO:0004741           |
| BMI-adjusted fasting blood glucose measurement   | EFO:0008036           |
| BMI-adjusted fasting blood insulin measurement   | EFO:0008037           |
| BMI-adjusted hip circumference                   | EFO:0008039           |
| BMI-adjusted waist circumference                 | EFO:0007789           |
| BMI-adjusted waist-hip ratio                     | EFO:0007788           |
| body fat percentage                              | EFO:0007800           |
| body height                                      | EFO:0004339           |
| body mass index                                  | EFO:0004340           |
| body weight                                      | EFO:0004338           |
| bone density                                     | EFO:0003923           |
| bone fracture                                    | EFO:0003931           |
| brain aneurysm                                   | MONDO:0005291         |
| C-peptide measurement                            | EFO:0005187           |
| C-reactive protein measurement                   | EFO:0004458           |
| calcium measurement                              | EFO:0004838           |
| cardiovascular disease                           | EFO:0000319           |
| cerebrovascular disorder                         | EFO:0003763           |
| chloride measurement                             | EFO:0009284           |
| chronic kidney disease                           | EFO:0003884           |
| chronic obstructive pulmonary disease            | EFO:0000341           |
| chronotype measurement                           | EFO:0008328           |
| chylomicron measurement                          | EFO:0008596           |
| citrate measurement                              | EFO:0010114           |
| coronary artery disease                          | EFO:0000378           |
| COVID-19                                         | MONDO:0100096         |
| creatine kinase measurement                      | EFO:0004534           |
| Crohn's disease                                  | EFO:0000384           |
| daytime rest measurement                         | EFO:0007828           |
| diabetic nephropathy                             | EFO:0000401           |
| diabetic neuropathy                              | EFO:1000783           |
| diabetic peripheral angiopathy                   | MONDO:0000960         |
| diabetic retinopathy                             | MONDO:0005266         |
| diastolic blood pressure                         | EFO:0006336           |
| diet measurement                                 | EFO:0008111           |
| disposition index measurement                    | EFO:0006832           |
| end stage renal failure                          | MONDO:0004375         |
| erythrocyte count                                | EFO:0004305           |
| fasting blood glucose change measurement         | EFO:0010120           |
| fasting blood glucose measurement                | EFO:0004465           |
| fasting blood insulin measurement                | EFO:0004466           |
| fasting C-peptide measurement                    | EFO:0010813           |
| fatty acid measurement                           | EFO:0005110           |
| femoral neck bone mineral density                | EFO:0007785           |
| femoral neck size                                | EFO:0010076           |
| FEV/FEC ratio                                    | EFO:0004713           |
| fibrinogen measurement                           | EFO:0004623           |
| fish consumption measurement                     | EFO:0010139           |
| forced expiratory volume                         | EFO:0004314           |
| glomerular filtration rate                       | EFO:0005208           |
| glucose measurement                              | EFO:0004468           |
| glucose tolerance test                           | EFO:0004307           |
| glutamine measurement                            | EFO:0009768           |
| glycerol measurement                             | EFO:0010115           |
| glycerophospholipid measurement                  | EFO:0007630           |
| glycine measurement                              | EFO:0009767           |
| glycoprotein measurement                         | EFO:0004555           |
| HbA1c measurement                                | EFO:0004541           |
| heart failure                                    | EFO:0003144           |
| heart rate                                       | EFO:0004326           |
| heel bone mineral density                        | EFO:0009270           |
| hemoglobin measurement                           | EFO:0004509           |
| high density lipoprotein cholesterol measurement | EFO:0004612           |
| hip bone size                                    | EFO:0004844           |
| hip circumference                                | EFO:0005093           |
| histidine measurement                            | EFO:0009769           |
| HOMA-B                                           | EFO:0004469           |
| HOMA-IR                                          | EFO:0004501           |
| hypersomnia                                      | EFO:0005246           |
| hypertension                                     | EFO:0000537           |
| hypothyroidism                                   | EFO:0004705           |
| inflammatory bowel disease                       | EFO:0003767           |
| insomnia                                         | EFO:0004698           |
| insulin measurement                              | EFO:0004467           |
| insulin response measurement                     | EFO:0008473           |
| insulin secretion measurement                    | EFO:0008001           |
| insulin sensitivity measurement                  | EFO:0004471           |
| Insulinogenic index measurement                  | EFO:0009961           |
| intermediate density lipoprotein measurement     | EFO:0008595           |
| intertrochanteric region size                    | EFO:0010075           |
| intracranial hemorrhage                          | EFO:0000551           |
| isoleucine measurement                           | EFO:0009793           |
| L lactate dehydrogenase measurement              | EFO:0004808           |
| late-onset Alzheimers disease                    | EFO:1001870           |
| latent autoimmune diabetes in adults             | EFO:0009706           |
| lean body mass                                   | EFO:0004995           |
| left ventricular diastolic function measurement  | EFO:0008204           |
| left ventricular ejection fraction measurement   | EFO:0008373           |
| left ventricular stroke volume measurement       | EFO:0010555           |
| left ventricular systolic function measurement   | EFO:0008206           |
| leptin measurement                               | EFO:0005000           |
| leucine measurement                              | EFO:0009770           |
| linoleic acid measurement                        | EFO:0006807           |
| lipoprotein measurement                          | EFO:0004732           |
| lobar intracerebral hemorrhage                   | EFO:0010177           |
| low density lipoprotein cholesterol measurement  | EFO:0004611           |
| mean arterial pressure                           | EFO:0006340           |
| membranous glomerulonephritis                    | MONDO:0005376         |
| myocardial infarction                            | EFO:0000612           |
| myocardial infarction (disease)                  | MONDO:0005068         |
| non-lobar intracerebral hemorrhage               | EFO:0010178           |
| nonischemic cardiomyopathy                       | EFO:0009881           |
| obesity                                          | EFO:0001073           |
| obesity disorder                                 | MONDO:0011122         |
| omega-3 polyunsaturated fatty acid measurement   | EFO:0010119           |
| omega-6 polyunsaturated fatty acid measurement   | EFO:0005680           |
| open-angle glaucoma                              | EFO:0004190           |
| osteoarthritis                                   | EFO:0002506           |
| osteoarthritis, hip                              | EFO:1000786           |
| osteoarthritis, knee                             | EFO:0004616           |
| P wave duration                                  | EFO:0005094           |
| peak expiratory flow                             | EFO:0009718           |
| peak insulin response measurement                | EFO:0008000           |
| phenylalanine measurement                        | EFO:0005001           |
| phosphorus measurement                           | EFO:0004861           |
| potassium measurement                            | EFO:0009283           |
| PR interval                                      | EFO:0004462           |
| primary angle closure glaucoma                   | EFO:1001506           |
| proinsulin measurement                           | EFO:0010814           |
| proliferative diabetic retinopathy               | MONDO:0001660         |
| pulse pressure measurement                       | EFO:0005763           |
| pyruvate measurement                             | EFO:0010117           |
| QRS duration                                     | EFO:0005055           |
| remnant cholesterol measurement                  | EFO:0010815           |
| schizophrenia                                    | EFO:0000692           |
| secondary hypertension                           | MONDO:0001200         |
| serum alanine aminotransferase measurement       | EFO:0004735           |
| serum albumin measurement                        | EFO:0004535           |
| serum creatinine measurement                     | EFO:0004518           |
| serum gamma-glutamyl transferase measurement     | EFO:0004532           |
| serum urea measurement                           | EFO:0009795           |
| severe nonproliferative diabetic retinopathy     | MONDO:0004687         |
| sleep apnea measurement                          | EFO:0007817           |
| sleep apnea measurement during non-REM sleep     | EFO:0008456           |
| sleep apnea measurement during REM sleep         | EFO:0008455           |
| sleep measurement                                | EFO:0004870           |
| sodium measurement                               | EFO:0009282           |
| sphingomyelin measurement                        | EFO:0010118           |
| spine bone mineral density                       | EFO:0007701           |
| spine bone size                                  | EFO:0004508           |
| systolic blood pressure                          | EFO:0006335           |
| total cholesterol measurement                    | EFO:0004574           |
| total cholines                                   | EFO:0010116           |
| triglyceride measurement                         | EFO:0004530           |
| triglyceride:HDL cholesterol ratio               | EFO:0007929           |
| trochanter size                                  | EFO:0010074           |
| type 2 diabetes nephropathy                      | EFO:0004997           |
| type I diabetes mellitus                         | EFO:0001359           |
| type II diabetes mellitus                        | EFO:0001360           |
| tyrosine measurement                             | EFO:0005058           |
| ulcerative colitis                               | EFO:0000729           |
| unipolar depression                              | EFO:0003761           |
| urate measurement                                | EFO:0004531           |
| uric acid measurement                            | EFO:0004761           |
| urinary albumin to creatinine ratio              | EFO:0007778           |
| urinary metabolite measurement                   | EFO:0005116           |
| valine measurement                               | EFO:0009792           |
| vital capacity                                   | EFO:0004312           |
| vitamin D measurement                            | EFO:0004631           |
| waist circumference                              | EFO:0004342           |
| waist-hip ratio                                  | EFO:0004343           |
| wet macular degeneration                         | EFO:0004683           |
| white matter hyperintensity measurement          | EFO:0005665           |
+--------------------------------------------------+-----------------------+
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



