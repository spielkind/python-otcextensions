CCE API
=======

.. automodule:: otcextensions.sdk.cce.v1._proxy

The Cloud Container Engine Class
--------------------------------

The cce high-level interface is available through the ``cce`` member of a
:class:`~openstack.connection.Connection` object.  The ``cce`` member will only
be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is
called.

Cluster Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.cce.v1._proxy.Proxy
  :noindex:
  :members: clusters, get_cluster, find_cluster, delete_cluster

Cluster Nodes Operations
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.cce.v1._proxy.Proxy
  :noindex:
  :members: cluster_nodes, get_cluster_node, find_cluster_node,
             delete_cluster_nodes, add_node
