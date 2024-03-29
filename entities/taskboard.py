"""
Copyright (c) 2019 Lineate LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE."""

import pandas as pd


class TaskBoard:
    def __init__(self, name):
        self.board = pd.DataFrame(
            {
                'tickets': [[], [], [], [], [], [], [], [], [], [], []],
                'max': [3, 3, 12, 5, 7, 1000, 1000, 1000, 1000, 1000, 1000],
                'min': [0, 0, 6, 0, 2, 0, 0, 0, 0, 0, 0],
                'count': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            },
            index=[
                'SELECTED FOR DEVELOPMENT',
                'IN ANALYSIS',
                'IN DEV',
                'REVIEW',
                'READY FOR QA',
                'IN QA',
                'BUGFIXING',
                'NEXT STAGING',
                'PRE-RELEASE QA',
                'DONE',
                'RELEASED',
            ],
        )
        self.board.index.name = name
