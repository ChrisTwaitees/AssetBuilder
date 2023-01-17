from model.build_step import build_step
from model.asset import asset


class NestedTestBuildStepTertiary(build_step.BuildStep):
    __step_name__ = "Nested Test Build Step Tertiary"
    __description__ = "Nested Tertiary Build Step from Another File."

    def __init__(self):
        super().__init__()

    def build(self, asset: asset.Asset) -> build_step.BuildStepResult:
        return build_step.BuildStepResult(message="Nested Third Build Step",
                                          success=True)


class NestedTestBuildStepFourth(build_step.BuildStep):
    __step_name__ = "Nested Fourth Test Build Step"
    __description__ = "Nested Fourth Build Step from Same file."

    def __init__(self):
        super().__init__()

    def build(self, asset: asset.Asset) -> build_step.BuildStepResult:
        return build_step.BuildStepResult(message="Nested Fourth Build Step",
                                          success=True)


