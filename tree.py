# adapted from:
# http://www.quesucede.com/page/show/id/python-3-tree-implementation#node-class


class Node(object):
    def __init__(self, name):
        self.__name = name
        self.__children = []
        self.__he = 0.0
        self.__filename = name + '.csv'

    @property
    def he(self):
        return self.__he

    @he.setter
    def he(self, he):
        self.__he = he

    @property
    def filename(self):
        return ''.join(self.__filename.split('.')[:-1])
    
    @filename.setter
    def filename(self, filename):
        self.__filename = filename + '.csv'

    @property
    def name(self):
        return self.__name

    @property
    def children(self):
        return self.__children

    def add_child(self, name):
        self.__children.append(name)


class Tree(object):
    def __init__(self):
        self.__nodes = dict()

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, name, he=None, filename=None, parent=None):
        node = Node(name)
        self[name] = node

        if he:
            node.he = he
        
        if filename:
            node.filename = filename
        
        if parent:
            self[parent].add_child(name)

        return node

    def add_raw(self, node, parent):
        self[node.name] = node
        self[parent].add_child(node.name)

        return node

    def display(self, name, depth=0):
        children = self[name].children
        print '-' * depth + '>', name, '(He: {:.5f}, Filename: {})'.format(self[name].he, self[name].filename)
        depth += 1
        for c in children:
            self.display(c, depth)

    def traverse(self, name):
        yield name
        queue = self[name].children

        while queue:
            yield queue[0]
            queue = self[queue[0]].children + queue[1:]  # DFS

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item
