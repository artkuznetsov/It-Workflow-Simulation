from roles.developer import Developer
from roles.product_owner import PO
from roles.qa import QA


class Project:
    def __init__(self):
        self.name = 'Dataswirch Core'
        self.qas = list()
        self.devs = list()
        self.pos = list()

    def qas_register(self, count, experience, available_working_hours, board, release_master=False):
        for employee in range(count):
            qa = QA(experience, available_working_hours, board, release_master=release_master)
            self.qas.append(qa)

    def po_register(self, count, frequency, board):
        for employee in range(count):
            po = PO(frequency=frequency, board=board)
            self.pos.append(po)

    def dev_register(self, count, experience, available_working_hours, components, board, backlog):
        for employee in range(count):
            dev = Developer(experience=experience,
                            available_working_hour=available_working_hours,
                            components=components,
                            board=board,
                            backlog=backlog)
            self.devs.append(dev)
