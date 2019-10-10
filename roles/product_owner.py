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

import numpy as np

from entities.ticket import Ticket
from model_parameters import GlobalParameters as g


class PO:
    def __init__(self, frequency, board):
        self.frequency = frequency
        self.board = board

    def increase_growth_backlog(self):
        while True:
            ticket_complexity = np.random.choice(
                g.complexity_types, 1, p=[0.1, 0.3, 0.4, 0.15, 0.05]
            )[0].copy()

            ticket_type = np.random.choice(
                g.ticket_types, 1, p=[0.47, 0.43, 0.05, 0.05]
            )[0].copy()

            ticket_priority = (
                np.random.choice(g.ticket_priority, 1, p=[0.15, 0.41, 0.38, 0.06])[0]
                .copy()
                .__int__()
            )
            ticket_components = []
            while not ticket_components:
                ticket_components = np.random.choice(
                    g.components, 1, p=[0.13, 0.16, 0.34, 0.2, 0.03, 0.08, 0.06]
                )[0].copy()

            ticket = Ticket(
                complexity=ticket_complexity,
                type=ticket_type,
                priority=ticket_priority,
                components=ticket_components,
                status='Backlog',
            )

            self.board.tickets.append(ticket)
            g.stat_backlog['created']['total'] += 1

            # print(f'\n\nPO have create a new ticket in {ticket.status} with are following parameters:\n'
            #       f'Type: {ticket.type}\n'
            #       f'Priority: {ticket.priority}\n'
            #       f'Complexity: {ticket.complexity}\n'
            #       f'Components: {ticket.components}\n\n'
            #       f'Current time is {g.env.now}\n\n')

            yield g.env.timeout(self.frequency)
        return
