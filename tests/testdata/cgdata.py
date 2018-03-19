graph_response = {
    'results': {
        'bindings': [
                        {
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
                    ] * 2  # check multiple results are handled correctly
    }
}

content_graph_api_response = {
    'Results': [
                   {
                       'TestId': 'ID1',
                       'TestDesc': 'This is a description.',
                       'Tags': [
                           {
                               'Source': 'tagsrc1',
                               'TagList': [{
                                   'Confidence': 0.5,
                                   'HumanReadable': 'tag1',
                                   'Tag': 'taguri1'
                               }]
                           },
                           {
                               'Source': 'tagsrc2',
                               'TagList': [{
                                   'Confidence': 0.6,
                                   'HumanReadable': 'tag2',
                                   'Tag': 'taguri2'
                               }]
                           }
                       ],
                       'Genres': {
                            'TopLevel': [{
                                'Genre': 'gentopuri',
                                'HumanReadable': 'gentop',
                                'Key': 'gentopkey'
                            }],
                            'SecondLevel': [{
                                'Genre': 'genseconduri',
                                'HumanReadable': 'gensecond',
                                'Key': 'gensecondkey'
                            }],
                            'ThirdLevel': [{
                                'Genre': 'genthirduri',
                                'HumanReadable': 'genthird',
                                'Key': 'genthirdkey'
                            }]
                       }
                   }
               ] * 2  # check multiple results are handled correctly
}

empty_graph_response = {
    'results':
        {
            'bindings': []
        }
}
empty_content_graph_api_response = {'Results': []}
