class Model:
    """
    Class not used at the moment, need some brainstorming to know what to 
    do with it.
    """

    path_to_modelfolder = "./ressources/model/"

    def __init__(self, name: str) -> None:
        self.name = name

    def get_model_path(self):
        return self.path_to_modelfolder + self.name + ".pt"
