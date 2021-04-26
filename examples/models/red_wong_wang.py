# -*- coding: utf-8 -*-

import numpy as np

from tvb_multiscale.core.tvb.cosimulator.models.reduced_wong_wang_exc_io import ReducedWongWangExcIO
from tvb_multiscale.core.tvb.cosimulator.models.reduced_wong_wang_exc_io_inh_i import ReducedWongWangExcIOInhI

from examples.example import main_example


def red_wong_wang_excio_example(spikeNet_model_builder, tvb_spikeNet_model_builder, **kwargs):

    spiking_proxy_inds = kwargs.pop("spiking_proxy_inds", [0, 1])
    populations_order = kwargs.pop("populations_order", 100)

    model_params = kwargs.pop("model_params", {})

    return main_example(ReducedWongWangExcIO, model_params,
                        spikeNet_model_builder, spiking_proxy_inds, populations_order,
                        tvb_spikeNet_model_builder,
                        **kwargs)


def red_wong_wang_excio_inhi_example(spikeNet_model_builder, tvb_spikeNet_model_builder, **kwargs):

    spiking_proxy_inds = kwargs.pop("spiking_proxy_inds", [0, 1])
    populations_order = kwargs.pop("populations_order", 100)

    model_params = kwargs.pop("model_params", {})

    return main_example(ReducedWongWangExcIOInhI, model_params,
                        spikeNet_model_builder, spiking_proxy_inds, populations_order,
                        tvb_spikeNet_model_builder,
                        **kwargs)