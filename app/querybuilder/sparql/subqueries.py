"""Building blocks for SPARQL queries."""
from app.utils import constants


def serialize_sparql_bindings(bindings):
    """Build a SPARQL VALUES string to bind each KV pair in bindings to the query"""
    bindings_statements = []
    for binding_name, binding_value in bindings.items():
        bindings_statements.append(f"VALUES (?{binding_name}) {{ ({binding_value.n3()}) }} .\n")
    return ' '.join(bindings_statements)


def build_sparql_anding_statement(object_list, predicate_str, object_binding='programme'):
    """Build a SPARQL query fragment that matches all objects in object_list"""
    if not object_list:
        return ''
    comma_separated_sparql_tags = ', '.join([uri.n3() for uri in object_list])
    tag_filter_statement = f"?{object_binding} {predicate_str} {comma_separated_sparql_tags} .\n"
    return tag_filter_statement


def build_values_oring_statement(binding, object_list):
    """Build a SPARQL VALUES string to bind everything in object_list by logical OR."""
    if not object_list:
        return ''
    object_bindings = ' '.join([f"({sparql_binding.n3()})" for sparql_binding in object_list])
    return f"VALUES (?{binding}) {{ {object_bindings} }} .\n"


def build_sort_statement(sort_fields):
    """
    Build terms that follow a SPARQL `ORDER BY` statement, assume sort_string is valid.

    Example output:
        'ORDER BY ASC (?duration)'
    """
    stmt = ''
    if sort_fields:
        for field in sort_fields:
            if field[0] == '-':
                order = 'DESC'
                field = field[1:]
            else:
                order = 'ASC'
                field = field
            stmt += f' {order}(?{field})'
    return stmt


def build_filter_statement(binding, filter_operation, object_literal):
    """
    Build a SPARQL FILTER statement.

    Example output:
        'FILTER ?duration < PT2H'
    """
    if object_literal is None:
        return ''
    stmt = f"FILTER (?{binding} {filter_operation} {object_literal.n3()}) .\n"
    return stmt


def build_similar_to_pattern_statement(subject, prog_uri, method):
    """
    Build SPARQL pattern statement that finds items with common tags, genres or masterBrands and rank by number of
    matches.

    Arguments:
        subject (str): RDF subject given to similar items found, must be prefixed with a `?`.
        prog_uri (rdflib.URIRef: uri of programme to find related entities
        method (str): how similarity is defined
            'genre' - by number of common genres
            'tag' - by number of common tags
            'masterbrand' - by common master brand
    """
    if method == 'tag':
        rdf_property = 'datalab:tag/datalab:tagValue'
    elif method == 'genre':
        rdf_property = 'po:genre'
    elif method == 'masterBrand':
        rdf_property = 'po:masterbrand'
    else:
        raise NotImplementedError(f'Similar to method, "{method}", is not implemented.')
    stmt = f"""
        {prog_uri.n3()} {rdf_property} ?common_property .
        {subject} {rdf_property} ?common_property .
        FILTER ({subject} != {prog_uri.n3()}) .
    """
    return stmt


def build_similar_to_select_statement():
    """Build SELECT statement for counting common properties (tags, genres OR master_brand) for related items."""
    stmt = f"(count(distinct ?common_property) as ?similarity)"
    return stmt


def build_regular_fields_pattern_statement(prog_uri="?programme"):
    """
    Build a pattern statement for matching fields that need no extra processing.

    Arguments:
        prog_uri (str): sparql variable or programme URI
    """
    stmt = f"""
    {prog_uri} a po:Programme ;
        rdfs:label ?title ;
        schema:image ?image ;
        po:version ?version ;
        datalab:pid ?pid ;
        dct:type ?media ;
        xsd:duration ?duration ;
        po:masterbrand ?masterBrand .
    """
    return stmt


def build_tags_select_statement():
    """Build SELECT statement for grouping tags."""
    stmt = f"""
    {build_group_concat_stmt('tag', 'tags')}
    {build_group_concat_stmt('taguri', 'taguris')}
    {build_group_concat_stmt('tagsource', 'tagsources')}
    {build_group_concat_stmt('tagconf', 'tagconfs')}
    """
    return stmt


def build_tags_pattern_statement(prog_uri="?programme"):
    """
    Build a pattern statement for matching tags and tag details.

    Arguments:
        prog_uri (str): sparql variable or programme URI
    """
    stmt = f"""
    {prog_uri} datalab:tag ?tagRelation .
    ?tagRelation
        datalab:tagValue ?taguri ;
        datalab:tagConfidence ?tagconf ;
        datalab:tagBy/dct:title ?tagsource .

    ?taguri dct:title ?tag .
    """
    return stmt


def build_genres_select_statement():
    """Build select statement for grouping genres and genre details."""
    stmt = f"""
    {build_group_concat_stmt('topLevelGenre', 'topLevelGenres')}
    {build_group_concat_stmt('topLevelGenreUri', 'topLevelGenreUris')}
    {build_group_concat_stmt('topLevelGenreKey', 'topLevelGenreKeys')}

    {build_group_concat_stmt('secondLevelGenre', 'secondLevelGenres')}
    {build_group_concat_stmt('secondLevelGenreUri', 'secondLevelGenreUris')}
    {build_group_concat_stmt('secondLevelGenreKey', 'secondLevelGenreKeys')}

    {build_group_concat_stmt('thirdLevelGenre', 'thirdLevelGenres')}
    {build_group_concat_stmt('thirdLevelGenreUri', 'thirdLevelGenreUris')}
    {build_group_concat_stmt('thirdLevelGenreKey', 'thirdLevelGenreKeys')}
    """
    return stmt


def build_genres_pattern_statement(prog_uri='?programme'):
    """
    Build a pattern statement for matching genres and genre details.

    Arguments:
        prog_uri (str): sparql variable or programme URI
    """
    stmt = f"""
    OPTIONAL {{
        {prog_uri} po:genre ?topLevelGenreUri .
        ?topLevelGenreUri
            a datalab:topLevelGenre ;
            dct:title ?topLevelGenre ;
            datalab:genreKey ?topLevelGenreKey .
    }}
    OPTIONAL {{
        {prog_uri} po:genre ?secondLevelGenreUri .
        ?secondLevelGenreUri
            a datalab:secondLevelGenre ;
            dct:title ?secondLevelGenre ;
            datalab:genreKey ?secondLevelGenreKey .
    }}
    OPTIONAL {{
        {prog_uri} po:genre ?thirdLevelGenreUri .
        ?thirdLevelGenreUri
            a datalab:thirdLevelGenre ;
            dct:title ?thirdLevelGenre ;
            datalab:genreKey ?thirdLevelGenreKey .
    }}
    """
    return stmt


def build_group_concat_stmt(singular, plural):
    """Build a group concat statement to aggregate results."""
    stmt = f'(GROUP_CONCAT(?{singular};separator="{constants.TAG_SEPARATOR}") as ?{plural})'
    return stmt
