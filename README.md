# It-Workflow-Simulation
**The simple solution to emulate your kanban flow and provide any process experiments into the simulation model**

### Opportunities
 - Simulating `Jira`, `Kaiten`, `Asana` and some other kanban boards by using isolated environment
 - Providing any experiments into the simulation mode, including adding new column on the board, adding new team member to the project and etc...

### Key modules

`entities` - all entities that you have on the project. For an example you can have board, tasks, subtasks, risks and etc (are subjects)

`roles` - all roles on the your project. It can be QA, Developer, Product Owner, Supervisors, Backlog groomers, Team Lead and etc (are objects)

`model_parameters` - the place where you need to setup some incoming parameters to the model. 
For an example - app components, ticket types and etc.

`model_run` - the main entrypoint for the application. In this place you should initialize all objects (e.g. board, team members, time range for the simulation model) 

#### How to use
1. *Optional*: Update model parameters according to requirements (module model_parameters)
2. *Required*: Run model by typing `python model_run.py`

#### Requirements
1. Python 3.6+

#### How to install
1. `pip install -r requirements.txt`

