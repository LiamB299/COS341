dfa_1 = {
    'dfa': "un-minimized",
    'states': [
        {
            'state': '0',
            'input': [
                '0',
                '1'
            ],
            'next_state': [
                {
                    'state': '1',
                },
                {
                    'state': '3'
                }
            ],
            'starting': True,
            'accepting': False
        },
        {
            'state': '1',
            'input': [
                '0',
                '1'
            ],
            'next_state': [
                {
                    'state': '0',
                },
                {
                    'state': '3'
                }
            ],
            'starting': False,
            'accepting': False
        },
        {
            'state': '3',
            'input': [
                '0',
                '1'
            ],
            'next_state': [
                {
                    'state': '5',
                },
                {
                    'state': '5'
                }
            ],
            'starting': False,
            'accepting': True
        },
        {
            'state': '5',
            'input': [
                '0',
                '1'
            ],
            'next_state': [
                {
                    'state': '5',
                },
                {
                    'state': '5'
                }
            ],
            'starting': False,
            'accepting': True
        }
    ]
}

################################################

