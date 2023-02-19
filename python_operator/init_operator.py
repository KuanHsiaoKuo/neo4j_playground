import csv

from py2neo import Graph, Node, Relationship
from py2neo.bulk import create_nodes, create_relationships

# graph = Graph('http://localhost:7474/', username='neo4j', password='khk123456')
graph = Graph("bolt://localhost:7687", auth=("neo4j", "khk123456"))


def manual_import():
    # Create entities for Rust grammar concepts
    rust_program = Node("Entity", name="Rust Program")
    module = Node("Entity", name="Module")
    function = Node("Entity", name="Function")
    struct = Node("Entity", name="Struct")
    enum = Node("Entity", name="Enum")
    trait = Node("Entity", name="Trait")
    lifetime = Node("Entity", name="Lifetime")
    macro = Node("Entity", name="Macro")
    type = Node("Entity", name="Type")

    # Create relationships between Rust grammar concepts
    contains = Relationship.type("CONTAINS")
    uses = Relationship.type("USES")
    has_field = Relationship.type("HAS_FIELD")

    rust_program_contains_module = contains(rust_program, module)
    module_contains_function = contains(module, function)
    module_contains_struct = contains(module, struct)
    module_contains_enum = contains(module, enum)
    module_contains_trait = contains(module, trait)
    function_uses_lifetime = uses(function, lifetime)
    function_uses_macro = uses(function, macro)
    struct_has_field_type = has_field(struct, type)

    # Add nodes and relationships to the graph
    tx = graph.begin()
    tx.create(rust_program)
    tx.create(module)
    tx.create(function)
    tx.create(struct)
    tx.create(enum)
    tx.create(trait)
    tx.create(lifetime)
    tx.create(macro)
    tx.create(type)
    tx.create(rust_program_contains_module)
    tx.create(module_contains_function)
    tx.create(module_contains_struct)
    tx.create(module_contains_enum)
    tx.create(module_contains_trait)
    tx.create(function_uses_lifetime)
    tx.create(function_uses_macro)
    tx.create(struct_has_field_type)
    tx.commit()


def bulk_import():
    # 节点类别
    node_label = "Syntax Entity"
    # 关系名称
    relationship_type_key = "relationship_type"

    # Create the nodes and relationships in bulk
    with open("nodes.csv", 'r') as nodes_file, open("relationships.csv", 'r') as relationships_file:
        nodes_data, relationships_data = list(csv.reader(nodes_file)), list(csv.reader(relationships_file))
        # Create the nodes
        nodes = list(create_nodes(graph, nodes_data[1:], labels={node_label}, keys=nodes_data[0]))

        # Create the relationships
        relationships = list(
            create_relationships(
                graph,
                relationships_data[1:],
                start_node_key=(node_label, "name"),
                end_node_key=(node_label, "name")
            )
        )

    # Print the number of nodes and relationships created
    print(f"{len(nodes)} nodes and {len(relationships)} relationships created.")


def sync_csv_graph(nodes_path, relationships_path):
    rel_types = {}
    nodes = {}
    process = graph.begin()
    with open(nodes_path, 'r') as nodes_file, open(relationships_path, 'r') as relationships_file:
        nodes_data, relationships_data = list(csv.reader(nodes_file)), list(csv.reader(relationships_file))
        nodes_keys = nodes_data[0]
        for node_name, node_type in nodes_data[1:]:
            node = Node(node_type, name=node_name)
            process.create(node)
            nodes[node_name] = node
        for start_node, end_node, rel_type in relationships_data[1:]:
            if rel_type not in rel_types.keys():
                rel_types[rel_type] = Relationship.type(rel_type)
            rel = rel_types[rel_type](nodes[start_node], nodes[end_node])
            process.create(rel)
    graph.commit(process)


if __name__ == "__main__":
    graph.delete_all()
    sync_csv_graph('nodes.csv', 'relationships.csv')
