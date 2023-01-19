from model.asset import asset
from model.build_step import build_step


class TestBuildStep(build_step.BuildStep):
    __step_name__ = "Test Build Step"
    __description__ = "This is a test Build Step"

    def __init__(self, asset_ref):
        """
        Here we initialize the data we'll need during the build step.
        BuildStepsTweakables will be editable by the user if desired.
        If data from the Asset is required, an AssetTweakable can be used with a getter.
        The getter will be resolved by the Builder.
        """
        # Set asset
        super(TestBuildStep, self).__init__(asset_ref)

        # Build Step Tweakables
        brands_temp = ["gucci", "prada", "dior"]
        self.brands = build_step.BuildStepListTweakable(name="Brand",
                                                        values=brands_temp,
                                                        value=brands_temp[0])
        self.marketplace_price = build_step.BuildStepTweakable(name="Purchase Price",
                                                               value=100)

        # Asset Settings
        self.tags = asset.AssetListTweakable(name="Tags",
                                             values=self.tags_getter())
        self.default_tx_path = asset.AssetTweakable(name="Default Texture",
                                                    value=self.default_texture_path_getter())

    def tags_getter(self):
        return ["hello", "who is this?"]

    def default_texture_path_getter(self):
        return self.asset.raw_path + ".psd"

    def build(self, asset):
        print("Tags : {}".format(self.tags.values))
        print("MarketPlace Sale Price : {}".format(self.marketplace_price.value))
        print("Default Texture Path : {}".format(self.default_tx_path.value))
        print("Brand : {}".format(self.brands.value))
        print("updating asset...")
        asset.source_path = "Edited by {}".format(self.__step_name__)

        return build_step.BuildStepResult(message="Test Build Step Message",
                                          success=False)


class ReportAssetStatusStep(build_step.BuildStep):
    __step_name__ = "Report Asset Status"
    __description__ = "This step reports the asset status during a build run"

    def __init__(self, asset_ref):
        """
        Here we initialize the data we'll need during the build step.
        BuildStepsTweakables will be editable by the user if desired.
        If data from the Asset is required, an AssetTweakable can be used with a getter.
        The getter will be resolved by the Builder.
        """
        # Set asset
        super(ReportAssetStatusStep, self).__init__(asset_ref=asset_ref)

    def build(self, asset):
        print("Arg asset :{}\n Local asset : {}".format(asset, self.asset))

        return build_step.BuildStepResult(message="Test Build Step Message",
                                          success=False)


class TestFBXStep(build_step.BuildStep):
    __step_name__ = "Test FBX Step"
    __description__ = "This step aims to only be ran on FBX files"

    def __init__(self, asset_ref):
        """
        Here we initialize the data we'll need during the build step.
        BuildStepsTweakables will be editable by the user if desired.
        If data from the Asset is required, an AssetTweakable can be used with a getter.
        The getter will be resolved by the Builder.
        """
        # Set asset
        super(TestFBXStep, self).__init__(asset_ref)

        # Asset Settings
        self.slot = asset.AssetTweakable(name="Slot",
                                         value="Top Under")
        self.re_import = asset.AssetTweakable(name="Force Re-import",
                                              value=False)

    def build(self, asset):
        print("Slot {}, reimport {}".format(self.slot, self.re_import))

        return build_step.BuildStepResult(message="Test Build Step Message",
                                          success=False)
