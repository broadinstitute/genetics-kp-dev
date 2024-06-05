
-- cacche table
drop table if exists tran_cache_entity;
create table tran_cache_entity (
  id                        INTEGER PRIMARY KEY,
  input_entity              TEXT not null,
  genetics_entity           TEXT not null,
  ancestry_type             TEXT CHECK(ancestry_type IN ('synonym', 'parent', 'parent_synonym')),
  created_at                DATE DEFAULT (DATE('now', 'localtime'))
);


