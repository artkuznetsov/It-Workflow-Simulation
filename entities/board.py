import pandas as pd


class StoriesBoard:
    board = pd.DataFrame()

    def __init__(self):
        self.board = pd.DataFrame({
            'tickets': [[], [], [], [], [], [], [], [], [], [], []],
            'max': [3, 3, 12, 5, 7, 1000, 1000, 1000, 1000, 1000, 1000],
            'min': [0, 0, 6, 0, 2, 0, 0, 0, 0, 0, 0],
            'count': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }, index=['SELECTED FOR DEVELOPMENT',
                  'IN ANALYSIS',
                  'IN DEV',
                  'REVIEW',
                  'READY FOR QA',
                  'IN QA',
                  'BUGFIXING',
                  'NEXT STAGING',
                  'PRE-RELEASE QA',
                  'DONE',
                  'RELEASED'])
        self.board.index.name = 'Stories Board'
        return