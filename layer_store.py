from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.stack_adt import ArrayStack


class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass


class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self):
        super().__init__()
        self.layer = None
        self.in_special_mode = False

    def add(self, layer: Layer) -> bool:
        """
        Set the single layer.
        Returns true if the LayerStore was actually changed.
        """
        """"
        Complexity:O(1)
        """
        if self.layer != layer:
            self.layer = layer
            return True
        else:
            return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        """"
        Complexity:O(1)
        """
        if self.layer is not None:
            if self.in_special_mode:
                return invert.apply(self.layer.apply(start, timestamp, x, y))
            return self.layer.apply(start, timestamp, x, y)
        else:
            if self.in_special_mode:
                return invert.apply(start, timestamp, x, y)
            return start

    def erase(self, layer: Layer) -> bool:
        """
        Remove the single layer. Ignore what is currently selected.
        Returns true if the LayerStore was actually changed.
        """
        """"
        Complexity:O(1)
        """
        if self.layer == layer:
            self.layer = None
            return True
        else:
            return False

    def special(self):
        """
        invert the colour output.
        """
        """"
        Complexity:O(1)
        """
        self.in_special_mode = not self.in_special_mode


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self, capacity: int):
        self._capacity = capacity
        self._layers = ArrayStack(self._capacity)
        self._special_mode = False

    def add_layer(self, layer):
        """"
        Complexity:O(1)
        """
        if self._special_mode:
            self._layers.push(layer)
        else:
            self._layers.insert(0, layer)

    def erase(self):
        """"
        Complexity:O(1)
        """
        self._layers.pop()

    def activate_special_mode(self):
        """"
            The activate_special_mode method reverses the order of the layers in the store,
            making the oldest layer the newest layer and vice versa.
            This is done by popping all the layers off the stack,
            storing them in a temporary list, creating a new empty stack,
            and pushing the layers back onto the stack in reverse order.
        """
        """"
        Complexity:O(n) (where n is the number of layers in the store)
        """
        if not self._special_mode:
            temp = []
            while not self._layers.is_empty():
                temp.append(self._layers.pop())
            self._layers = ArrayStack(self._capacity)
            for layer in reversed(temp):
                self._layers.push(layer)
            self._special_mode = True

    def deactivate_special_mode(self):
        """"
        The deactivate_special_mode method undoes the special mode by reversing the order of the layers again.
        This is done in a similar way to activate_special_mode, by popping all the layers off the stack,
        storing them in a temporary list, creating a new empty stack,
        and pushing the layers back onto the stack in the original order.
        """
        """"
        Complexity:O(n) (where n is the number of layers in the store)
        """
        if self._special_mode:
            temp = []
            while not self._layers.is_empty():
                temp.append(self._layers.pop())
            self._layers = ArrayStack(self._capacity)
            for layer in temp:
                self._layers.push(layer)
            self._special_mode = False

    def get_color(self, color):
        """
        Returns the color obtained after applying all the layers in the store.
        """
        """"
        Complexity:O(n) (where n is the number of layers in the store)
        """
        result = color
        for layer in self._layers:
            if layer.is_applying():
                result = layer.apply(result)
        return result


class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self):
        """
        This is the constructor method for the SequenceLayerStore class.
        It initializes an empty list self.layers to keep track of the layers.
        """
        """
        Complexity:O(1)
        """
        self.layers = []

    def add(self, name):
        """
        This is the add method of the SequenceLayerStore class.
        It takes a name argument, creates a new Layer object with
        the given name and index equal to the current length of the self.layers list,
        adds the new layer to the list, and sets its applying attribute to True.
        """
        index = len(self.layers)
        layer = Layer(name, index)
        self.layers.append(layer)
        layer.applying = True

    def erase(self, name):
        """
        This is the erase method of the SequenceLayerStore class.
        It takes a name argument and iterates over the layers in self.layers.
        If a layer with the given name is found, its applying attribute is set to False
        """
        for layer in self.layers:
            if layer.name == name:
                layer.applying = False

    def get_layers(self):
        """
        This is the get_layers method of the SequenceLayerStore class.
        It returns a list of all the layers in self.layers whose applying attribute is True.
        """
        return sorted([layer for layer in self.layers if layer.applying], key=lambda layer: layer.index)

    def get_color(self):
        layers = self.get_layers()
        color = "white"
        for layer in layers:
            color = layer.apply(color)
        return color

    def special(self):
        """
        The special method of SequentialLayerStore removes the layer with the median name, lexicographically ordered,
        from all the currently "applying" layers. In the case of an even number of applying layers, it removes the
        lexicographically smaller of the two layers with median names. It does this by first getting all the
        currently "applying" layers using the get_layers method, and then sorting them based on their name. It then
        removes the layer with the median name using the same method as the previous explanation.
        """
        """"
        Complexity:O(n log n) (where n is the number of layer types in the store, due to sorting)
        """
        layers = sorted(self.get_layers(),
                        key=lambda layer: layer.name)  # The lambda keyword is used here to define a one-line anonymous
        # function that takes a layer object as input and returns its index attribute. This lambda function is passed
        # as the key argument to sorted,which will use the index attribute to sort the layers list
        count = len(layers)
        if count == 0:
            return
        elif count == 1:
            self.erase(layers[0].name)
        elif count % 2 == 1:
            median_name = layers[count // 2].name
            for layer in reversed(layers):
                if layer.name == median_name:
                    self.erase(layer.name)
                    break
        else:
            median_right = count // 2
            median_left = median_right - 1
            median_names = [layers[median_left].name, layers[median_right].name]
            smallest_median_name = min(median_names)
            for layer in reversed(layers):
                if layer.name in median_names:
                    if layer.name == smallest_median_name:
                        self.erase(layer.name)
                        break
