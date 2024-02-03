class MyLoadingBar:
    def __init__(self, progress: int, steps: int, progressPerStep: int = 1):
        self.progress = progress
        self.steps = steps
        self.progressPerStep = progressPerStep
    def __str__(self):
        bar = f"|{'#'*self.progress}{'.'*(self.steps-self.progress)}|"
        return bar
    def complete(self):
        self.progress = self.steps
    def incrementProgress(self):
        if self.progress < self.steps:
            remainingSteps = self.steps - self.progress
            if remainingSteps <= self.progressPerStep:
                MyLoadingBar.complete(self)
            else:
                self.progress += self.progressPerStep
