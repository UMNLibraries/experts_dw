-- :name record_reporting_of_umn_data_errors :affected
update umn_data_error set reported = sysdate where reported is null

