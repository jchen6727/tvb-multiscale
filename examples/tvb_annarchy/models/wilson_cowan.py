# -*- coding: utf-8 -*-

from examples.tvb_annarchy.example import main_example
from examples.models.wilson_cowan import wilson_cowan_example as wilson_cowan_example_base

from tvb_multiscale.tvb_annarchy.annarchy_models.models.wilson_cowan import WilsonCowanBuilder
from tvb_multiscale.tvb_annarchy.interfaces.models.builders.wilson_cowan \
    import WilsonCowanBuilder as WilsonCowanTVBANNarchyInterfaceBuilder


def wilson_cowan_example(**kwargs):
    return main_example(wilson_cowan_example_base, WilsonCowanBuilder, WilsonCowanTVBANNarchyInterfaceBuilder,
                        **kwargs)


if __name__ == "__main__":
    wilson_cowan_example()