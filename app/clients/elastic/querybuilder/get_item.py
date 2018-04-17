from random import randint

from app.utils import constants
from exceptions.queryexceptions import InvalidInputParameterCombination


########
# add uri as index
# see where uri returned for sparql content graph (in PR somewheer?
#



from elasticsearch_dsl import Search, Q


def build_query_body(item_uri):

    search = Search(index='pips')

    return search.to_dict()
