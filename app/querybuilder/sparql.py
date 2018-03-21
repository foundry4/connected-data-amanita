from app.utils import constants
from exceptions.queryexceptions import InvalidInputParameterCombination


def build_get_content_query(media=None, tags=None, sort=None, max_duration=None, published_after=None, categories=None,
                            region=None, random=False, similar_to=None, limit=constants.DEFAULT_QUERY_LIMIT,
                            offset=constants.DEFAULT_QUERY_OFFSET):
    """
    Construct a SPARQL query to retrieve content from the content graph. Filter by query_params

    NOTE: query time skyrockets with added OPTIONAL patterns, see:
    https://stackoverflow.com/questions/25609691/alternative-for-optional-keyword-in-sparql-queries

    NOTE: query assumes ordering of group concat operations are same across tag and source - have eyeballed and
    looks good

    Arguments:
        media (Literal): type of media to be returned eg Audio, Video
        tags (list): list of Literal tags to filter by
        sort (str): field to sort by eg `duration`
        max_duration (str,ISO8601): maximum duration of content
        published_after (str, ISO8601): return content published after this date [NOT IMPLEMENTED]
        region (str): region of content [NOT IMPLEMENTED]
        limit (int): number of results to return (for pagination)
        offset (int): offset of results to return (for pagination)

    Returns:
        query_string (string): SPARQL query
    """
    tag_bindings_statement = _build_sparql_anding_statement(
        object_list=tags,
        predicate_str='datalab:tag/datalab:tagValue',
        object_binding='programme'
    )

    genre_bindings_statement = _build_sparql_anding_statement(
        object_list=categories,
        predicate_str='po:genre/datalab:genreKey',
        object_binding='programme'
    )

    if published_after is not None:
        raise NotImplementedError('The parameter `publishedAfter` is not yet implemented')
    if region is not None:
        raise NotImplementedError('The parameter `region` is not yet implemented')
    if sort is not None and random:
        raise InvalidInputParameterCombination('Cannot specify both sort and random.')

    regular_fields = '?programme ?pid ?media ?duration ?publicationDate ?masterBrand'
    query_string = f"""
        SELECT 
            {regular_fields}

            #tags
            (GROUP_CONCAT(?tag;separator="{constants.TAG_SEPARATOR}") as ?tags)
            (GROUP_CONCAT(?taguri;separator="{constants.TAG_SEPARATOR}") as ?taguris)
            (GROUP_CONCAT(?tagsource;separator="{constants.TAG_SEPARATOR}") as ?tagsources)
            (GROUP_CONCAT(?tagconf;separator="{constants.TAG_SEPARATOR}") as ?tagconfs)
            
            #genres
            (GROUP_CONCAT(?topLevelGenre;separator="{constants.TAG_SEPARATOR}") as ?topLevelGenres)
            (GROUP_CONCAT(?topLevelGenreUri;separator="{constants.TAG_SEPARATOR}") as ?topLevelGenreUris)
            (GROUP_CONCAT(?topLevelGenreKey;separator="{constants.TAG_SEPARATOR}") as ?topLevelGenreKeys)

            (GROUP_CONCAT(?secondLevelGenre;separator="{constants.TAG_SEPARATOR}") as ?secondLevelGenres)
            (GROUP_CONCAT(?secondLevelGenreUri;separator="{constants.TAG_SEPARATOR}") as ?secondLevelGenreUris)
            (GROUP_CONCAT(?secondLevelGenreKey;separator="{constants.TAG_SEPARATOR}") as ?secondLevelGenreKeys)

            (GROUP_CONCAT(?thirdLevelGenre;separator="{constants.TAG_SEPARATOR}") as ?thirdLevelGenres)
            (GROUP_CONCAT(?thirdLevelGenreUri;separator="{constants.TAG_SEPARATOR}") as ?thirdLevelGenreUris)
            (GROUP_CONCAT(?thirdLevelGenreKey;separator="{constants.TAG_SEPARATOR}") as ?thirdLevelGenreKeys)

        WHERE {{
            {_build_similar_to_statement(similar_to, 'po:masterbrand', 'masterBrand')}
            
            ?programme 
                a po:Programme ;
                datalab:pid ?pid ;
                dct:type ?media ;
                xsd:duration ?duration ;
                po:masterbrand ?masterBrand ;
                datalab:tag ?tagRelation .

            # using path predicate eg `datalab:tag/datalab:tagValue` in `?programme` block above causes duplicates
            ?tagRelation
                datalab:tagValue ?taguri ;
                datalab:tagConfidence ?tagconf ;
                datalab:tagBy ?sourceuri .

            ?taguri dct:title ?tag .
            ?sourceuri dct:title ?tagsource .  
            
            
            OPTIONAL {{            
                ?programme po:genre ?topLevelGenreUri .
                ?topLevelGenreUri 
                    a datalab:topLevelGenre ;
                    dct:title ?topLevelGenre ;
                    datalab:genreKey ?topLevelGenreKey .
            }}
            OPTIONAL {{
                ?programme po:genre ?secondLevelGenreUri .
                ?secondLevelGenreUri 
                    a datalab:secondLevelGenre ;
                    dct:title ?secondLevelGenre ;
                    datalab:genreKey ?secondLevelGenreKey .

            }}
            OPTIONAL {{
                ?programme po:genre ?thirdLevelGenreUri .
                ?thirdLevelGenreUri 
                    a datalab:thirdLevelGenre ;
                    dct:title ?thirdLevelGenre ;
                    datalab:genreKey ?thirdLevelGenreKey .

            }}
            
            {tag_bindings_statement}
            {_build_values_oring_statement('media', media)}
            {_build_filter_statement('duration', '<', max_duration)}
            {_build_filter_statement('published_date', '>', published_after)}
            {genre_bindings_statement}      
        }}
        GROUP BY {regular_fields} 
        {'ORDER BY RAND()' if random else _build_sort_statement(sort)}
        LIMIT {limit}
        OFFSET {offset}
    """

    return query_string


