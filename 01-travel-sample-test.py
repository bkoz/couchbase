#
# https://docs.couchbase.com/python-sdk/current/hello-world/start-using-sdk.html
#

import argparse
import sys

# needed for any cluster connection
from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator

# needed to support SQL++ (N1QL) query
from couchbase.cluster import QueryOptions

def upsert_document(cb_coll, doc):
  print("\nUpsert CAS: ")
  try:
    # key will equal: "airline_8091"
    key = doc["type"] + "_" + str(doc["id"])
    result = cb_coll.upsert(key, doc)
    print(result.cas)
  except Exception as e:
    print(e)

# get document function
def get_airline_by_key(cb_coll, key):
  print("\nGet Result: ")
  try:
    result = cb_coll.get(key)
    print(result.content_as[str])
  except Exception as e:
    print(e)

# query for new document by callsign
def lookup_by_callsign(cluster, cs):
  print("\nLookup Result: ")
  try:
    sql_query = 'SELECT VALUE name FROM `travel-sample` WHERE type = "airline" AND callsign = $1'
    row_iter = cluster.query(
      sql_query,
      QueryOptions(positional_parameters=[cs]))
    for row in row_iter: print(row)
  except Exception as e:
    print(e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", default="localhost")
    parser.add_argument("-u", "--user", default="admin")
    parser.add_argument("-p", "--password", default="password")
    args = parser.parse_args()

    url = "couchbase://{0}".format(args.server)

    # get a reference to our cluster
    try:
      cluster = Cluster(url, ClusterOptions(PasswordAuthenticator(args.user, args.password)))
    except Exception as e:
      print('Exception raised. Connection to the cluster failed. {0}'.format(e))
      sys.exit()

    # get a reference to our bucket
    try:
      cb = cluster.bucket('travel-sample')
    except Exception as e:
      print('Exception raised. Bucket reference failed. {0}'.format(e))
      sys.exit()

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

    upsert_document(cb_coll, airline)

    get_airline_by_key(cb_coll, "airline_8091")
    get_airline_by_key(cb_coll, "airline_10")

    print("Lookup by callsign")
    lookup_by_callsign(cluster, "CBS")
    lookup_by_callsign(cluster, "TXW")

if __name__ == "__main__":
    main()

