-- :name count_pure_eligible_persons_in_dept :scalar
select count(distinct emplid) from (
  select emplid from pure_eligible_employee_job where deptid = :deptid
  union
  select emplid from pure_eligible_affiliate_job where deptid = :deptid
)
