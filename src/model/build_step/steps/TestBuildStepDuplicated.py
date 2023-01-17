from model.build_step import build_step
from model.asset import asset


class TestBuildStepTertiary(build_step.BuildStep):
    __step_name__ = "Test Build Step Tertiary"
    __description__ = "Tertiary Build Step from Another File."

    def __init__(self):
        super().__init__()

    def build(self, asset: asset.Asset) -> build_step.BuildStepResult:
        return build_step.BuildStepResult(message="Third Build Step",
                                          success=True)


class TestBuildStepFourth(build_step.BuildStep):
    __step_name__ = "Fourth Test Build Step HELLO"
    __description__ = "Fourth Build Step from Same file."

    def __init__(self):
        super().__init__()

    def build(self, asset: asset.Asset) -> build_step.BuildStepResult:
        return build_step.BuildStepResult(message="Fourth Build Step",
                                          success=True)
