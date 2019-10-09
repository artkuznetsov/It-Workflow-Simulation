from entities.project import Project
from entities.backlog import Backlog
from entities.board import Board
from model_parameters import GlobalParameters as g

"""
Class where we've described or simulation model on the high level
"""


class Model(object):
    def __init__(self):
        """
        Constructor class for new model.
        """
        self.board = Board('Stories Board')
        self.project = Project('DataSwitch Core')
        self.backlog = Backlog()

        return

    def run(self):
        """
        Controls the main model run. Initialises model and patient arrival and
        audit processes. Instigates the run. At end of run calls for an audit
        summary and bed occupancy plot
        """

        """
        EMPLOYEES REGISTER TO THE PROJECT

        Adding 2 QAs with best experience on the project
        """
        self.project.qas_register(count=2, experience=10, available_working_hours=10, board=self.board)

        """
        Adding 1 release master (for our project we have release master as QA)
        """
        self.project.qas_register(count=1, experience=7, available_working_hours=10, board=self.board,
                                  release_master=True)
        """
        Adding 1 middle QA on the project
        """
        self.project.qas_register(count=1, experience=4, available_working_hours=8, board=self.board)

        """
        Adding 1 new QA to the project
        """
        self.project.po_register(count=5, frequency=1, board=self.backlog)

        """
        Adding 1 crazy developer
        """
        self.project.dev_register(count=1, experience=10, available_working_hours=15, components=['CM'],
                                  board=self.board,
                                  backlog=self.backlog)
        """
        Adding 2 UI developers with middle experience
        """
        self.project.dev_register(count=2, experience=7, available_working_hours=8, components=['UI'], board=self.board,
                                  backlog=self.backlog)

        """
        Adding 1 UI developer with best experience
        """
        self.project.dev_register(count=1, experience=10, available_working_hours=10, components=['UI'],
                                  board=self.board,
                                  backlog=self.backlog)

        """
        Adding 2 cross-component developers with best experience
        """
        self.project.dev_register(count=2, experience=10, available_working_hours=8, components=['CM', 'ASE'],
                                  board=self.board, backlog=self.backlog)

        """
        Adding 2 single-component developers
        """
        self.project.dev_register(count=2, experience=7, available_working_hours=8, components=['CM'], board=self.board,
                                  backlog=self.backlog)

        """
        Adding 2 single component developers with best experience
        """
        self.project.dev_register(count=2, experience=10, available_working_hours=8, components=['ASE'],
                                  board=self.board,
                                  backlog=self.backlog)

        """
        Adding 1 single component developer
        """
        self.project.dev_register(count=1, experience=7, available_working_hours=8, components=['ASE'],
                                  board=self.board,
                                  backlog=self.backlog)

        """
        Register processES that will be run into our simulation model
        """
        g.env.process(self.increase_growth_backlog())
        g.env.process(self.development())
        g.env.process(self.testing())
        g.env.process(self.uat())
        g.env.process(self.time())
        # g.env.process(self.release())

        """
        Run simulation model.
        until parameter = estimated hours for our model. 
        
        Here we have 1 working month (8 hours * 5 days on the week * 4 weeks)
        """
        g.env.run(until=8 * 5 * 4)

        """
        After our simulation is ended we need to know some performance metrics.
        For an example we would like to know how much tickets was created/selected from backlog
        """
        print(self.board.board)
        print(f"Spent {g.env.now} hours")
        print(f'Backlog. Size is \t\t{self.backlog.tickets.__len__()} tickets\n'
              f"Backlog. Created \t\t{g.stat_backlog['created']['total']} tickets\n")

        return

    """
    Here and above we would like to describe our simualtion's processes on the project.
    
    For an example we have:
    1. Testing (QA accountable for this process)
    2. UAT (QA accountable for this process too). Re-checking on staging environment (not optimal process, yeah)
    3. Release (We have the Release Manager that also is QA).
    4. Increasing Growth Backlog (our product owner is accountable for this process)
    5. Development (our developers are accountable for this process)
    6. Time (is a static method that should allow us to know - What is day of the week today? 
        It needs for Release Manager for releases (we would like to release each Monday and Thursday)  
    """

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
