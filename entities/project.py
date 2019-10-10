from roles.developer import Developer
from roles.product_owner import PO
from roles.qa import QA


class Project:
    def __init__(self, name):
        self.name = name
        self.qas = list()
        self.devs = list()
        self.pos = list()

    def qas_register(self, **kwargs):
        for _ in range(kwargs['count']):
            qa = QA(
                kwargs['experience'],
                kwargs['available_working_hours'],
                kwargs['board'],
                release_master=kwargs.get('release_master'),
            )
            self.qas.append(qa)

    def po_register(self, **kwargs):
        for _ in range(kwargs['count']):
            po = PO(kwargs['frequency'], kwargs['board'])
            self.pos.append(po)

    def dev_register(self, **kwargs):
        for _ in range(kwargs['count']):
            dev = Developer(
                experience=kwargs['experience'],
                available_working_hour=kwargs['available_working_hours'],
                components=kwargs['components'],
                board=kwargs['board'],
                backlog=kwargs['backlog'],
            )
            self.devs.append(dev)
