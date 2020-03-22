## gcloud commands

* Start
    * gcloud init

* Deploy the app
    * `gcloud app deploy`

* Create new indexes:
    * gcloud datastore indexes create index.yaml

* Clean indexes and keep the ones defined:
    * gcloud datastore indexes cleanup index.yaml

## Restful API design
* https://stoplight.io/blog/crud-api-design/
* https://opensource.zalando.com/restful-api-guidelines/index.html#introduction
* https://github.com/whitehouse/api-standards
* https://geemus.gitbooks.io/http-api-design/content/en/
* https://martinfowler.com/bliki/TolerantReader.html
* https://flask-oauthlib.readthedocs.io/en/latest/oauth2.html
* https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful
* https://flask-restplus.readthedocs.io/en/stable/swagger.html#documenting-with-the-api-doc-decorator

### Flask-Restplus

* https://flask-restplus.readthedocs.io/en/stable/example.html

## Cloud

* https://cloud.google.com/appengine/docs/standard/python/getting-started/storing-data-datastore
* https://cloud.google.com/datastore/docs/concepts/multitenancy
* https://cloud.google.com/appengine/docs/standard/python3/building-app/personalizing-data-for-authenticated-users?hl=es
* https://cloud.google.com/datastore/docs/concepts/queries
* https://stackoverflow.com/questions/47420936/google-datastore-filter-with-or-condition
* https://cloud.google.com/datastore/docs/concepts/indexes#index_configuration
* https://cloud.google.com/appengine/docs/standard/python/datastore/query-restrictions
* https://cloud.google.com/datastore/docs/concepts/entities

## Google Maps Javascript API

* https://developers.google.com/maps/documentation/javascript/shapes#draggable

## MGRS how to store locations to ease the fetch

* https://en.wikipedia.org/wiki/Discrete_global_grid#Geocodind_variants
* https://en.wikipedia.org/wiki/Military_Grid_Reference_System
* https://legallandconverter.com/cgi-bin/shopmgrs201807.cgi
* https://upload.wikimedia.org/wikipedia/commons/b/b7/Universal_Transverse_Mercator_zones.svg

## Send Mail

* https://stackoverflow.com/questions/52082368/sending-emails-on-gae-through-smtp-gmail-com-in-python
* https://developers.google.com/gmail/api/quickstart/python
* https://developers.google.com/gmail/api/v1/reference/?apix=true

## Trying SQL databases

* https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/cloud-sql/mysql/sqlalchemy
* https://cloud.google.com/sql/docs/mysql/sql-proxy#install
* https://cloud.google.com/sql/docs/mysql/create-instance
* https://cloud.google.com/sql/docs/mysql/create-manage-databases

### Some SQL commands

Create bbdd:
gcloud sql databases create [DATABASE_NAME] --instance=[INSTANCE_NAME]

List databases:
gcloud sql databases list --instance=[INSTANCE_NAME]

Delete bbdd:
gcloud sql databases delete [DATABASE_NAME] --instance=[INSTANCE_NAME]

#### CUP Barcelona map example
* https://www.google.com/maps/d/u/0/viewer?mid=1cQsdTpZCEwNy3f5bS51bJsuwChhq5_wS&ll=41.415678409641835%2C2.2131689467335036&z=21



