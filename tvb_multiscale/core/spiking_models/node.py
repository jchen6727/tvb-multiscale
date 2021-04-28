# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from tvb_multiscale.core.config import initialize_logger
from tvb_multiscale.core.utils.data_structures_utils import summarize, extract_integer_intervals

from tvb.basic.neotraits.api import HasTraits, Attr, Int


LOG = initialize_logger(__name__)


class SpikingNodeCollection(HasTraits):
    __metaclass__ = ABCMeta

    """SpikingNodeCollection is a class that 
       represents a nodes collection of the spiking network of the same neural model, 
       residing at the same brain region.
       The abstract methods have to be implemented by 
       spiking simulator specific classes that will inherit this class.
    """

    _nodes = None  # Class instance of a sequence of nodes, that depends on its spiking simulator

    label = Attr(field_type=str, default="", required=True,
                 label="Node label", doc="""Label of SpikingNodeCollection""")

    model = Attr(field_type=str, default="", required=True, label="Node model",
                 doc="""Label of model of SpikingNodeCollection's nodes""")

    brain_region = Attr(field_type=str, default="", required=True, label="Brain region",
                        doc="""Label of the brain region the SpikingNodeCollection resides""")

    _size = Int(field_type=int, default=0, required=True, label="Size",
                doc="""The number of elements of SpikingNodeCollection """)

    _weight_attr = ""
    _delay_attr = ""
    _receptor_attr = ""

    def __init__(self, nodes=None, **kwargs):
        """Constructor of a population class.
           Arguments:
            nodes: Class instance of a sequence of spiking network elements, 
                  that depends on each spiking simulator. Default=None.
            **kwargs that may contain:
                label: a string with the label of the node
                model: a string with the name of the model of the node
                brain_region: a string with the name of the brain_region where the node resides
        """
        self._nodes = nodes
        self.label = str(kwargs.get("label", self.__class__.__name__))
        self.model = str(kwargs.get("model", self.__class__.__name__))
        self.brain_region = str(kwargs.get("brain_region", ""))
        self._size = self.get_size()
        HasTraits.__init__(self)

    def __getitem__(self, keys):
        """Slice specific nodes (keys) of this SpikingNodeCollection.
           Argument:
            keys: sequence of target populations' keys.
           Returns:
            Sub-collection of SpikingNodeCollection nodes.
        """
        return self._nodes[keys]

    @property
    def node_collection(self):
        return self._nodes

    @property
    @abstractmethod
    def spiking_simulator_module(self):
        pass

    @abstractmethod
    def _assert_spiking_simulator(self):
        """Method to assert that the node of the network is valid"""
        pass

    @abstractmethod
    def _assert_nodes(self, nodes=None):
        """Method to assert that the node of the network is valid"""
        pass

    @property
    @abstractmethod
    def gids(self):
        """Method to get a sequence (list, tuple, array) of the individual gids of nodes's elements"""
        pass

    @property
    def nodes(self):
        return self._nodes

    def summarize_nodes_indices(self, print=False):
        """Method to summarize nodes' indices' intervals.
        Arguments:
         print: if True, a string is returned, Default = False
        Returns:
         a list of intervals' limits, or of single indices, or a string of the list if print = True"""
        return extract_integer_intervals(self.gids, print=print)

    def _print_nodes(self):
        return "%d neurons: %s" % (self.number_of_neurons, self.summarize_nodes_indices(print=True))

    def __repr__(self):
        return "%s - Label: %s \nmodel: %s\n%s" % \
               (self.__class__.__name__, self.label, self.model, self._print_nodes())

    def __str__(self):
        return "\n%s" \
               "\nparameters: %s," % \
                          (self.__repr__(), str(self.get_attributes(summary=True)))

    # Methods to get or set attributes for nodes and/or their connections:

    @abstractmethod
    def _Set(self, values_dict, nodes=None):
        """Method to set attributes of the SpikingNodeCollection's nodes.
        Arguments:
            values_dict: dictionary of attributes names' and values.
            nodes: instance of a nodes class,
                   or sequence (list, tuple, array) of nodes the attributes of which should be set.
                   Default = None, corresponds to all nodes.
        """
        pass

    @abstractmethod
    def _Get(self, attr=None, nodes=None):
        """Method to get attributes of the SpikingNodeCollection's nodes.
           Arguments:
            attrs: sequence (list, tuple, array) of the attributes to be included in the output.
                   Default = None, corresponding to all attributes
            nodes: instance of a nodes class,
                     or sequence (list, tuple, array) of nodes the attributes of which should be set.
                     Default = None, corresponds to all nodes.
           Returns:
            Dictionary of sequences (lists, tuples, or arrays) of nodes' attributes.
        """
        pass

    @abstractmethod
    def _GetConnections(self, nodes=None, source_or_target=None):
        """Method to get all the connections from/to a SpikingNodeCollection node.
           Arguments:
            nodes: instance of a nodes class,
                   or sequence (list, tuple, array) of nodes the attributes of which should be set.
                   Default = None, corresponds to all nodes.
            source_or_target: Direction of connections relative to nodes
                              "source", "target" or None (Default; corresponds to both source and target)
           Returns:
            connections' objects.
        """
        pass

    @abstractmethod
    def _SetToConnections(self, values_dict, connections=None):
        """Method to set attributes of the connections from/to the SpikingNodeCollection's nodes.
           Arguments:
             values_dict: dictionary of attributes names' and values.
             connections: connections' objects.
                          Default = None, corresponding to all connections to/from the present nodes.
        """
        pass

    @abstractmethod
    def _GetFromConnections(self, attr=None, connections=None):
        """Method to get attributes of the connections from/to the SpikingNodeCollection's nodes.
            Arguments:
             attrs: sequence (list, tuple, array) of the attributes to be included in the output.
                    Default = None, corresponding to all attributes
             connections: connections' objects.
                          Default = None, corresponding to all connections to/from the present nodes.
            Returns:
             Dictionary of sequences (lists, tuples, or arrays) of connections' attributes.

        """
        pass

    def get_size(self):
        """Method to compute the total number of SpikingNodeCollection's nodes.
            Returns:
                int: number of nodes.
        """
        if self._nodes:
            return len(self._nodes)
        else:
            return 0

    def Set(self, values_dict, nodes=None):
        """Method to set attributes of the SpikingNodeCollection's nodes.
        Arguments:
            values_dict: dictionary of attributes names' and values.
            nodes: instance of a nodes class,
                     or sequence (list, tuple, array) of nodes the attributes of which should be set.
                     Default = None, corresponds to all nodes.
        """
        self._Set(values_dict, nodes)

    def Get(self, attrs=None, nodes=None, summary=None):
        """Method to get attributes of the SpikingNodeCollection's nodes.
           Arguments:
            attrs: names of attributes to be returned. Default = None, corresponds to all nodes' attributes.
            nodes: instance of a nodes class,
                     or sequence (list, tuple, array) of nodes the attributes of which should be set.
                     Default = None, corresponds to all nodes.
            summary: if integer, return a summary of unique output values
                                 within accuracy of the specified number of decimal digits
                     otherwise, if it is not None or False return
                     either a dictionary of a statistical summary of mean, minmax, and variance for numerical attributes,
                     or a list of unique string entries for all other attributes,
                     Default = None, corresponds to returning all values
           Returns:
            Dictionary of sequences (lists, tuples, or arrays) of nodes' attributes.
        """
        attributes = self._Get(attrs, nodes)
        if summary:
            return summarize(attributes, summary)
        else:
            return attributes

    def get_attributes(self, nodes=None, summary=False):
        """Method to get all attributes of the SpikingNodeCollection's nodes.
           Arguments:
            nodes: instance of a nodes class,
                     or sequence (list, tuple, array) of nodes the attributes of which should be set.
                     Default = None, corresponds to all nodes.
            summary: if integer, return a summary of unique output values
                                 within accuracy of the specified number of decimal digits
                     otherwise, if it is not None or False return
                     either a dictionary of a statistical summary of mean, minmax, and variance for numerical attributes,
                     or a list of unique string entries for all other attributes,
                     Default = None, corresponds to returning all values
           Returns:
            Dictionary of sequences (lists, tuples, or arrays) of nodes' attributes.
        """
        return self.Get(nodes=nodes, summary=summary)

    def GetConnections(self, nodes=None,  source_or_target=None):
        """Method to get all connections of the device to/from nodes.
           Arguments:
            nodes: instance of a nodes class,
                     or sequence (list, tuple, array) of nodes the attributes of which should be set.
                     Default = None, corresponds to all nodes.
            Returns:
                connections' objects.
        """
        return self._GetConnections(nodes, source_or_target)

    def SetToConnections(self, values_dict, nodes=None, source_or_target=None):
        """Method to set attributes of the connections from/to the SpikingNodeCollection's nodes.
           Arguments:
            values_dict: dictionary of attributes names' and values.
            nodes: instance of a nodes class,
                     or sequence (list, tuple, array) of nodes the attributes of which should be set.
                     Default = None, corresponds to all nodes.
            source_or_target: Direction of connections relative to the populations' nodes
                              "source", "target" or None (Default; corresponds to both source and target)
        """
        if source_or_target is None:
            # In case we deal with both source and target connections, treat them separately:
            for source_or_target in ["source", "target"]:
                self.SetToConnections(values_dict, nodes, source_or_target)
        self._SetToConnections(values_dict, self.GetConnections(nodes, source_or_target))

    def GetFromConnections(self, attrs=None, nodes=None, source_or_target=None, summary=None):
        """Method to get attributes of the connections from/to the SpikingNodeCollection's nodes.
           Arguments:
            attrs: sequence (list, tuple, array) of the attributes to be included in the output.
                   Default = None, correspondingn to all attributes
            nodes: instance of a nodes class,
                     or sequence (list, tuple, array) of nodes the attributes of which should be set.
                     Default = None, corresponds to all nodes.
            source_or_target: Direction of connections relative to the populations' nodes
                              "source", "target" or None (Default; corresponds to both source and target)
            summary: if integer, return a summary of unique output values
                                 within accuracy of the specified number of decimal digits
                     otherwise, if it is not None or False return
                     either a dictionary of a statistical summary of mean, minmax, and variance for numerical attributes,
                     or a list of unique string entries for all other attributes,
                     Default = None, corresponds to returning all values
           Returns:
            Dictionary of lists of connections' attributes.
        """
        if source_or_target is None:
            # In case we deal with both source and target connections, treat them separately:
            output = []
            for source_or_target in ["source", "target"]:
                output.append(self.GetFromConnections(attrs, nodes, source_or_target, summary))
            return tuple(output)
        outputs = self._GetFromConnections(attrs, self.GetConnections(nodes, source_or_target))
        if summary is not None:
            outputs = summarize(outputs, summary)
        return outputs

    def get_weights(self, nodes=None, source_or_target=None, summary=None):
        """Method to get the connections' weights of the SpikingNodeCollections's nodes.
           Arguments:
            nodes: instance of a nodes class,
                     or sequence (list, tuple, array) of nodes the attributes of which should be set.
                     Default = None, corresponds to all nodes.
            source_or_target: Direction of connections relative to the populations' nodes
                              "source", "target" or None (Default; corresponds to both source and target)
            summary: if integer, return a summary of unique output values
                                 within accuracy of the specified number of decimal digits
                     otherwise, if it is not None or False return
                     either a dictionary of a statistical summary of mean, minmax, and variance for numerical attributes,
                     or a list of unique string entries for all other attributes,
                     Default = None, corresponds to returning all values
           Returns:
            Sequence (list, tuple, or array) of nodes's connections' weights.
        """
        if source_or_target is None:
            # In case we deal with both source and target connections, treat them separately:
            outputs = []
            for source_or_target in ["source", "target"]:
                outputs.append(self.get_weights(nodes, source_or_target, summary))
            return tuple(outputs)
        return self.GetFromConnections(self._weight_attr, nodes, source_or_target, summary).get(self._weight_attr, [])

    def get_delays(self, nodes=None, source_or_target=None, summary=None):
        """Method to get the connections' delays of the SpikingNodeCollections's nodes.
           Arguments:
            nodes: instance of a nodes class,
                     or sequence (list, tuple, array) of nodes the attributes of which should be set.
                     Default = None, corresponds to all nodes.
            source_or_target: Direction of connections relative to the populations' nodes
                              "source", "target" or None (Default; corresponds to both source and target)
            summary: if integer, return a summary of unique output values
                                 within accuracy of the specified number of decimal digits
                     otherwise, if it is not None or False return
                     either a dictionary of a statistical summary of mean, minmax, and variance for numerical attributes,
                     or a list of unique string entries for all other attributes,
                     Default = None, corresponds to returning all values
           Returns:
            Sequence (list, tuple, or array) of nodes's connections' delays.
        """
        if source_or_target is None:
            # In case we deal with both source and target connections, treat them separately:
            outputs = []
            for source_or_target in ["source", "target"]:
                outputs.append(self.get_delays(nodes, source_or_target, summary))
            return tuple(outputs)
        return self.GetFromConnections(self._delay_attr, nodes, source_or_target, summary).get(self._delay_attr, [])

    def get_receptors(self, nodes=None, source_or_target=None, summary=None):
        """Method to get the connections' receptors of the SpikingNodeCollections's nodes.
            nodes: instance of a nodes class,
                     or sequence (list, tuple, array) of nodes the attributes of which should be set.
                     Default = None, corresponds to all nodes.
            source_or_target: Direction of connections relative to the populations' nodes
                              "source", "target" or None (Default; corresponds to both source and target)
            summary: if integer, return a summary of unique output values
                                 within accuracy of the specified number of decimal digits
                     otherwise, if it is not None or False return
                     either a dictionary of a statistical summary of mean, minmax, and variance for numerical attributes,
                     or a list of unique string entries for all other attributes,
                     Default = None, corresponds to returning all values
           Returns:
            Sequence (list, tuple, or array) of nodes's connections' receptors.
        """
        if source_or_target is None:
            # In case we deal with both source and target connections, treat them separately:
            outputs = []
            for source_or_target in ["source", "target"]:
                outputs.append(self.get_receptors(nodes, source_or_target, summary))
            return tuple(outputs)
        return \
            self.GetFromConnections(self._receptor_attr, nodes, source_or_target, summary).get(self._receptor_str, [])

    @property
    def number_of_nodes(self):
        """Method to get the total number of SpikingNodeCollection's nodes and set the respective protected property.
            Returns:
             int: number of nodes.
        """
        if self._size == 0 or self._size is None:
            self._size = self.get_size()
        return self._size

    @property
    def attributes(self):
        """Method to get the attributes of the SpikingNodeCollection's nodes.
           Returns:
            Dictionary of sequences (lists, tuples, or arrays)  of nodes's nodes' attributes.
        """
        return self.get_attributes()

    @property
    def connections(self):
        """Method to get the connections of the SpikingNodeCollection's nodes.
           Returns:
            connections' objects.
        """
        return self.GetConnections()

    @property
    def weights(self):
        """Method to get the connections' weights' statistical summary of the SpikingNodeCollections's nodes.
           Returns:
            Dictionary of sequences (lists, tuples, or arrays) of nodes's connections' weights.
        """
        return self.get_weights()

    @property
    def delays(self):
        """Method to get the connections' delays of the SpikingNodeCollections's nodes.
           Returns:
            Dictionary of sequences (lists, tuples, or arrays) of nodes's connections' delays.
        """
        return self.get_delays()

    @property
    def receptors(self):
        """Method to get the connections' receptors of the SpikingNodeCollections's nodes.
           Returns:
            Dictionary of sequences (lists, tuples, or arrays) of nodes's connections' receptors.
        """
        return self.get_receptors()