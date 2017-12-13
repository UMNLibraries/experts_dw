# One-off to populate the Pure Organisations Tree table, assumed to be empty.

import db
session = db.session('hotel')
# Added these next two lines to avoid insertions of nulls into non-nullable columns:
session.autocommit = False
session.autoflush = False

from models import PureOrg

from sqlalchemy_mptt import tree_manager
# The mptt docs recommend including this, but I get insertions of
# nulls into non-nullable columns:
#tree_manager.register_events(remove=True)

import csv
import sys
filename = sys.argv[1]
nodes = {}
pure_root_id = ''

# There's certainly a better way to generate these node_id's, probably
# with a generator. According to the mptt docs, I don't *think* I should have
# to generate them at all, but maybe I do:
node_id = 1

with open(filename) as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    pure_parent_id = row[0]
    pure_child_id = row[1]

    if (pure_root_id == ''):
      pure_root_id = pure_parent_id
      nodes[pure_root_id] = node_id
      root_org = PureOrg(pure_id=pure_root_id, id=node_id)
      session.add(root_org)
      node_id = node_id + 1
      # One or both of these lines cause(s) an insertion of a null into a non-nullable column:
      #session.flush()
      #session.commit()

    #print(root_org)

#    This didn't work: No objects found in the current session.
#    pure_parent_org = (
#      session.query(PureOrg)
#      .filter(PureOrg.pure_id == pure_parent_id)
#      .one()
#    )

    parent_id = nodes[pure_parent_id]
    nodes[pure_child_id] = node_id
    child_org = PureOrg(pure_id=pure_child_id, parent_id=parent_id, id=node_id)
    session.add(child_org)
    node_id = node_id + 1
    # One or both of these lines cause(s) an insertion of a null into a non-nullable column:
    #session.flush()
    #session.commit()

session.commit()

# Commented this (and the following line) out due to commenting out the similar line above:
#tree_manager.register_events()
#PureOrg.rebuild_tree(session, PureOrg.tree_id)
