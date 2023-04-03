

select count(id) from data_600k_gene_phenotype;
-- +-----------+
-- | count(id) |
-- +-----------+
-- |  22165137 |
-- +-----------+
-- 1 row in set (15.33 sec)

desc data_600k_gene_phenotype;
-- +------------------------+--------------+------+-----+-------------------+-------------------+
-- | Field                  | Type         | Null | Key | Default           | Extra             |
-- +------------------------+--------------+------+-----+-------------------+-------------------+
-- | id                     | int          | NO   | PRI | NULL              | auto_increment    |
-- | gene_code              | varchar(250) | NO   |     | NULL              |                   |
-- | phenotype_code         | varchar(50)  | NO   | MUL | NULL              |                   |
-- | phenotype              | varchar(150) | NO   |     | NULL              |                   |
-- | ancestry               | varchar(50)  | NO   |     | NULL              |                   |
-- | mask                   | varchar(50)  | NO   | MUL | NULL              |                   |
-- | combined_af            | double       | YES  |     | NULL              |                   |
-- | std_error              | double       | YES  |     | NULL              |                   |
-- | beta                   | double       | YES  |     | NULL              |                   |
-- | p_value                | double       | NO   | MUL | NULL              |                   |
-- | date_created           | datetime     | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
-- | probability_calculated | double       | YES  |     | NULL              |                   |
-- +------------------------+--------------+------+-----+-------------------+-------------------+
-- 12 rows in set (0.01 sec)

select count(id) from data_600k_gene_phenotype where probability_calculated is null;
-- +-----------+
-- | count(id) |
-- +-----------+
-- |   3778227 |
-- +-----------+
-- 1 row in set (6.99 sec)

select count(id) from data_600k_gene_phenotype where probability_calculated > 0.15;
-- +-----------+
-- | count(id) |
-- +-----------+
-- |   2936177 |
-- +-----------+
-- 1 row in set (6.98 sec)

select count(id) from data_genebass_gene_phenotype where probability > 0.15;
-- +-----------+
-- | count(id) |
-- +-----------+
-- |     17201 |
-- +-----------+
-- 1 row in set (1.63 sec)

select count(id) from data_genebass_gene_phenotype;
-- +-----------+
-- | count(id) |
-- +-----------+
-- |   2780551 |
-- +-----------+
-- 1 row in set (0.21 sec)