def _serialize_sparql_bindings(bindings):
    """Build a SPARQL VALUES string to bind each KV pair in bindings to the query"""
    bindings_statements = []
    for binding_name, binding_value in bindings.items():
        bindings_statements.append(f"VALUES (?{binding_name}) {{ ({binding_value.n3()}) }} .\n")
    return ' '.join(bindings_statements)


def _build_sparql_anding_statement(object_list, predicate_str, object_binding='programme'):
    """Build a SPARQL query fragment that matches all objects in object_list"""
    if not object_list:
        return ''
    comma_separated_sparql_tags = ', '.join([uri.n3() for uri in object_list])
    tag_filter_statement = f"?{object_binding} {predicate_str} {comma_separated_sparql_tags} .\n"
    return tag_filter_statement


def _build_values_oring_statement(binding, object_list):
    """Build a SPARQL VALUES string to bind everything in object_list by logical OR."""
    if not object_list:
        return ''
    object_bindings = ' '.join([f"({sparql_binding.n3()})" for sparql_binding in object_list])
    return f"VALUES (?{binding}) {{ {object_bindings} }} .\n"


def _build_sort_statement(sort_string):
    """
    Build a SPAQRL ORDER BY string, assume sort_string is valid.

    Example output:
        'ORDER BY ASC (?duration)'
    """
    stmt = ''
    if sort_string is not None:
        if sort_string[0] == '-':
            order = 'DESC'
            field = sort_string[1:]
        else:
            order = 'ASC'
            field = sort_string
        stmt = f'ORDER BY {order}(?{field})'
    return stmt


def _build_filter_statement(binding, filter_operation, object_literal):
    """
    Build a SPARQL FILTER statement.

    Example output:
        'FILTER ?duration < PT2H'
    """
    if object_literal is None:
        return ''
    stmt = f"FILTER (?{binding} {filter_operation} {object_literal.n3()}) .\n"
    return stmt


def _build_similar_to_statement(pid, field, varname):
    if pid is None:
        return ''
    stmt = f"""
            ?programmeSimilar 
                a po:Programme ;
                datalab:pid {pid.n3()} ;
                {field} ?{varname} .
    """
    return stmt
