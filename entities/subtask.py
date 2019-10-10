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
