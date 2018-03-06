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
                        },
                        {
                            'testId': {
                                'extraneous': 'info',
                                'value': 'ID2'
                            },
                            'testDesc': {
                                'extraneous': 'info',
                                'value': 'This is another description.'
                            },
                        }
                    ] * 2  # check multiple results are handled correctly
    }
}

content_graph_api_response = {
    'Results': [
                   {
                       'TestId': 'ID1',
                       'TestDesc': 'This is a description.'
                   },
                   {
                       'TestId': 'ID2',
                       'TestDesc': 'This is another description.'
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
