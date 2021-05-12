# Read-only role management

How to manage members and access for the `oit_expert_rd_all` role, which
provides read-only access to Experts Data Warehouse. Adapted from
[OIT Data Dictionary and Functions](https://sites.google.com/a/umn.edu/dbcentral/home/oracle/oit-data-dictionary-and-functions).

## List members

Only OIT DBAs can add and remove role members, but we can list members:

```sql
SELECT grantee FROM oit_role_privs
WHERE granted_role = 'OIT_EXPERT_RD_ALL';
```

## List objects

To list the objects to which the role has acess:

```sql
SELECT * FROM oit_tab_privs
WHERE grantee = 'OIT_EXPERT_RD_ALL';
```

## Add objects

```sql
GRANT SELECT ON {object_name} TO oit_expert_rd_all;
```

## Remove objects

```sql
REVOKE SELECT ON {object_name} FROM oit_expert_rd_all;
```
