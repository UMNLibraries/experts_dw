import dotenv_switch.auto

# Execution example: APP_ENV=prd python ./reload_missing_pubs.py {emplid} > output.txt

import csv
from datetime import datetime
from dateutil.parser import isoparse
import json
import sys

from sqlalchemy import and_

from pureapi import client
from experts_dw import db
from experts_dw.models import Person, PureApiExternalOrg, PureApiExternalPerson, PureApiPub, Pub
from pureapi import client

emplid = sys.argv[1]

supported_pure_types = {
    'contributiontojournal': [
        'article', # Article: A presentation of new research with other scientists as primary audience.
        'letter', # Letter: A short description of new, important research results.
        'comment', # Comment/debate: Short commentary/contribution to debate in a scientific publication, often about former printed articles.
        'book', # Book/Film/Article review: Review of a book/film/article, published in a journal.
        'scientific', # Literature review: A critical review and evaluation of a (scientific) publication
        'editorial', # Editorial: An article-like text with the official opinion about a subject, from a journal's point of view.
        'special', # Special issue: A specific journal issue with focus on a special theme or subject.
        'abstract', # Meeting Abstract
        'systematicreview', # Review article: An article that review previous research on a topic and provides a summarization of the current understanding of the topic.
        'shortsurvey', # Short survey: A short survey is a mini-review of previous research on a topic, including a summarization of the current understanding of the topic. It is generally shorter than systematic review articles and contains a less extensive bibliography.
        'conferencearticle', # Conference article: An article that has been presented at a conference and published in a journal
  ],
}

# This code was originally used to handle cases of duplicate persons. Keeping the
# following in case it may be useful later.
#with open(filename) as csvfile:
#    reader = csv.DictReader(csvfile)
#    for row in reader:
#        pure_uuid = row['pure_uuid']
#        emplid = row['emplid']
#        created_by = row['created_by']
#
#        if emplid not in emplids:
#            emplids[emplid] = {}
#        if created_by == 'sync_user':
#            emplids[emplid]['duplicate_pure_uuid'] = pure_uuid
#            emplids[emplid]['duplicate_name'] = row['name']
#            emplids[emplid]['duplicate_internet_id'] = row['internet_id']
#            emplids[emplid]['duplicate_created_date'] = row['created_date']
#            emplids[emplid]['duplicate_created_by'] = created_by
#        else:
#            emplids[emplid]['original_pure_uuid'] = pure_uuid
#            emplids[emplid]['original_name'] = row['name']
#            emplids[emplid]['original_internet_id'] = row['internet_id']
#            emplids[emplid]['original_created_date'] = row['created_date']
#            emplids[emplid]['original_created_by'] = created_by

def load_external_orgs(session, uuids):
   for external_org in client.filter_all_by_uuid_transformed('external-organisations', uuids=uuids):
        uuid = external_org.uuid
        modified = isoparse(external_org.info.modifiedDate)

        pure_api_external_org = (
            session.query(PureApiExternalOrg)
            .filter(and_(
                PureApiExternalOrg.uuid == uuid,
                PureApiExternalOrg.modified == modified,
            ))
            .one_or_none()
        )
        if pure_api_external_org is None:
            print(f'  missing external org with uuid {uuid}')
            pure_api_external_org = PureApiExternalOrg(
                uuid=uuid,
                modified=modified,
                downloaded=datetime.now(),
                json=json.dumps(external_org),
            )
            session.add(pure_api_external_org)

def load_external_persons(session, uuids):
    external_org_uuids = set()
    for external_person in client.filter_all_by_uuid_transformed('external-persons', uuids=uuids):
        uuid = external_person.uuid
        modified = isoparse(external_person.info.modifiedDate)

        for org in external_person.externalOrganisations:
            external_org_uuids.add(org['uuid'])

        pure_api_external_person = (
            session.query(PureApiExternalPerson)
            .filter(and_(
                PureApiExternalPerson.uuid == uuid,
                PureApiExternalPerson.modified == modified,
            ))
            .one_or_none()
        )
        if pure_api_external_person is None:
            print(f'  missing external person with uuid {uuid}')
            pure_api_external_person = PureApiExternalPerson(
                uuid=uuid,
                modified=modified,
                downloaded=datetime.now(),
                json=json.dumps(external_person),
            )
            session.add(pure_api_external_person)

    return external_org_uuids

with db.session('hotel') as session:
    person = (
        session.query(Person)
        .filter(
            Person.emplid == emplid,
        )
        .one_or_none()
    )
    print(f'{person.first_name} {person.last_name} - {person.pure_uuid}:')

    payload = {
        "forPersons": {
            "uuids": [
                #record['uuid']
                person.pure_uuid
            ]
        }
    }
    for pub in client.filter_all_transformed('research-outputs', payload):
        uuid = pub.uuid
        print(f'{uuid}: {pub.title.value}')

        type_uri_parts = pub.type.uri.split('/')
        type_uri_parts.reverse()
        pure_subtype, pure_type, pure_parent_type = type_uri_parts[0:3]

        if pure_type not in supported_pure_types or pure_subtype not in supported_pure_types[pure_type]:
            print(f'  has an unsupported pure type ({pure_type}) or subtype ({pure_subtype}). Skipping.')
            continue

        modified = isoparse(pub.info.modifiedDate)

        external_org_uuids = set()
        external_person_uuids = set()
        for person_assoc in pub.personAssociations:
            if 'authorCollaboration' in person_assoc:
                #print(f'authorCollaboration: {person_assoc.authorCollaboration.uuid}')
                continue
            if 'externalPerson' in person_assoc:
                #print(f'externalPerson: {person_assoc.externalPerson.uuid}')
                #external_person_uuids.append(person_assoc.externalPerson.uuid)
                external_person_uuids.add(person_assoc.externalPerson.uuid)
                for external_org in person_assoc.externalOrganisations:
                    #print(f'externalOrganisation: {external_org.uuid}')
                    #external_org_uuids.append(external_org.uuid)
                    external_org_uuids.add(external_org.uuid)
            if 'person' in person_assoc:
                #print(f'person: {person_assoc.person.uuid}')
                continue

        #print('external persons:', list(external_person_uuids))
        external_org_uuids.update(
            load_external_persons(session, list(external_person_uuids))
        )
        #print('external orgs:', list(external_org_uuids))
        load_external_orgs(session, list(external_org_uuids))

        db_pub = (
            session.query(Pub)
            .filter(and_(
                Pub.pure_uuid == uuid,
                Pub.pure_modified == modified,
            ))
            .one_or_none()
        )
        if db_pub:
            print('  in Experts DW. Skipping.')
            continue
        else:
            print('  not in Experts DW pub.')

        pure_api_pub = (
            session.query(PureApiPub)
            .filter(and_(
                PureApiPub.uuid == uuid,
                PureApiPub.modified == modified,
            ))
            .one_or_none()
        )
        if pure_api_pub is None:
            print('  not in Experts DW pure_api_pub. Loading.')
            pure_api_pub = PureApiPub(
                uuid=uuid,
                modified=modified,
                downloaded=datetime.now(),
                json=json.dumps(pub),
            )
            session.add(pure_api_pub)
        else:
            print('  in Experts DW pure_api_pub. Skipping.')

        session.commit()
