import uuid
import numpy as np

from model_parameters import GlobalParameters as g


class Developer(object):
    def __init__(self, experience, available_working_hour, components, board, backlog):
        self.available_working_hour = available_working_hour
        self.experience = experience
        self.components = components
        self.board = board
        self.backlog = backlog
        self.wip = None
        self.uuid = uuid.uuid4()

    def start_to_work(self, ticket, direct):
        if ticket.type in g.subtask_types:
            ticket.move_on(direct)
        else:
            ticket.move_on(direct, self.board.board)

        ticket.assigned_to = self.uuid
        print(self.board.board)

    def search_ticket(self):
        for ticket in self.board.board.tickets['SELECTED FOR DEVELOPMENT']:
            for ticket_component in ticket.components:
                if ticket_component in self.components:
                    if ticket.type == g.subtask_types:

                        """TAKE COMPLETION BLOCKER"""
                        self.start_to_work(ticket, 'IN DEV')
                        return True
                    elif ticket.type in g.subtask_types:

                        """TAKE SUB-TASK"""
                        self.start_to_work(ticket, 'IN DEV')
                        return True
                    elif ticket.type == 'Feature':

                        """TAKE FEATURE"""
                        self.start_to_work(ticket, 'IN ANALYSIS')
                        ticket.move_on('IN ANALYSIS', self.board.board)
                        return True
                    else:

                        """TAKE TASK, DECHNICAL DEBT AND OTHER PARENT CARD"""
                        self.start_to_work(ticket, 'IN DEV')
                        return True
        return False

    def _review_ticket(self, ticket):
        if ticket.type in g.ticket_types and ticket.type != 'Feature':
            ticket.move_on('READY FOR QA', self.board.board)
            ticket.assigned_to = None
        elif ticket.type == 'Feature':
            pass
        elif ticket.type == 'Sub-Task':
            ticket.move_on('DONE')
            if ticket.parent.is_ready_for_qa():
                ticket.parent.move_on('READY FOR QA', self.board.board)
                ticket.parent.assigned_to = None
        elif ticket.type == 'Completion blocker':
            ticket.move_on('READY FOR QA')
            if ticket.parent.is_ready_for_qa():
                ticket.parent.move_on('READY FOR QA', self.board.board)
                ticket.parent.assigned_to = None
        ticket.assigned_to = None
        print(self.board.board)

    def review(self):
        """Review subtask and move on to READY for QA. Unassigne ticket"""
        for ticket in self.board.board.tickets['REVIEW']:
            # Move on subtask to Ready For QA
            for ticket_component in ticket.components:
                if ticket_component in self.components:
                    if ticket.assigned_to is None:
                        ticket.assigned_to = self.uuid
                        self._review_ticket(ticket)

    def _development(self, ticket):
        ticket_done = False
        if ticket.type in g.ticket_types and ticket.type != 'Feature':

            """DEVELOP BUG, TASK, TECHNICAL DEBT"""
            ticket.move_on('REVIEW', self.board.board)
            ticket_done = True
        elif ticket.type in g.subtask_types:

            """DEVELOP COMPLETION BLOCKER OR SUBTASK"""
            ticket.move_on('REVIEW')
            if ticket.parent.is_ready_to_review():
                ticket.parent.move_on('REVIEW', self.board.board)
                ticket.parent.assigned_to = None
            ticket_done = True

        if ticket_done:
            ticket.assigned_to = None
            print(self.board.board)

    def _get_development_time(self, ticket):
        # TODO: CONFIGURE THIS MORE CORRECTLY
        if ticket.type in g.subtask_types:
            return (g.develop_complexity_coefficient[ticket.parent.complexity] / self.experience) * 460 * 4
        else:
            return (g.develop_complexity_coefficient[ticket.complexity] / self.experience) * 1000 * 4

    def _component_validation(self, ticket):
        if ticket.components.__len__() is 3:

            component_available_states = ['correct', 'remove']
            var = np.random.choice(component_available_states, 1,
                                   p=[g.backlog__ticket_correct_component,
                                      1 - g.backlog__ticket_correct_component])[0].__str__()
        elif ticket.components.__len__() is 1:
            component_available_states = ['correct', 'change', 'add']
            var = np.random.choice(component_available_states, 1,
                                   p=[g.backlog__ticket_correct_component,
                                      g.backlog__ticket_need_to_change_component,
                                      1 - (g.backlog__ticket_correct_component +
                                           g.backlog__ticket_need_to_change_component)])[0].__str__()
        else:
            component_available_states = ['correct', 'change', 'add', 'remove']
            var = np.random.choice(component_available_states, 1,
                                   p=[g.backlog__ticket_correct_component,
                                      g.backlog__ticket_need_to_change_component,
                                      g.backlog__ticket_need_to_add_component,
                                      g.backlog__ticket_need_to_remove_component])[0].__str__()

        # Developer adds some component to the ticket
        if var == 'add':
            global_components = g.components[:3]
            for component in global_components:
                component = component[0]
                if component not in ticket.components:
                    ticket.components.append(component)
                    break

        # Developer removes some component to the ticket
        elif var == 'remove':
            redudant = np.random.choice(ticket.components, 1)[0].copy().__str__()
            for component_index in range(ticket.components.__len__()):
                if ticket.components[component_index] == redudant:
                    del ticket.components[component_index]
                    break

        # Developer changes some component to the ticket
        elif var == 'change':
            change_candidat = np.random.choice(ticket.components, 1)[0].copy().__str__()
            for component in g.components[:3]:
                if change_candidat != component[0] and component[0] not in ticket.components:
                    ticket.components.append(component[0])
                    break

            for component_index in range(ticket.components.__len__()):
                if ticket.components[component_index] == change_candidat:
                    del ticket.components[component_index]
                    break

    def backlog_pull_out(self, ticket_selected):
        if not ticket_selected:
            for ticket_index in range(self.backlog.tickets.__len__()):
                ticket = self.backlog.tickets[ticket_index]
                for component in self.components:
                    if component in ticket.components:
                        # TODO: yield g.env.timeout(random.uniform(0,0.5)) # Time, spend to search a ticket int backlog

                        # Grap this ticket to the board
                        self.board.board.at['SELECTED FOR DEVELOPMENT', 'tickets'].append(ticket)

                        self.board.board.at['SELECTED FOR DEVELOPMENT', 'count'] += 1

                        ticket.status = 'SELECTED FOR DEVELOPMENT'
                        ticket.assigned_to = self.uuid
                        ticket_selected = 1

                        # Removing ticket from backlog
                        self.backlog.tickets.pop(ticket_index)

                        # Level up backlog statistic
                        g.stat_backlog['resolved']['total'] += 1

                        print(self.board.board)

                        if ticket_selected:
                            break
                    if ticket_selected:
                        break
                if ticket_selected:
                    break

    def development(self):
        while True:

            """START TO WORK"""
            yield g.env.timeout(0.25)

            """START TO WORK: SEARCH TICKET"""
            ticket_selected = self.search_ticket()

            """Review subtask and move on to READY for QA. Unassigned ticket"""
            self.review()

            """DEVELOPMENT PROCESS"""
            for ticket in self.board.board.tickets['IN DEV']:
                if ticket.assigned_to is self.uuid:
                    yield g.env.timeout(self._get_development_time(ticket))
                    self._development(ticket)
                    break

            """Analysis"""
            for ticket in self.board.board.tickets['IN ANALYSIS']:
                if ticket.assigned_to is self.uuid:
                    yield g.env.timeout(1)

                    # Component validation
                    self._component_validation(ticket)

                    # Creation a new subtask
                    for component in ticket.components:
                        ticket.add_subtask(component=component,
                                           type='Sub-Task',
                                           board=self.board,
                                           status='SELECTED FOR DEVELOPMENT')

                    # Move on "Development"
                    ticket.move_on('IN DEV', self.board.board)

            # Backlog pull out. Select a scope for development
            self.backlog_pull_out(ticket_selected)
