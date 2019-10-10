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

from entities.subtask import Subtask


class Ticket:
    def __init__(self, complexity, components, type, priority, status):
        self.type = type
        self.priority = priority
        self.complexity = complexity
        self.components = components
        self.status = status
        self.fix_version = int()
        self.assigned_to = None
        self.subtasks = list()
        self.uuid = uuid.uuid4()
        self.is_parent = True

    def move_on(self, direct, board):

        # Remove from the old column
        tickets = board.tickets[self.status]
        for ticket_index in range(len(tickets)):
            if tickets[ticket_index] is self:
                board.at[self.status, 'count'] -= 1
                del tickets[ticket_index]
                break

        # Move the ticket
        board.tickets[direct].append(self)
        board.at[direct, 'count'] += 1
        self.status = direct
        print(board)

    def add_subtask(self, component, type, status, board):
        components = [component]
        subtask = Subtask(
            component=components, type=type, status=status, board=board, parent=self
        )
        board.board.tickets['SELECTED FOR DEVELOPMENT'].append(subtask)
        self.subtasks.append(subtask)

    def is_ready_to_review(self):
        for subtask in self.subtasks:
            if (
                subtask.status in ('SELECTED FOR DEVELOPMENT', 'IN DEV')
                and self.status != 'BUGFIXING'
            ):
                return False
        return True

    def is_ready_for_qa(self):
        for subtask in self.subtasks:
            if subtask.status in ('SELECTED FOR DEVELOPMENT', 'IN DEV', 'REVIEW'):
                return False
        return True

    def is_ready_to_deploy(self):
        for subtask in self.subtasks:
            if subtask.status in (
                'SELECTED FOR DEVELOPMENT',
                'IN DEV',
                'REVIEW',
                'READY FOR QA',
                'IN QA',
            ):
                return False
            return True
