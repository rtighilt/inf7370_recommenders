import os
from anytree import Node, Resolver, RenderTree, find, ChildResolverError, LevelOrderGroupIter
from anytree.exporter import DotExporter
from anytree.util import commonancestors
from FileReader import FileReader
from collections import defaultdict
import pickle


class ProductsWorker(FileReader):

    tree = Node("Products")
    nodes = defaultdict()

    def __init__(self, filepath, shape):
        super().__init__(filepath, shape)
        self.build_tree()
        if os.path.exists(r'nodes/products'):
            print("Loading nodes from cache")
            self.nodes = self.load_products_nodes()
        else:
            print("Nodes aren't present in cache, building in process")
            for product in self.data.iterrows():
                self.nodes[product[1]["PRODUCT_ID"]] = self.find_node(product[1]["PRODUCT_ID"])
            self.save_products_nodes()

    @staticmethod
    def get_path_for_index_at_row(row, index):
        # Builds the breadcrumb for a specific entry to a specific level
        return "/Products/" + "/".join(row[:index])

    def find_node(self, product_id):
        return find(self.tree, lambda n: n.name == product_id)

    def get_node(self, product_id):
        return self.nodes.get(product_id)

    @staticmethod
    def get_common_ancestors(p1, p2):
        return commonancestors(p1, p2)

    def to_png(self, path):
        print("Rendering graph, this may take a while...")
        DotExporter(self.tree).to_picture(path)
        return self

    def get_tree(self):
        return self.tree

    def save_tree(self, num_rows):
        file = open(r'trees/' + str(num_rows), 'wb')
        pickle.dump(self.tree, file)
        file.close()

    def load_tree(self, num_rows):
        file = open(r'trees/' + str(num_rows), 'rb')
        self.tree = pickle.load(file)
        file.close()
        return self

    def build_tree(self):
        print("Building product tree for " + str(len(self.data)) + " products")
        if os.path.exists('trees/' + str(self.num_rows)):
            return self.load_tree(self.num_rows)
        """
            Constructing the tree structure with unique data from each column,
            the hierarchy goes like :
                - Products
                    |- Department
                    |- Commodity-Desc
                    |- SubCommodity-Desc
                    |- Size of the product
                    |- Brand name
                    |- Product ID
        """
        r = Resolver('name')
        for row in self.data.iterrows():
            row = row[1]
            for index, node_name in enumerate(row):
                if index == 0:
                    # The first index will be attached to the root node
                    try:
                        # If we find the child, we do nothing
                        r.get(self.tree, node_name)
                    except ChildResolverError:
                        # If we don't (that raises an exception), we add the child to the root
                        Node(node_name, self.tree)
                else:
                    parent = r.get(self.tree, self.get_path_for_index_at_row(row, index))
                    Node(node_name, parent=parent)
        self.save_tree(self.num_rows)
        return self

    def get_neighbors(self, product, level=0):
        if isinstance(product, str):
            product = self.get_node(product)

        print("Getting neighbors of " + product.name)
        """ Getting parents for a specific product at a specific level, level 0 is the leafs of the tree (ie. The products themselves) """
        parent = product
        for i in range(0, level):
            # Getting the right parent
            parent = parent.parent
        # Returning the corresponding children at specific level similarity ([-1] is fo getting only product IDs)
        return [[node.name for node in children] for children in LevelOrderGroupIter(parent)][-1]

    def save_products_nodes(self):
        file = open(r'nodes/products', 'wb')
        pickle.dump(self.nodes, file)
        file.close()

    @staticmethod
    def load_products_nodes():
        file = open(r'nodes/products', 'rb')
        nodes = pickle.load(file)
        file.close()
        return nodes

