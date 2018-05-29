-- We now have access to PSSNAP tables, as of 2018-05-04!
-- But ask about the "department tree" or whatever it was Chris Dinger called it, too.
describe table hr_ps_job@dweprd.oit;
describe table hr_ps_position_data@dweprd.oit;

-- Do I need to commit these?
grant select on person to oit_expert_rd_all;
grant select on umn_dept_pure_org to oit_expert_rd_all;
grant select on umn_person_pure_org to oit_expert_rd_all;
grant select on pure_org to oit_expert_rd_all;
grant select on pure_internal_org to oit_expert_rd_all;
grant select on pub to oit_expert_rd_all;
grant select on pub_person to oit_expert_rd_all;
grant select on pub_person_pure_org to oit_expert_rd_all;

select * from pure_internal_org where lft >= 505 and rgt <= 520;
select * from pure_internal_org where "level" > 3;
select count(*) from pure_org;
select * from pure_internal_org where pure_id = 'LKTQDNVXHPZC';
select * from pure_internal_org where pure_id = 'MNDRIVE';
select * from pure_org where pure_id in ('ZNVNNMA','NNIWQIQRQ');
select * from pure_internal_org where pure_id in ('ZNVNNMA','NNIWQIQRQ');
select * from pure_org where name_en = 'Minnesota Agriculture Experiment Station';
select * from pure_internal_org where pure_uuid = 'a6bfaa1e-53d6-49ae-952b-62b78aef7c70';
select * from pure_org where pure_id is null;
select * from pure_org po left outer join pure_internal_org pio on po.pure_uuid = pio.pure_uuid;
select pure_uuid, count(*) from pure_internal_org group by pure_uuid having count(*) > 1;
select * from pure_internal_org where pure_uuid is null;
