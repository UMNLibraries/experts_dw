# Pure raw JSON flow

## Goals

* readability
* performance
* diagnostics

## Ideas

* number of defunct uuids should always be small for each set of changes
* cache results of various defunct uuid queries in a defunct uuid table
* if anything fails, leave unprocessed records alone and process them next time
* maybe use railway oriented programming? maybe with python "returns" package?

## Flow

* get change create and update uuids for collection (query function done)
* download records with matching uuids from pure to staging
  * async!
* get uuids of any missing records
* if missing records
  * request each individually from pure api and check for 404
  * store uuids of any 404s in a missing uuids list
  * add records of any 200s to list of downloaded records
  * log errors for any other HTTP status responses
  * (should be few of these, so performance penalty should be low)
* get previous uuids from staging records
  * store uuids in a previous uuids list
* get change delete uuids for collection
  * store uuids in a deleted uuids list
* if missing uuids or change delete uuids or previous uuids exist
  * combine all uuids into a single defunct uuids list
  * start transaction
    * add uuids to defunct uuids for collection (does this really need to be in a transaction?)
    * delete records with matching uuids from collection canonical
    * add changes with matching uuids to change history (does this really need to be in a transaction?)
    * delete changes with matching uuids
      * assumptions:
        * if we have any delete change record for a uuid, we can ignore all other change records for that uuid
        * uuids will never be re-used for new records (?)
  * if failure
    * log error and affected uuids
    * rollback
* if previous uuids exist
  * start transaction
    * delete records with matching uuids from staging
  * if failure
    * log error (and affected uuids?)
    * rollback
* merge staging records into canonical
  * start transaction
    * merge
  * if failure
    * log error (and affected uuids?)
    * rollback
  * else
    * truncate staging?
    
