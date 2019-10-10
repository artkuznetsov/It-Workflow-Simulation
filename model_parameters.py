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

import simpy


# TODO: will be great to use Enums instead of these variables

class GlobalParameters:
    """g holds Global variables. No individual instance is required"""

    free_time_qa = 0
    components = [
        ['CM'],
        ['ASE'],
        ['UI'],
        ['CM', 'UI'],
        ['CM', 'ASE'],
        ['UI', 'ASE'],
        ['UI', 'ASE', 'CM'],
    ]
    ticket_priority = [2, 1, 0, 3]

    ticket_types = ['Bug', 'Feature', 'Task', 'Technical Debt']
    subtask_types = ['Completion blocker', 'Sub-Task']
    complexity_types = ['Trainee', 'Junior', 'Regular', 'Senior', 'Architect']
    dow = 1  # Day of the week
    last_release_day = 0

    probability_to_find_bug = dict(
        types={
            'Bug': 0.2,
            'Feature': 0.7,
            'Task': 0.05,
            'Technical Debt': 0.05,
            'Completion blocker': 0.2,
        },
        complexity={
            'Architect': 0.95,
            'Senior': 0.75,
            'Regular': 0.5,
            'Junior': 0.3,
            'Trainee': 0.1,
        },
        component={'CM': 0.9, 'UI': 0.6, 'ASE': 0.2},
    )

    develop_complexity_coefficient = {
        'Architect': 0.4,
        'Senior': 0.32,
        'Regular': 0.1,
        'Junior': 0.05,
        'Trainee': 0.01,
    }
    inter_arrival_time = 1  # Average time (days) between arrivals
    sim_duration = 30  # Duration of simulation (days)
    env = simpy.Environment()

    stat_backlog = dict(created=dict(total=int()), resolved=dict(total=int()))

    stat_dev = dict(free_time=int())  # hours

    # Probability that ticket in backlog already has correct list of components (%)
    backlog__ticket_correct_component = 0.8

    backlog__ticket_need_to_change_component = 0.12  # 60%
    backlog__ticket_need_to_add_component = 0.06  # 30%
    backlog__ticket_need_to_remove_component = 0.02  # 10%
