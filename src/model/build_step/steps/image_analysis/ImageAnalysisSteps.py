from model.build_step import build_step
from model.asset import asset


class ImageAnalysis(build_step.BuildStep):
    __step_name__ = "Image Analysis"
    __description__ = "A Variety of image analysis options."

    def __init__(self, asset_ref):
        super().__init__(asset_ref=asset_ref)

    def build(self, asset: asset.Asset) -> build_step.BuildStepResult:
        return build_step.BuildStepResult(message="Nested Fourth Build Step",
                                          success=True)