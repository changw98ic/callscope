"""Adapt Axon's bundled graph core to CallScope's certain-call index.

The upstream KnowledgeGraph owns the node-label, relationship-type and
adjacency indexes. CallScope keeps its own source identities and resolution
policy; Axon's graph does not resolve calls or assign confidence here.

These runtime graph objects are never attached to serializable snapshots.
"""

from collections.abc import Mapping

from ._vendor.axon.graph import KnowledgeGraph
from ._vendor.axon.model import GraphNode, GraphRelationship, NodeLabel, RelType
from .models import Edge, Node


_LABEL_BY_KIND = {label.value: label for label in NodeLabel}
_LABEL_BY_KIND.update({
    # Axon has no generic module/trait/closure labels. This grouping is only
    # for index lookup; the original CallScope kind remains in properties.
    "module": NodeLabel.FILE,
    "trait": NodeLabel.INTERFACE,
    "type": NodeLabel.TYPE_ALIAS,
    "closure": NodeLabel.FUNCTION,
    "lambda": NodeLabel.FUNCTION,
    "constructor": NodeLabel.METHOD,
})


class AxonCallGraph:
    """Build the definite graph and return the existing sorted Edge API.

GraphIndex decides which calls are certain. This adapter additionally guards
against absent or duplicate-definition endpoints before indexing a call.
Unresolved candidates and callback boundaries never enter this graph.
"""

    def __init__(self, nodes: Mapping[str, Node]) -> None:
        self.graph = KnowledgeGraph()
        self._node_order = tuple(nodes)
        self._relationship_ids: set[str] = set()
        self._ambiguous_nodes = {
            node.id for node in nodes.values()
            if node.metadata.get("duplicate_definition")
        }
        for node in nodes.values():
            self.graph.add_node(GraphNode(
                id=node.id,
                label=_LABEL_BY_KIND.get(node.kind, NodeLabel.FILE),
                name=node.name,
                file_path=node.file,
                start_line=node.line,
                end_line=node.end_line,
                signature=node.signature,
                language=node.metadata.get("language", ""),
                properties={
                    "callscope_kind": node.kind,
                    "qualname": node.qualname,
                    "module": node.module,
                },
            ))

    def add_call(self, edge: Edge) -> None:
        if edge.resolution != "resolved" or edge.target is None:
            raise ValueError("AxonCallGraph accepts only resolved internal calls.")
        if self.graph.get_node(edge.source) is None or self.graph.get_node(edge.target) is None:
            raise ValueError("A certain call must have both local endpoints.")
        if edge.source in self._ambiguous_nodes or edge.target in self._ambiguous_nodes:
            raise ValueError("Duplicate definitions cannot enter certain-call adjacency.")

        # KnowledgeGraph replaces relationships sharing an ID. Preserve the
        # old GraphIndex's multiedge behavior even for malformed duplicate IDs:
        # only the private backend key changes, never the source Edge identity.
        relationship_id = edge.id
        occurrence = 0
        while relationship_id in self._relationship_ids:
            occurrence += 1
            relationship_id = f"{edge.id}:callscope_occurrence:{occurrence}"
        self.graph.add_relationship(GraphRelationship(
            id=relationship_id,
            type=RelType.CALLS,
            source=edge.source,
            target=edge.target,
            properties={"callscope_edge": edge},
        ))
        self._relationship_ids.add(relationship_id)

    def adjacency(self) -> tuple[dict[str, list[Edge]], dict[str, list[Edge]]]:
        """Materialize compatibility lists from Axon's actual indexed graph.

Label and relationship-type indexes supply the indexed entities; Axon's
directed adjacency determines membership. Returned lists contain original
Edge instances and retain CallScope's deterministic neighbor ordering.
"""
        nodes = {
            node.id: node
            for label in NodeLabel
            for node in self.graph.get_nodes_by_label(label)
        }
        calls: dict[str, Edge] = {
            relationship.id: relationship.properties["callscope_edge"]
            for relationship in self.graph.get_relationships_by_type(RelType.CALLS)
        }
        outgoing: dict[str, list[Edge]] = {}
        incoming: dict[str, list[Edge]] = {}
        for node_id in self._node_order:
            # Read the label index while preserving the original key order.
            indexed_id = nodes[node_id].id
            outgoing[node_id] = sorted(
                (calls[relationship.id] for relationship in self.graph.get_outgoing(indexed_id, RelType.CALLS)),
                key=lambda edge: (edge.target or "", edge.id),
            )
            incoming[node_id] = sorted(
                (calls[relationship.id] for relationship in self.graph.get_incoming(indexed_id, RelType.CALLS)),
                key=lambda edge: (edge.source, edge.id),
            )
        return outgoing, incoming
