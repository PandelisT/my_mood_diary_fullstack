from controllers.main import main
from controllers.auth import auth
from controllers.journal import journal


registerable_controllers = [
    auth,
    main,
    journal
]