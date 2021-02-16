from controllers.main import main
from controllers.auth import auth
from controllers.journal import journal
from controllers.psychologist import psychologist


registerable_controllers = [
    auth,
    main,
    journal,
    psychologist
]