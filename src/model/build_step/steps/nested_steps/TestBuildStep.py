from model.build_step import build_step
from model.asset import asset


class NestedTestBuildStep(build_step.BuildStep):
    __step_name__ = "Nested Test Build Step Primary"
    __description__ = "Build Step used for testing."

    def __init__(self):
        super().__init__()

    def build(self, asset: asset.Asset) -> build_step.BuildStepResult:
        return build_step.BuildStepResult(message="Nested Fourth Build Step",
                                          success=True)


class NestedTestBuildStepSecondary(build_step.BuildStep):
    __step_name__ = "Nested Test Build Step Secondary - Same File"
    __description__ = "Build Step Secondary used for Testing."

    def __init__(self):
        super().__init__()

    def build(self, asset: asset.Asset) -> build_step.BuildStepResult:
        return build_step.BuildStepResult(message="Nested Fourth Build Step",
                                          success=True)


