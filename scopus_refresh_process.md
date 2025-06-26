# Scopus refresh process

* get scopus ids of created/modified research outputs since last refresh
  * where last refresh = max inserted or updated in authored/cited table
* merge above scopus ids into an `authored_abstracts_to_download` table
  * download table columns:
    * scopus id
    * inserted
    * updated
* download abstracts by scopus id
* for successful downloads
  * load abstracts
  * add cited scopus ids to `cited_abstracts_to_download` table
  * delete scopus ids from `authored_abstracts_to_download`
* for defunct abstracts
  * delete abstracts from both authored/cited tables
  * delete scopus ids from authored/cited `to_download` tables
* for error results
  * log errors
* repeat most of the above process for cited abstracts
