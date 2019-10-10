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

import uuid


class Subtask:
    def __init__(self, component, type, status, board, parent):
        self.type = type
        self.components = component
        self.status = str()
        self.assigned_to = None
        self.status = status
        self.board = board
        self.uuid = uuid.uuid4()
        self.parent = parent

    def move_on(self, direct):
        # Remove from the old column
        tickets = self.board.board.tickets[self.status]
        for ticket_index in range(len(tickets)):
            if tickets[ticket_index] is self:
                del tickets[ticket_index]
                break

        # Move the ticket
        self.board.board.tickets[direct].append(self)
        self.status = direct

    def move_parent_to(self, direct):
        self.parent.move_on(direct, self.board.board)
