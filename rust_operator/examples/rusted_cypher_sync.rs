use rusted_cypher::{GraphClient, Statement};

fn main() {
    // Connect to the Neo4j graph database
    let graph = GraphClient::connect(
        format!("http://{username}:{passwd}@localhost:7474/db/data/", username = "neo4j", passwd = "khk123456")).unwrap();
    // Delete all nodes and relationships
    graph.exec("MATCH (n) DETACH DELETE n")?;

    // Define the Rust grammar concepts
    let concepts = vec![
        "Rust Program",
        "Module",
        "Function",
        "Struct",
        "Enum",
        "Trait",
        "Lifetime",
        "Macro",
        "Type",
    ];

    // Create the nodes
    for concept in &concepts {
        // 使用{}转义
        let statement = format!("CREATE (:Entity {{name: {}}})", *concept);
        graph.exec(statement).unwrap();
    }

    // Create the relationships
    let statements = vec![
        Statement::new("MATCH (s:Entity {name: 'Rust Program'}), (t:Entity {name: 'Module'}) CREATE (s)-[:CONTAINS]->(t)"),
        Statement::new("MATCH (s:Entity {name: 'Module'}), (t:Entity {name: 'Function'}) CREATE (s)-[:CONTAINS]->(t)"),
        Statement::new("MATCH (s:Entity {name: 'Module'}), (t:Entity {name: 'Struct'}) CREATE (s)-[:CONTAINS]->(t)"),
        Statement::new("MATCH (s:Entity {name: 'Module'}), (t:Entity {name: 'Enum'}) CREATE (s)-[:CONTAINS]->(t)"),
        Statement::new("MATCH (s:Entity {name: 'Module'}), (t:Entity {name: 'Trait'}) CREATE (s)-[:CONTAINS]->(t)"),
        Statement::new("MATCH (s:Entity {name: 'Function'}), (t:Entity {name: 'Lifetime'}) CREATE (s)-[:USES]->(t)"),
        Statement::new("MATCH (s:Entity {name: 'Function'}), (t:Entity {name: 'Macro'}) CREATE (s)-[:USES]->(t)"),
        Statement::new("MATCH (s:Entity {name: 'Struct'}), (t:Entity {name: 'Type'}) CREATE (s)-[:HAS_FIELD]->(t)"),
    ];

    for statement in statements {
        graph.exec(statement).unwrap();
    }
}
