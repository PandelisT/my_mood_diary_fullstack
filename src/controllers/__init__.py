from controllers.main import main
from controllers.auth import auth
from controllers.journal import journal
from controllers.psychologist import psychologist
from controllers.skills import skill
from controllers.problemareas import problem_area


registerable_controllers = [
    auth,
    main,
    journal,
    psychologist,
    skill,
    problem_area
]
