# Person-Org Map Notes

## Record Uniqueness

To ensure unique records, so far it seems we need to include all these fields in the PK:

* emplid/person_uuid/pure_person_id
* pure_org_id
* job_description
* start_date
* end_date

Example that violated uniqueness because end_date was not included in the PK:

```csv
"ID","PersonID","OrganisationID","JobDescription","EmployedAs","StaffType","FTE","StartDate","EndDate","DirectPhoneNr","MobilePhoneNr","FaxNr","Email","WebsiteURL","Primary","DWHR_Status"
12129,5002047,"LGKNDITA","Adjunct Professor","Academic","nonacademic",,2013-05-15,2016-08-30,,,,,,"Yes","Remove"
13596,5002047,"LGKNDITA","Adjunct Professor","Academic","nonacademic",,2013-05-15,,,,,,,"Yes","Add"
```

Had to modify the PK manually, without alembic at all, because it seems I'm missing an alembic version file. PK constraint name: SYS_C00284282 

**Update:** But if I add end_date to the PK, then it can't be nullable, which forces me to add bogus end_date's. Decided to just remove rows like the above that are identical, except for end_date's, and take end_date back out of the PK. 
