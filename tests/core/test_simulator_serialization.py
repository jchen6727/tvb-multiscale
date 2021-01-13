# -*- coding: utf-8 -*-

import os
import dill

import numpy as np

from tvb.basic.profile import TvbProfile
TvbProfile.set_profile(TvbProfile.LIBRARY_PROFILE)

from tvb.simulator.models.wilson_cowan_constraint import WilsonCowan
from tvb.simulator.models.reduced_wong_wang_exc_io import ReducedWongWangExcIO
from tvb.simulator.models.reduced_wong_wang_exc_io_inh_i import ReducedWongWangExcIOInhI

from tvb_multiscale.core.config import CONFIGURED
from tvb_multiscale.core.tvb.simulator_builder import SimulatorBuilder
from tvb_multiscale.core.tvb.simulator_serialization import \
    serialize_tvb_simulator, dump_serial_tvb_simulator, load_serial_tvb_simulator


def test_simulator_serialization(test_models=[WilsonCowan, ReducedWongWangExcIO, ReducedWongWangExcIOInhI]):
    for test_model in test_models:
        simulator_builder = SimulatorBuilder()
        simulator_builder.connectivity = CONFIGURED.DEFAULT_CONNECTIVITY_ZIP
        simulator_builder.model = test_model
        simulator = simulator_builder.build()
        serial_sim = serialize_tvb_simulator(simulator)
        filepath = os.path.join(CONFIGURED.out.FOLDER_RES, serial_sim["model"]+".dil")
        dump_serial_tvb_simulator(filepath)
        serial_sim2 = load_serial_tvb_simulator()
        for key, val in serial_sim.items():
            assert np.all(serial_sim2[key] == val)







