'''
class Node:
    def __init__(self, prefix):
        """
        Creates a Node with the given string prefix.
        The root node will be given prefix ''.
        You will need to track:
        - the prefix
        - whether this prefix is also a complete word
        - child nodes
        """
        # pass
        self._prefix = prefix
        self._is_word = False
        self.children = {}

    def get_prefix(self):
        """
        Returns the string prefix for this node.
        """
        # pass
        return self._prefix

    def get_children(self):
        """
        Returns a list of child Node objects, in any order.
        """
        # pass
        return [self.children[child] for child in self.children]

    def is_word(self):
        """
        Returns True if this node prefix is also a complete word.
        """
        # pass
        return self._is_word

    def add_word(self, word):
        """
        Adds the complete word into the trie, causing child nodes to be created as needed.
        We will only call this method on the root node, e.g.
        >>> root = Node('')
        >>> root.add_word('cheese')
        """
        # pass
        pointer = len(self._prefix)
        if word[:pointer+1] not in self.children:
            self.children[word[:pointer+1]] = Node(word[:pointer+1])
        if len(word) == pointer+1:
            self.children[word[:pointer+1]]._is_word = True
            return
        else:
            self.children[word[:pointer+1]].add_word(word)

    def find(self, prefix):
        """
        Returns the node that matches the given prefix, or None if not found.
        We will only call this method on the root node, e.g.
        >>> root = Node('')
        >>> node = root.find('te')
        """
        # pass
        pointer = len(self._prefix)
        if prefix == prefix[:pointer+1]:
            # if the child is the word, return the child??
            try:
                return self.children[prefix]
            except KeyError:  # if there is no prefix node
                return None
        if prefix[:pointer+1] not in self.children:
            return None  # if the child is not in the dict, return None
        else:
            # run find on the next child
            return self.children[prefix[:pointer+1]].find(prefix)

    def words(self):
        """
        Returns a list of complete words that start with my prefix.
        The list should be in lexicographical order.
        """
        # pass
        output = []
        if self.is_word():
            # if I am a word, append myself to the output
            output.append(self._prefix)
        if len(self.get_children()) == 0:
            return output  # return the list of words if there are no more children
            # (when it reaches the bottom of recursion)
        for child in self.children:
            output += self.children[child].words()  # otherwise, recurse
            # (add the words of each of the children to the output)

        return sorted(output)

with open("data/web2.txt") as f:
    words = f.read().split()
    root = Node('')
    for word in words:
        root.add_word(word)
    print(root.find('friend').words())
'''


class Node:
    def __init__(self, prefix):
        """
        Creates a Node with the given string prefix.
        The root node will be given prefix ''.
        You will need to track:
        - the prefix
        - whether this prefix is also a complete word
        - child nodes
        """
        # pass
        self._prefix = prefix
        self._is_word = False
        self.occurences = 0
        self.children = {}

    def get_prefix(self):
        """
        Returns the string prefix for this node.
        """
        # pass
        return self._prefix

    def get_children(self):
        """
        Returns a list of child Node objects, in any order.
        """
        # pass
        return [self.children[child] for child in self.children]

    def is_word(self):
        """
        Returns True if this node prefix is also a complete word.
        """
        # pass
        return self._is_word

    def add_word(self, word):
        """
        Adds the complete word into the trie, causing child nodes to be created as needed.
        We will only call this method on the root node, e.g.
        >>> root = Node('')
        >>> root.add_word('cheese')
        """
        # pass
        pointer = len(self._prefix)
        if word[:pointer+1] not in self.children:
            self.children[word[:pointer+1]] = Node(word[:pointer+1])
        if len(word) == pointer+1:
            self.children[word[:pointer+1]]._is_word = True
            self.children[word[:pointer+1]].occurences += 1
            return
        else:
            self.children[word[:pointer+1]].add_word(word)

    def find(self, prefix):
        """
        Returns the node that matches the given prefix, or None if not found.
        We will only call this method on the root node, e.g.
        >>> root = Node('')
        >>> node = root.find('te')
        """
        # pass
        pointer = len(self._prefix)
        if prefix == prefix[:pointer+1]:
            # if the child is the word, return the child??
            try:
                return self.children[prefix]
            except KeyError:  # if there is no prefix node
                return None
        if prefix[:pointer+1] not in self.children:
            return None  # if the child is not in the dict, return None
        else:
            # run find on the next child
            return self.children[prefix[:pointer+1]].find(prefix)

    def words(self):
        """
        Returns a list of complete words that start with my prefix.
        The list should be in lexicographical order.
        """
        # pass
        output = []
        if self.is_word():
            # if I am a word, append myself to the output
            output.append((self._prefix, self.occurences))
        if len(self.get_children()) == 0:
            return output  # return the list of words if there are no more children
            # (when it reaches the bottom of recursion)
        for child in self.children:
            output += self.children[child].words()  # otherwise, recurse
            # (add the words of each of the children to the output)

        # https://stackoverflow.com/questions/50885410/python-sort-dictionary-by-descending-values-and-then-by-keys-alphabetically
        return sorted(output, key=lambda x: (-x[1], x[0]))

        # other solutions that didn't work as expected
        # return [x[0] for x in sorted(output, key=lambda x: x(x[1], x[0]), reverse=True)]
        # return sorted(output, key=lambda x: (x[1], x[0]), reverse=True) # will sort in descending order but break ties in reverse alphabetical
        # return sorted(output, key=lambda x: x[1], reverse=True)
        # print(f"output: {output}")
        # return sorted(output)


with open("data/words_test.txt") as f:
    words = f.read().split()
    root = Node('')
    for word in words:
        root.add_word(word)
        words = [word.lower() for word in words]
    # print(root.find('t').words())
    print(root.words())
    print(root.words()[0][1])

    predictions = root.find("t").words()
    predictions = [x[0] for x in predictions]
    print(predictions)
