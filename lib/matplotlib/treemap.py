from abc import ABC, abstractmethod
import collections
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colorbar as colorbar
import math
import random


class BaseNode:
    """
    Abstract class to represent the base node of a tree map
    """
    def __init__(self, children):
        self._children = children
        self._size = 1

    @abstractmethod
    def add_single_child(self, child):
        """
        Add single child to current node
        :param child: child to add
        :return: None
        """
        pass

    @abstractmethod
    def add_multiple_children(self, children):
        """
        Add multiple children to current node.
        :param children: Children to add. Should be an iterable
        :return:
        """
        pass

    @abstractmethod
    def get_max_size(self):
        """
        Find leaf with greatest size
        :return: Greatest size
        """
        pass

    @abstractmethod
    def get_min_size(self):
        """
        Find leaf with least size
        :return: Least size
        """
        pass

    def get_children(self):
        return self._children

    def get_size(self):
        return self._size



class Tree(BaseNode):
    def __init__(self, children):
        super().__init__(children)
        self._size = 0
        for child in children:
            self._size += child.get_size()

    def add_single_child(self, child):
        self._children.append(child)
        self._size += child.get_size()

    def add_multiple_children(self, children):
        for child in children:
            self._children.append(child)
            self._size += child.get_size()

    def recalculate_size(self):
        self._size = 0
        for child in self._children:
            self._size += child.get_size()

    def get_max_size(self):
        max = 0
        for child in self._children:
            child_max = child.get_max_size()
            if child_max > max:
                max = child_max
        return max

    def get_min_size(self):
        min = math.inf
        for child in self._children:
            child_min = child.get_min_size()
            if child_min < min:
                min = child_min
        return min

    def __str__(self):
        tree_val = "("
        for i in range(0, len(self._children)):
            if i != 0:
                tree_val += ", "
            tree_val += self._children[i].__str__()
        tree_val += ")"
        return tree_val


class Leaf(BaseNode):
    def __init__(self, size, children=None, color=None):
        super().__init__(children)
        self._size = size
        self._color = color

    def add_single_child(self, child):
         self._children = child

    def add_multiple_children(self, children):
        self._children = ""
        for child in children:
            self._children += child

    def set_color(self, color):
        self._color = color

    def get_color(self):
        return self._color

    def get_max_size(self):
        return self._size

    def get_min_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    def __str__(self):
        return str(self._size)

class TreeMap:
    def __init__(self, node, cmap=None, ax=None):
        """
        Create a tree map instance
        :param node: Tree Node
        :param cmap: Color map if user wants tree map colors to be in a specific theme
        :param ax: Pre-existing axes if user doesn't want to add to existing axes
        """
        #Create a tree if user has entered an iterable
        if isinstance(node, collections.Iterable):
            self.tree = TreeMap.create_tree(node)
        else:
            self.tree = node

        #create new axes if one is not provided
        if ax is None:
            fig = plt.gcf()
            self.ax = fig.add_subplot(111, aspect="equal")
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        else:
            self.ax = ax

        #setup cmap if it is provided
        self.cmap = cmap
        self.norm = None
        self._setup_cmap()

    def set_cmap(self, cmap):
        self.cmap = cmap
        self._setup_cmap()

    def _setup_cmap(self):
        """
        Normalize cmap and create a color bar associated with it on a different axes
        :return: None
        """
        if not self.cmap is None:
            #use tree max and min sizes to normalize color
            mini = self.tree.get_min_size()
            maxi = self.tree.get_max_size()
            self.norm = colors.Normalize(vmin=mini, vmax=maxi)
            #create a color bar
            divider = make_axes_locatable(self.ax)
            cax = divider.append_axes("right", size="5%", pad=0.2)
            colorbar.ColorbarBase(cax, cmap=self.cmap, norm=self.norm, orientation="vertical")


    def get_ax(self):
        return self.ax

    def draw(self):
        """
        Draw TreeMap
        :return: None
        """
        self._draw_map(self.tree, [1, 1], [0, 0])

    @staticmethod
    def create_tree(data):
        """
        Create tree out of iterable
        :param data: iterable to create tree out of.
        :return: None
        """
        directory = Tree([])
        for item in data:
            if isinstance(item, Leaf):
                node = item
            else:
                node = TreeMap.create_tree(item)
            directory.add_single_child(node)
        return directory


    def _draw_map(self, node, size, location):
        if isinstance(node, Tree):
            total_size = max(node.get_size(), 1)
            for item in node.get_children():
                percent = item.get_size() / total_size
                item_area = (size[0] * size[1]) * percent
                if size[1] > size[0]:
                    width = size[0]
                    height = item_area/width
                    self._draw_rectangle(item, [width, height], location)
                    location[1] += height
                else:
                    height = size[1]
                    width = item_area/height
                    self._draw_rectangle(item, [width, height], location)
                    location[0] += width

    def _use_color(self, node):
        """
        Determine what color to use
        :param node: Node to apply color to
        :return: color
        """
        #use cmap, provided color or random color
        if not self.cmap is None:
            return self.cmap(self.norm(node.get_size()))

        if not node.get_color() is None:
            return node.get_color()

        return random.random(),random.random(),random.random()



    def _draw_rectangle(self, node, size, location):
        if isinstance(node, Leaf):
            #draw rectangle at coordinates
            width = size[0]
            height = size[1]
            x = location[0]
            y = location[1]
            use_color = self._use_color(node)
            r = Rectangle((x, y), width, height, label=node.get_size(), linewidth=2, edgecolor='k', facecolor=use_color)
            self.ax.add_patch(r)
            if not node.get_children() is None:
                self.ax.text(x + width / 2, y + height / 2, node.get_children(), va='bottom', ha='center')
        self._draw_map(node, size, location[:])
