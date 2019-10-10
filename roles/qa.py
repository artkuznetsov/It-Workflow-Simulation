import uuid
import numpy as np

from model_parameters import GlobalParameters as g


class QA(object):
    def __init__(self, experience, available_working_hour, board, release_master=False):
        # QA experience for this project. Can be in range [0 - 10]
        self.experience = experience

        self.available_working_hour = available_working_hour
        self.board = board
        self.uuid = uuid.uuid4()
        self.release_master = release_master

    def _start_to_work(self, ticket):
        ticket.assigned_to = self.uuid
        if ticket.type in g.subtask_types:
            ticket.move_on('IN QA')

            """MOVE PARENT TO RFQ"""
            if ticket.parent.is_ready_for_qa():
                ticket.move_parent_to('IN QA')
                if ticket.parent.assigned_to is None:
                    ticket.parent.assigned_to = self.uuid
        else:
            ticket.move_on('IN QA', self.board.board)

    def get_testing_time(self, ticket):
        if ticket.type in g.subtask_types:
            return (
                (g.probability_to_find_bug['types'][ticket.type]) / self.experience
            ) * 10
        else:
            return (
                (
                    g.probability_to_find_bug['types'][ticket.type]
                    * g.probability_to_find_bug['complexity'][ticket.complexity]
                )
                / (10 / self.experience)
            ) * 10
        # yield g.env.timeout(testing_time)  # Testing time

    def _bug(self, ticket):
        cb_component = None
        probability_to_bug_found = 0.0
        if ticket.type in g.subtask_types:
            probability_to_bug_found = (
                g.probability_to_find_bug['types'][ticket.type]
                * g.probability_to_find_bug['component'][ticket.components[0]]
                * (self.experience / 10)
            )
        else:
            cb_component = np.random.choice(ticket.components, 1)[0].copy()
            probability_to_bug_found = (
                g.probability_to_find_bug['types'][ticket.type]
                * g.probability_to_find_bug['component'][cb_component]
                * g.probability_to_find_bug['complexity'][ticket.complexity]
                * (self.experience / 10)
            )
            probability_to_bug_found = (
                probability_to_bug_found if probability_to_bug_found <= 1 else 1
            )

        bug_is_found = np.random.choice(
            [True, False], 1, p=[probability_to_bug_found, 1 - probability_to_bug_found]
        )[0].copy()

        return {'is_found': bug_is_found, 'component': cb_component}

    def _register_bug(self, ticket, cb_component=None):
        if ticket.type in g.subtask_types:
            # yield g.env.timeout(0.25)
            ticket.move_on('SELECTED FOR DEVELOPMENT')
            ticket.parent.move_on('BUGFIXING', self.board.board)
            ticket.parent.assigned_to = None
            print(f"QA has tested CB and moved back")
        else:
            # yield g.env.timeout(0.5)
            ticket.add_subtask(
                component=cb_component,
                type='Completion blocker',
                status='SELECTED FOR DEVELOPMENT',
                board=self.board,
            )
            ticket.move_on('BUGFIXING', self.board.board)
            print(f"QA has tested {ticket.type} and moved to Bufgixing with CB")

        ticket.assigned_to = None
        print(f'Now is {g.dow}. Board is {self.board.board}')

    def _testing_pass(self, ticket):
        if ticket.type in g.subtask_types:
            ticket.move_on('DONE')
        else:
            ticket.move_on('NEXT STAGING', self.board.board)
            print(f"QA has tested {ticket.type} and moved forward")
        print(f'Now is {g.dow}. Board is {self.board.board}')
        ticket.assigned_to = None

    def _uat_pass(self, ticket):
        ticket.move_on('DONE', self.board.board)
        print(f"QA has tested {ticket.type} and moved forward")
        print(f'Now is {g.dow}. Board is {self.board.board}')
        ticket.assigned_to = None

    def testing(self):
        while True:
            if self.release_master and g.dow in (1, 4) and g.last_release_day != g.dow:
                g.env.process(self.release())
                # yield g.env.timeout(24)

            for ticket in self.board.board.tickets['IN QA']:
                if ticket.assigned_to == self.uuid:
                    yield g.env.timeout(self.get_testing_time(ticket))

                    bug = self._bug(ticket)

                    if bug['is_found']:
                        yield g.env.timeout(0.5)
                        self._register_bug(ticket, bug['component'])
                    else:
                        self._testing_pass(ticket)

            if self.board.board.tickets['READY FOR QA']:
                for ticket in self.board.board.tickets['READY FOR QA']:
                    if ticket.type in g.ticket_types:
                        for subtask in ticket.subtasks:
                            if (
                                subtask.type == 'Completion blocker'
                                and subtask.status == 'READY FOR QA'
                            ):
                                ticket = subtask
                                break

                    self._start_to_work(ticket)

                    yield g.env.timeout(self.get_testing_time(ticket))

                    bug = self._bug(ticket)

                    if bug['is_found']:
                        yield g.env.timeout(0.5)
                        self._register_bug(ticket, bug['component'])
                    else:
                        self._testing_pass(ticket)
            else:
                """QA CAN"T FIND CARDS FOR WORK: HE/SHE SPEND 30 MINUTES TO ANY OTHER WORK (TEST CASES, REGRESSION AND SO ON)"""
                # print("QA don't have any tickets for testing... He/she will work under process issues...")
                yield g.env.timeout(0.5)
                g.free_time_qa += 0.5
        return

    def _move_all_tickets(self, source, direct):
        for ticket in self.board.board.tickets[source]:
            if ticket.type in g.ticket_types:
                ticket.move_on(direct, self.board.board)
            else:
                ticket.move_on(direct)
            print(f'Now is {g.dow}. Board is {self.board.board}')

    def release(self):
        while True:
            if g.dow == 1 or g.dow == 4:
                if g.last_release_day == g.dow:
                    break
                """RELEASE"""

                """COLLECT BRANCHES"""
                yield g.env.timeout(0.25)

                """RELEASE: DEPLOY TO PRODS"""
                if self.board.board.tickets['DONE']:
                    yield g.env.timeout(0.75 * 3)
                    while self.board.board.tickets['DONE'].__len__() > 0:
                        self._move_all_tickets('DONE', 'RELEASED')
                        g.last_release_day = g.dow
                else:
                    print("SLIDE PROD RELEASE")

                """RELEASE: DEPLOY TO STG"""
                if self.board.board.tickets['NEXT STAGING']:
                    yield g.env.timeout(0.75)
                    while self.board.board.tickets['NEXT STAGING'].__len__() > 0:
                        self._move_all_tickets('NEXT STAGING', 'PRE-RELEASE QA')
                        g.last_release_day = g.dow
                else:
                    print("SLIDE STG RELEASE")
        return

    def uat(self):
        while True:
            for ticket in self.board.board.tickets['PRE-RELEASE QA']:
                """RELEASE: UAT"""
                if ticket.assigned_to is None:
                    ticket.assigned_to = self.uuid
                    yield g.env.timeout(self.get_testing_time(ticket))

                    """RELEASE: UAT: CALCULATE BUG PROBABILITY"""
                    bug = self._bug(ticket)

                    if bug['is_found']:

                        """RELEASE: UAT: REGISTER BUG"""
                        yield g.env.timeout(0.5)
                        self._register_bug(ticket, bug['component'])
                    else:

                        """RELEASE: UAT: TESTING PASSED"""
                        self._uat_pass(ticket)
            yield g.env.timeout(0.5)
        return
