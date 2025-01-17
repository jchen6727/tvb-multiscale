# -*- coding: utf-8 -*-

from abc import ABCMeta, ABC

from tvb_multiscale.core.interfaces.models.wilson_cowan import WilsonCowanTVBSpikeNetInterfaceBuilder, \
    WilsonCowanSpikeNetRemoteInterfaceBuilder, WilsonCowanSpikeNetTransformerInterfaceBuilder, \
    WilsonCowanSpikeNetOutputTransformerInterfaceBuilder, WilsonCowanSpikeNetInputTransformerInterfaceBuilder, \
    WilsonCowanSpikeNetInterfaceBuilder, WilsonCowanSpikeNetProxyNodesBuilder

from tvb_multiscale.tvb_nest.interfaces.builders import NESTProxyNodesBuilder, NESTInterfaceBuilder, \
    NESTRemoteInterfaceBuilder, TVBNESTInterfaceBuilder, \
    NESTTransformerInterfaceBuilder, NESTOutputTransformerInterfaceBuilder, NESTInputTransformerInterfaceBuilder

from tvb_multiscale.tvb_nest.nest_models.builders.nest_templates import receptor_by_source_region


class WilsonCowanNESTProxyNodesBuilder(NESTProxyNodesBuilder, WilsonCowanSpikeNetProxyNodesBuilder, ABC):
    __metaclass__ = ABCMeta

    pass


class WilsonCowanNESTInterfaceBuilder(WilsonCowanNESTProxyNodesBuilder, NESTInterfaceBuilder,
                                      WilsonCowanSpikeNetInterfaceBuilder):
    pass


class WilsonCowanNESTRemoteInterfaceBuilder(WilsonCowanNESTInterfaceBuilder, NESTRemoteInterfaceBuilder,
                                            WilsonCowanSpikeNetRemoteInterfaceBuilder):

    def default_output_config(self):
        WilsonCowanSpikeNetRemoteInterfaceBuilder.default_output_config(self)

    def default_input_config(self):
        WilsonCowanSpikeNetRemoteInterfaceBuilder.default_input_config(self)


class WilsonCowanNESNetOutputTransformerInterfaceBuilder(WilsonCowanNESTInterfaceBuilder,
                                                         NESTOutputTransformerInterfaceBuilder,
                                                         WilsonCowanSpikeNetOutputTransformerInterfaceBuilder):

    def default_output_config(self):
        WilsonCowanSpikeNetOutputTransformerInterfaceBuilder.default_output_config(self)

    def default_input_config(self):
        WilsonCowanSpikeNetOutputTransformerInterfaceBuilder.default_input_config(self)


class WilsonCowanNESTInputTransformerInterfaceBuilder(WilsonCowanNESTInterfaceBuilder,
                                                      NESTInputTransformerInterfaceBuilder,
                                                      WilsonCowanSpikeNetInputTransformerInterfaceBuilder):

    def default_output_config(self):
        WilsonCowanSpikeNetInputTransformerInterfaceBuilder.default_output_config(self)

    def default_input_config(self):
        WilsonCowanSpikeNetInputTransformerInterfaceBuilder.default_input_config(self)


class WilsonCowanNESTTransformerInterfaceBuilder(WilsonCowanNESTInterfaceBuilder, NESTTransformerInterfaceBuilder,
                                                 WilsonCowanSpikeNetTransformerInterfaceBuilder):

    def default_output_config(self):
        WilsonCowanSpikeNetTransformerInterfaceBuilder.default_output_config(self)

    def default_input_config(self):
        WilsonCowanSpikeNetTransformerInterfaceBuilder.default_input_config(self)


class WilsonCowanTVBNESTInterfaceBuilder(WilsonCowanNESTProxyNodesBuilder, TVBNESTInterfaceBuilder,
                                         WilsonCowanTVBSpikeNetInterfaceBuilder):

    def default_output_config(self):
        WilsonCowanTVBSpikeNetInterfaceBuilder.default_output_config(self)

    def default_input_config(self):
        WilsonCowanTVBSpikeNetInterfaceBuilder.default_input_config(self)


class WilsonCowanMultisynapseNESTProxyNodesBuilder(WilsonCowanNESTProxyNodesBuilder, ABC):
    __metaclass__ = ABCMeta

    def _default_receptor_type(self, source_node, target_node):
        return receptor_by_source_region(source_node, target_node, start=3)


class WilsonCowanMultisynapseNESTInterfaceBuilder(WilsonCowanMultisynapseNESTProxyNodesBuilder,
                                                  WilsonCowanNESTInterfaceBuilder):

    pass


class WilsonCowanMultisynapseNESTRemoteInterfaceBuilder(WilsonCowanMultisynapseNESTInterfaceBuilder,
                                                        NESTRemoteInterfaceBuilder,
                                                        WilsonCowanSpikeNetRemoteInterfaceBuilder):

    def default_output_config(self):
        WilsonCowanSpikeNetRemoteInterfaceBuilder.default_output_config(self)

    def default_input_config(self):
        WilsonCowanSpikeNetRemoteInterfaceBuilder.default_input_config(self)


class WilsonCowanMultisynapseNESTOutputTransformerInterfaceBuilder(
    WilsonCowanMultisynapseNESTInterfaceBuilder, NESTOutputTransformerInterfaceBuilder,
    WilsonCowanSpikeNetOutputTransformerInterfaceBuilder):

    def default_output_config(self):
        WilsonCowanSpikeNetOutputTransformerInterfaceBuilder.default_output_config(self)

    def default_input_config(self):
        WilsonCowanSpikeNetOutputTransformerInterfaceBuilder.default_input_config(self)


class WilsonCowanMultisynapseNESTInputTransformerInterfaceBuilder(WilsonCowanMultisynapseNESTInterfaceBuilder,
                                                                  NESTInputTransformerInterfaceBuilder,
                                                                  WilsonCowanSpikeNetInputTransformerInterfaceBuilder):

    def default_output_config(self):
        WilsonCowanSpikeNetInputTransformerInterfaceBuilder.default_output_config(self)

    def default_input_config(self):
        WilsonCowanSpikeNetInputTransformerInterfaceBuilder.default_input_config(self)


class WilsonCowanMultisynapseNESTTransformerInterfaceBuilder(WilsonCowanMultisynapseNESTInterfaceBuilder,
                                                             NESTTransformerInterfaceBuilder,
                                                             WilsonCowanSpikeNetTransformerInterfaceBuilder):

    def default_output_config(self):
        WilsonCowanSpikeNetTransformerInterfaceBuilder.default_output_config(self)

    def default_input_config(self):
        WilsonCowanSpikeNetTransformerInterfaceBuilder.default_input_config(self)


class WilsonCowanMultisynapseTVBNESTInterfaceBuilder(WilsonCowanMultisynapseNESTProxyNodesBuilder,
                                                     TVBNESTInterfaceBuilder,
                                                     WilsonCowanTVBSpikeNetInterfaceBuilder):

    def default_output_config(self):
        WilsonCowanTVBSpikeNetInterfaceBuilder.default_output_config(self)

    def default_input_config(self):
        WilsonCowanTVBSpikeNetInterfaceBuilder.default_input_config(self)
