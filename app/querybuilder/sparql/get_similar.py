from app.querybuilder.sparql.subqueries import build_values_oring_statement, \
    build_filter_statement, build_sort_statement, build_regular_fields_pattern_statement, \
    build_tags_pattern_statement, build_genres_pattern_statement, build_tags_select_statement, \
    build_genres_select_statement, build_similar_to_select_statement, build_similar_to_pattern_statement
from app.utils import constants


def build_query(item_uri=None, media_type=None, sort=None, max_duration=None, published_after=None,
                region=None, similarity_method='genre', limit=constants.DEFAULT_QUERY_LIMIT,
                offset=constants.DEFAULT_QUERY_OFFSET):
    """
    Construct a SPARQL query to retrieve related content, given a programme URI.

    Arguments:
        item_uri (rdflib.URIRef): URI of item to find related results
        similarity_method (str): method by which to fetch related content
            'genre' finds and ranks items that share genres (across levels)
            'tag' finds and ranks items that share tags
            'masterBrand' finds items that share same master brand
        media_type (Literal): type of media to be returned eg audio, Video
        sort (str): field to sort by eg `duration`
        max_duration (str,ISO8601): maximum duration of content
        published_after (str, ISO8601): return content published after this date [NOT IMPLEMENTED]
        region (str): region of content [NOT IMPLEMENTED]
        limit (int): number of results to return (for pagination)
        offset (int): offset of results to return (for pagination)

    Returns:
        query_string (string): SPARQL query
    """

    if published_after is not None:
        raise NotImplementedError('The parameter `publishedAfter` is not yet implemented')
    if region is not None:
        raise NotImplementedError('The parameter `region` is not yet implemented')

    regular_fields = '?title ?image ?version ?programme ?pid ?media ?duration ?publicationDate ?masterBrand'
    query_string = f"""
        SELECT
            {regular_fields}
            {build_similar_to_select_statement()}
            {build_tags_select_statement()}
            {build_genres_select_statement()}

        WHERE {{
            {build_similar_to_pattern_statement('?programme', item_uri, similarity_method)}
            {build_regular_fields_pattern_statement('?programme')}
            {build_tags_pattern_statement('?programme')}
            {build_genres_pattern_statement('?programme')}


            {build_values_oring_statement('media', media_type)}
            {build_filter_statement('duration', '<', max_duration)}
            {build_filter_statement('published_date', '>', published_after)}
        }}
        GROUP BY {regular_fields}
        ORDER BY DESC(?similarity) {build_sort_statement(sort)}
        LIMIT {limit}
        OFFSET {offset}
    """

    return query_string
