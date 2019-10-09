from entities.project import Project
from entities.backlog import Backlog
from entities.board import StoriesBoard
from model_parameters import GlobalParameters as g


class Model(object):
    def __init__(self):
        """
        Constructor class for new model.
        """
        self.board = StoriesBoard('Stories Board')
        self.project = Project('DataSwitch Core')
        self.backlog = Backlog()

        return

    def run(self):
        """
        Controls the main model run. Initialises model and patient arrival and
        audit processes. Instigates the run. At end of run calls for an audit
        summary and bed occupancy plot
        """

        # Employees register
        # Kuznetsov, Chernobrivets
        # self.project.qas_register(count=2, experience=10, available_working_hours=10, board=self.board)
        # Kushakova
        self.project.qas_register(count=1, experience=7, available_working_hours=10, board=self.board,
                                  release_master=True)
        # Savchuk
        # self.project.qas_register(count=1, experience=4, available_working_hours=8, board=self.board)

        # Ivy
        self.project.po_register(count=5, frequency=1, board=self.backlog)

        # Grakov
        self.project.dev_register(count=1, experience=10, available_working_hours=15, components=['CM'],
                                  board=self.board,
                                  backlog=self.backlog)
        # Metel, Leonenko
        self.project.dev_register(count=2, experience=7, available_working_hours=8, components=['UI'], board=self.board,
                                  backlog=self.backlog)

        # Nazarchuk
        self.project.dev_register(count=1, experience=10, available_working_hours=10, components=['UI'],
                                  board=self.board,
                                  backlog=self.backlog)

        # Obzor, Shvets
        self.project.dev_register(count=2, experience=10, available_working_hours=8, components=['CM', 'ASE'],
                                  board=self.board, backlog=self.backlog)

        # Dubik,Glukhova
        self.project.dev_register(count=2, experience=7, available_working_hours=8, components=['CM'], board=self.board,
                                  backlog=self.backlog)

        # Kruten, Ustyugova
        self.project.dev_register(count=2, experience=10, available_working_hours=8, components=['ASE'],
                                  board=self.board,
                                  backlog=self.backlog)

        # Grogolev
        self.project.dev_register(count=1, experience=7, available_working_hours=8, components=['ASE'],
                                  board=self.board,
                                  backlog=self.backlog)

        g.env.process(self.increase_growth_backlog())
        g.env.process(self.development())
        g.env.process(self.testing())
        g.env.process(self.uat())
        g.env.process(self.time())
        # g.env.process(self.release())
        g.env.run(until=8 * 5 * 4)

        print(self.board.board)
        print(f"Spent {g.env.now} hours")
        print(f'Backlog. Size is \t\t{self.backlog.tickets.__len__()} tickets\n'
              f"Backlog. Created \t\t{g.stat_backlog['created']['total']} tickets\n")

        return

    def testing(self):
        while True:
            for qa in self.project.qas:
                g.env.process(qa.testing())
            yield g.env.timeout(1000000)
        return

    def uat(self):
        while True:
            for qa in self.project.qas:
                g.env.process(qa.uat())
            yield g.env.timeout(1000000)
        return

    def release(self):
        while True:
            release_master = self.project.qas[0]
            g.env.process(release_master.release())
            yield g.env.timeout(1000000)
        return

    def increase_growth_backlog(self):
        while True:
            for po in self.project.pos:
                g.env.process(po.increase_growth_backlog())
            yield g.env.timeout(1000000)
        return

    def development(self):
        while True:
            for dev in self.project.devs:
                g.env.process(dev.development())
            yield g.env.timeout(1000000)

    @staticmethod
    def time():
        while True:
            yield g.env.timeout(24)
            print(f"Day of the week is {g.dow}\n\n")
            g.dow += 1
            if g.dow == 6:
                g.dow = 1
        return


def main():
    """
    Code entry point after: if __name__ == '__main__'
    Creates model object, and runs model
    """

    model = Model()
    model.run()

    return


# Code entry point. Calls main method.
if __name__ == '__main__':
    main()
