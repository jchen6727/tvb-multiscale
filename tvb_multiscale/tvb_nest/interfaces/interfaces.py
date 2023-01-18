# -*- coding: utf-8 -*-

from abc import ABCMeta

from tvb.basic.neotraits.api import HasTraits, Attr, List

from tvb_multiscale.core.interfaces.tvb.interfaces import \
    TVBtoSpikeNetInterface, SpikeNetToTVBInterface, TVBOutputInterfaces, TVBInputInterfaces, TVBtoSpikeNetModels, \
    SpikeNetToTVBModels
from tvb_multiscale.core.interfaces.spikeNet.interfaces import \
    SpikeNetOutputInterface, SpikeNetInputInterface, \
    SpikeNetOutputRemoteInterfaces, SpikeNetInputRemoteInterfaces,\
    SpikeNetSenderInterface, SpikeNetReceiverInterface, \
    SpikeNetTransformerSenderInterface, SpikeNetReceiverTransformerInterface

from tvb_multiscale.tvb_nest.interfaces.io import \
    NESTInputDeviceSet, NESTOutputDeviceSet
from tvb_multiscale.tvb_nest.nest_models.network import NESTNetwork


TVBtoNESTModels = TVBtoSpikeNetModels
NESTtoTVBModels = SpikeNetToTVBModels


class NESTInterface(HasTraits):
    __metaclass__ = ABCMeta

    """NESTInterface base class for interfaces sending/receiving data from/to NEST."""

    spiking_network = None
    # spiking_network = Attr(label="NEST Network",
    #                        doc="""The instance of NESTNetwork class""",
    #                        field_type=NESTNetwork,
    #                        required=True)

    def __init__(self, spiking_network=None, **kwargs):
        if spiking_network:
            self.spiking_network = spiking_network
        super().__init__(**kwargs)

    @property
    def nest_network(self):
        return self.spiking_network

    @property
    def nest_instance(self):
        return self.spiking_network.nest_instance


class NESTOutputInterface(SpikeNetOutputInterface, NESTInterface):

    """NESTOutputInterface base class for interfaces sending data from NEST."""

    proxy = Attr(label="Proxy",
                 doc="""An instance of NESTOutputDeviceSet implementing a proxy node 
                        sending outputs from the NEST network to the co-simulator""",
                 field_type=NESTOutputDeviceSet,
                 required=True)

    def __init__(self, spiking_network=None, **kwargs):
        if spiking_network:
            self.spiking_network = spiking_network
        super().__init__(**kwargs)

    @property
    def _time(self):
        return self.nest_instance.GetKernelStatus("biological_time")

    @property
    def _time(self):
        return self.nest_instance.GetKernelStatus("biological_time")

    @property
    def proxy_gids(self):
        return self._get_proxy_gids(self.proxy.source)


class NESTSenderInterface(SpikeNetSenderInterface, NESTOutputInterface):

    """NESTSenderInterface"""

    def __init__(self, spiking_network=None, **kwargs):
        if spiking_network:
            self.spiking_network = spiking_network
        super().__init__(**kwargs)

    def __call__(self):
        return self.send(NESTOutputInterface.get_proxy_data(self))


class NESTTransformerSenderInterface(SpikeNetTransformerSenderInterface, NESTOutputInterface):
    """NESTTransformerSenderInterface"""

    def __init__(self, spiking_network=None, **kwargs):
        if spiking_network:
            self.spiking_network = spiking_network
        super().__init__(**kwargs)

    def __call__(self):
        return self.transform_send(NESTOutputInterface.get_proxy_data(self))


class NESTInputInterface(NESTInterface, SpikeNetInputInterface):

    """NESTInputInterface base class for interfaces receiving data to NEST."""

    proxy = Attr(label="Proxy",
                 doc="""An instance of NESTInputDeviceSet implementing a proxy node 
                        receiving inputs from the co-simulator as an input to the NEST network""",
                 field_type=NESTInputDeviceSet,
                 required=True)

    def __init__(self, spiking_network=None, **kwargs):
        if spiking_network:
            self.spiking_network = spiking_network
        super().__init__(**kwargs)

    @property
    def proxy_gids(self):
        return self._get_proxy_gids(self.proxy.target)


class NESTReceiverInterface(SpikeNetReceiverInterface, NESTInputInterface):
    """NESTReceiverInterface"""

    def __init__(self, spiking_network=None, **kwargs):
        if spiking_network:
            self.spiking_network = spiking_network
        super().__init__(**kwargs)


class NESTReceiverTransformerInterface(SpikeNetReceiverTransformerInterface, NESTInputInterface):
    """NESTReceiverTransformerInterface"""

    def __init__(self, spiking_network=None, **kwargs):
        if spiking_network:
            self.spiking_network = spiking_network
        super().__init__(**kwargs)


class TVBtoNESTInterface(TVBtoSpikeNetInterface, NESTInputInterface):

    """TVBtoNESTInterface class to get data from TVB, transform them,
       and finally set them to NEST, all processes taking place in shared memmory.
    """

    def __init__(self, spiking_network=None, **kwargs):
        if spiking_network:
            self.spiking_network = spiking_network
        super().__init__(**kwargs)


class NESTtoTVBInterface(SpikeNetToTVBInterface, NESTOutputInterface):

    """NESTtoTVBInterface class to get data from NEST, transform them,
       and finally set them to TVB, all processes taking place in shared memmory.
    """

    def __init__(self, spiking_network=None, **kwargs):
        if spiking_network:
            self.spiking_network = spiking_network
        super().__init__(**kwargs)

    def get_proxy_data(self):
        return NESTOutputInterface.get_proxy_data(self)


class NESTInterfaces(HasTraits):

    """NESTInterfaces class holding a list of NESTInterface instances"""

    interfaces = List(of=NESTInterface)

    @property
    def proxy_gids(self):
        return self._loop_get_from_interfaces("proxy_gids")

    @property
    def number_of_proxy_gids(self):
        return self.proxy_gids.shape[0]

    @property
    def nest_network(self):
        if len(self.interfaces):
            return self.interfaces[0].spiking_network
        else:
            return None

    @property
    def nest_instance(self):
        if len(self.interfaces):
            return self.interfaces[0].nest_instance
        else:
            return None


class NESTOutputInterfaces(SpikeNetOutputRemoteInterfaces, NESTInterfaces):

    """NESTOutputInterfaces holding a list of NESTOutputInterface instances"""

    pass


class NESTInputInterfaces(SpikeNetInputRemoteInterfaces, NESTInterfaces):

    """NESTInputInterfaces holding a list of NESTInputInterface instances"""

    pass


class TVBtoNESTInterfaces(TVBOutputInterfaces, NESTInputInterfaces):

    """TVBtoNESTInterfaces class holding a list of TVBtoNESTInterface instances"""

    pass


class NESTtoTVBInterfaces(TVBInputInterfaces, NESTOutputInterfaces):
    """NESTtoTVBInterfaces class holding a list of NESTtoTVBInterface instances"""

    pass
