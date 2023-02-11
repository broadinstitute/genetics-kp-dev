

-- hack for now, but add field on edge that indicates there are qualifiers
-- indicates to make a second query and add to object
-- this keeps the joins minimal and keeps the fast result turnaround by the WS
-- TODO - add has_qualifier to edge table


-- create qualifier table
drop table if exists comb_qualifier;
create table comb_qualifier (
  id                        varchar(50) not null primary key,
  qualifier_type            varchar(50) not null,
  qualifier_value           varchar(50) not null,
  study_id                  int(3) not null,
  date_created              datetime DEFAULT CURRENT_TIMESTAMP
);


-- create qualifiers
-- aspect qualifiers
insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('subject_aspect_activity', 'subject_aspect_qualifier', 'activity');

insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('subject_aspect_severity', 'subject_aspect_qualifier', 'severity');

-- direction qualifiers
insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('subject_direction_increased', 'subject_direction_qualifier', 'increased');

insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('subject_direction_decreased', 'subject_direction_qualifier', 'decreased');

insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('object_direction_increased', 'object_direction_qualifier', 'increased');

insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('object_direction_decreased', 'object_direction_qualifier', 'decreased');

-- predicate qualifier
insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('qualified_predicate_causes', 'qualified_predicate', 'causes');


-- create qualifier link table
drop table if exists comb_edge_qualifier;
create table comb_edge_qualifier (
  id                        int not null auto_increment primary key,
  edge_id                   int(9) not null,
  qualifier_id              varchar(50) not null,
  date_created              datetime DEFAULT CURRENT_TIMESTAMP
);

-- indices
alter table comb_edge_qualifier add index comb_edg_qua_edg_idx (edge_id);








-- updates to existing tables 
-- 20230208 - adding 600k ellinor study
insert into comb_study_type (study_id, study_name) values(18, '600k Ellinor');

-- 20230208 - add flag if has qualifiers indicating 2nd query 
alter table comb_edge_node add column has_qualifiers enum('N', 'Y') default 'N';

