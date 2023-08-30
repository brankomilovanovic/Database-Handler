from handlers.rel.Workspace.RelDBWorkspaceHandler import RelDBWorkspaceHandler


class MySqlWorkspaceHandler(RelDBWorkspaceHandler):

    def __init__(self):
        super().__init__()