from app.querybuilder.sparql.subqueries import build_sparql_anding_statement, build_values_oring_statement, \
    build_filter_statement, build_sort_statement, build_regular_fields_pattern_statement, \
    build_tags_pattern_statement, build_genres_pattern_statement, build_tags_select_statement, \
    build_genres_select_statement
from app.utils import constants
from exceptions.queryexceptions import InvalidInputParameterCombination


def build_query(media_type=None, tags=None, sort=None, max_duration=None, published_after=None, categories=None,
                region=None, random=False, limit=constants.DEFAULT_QUERY_LIMIT,
                offset=constants.DEFAULT_QUERY_OFFSET):
    """
    Construct a SPARQL query to retrieve content from the content graph. Filter by validated query params.

    Arguments:
        media_type (rdflib.Literal): type of media to be returned eg Audio, Video
        tags (list of rdflib.URIRef): list of tag URIs to filter by
        sort (str): field to sort by eg `duration`
        max_duration (str,ISO8601): maximum duration of content
        published_after (str, ISO8601): return content published after this date [NOT IMPLEMENTED]
        region (rdflib.Literal): region of content [NOT IMPLEMENTED]
        limit (int): number of results to return (for pagination)
        offset (int): offset of results to return (for pagination)
        random (bool): toggle to return random result
        categories (list): list of category keys to filter by

    Returns:
        query_string (string): SPARQL query
    """
    # NOTE: query time skyrockets with added OPTIONAL patterns, see:
    # https://stackoverflow.com/questions/25609691/alternative-for-optional-keyword-in-sparql-queries
    #
    # NOTE: query assumes ordering of group concat operations are same across tag and source - have eyeballed and
    # looks good
    if published_after is not None:
        raise NotImplementedError('The parameter `publishedAfter` is not yet implemented')
    if region is not None:
        raise NotImplementedError('The parameter `region` is not yet implemented')
    if sort is not None and random:
        raise InvalidInputParameterCombination('Cannot specify both `sort` and `random`.')

    regular_fields = '?title ?image ?version ?programme ?pid ?media ?duration ?publicationDate ?masterBrand'
    query_string = f"""
        SELECT
            {regular_fields}
            {build_tags_select_statement()}
            {build_genres_select_statement()}

        WHERE {{
            {build_regular_fields_pattern_statement()}
            {build_tags_pattern_statement()}
            {build_genres_pattern_statement()}

            {build_sparql_anding_statement(
                object_list=tags,
                predicate_str='datalab:tag/datalab:tagValue',
                object_binding='programme'
            )}
            {build_values_oring_statement('media', media_type)}
            {build_filter_statement('duration', '<', max_duration)}
            {build_filter_statement('published_date', '>', published_after)}
            {build_sparql_anding_statement(
                object_list=categories,
                predicate_str='po:genre/datalab:genreKey',
                object_binding='programme'
            )}
        }}
        GROUP BY {regular_fields}
        {'ORDER BY RAND()' if random else 'ORDER BY ' + build_sort_statement(sort) if sort is not None else ''}
        LIMIT {limit}
        OFFSET {offset}
    """

    return query_string
