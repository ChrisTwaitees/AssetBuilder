from model.build_step import build_step
from model.asset import asset


class TestBuildStep(build_step.BuildStep):
    __step_name__ = "Test Build Step Primary"
    __description__ = "Build Step used for testing."

    def __init__(self, asset):
        super(TestBuildStep, self).__init__(asset_ref=asset)


    def build(self, asset):
        return build_step.BuildStepResult(message="Fourth Build Step",
                                          success=True)


class TestBuildStepSecondary(build_step.BuildStep):
    __step_name__ = "Test Build Step Secondary - Same File"
    __description__ = "Build Step Secondary used for Testing."

    def __init__(self):
        super(TestBuildStepSecondary, self).__init__(asset_ref=asset)

    def build(self, asset):
        return build_step.BuildStepResult(message="Fourth Build Step",
                                          success=True)
