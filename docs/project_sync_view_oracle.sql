-- Source: https://static.helpjuice.com/helpjuice_production/uploads/upload/image/15881/direct/1748433703411/project_sync_view_oracle.sql

CREATE TABLE PROJECT_DATA
(
	PROJECT_ID varchar(1024) not null,
	PROJECT_TYPE varchar(1024) not null,
	TITLE varchar(1024) not null,
	SHORT_TITLE varchar(256),
	ACRONYM varchar(64),
	START_DATE date,
	END_DATE date,
	CURTAIL_DATE date,
	CURTAIL_REASON CLOB,
	COLLABORATIVE_PROJECT number(1,0) not null,
	MANAGED_BY_ORG_ID varchar(1024) not null,
	VISIBILITY varchar(1024),
	MANAGED_IN_PURE number(1,0)
)
;
CREATE TABLE INTERNAL_PARTICIPANTS
(
	PROJECT_ID varchar(1024) not null,
	PERSON_ID varchar(1024) not null,
	ORGANISATION_ID varchar(1024) not null,
	ROLE varchar(1024) not null,
	ACADEMIC_OWNERSHIP_PERCENTAGE number,
	PLANNED_RESEARCHER_COMMITMENT number,
	ASSOCIATION_PERIOD_START_DATE date,
	ASSOCIATION_PERIOD_END_DATE date
)
;
CREATE TABLE EXTERNAL_PARTICIPANTS
(
	PROJECT_ID varchar(1024) not null,
	FIRSTNAME varchar(1024) not null,
	LASTNAME varchar(1024) not null,
	COUNTRY varchar(1024),
	ROLE varchar(1024) not null,
	EXTERNAL_ORG_NAME varchar(1024),
	EXTERNAL_ORG_TYPE varchar(1024),
	EXTERNAL_ORG_ID varchar(1024)
)
;
CREATE TABLE INT_PROJECT_CO_MANAGING_ORG
(
    PROJECT_ID varchar(1024) not null,
    ORGANISATION_ID varchar(1024) not null
)
;
CREATE TABLE INTERNAL_PROJECT_ORGANISATIONS
(
	PROJECT_ID varchar(1024) not null,
	ORGANISATION_ID varchar(1024) not null
)
;
CREATE TABLE EXTERNAL_PROJECT_ORGANISATIONS
(
	PROJECT_ID varchar(1024) not null,
	EXTERNAL_ORG_NAME varchar(1024),
	EXTERNAL_ORG_TYPE varchar(1024),
	EXTERNAL_ORG_ID varchar(1024)
)
;
CREATE TABLE EXTERNAL_PROJECT_COLLABORATORS
(
	PROJECT_ID varchar(1024) not null,
	EXTERNAL_ORG_NAME varchar(1024),
	EXTERNAL_ORG_TYPE varchar(1024),
	EXTERNAL_ORG_ID varchar(1024),
	LEAD_COLLABORATOR number(1,0),
	COLLABORATOR_TYPE varchar(1024),
    	ORGANISATION_ID varchar(1024)
)
;
CREATE TABLE INT_PARTICIPANTS_COMMITMENT
(
	PROJECT_ID varchar(1024) not null,
	PERSON_ID varchar(1024) not null,
	YEAR integer not null,
	MONTH integer not null,
	PLANNED_COMMITMENT_PERCENTAGE number,
	ACTUAL_COMMITMENT_PERCENTAGE number
)
;
CREATE TABLE PROJECT_PROJECT_RELATION
(
	PROJECT_ID varchar(1024) not null,
	TARGET_PROJECT_ID varchar(1024) not null,
	RELATION_TYPE varchar(1024) not null
)
;
CREATE TABLE PROJECT_AWARD_RELATION
(
	PROJECT_ID varchar(1024) not null,
	AWARD_ID varchar(1024) not null
)
;
CREATE TABLE PROJECT_APPLICATION_RELATION
(
	PROJECT_ID varchar(1024) not null,
	APPLICATION_ID varchar(1024) not null
)
;

CREATE TABLE PROJECT_DATASET_RELATION
(
	PROJECT_ID varchar(1024) not null,
	DATASET_ID varchar(1024) not null
)
;

CREATE TABLE PROJECT_PRIZE_RELATION
(
	PROJECT_ID varchar(1024) not null,
	PRIZE_ID varchar(1024) not null
)
;

CREATE TABLE PROJECT_ACTIVITY_TYPE
(
	PROJECT_ID varchar(1024) not null,
	ACTIVITY_TYPE varchar(1024) not null
)
;
CREATE TABLE PROJECT_DESCRIPTIONS
(
	PROJECT_ID varchar(1024) not null,
	DESCRIPTION_TYPE varchar(1024) not null,
	DESCRIPTION_TEXT clob not null
)
;
CREATE TABLE PROJECT_IDS
(
	PROJECT_ID varchar(1024) not null,
	ID_SOURCE varchar(1024) not null,
	ID varchar(64) not null
)
;

CREATE TABLE RESEARCHOUTPUT_RELATION
(
	PROJECT_ID varchar(1024) not null,
	RESEARCHOUTPUT_ID varchar(1024) not null
)
;
CREATE TABLE PROJECT_KEYWORDS
(
	PROJECT_ID varchar(1024) not null,
	LOGICAL_NAME varchar(1024) not null,
	TYPE varchar(255),
	FREE_KEYWORD varchar(1024)
)
;
CREATE TABLE PROJECT_LINKS
(
	PROJECT_ID varchar(1024) not null,
	LINK_ID varchar(1024) not null,
	LINK_URL varchar(1024),
	LINK_TYPE varchar(255),
	LINK_DESCRIPTION varchar(1024)
)
;
CREATE TABLE ACTIVITY_RELATION
(
	PROJECT_ID varchar(1024) not null,
	ACTIVITY_ID varchar(1024) not null
)
;
