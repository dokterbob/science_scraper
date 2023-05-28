from .common import parse_xml

client = Client("http://localhost:8080")


def create_schema():
    # Define the schema
    schema = Schema()
    document_class = (
        Schema.Class("Document")
            .add_property(
                Schema.Property("doi", "string")
                    .set_cardinality_to_single()
                    .add_property_description("The DOI of the document")
            )
            .add_property(
                Schema.Property("authors", "string")
                    .set_cardinality_to_many()
                    .add_property_description("The authors of the document")
            )
            .add_property(
                Schema.Property("institutes", "string")
                    .set_cardinality_to_many()
                    .add_property_description("The institutes of the document")
            )
            .add_property(
                Schema.Property("topics", "string")
                    .set_cardinality_to_many()
                    .add_property_description("The topics of the document")
            )
            .add_property(
                Schema.Property("journal_name", "string")
                    .set_cardinality_to_single()
                    .add_property_description("The journal name of the document")
            )
            .add_property(
                Schema.Property("pub_date", "string")
                    .set_cardinality_to_single()
                    .add_property_description("The publication date of the document")
            )
            .add_property(
                Schema.Property("embedding", "text")
                    .set_cardinality_to_single()
                    .add_property_description("The document embedding")
            )
    )

    # Create the schema in Weaviate only if it doesn't exist
    if not client.schema.contains("Document"):
        schema.add_class(document_class)
        client.schema.create(schema)
