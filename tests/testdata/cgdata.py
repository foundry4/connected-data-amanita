raw_graph_response_item = {
    'testId': {
        'extraneous': 'info',
        'value': 'ID1'
    },
    'testDesc': {
        'extraneous': 'info',
        'value': 'This is a description.'
    },
    'tags': {
        'extraneous': 'info',
        'value': 'tag1^tag2'
    },
    'taguris': {
        'extraneous': 'info',
        'value': 'taguri1^taguri2'
    },
    'tagsources': {
        'extraneous': 'info',
        'value': 'tagsrc1^tagsrc2'
    },
    'tagconfs': {
        'extraneous': 'info',
        'value': '0.5^0.6'
    },
    'topLevelGenres': {
        'extraneous': 'info',
        'value': 'gentop'
    },
    'secondLevelGenres': {
        'extraneous': 'info',
        'value': 'gensecond'
    },
    'thirdLevelGenres': {
        'extraneous': 'info',
        'value': 'genthird'
    },
    'topLevelGenreUris': {
        'extraneous': 'info',
        'value': 'gentopuri'
    },
    'secondLevelGenreUris': {
        'extraneous': 'info',
        'value': 'genseconduri'
    },
    'thirdLevelGenreUris': {
        'extraneous': 'info',
        'value': 'genthirduri'
    },
    'topLevelGenreKeys': {
        'extraneous': 'info',
        'value': 'gentopkey'
    },
    'secondLevelGenreKeys': {
        'extraneous': 'info',
        'value': 'gensecondkey'
    },
    'thirdLevelGenreKeys': {
        'extraneous': 'info',
        'value': 'genthirdkey'
    }
}

# /item/<> endpoint returns single result always
single_item_graph_response = {
    'results': {
        'bindings': [raw_graph_response_item]
    }
}

# /content and /similar will return multiple items (or empty list)
multi_item_graph_response = {
    'results': {
        'bindings': [raw_graph_response_item] * 2  # check multiple results are handled correctly
    }
}


processed_api_response_item = {
   'TestId': 'ID1',
   'TestDesc': 'This is a description.',
   'Tags': [
       {
           'Source': 'tagsrc1',
           'TagList': [{
               'Confidence': 0.5,
               'Label': 'tag1',
               'Uri': 'taguri1'
           }]
       },
       {
           'Source': 'tagsrc2',
           'TagList': [{
               'Confidence': 0.6,
               'Label': 'tag2',
               'Uri': 'taguri2'
           }]
       }
   ],
   'Genres': {
        'TopLevel': [{
            'Uri': 'gentopuri',
            'Label': 'gentop',
            'Key': 'gentopkey'
        }],
        'SecondLevel': [{
            'Uri': 'genseconduri',
            'Label': 'gensecond',
            'Key': 'gensecondkey'
        }],
        'ThirdLevel': [{
            'Uri': 'genthirduri',
            'Label': 'genthird',
            'Key': 'genthirdkey'
        }]
   }
}

multi_item_api_response = {
    'Results': [processed_api_response_item] * 2  # check multiple results are handled correctly
}

single_item_api_response = processed_api_response_item


empty_graph_response = {
    'results':
        {
            'bindings': []
        }
}
empty_multi_item_api_response = {'Results': []}
