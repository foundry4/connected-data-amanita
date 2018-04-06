from app.querybuilder.sparql.subqueries import build_regular_fields_pattern_statement, \
    build_tags_pattern_statement, build_genres_pattern_statement, build_tags_select_statement, \
    build_genres_select_statement


def build_query(item_uri):
    """
    Get info for a single item from the content graph.

    Arguments:
        item_uri (rdflib.URIRef)

    Returns:
        query_string (string): SPARQL query
    """
    regular_fields = '?title ?image ?version ?pid ?media ?duration ?publicationDate ?masterBrand'
    query_string = f"""
        SELECT
            {regular_fields}
            {build_tags_select_statement()}
            {build_genres_select_statement()}

        WHERE {{
            {build_regular_fields_pattern_statement(item_uri.n3())}
            {build_tags_pattern_statement(item_uri.n3())}
            {build_genres_pattern_statement(item_uri.n3())}
        }}
        GROUP BY {regular_fields}
    """

    return query_string
