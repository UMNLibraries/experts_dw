drop table all_jobs_previous;
create table all_jobs_previous as (
  select * from all_jobs_current
);
