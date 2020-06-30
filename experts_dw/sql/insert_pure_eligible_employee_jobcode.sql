-- :name insert_pure_eligible_employee_jobcode
INSERT INTO pure_eligible_employee_jobcode
(
  jobcode,
  jobcode_descr,
  pure_job_description,
  default_employed_as,
  default_staff_type,
  default_visibility,
  default_profiled,
  default_profiled_overrideable
) VALUES (
  :jobcode,
  :jobcode_descr,
  :pure_job_description,
  :default_employed_as,
  :default_staff_type,
  :default_visibility,
  :default_profiled,
  :default_profiled_overrideable
)
