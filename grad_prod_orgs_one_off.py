import dotenv_switch.auto

from requests import Request, Session

from experts_dw import db

with db.cx_oracle_connection() as session:
    cur = session.cursor()
    cur.execute(
       "SELECT DISTINCT p.um_acad_plan_prima, p.acad_plan_sdesc, \
        p.acad_plan_ldesc, p.deptid, u.pure_org_uuid \
        FROM ps_dwsa_stix_1223_pr@dweprd.oit p \
            JOIN umn_dept_pure_org u \
            ON p.deptid = u.deptid \
        WHERE level2 = 'GRAD' OR level2 = 'PRFL'"
    )
    cur.rowfactory = lambda *args: dict(
        zip([col[0] for col in cur.description], args)
    )

    with Session() as s:
        rows = cur.fetchall()
        for row in rows:
            org = {
                  "name": {
                  "en_US": row["ACAD_PLAN_LDESC"]
                },
                "type": {
                    "uri": "/dk/atira/pure/organisation/organisationtypes/organisation/academic_plan",
                    "term": {
                        "en_US": "Academic Plan"
                    }
                },
                "identifiers": [
                    {
                        "typeDiscriminator": "PrimaryId",
                        "idSource": "synchronisedUnifiedOrganisation",
                        "value": row["UM_ACAD_PLAN_PRIMA"]
                    },
                    {
                        "typeDiscriminator": "ClassifiedId",
                        "id": row["UM_ACAD_PLAN_PRIMA"],
                        "type": {
                            "uri": "/dk/atira/pure/organisation/organisationsources/academic_plan_id",
                            "term": {
                                "en_US": "Academic Plan ID"
                            }
                        }
                    }],
                "nameVariants": [{
                    "value": {
                        "en_US": row["ACAD_PLAN_SDESC"]
                    },
                    "type": {
                        "uri": "/dk/atira/pure/organisation/namevariants/shortname",
                        "term": {
                            "en_US": "Short name"
                        }
                    }
                }],
                "lifecycle": {
                    "startDate": "1970-01-01"
                },
                "parents": [{
                    "uuid": row["PURE_ORG_UUID"],
                    "systemName": "Organization"
                }],
                "visibility": {
                    "key": "BACKEND",
                    "description": {
                        "en_US": "Backend - Restricted to Pure users"
                    }
                }
            }
            req = Request(
                'PUT',
                'https://minnesota-staging.pure.elsevier.com/ws/api/organizations',
                json=org,
            )
            prepped = req.prepare()
            prepped.headers['api-key'] = 'a4fb1bc8-94fd-42a3-918f-e7348a666918'
            resp = s.send(prepped)

            if resp.status_code != "200":
                print(resp.status_code)
                print(resp.text)
                print(org)
