#
# Modified for beer-sample bucket
#

#
# https://docs.couchbase.com/python-sdk/current/hello-world/start-using-sdk.html
#

# needed for any cluster connection
from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator

# needed to support SQL++ (N1QL) query
from couchbase.cluster import QueryOptions

# get a reference to our cluster
cluster = Cluster('couchbase://localhost', ClusterOptions(
  PasswordAuthenticator('admin', 'mypassword')))

# get a reference to our bucket
cb = cluster.bucket('beer-sample')

# get a reference to the default collection
cb_coll = cb.default_collection()

airline = {
  "type": "airline",
  "id": 8091,
  "callsign": "CBS",
  "iata": None,
  "icao": None,
  "name": "Couchbase Airways",
}

def upsert_document(doc):
  print("\nUpsert CAS: ")
  try:
    # key will equal: "airline_8091"
    key = doc["type"] + "_" + str(doc["id"])
    result = cb_coll.upsert(key, doc)
    print(result.cas)
  except Exception as e:
    print(e)

# upsert_document(airline)

# get document function
def get_doc_by_key(key):
  print("\nGet Result: ")
  try:
    result = cb_coll.get(key)
    print(result.content_as[str])
  except Exception as e:
    print(e)

get_doc_by_key("512_brewing_company-one")

# query for new document by callsign
def lookup_by_callsign(cs):
  print("\nLookup Result: ")
  try:
    sql_query = 'SELECT VALUE name FROM `travel-sample` WHERE type = "airline" AND callsign = $1'
    row_iter = cluster.query(
      sql_query,
      QueryOptions(positional_parameters=[cs]))
    for row in row_iter: print(row)
  except Exception as e:
    print(e)

print("Lookup by callsign")
lookup_by_callsign("CBS")
lookup_by_callsign("TXW")


