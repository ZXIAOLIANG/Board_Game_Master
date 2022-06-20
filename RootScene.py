class RootScene:
    def __init__(self):
        self.next_scene = self
    
    def HandleEvents(self, events):
        pass

    def Draw(self, screen):
        pass

    def ChangeNext(self, next_scene):
        self.next_scene = next_scene
    
    def Terminate(self):
        self.ChangeNext(None)