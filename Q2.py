import math
import heapq


class Node:
    def __init__(self, to_be_added_tile, position, m, n, used_tiles: dict,
                 free_positions: list):
        self.used_tiles = used_tiles.copy()
        self.free_positions = free_positions.copy()
        self.add_tile(m, n, to_be_added_tile, position)
        self.g = math.inf
        self.h = math.inf
        self.f = math.inf

    def __lt__(self, other):
        if self.f < other.f:
            return True
        else:
            return False

    def add_tile(self, m, n, tile, position):
        used_tiles = self.used_tiles
        if tile is None:
            return
        used_tiles[position] = tile
        self.add_new_free_positions(position, m, n, tile)
        self.delete_from_free_positions(position)

    def add_new_free_positions(self, position, m, n, tile: tuple):
        i, j = position
        full_positions = list(self.used_tiles.keys())
        u, r, d, l = tile
        if (i - 1, j) not in full_positions and i != 0:
            self.free_positions.append(((i - 1, j), (l, 'R')))
        if (i, j - 1) not in full_positions and j != 0:
            self.free_positions.append(((i, j - 1), (d, 'U')))
        if (i, j + 1) not in full_positions and j != m - 1:
            self.free_positions.append(((i, j + 1), (u, 'D')))
        if (i + 1, j) not in full_positions and i != n - 1:
            self.free_positions.append(((i + 1, j), (r, 'L')))

    def delete_from_free_positions(self, position):
        for free_position, condition in self.free_positions:
            if free_position == position:
                self.free_positions.remove((free_position, condition))

    def get_adjacent_nodes(self, is_start: bool, m, n, tiles: list):
        result_nodes = list()
        result_edge_values = list()
        if is_start:
            first_tile = tiles[0]
            for i in range(n):
                for j in range(m):
                    node = Node(first_tile, (i, j), m, n, dict(), list())
                    result_nodes.append(node)
                    result_edge_values.append(0)
        else:
            for tile in set(tiles).difference(set(self.used_tiles.values())):
                u, r, d, l = tile
                for position, condition in self.free_positions:
                    free_value, free_side = condition
                    if (free_side == 'L' and free_value == l) or (free_side == 'R' and free_value == r) or (
                            free_side == 'D' and free_value == d) or (free_side == 'U' and free_value == u):
                        if position in list(self.used_tiles.keys()):
                            continue
                        node = Node(tile, position, m, n, self.used_tiles,
                                    self.free_positions)
                        result_nodes.append(node)
                        result_edge_values.append(free_value)
        return result_nodes, result_edge_values

    def is_this_goal(self, m, n):
        if len(self.used_tiles) != m * n:
            return False
        return True

    def get_f(self):
        return self.g + self.h

    def get_h(self, tiles: list):
        min_cost = 0
        for u, r, d, l in set(tiles).difference(set(self.used_tiles.values())):
            min_cost += min(u, r, d, l)
        return min_cost


class Search:

    @staticmethod
    def get_start_node(tiles, m, n):
        node = Node(None, None, m, n, dict(), [])
        node.g = 0
        node.h = node.get_h(tiles)
        node.f = node.get_f()
        return node

    @staticmethod
    def compare(child: Node, heap: list):
        for i in range(len(heap)):
            _, node = heap[i]
            if node.used_tiles == child.used_tiles and child.g >= node.g:
                return True
            elif node.used_tiles == child.used_tiles:
                heap[i] = heap[-1]
                heap.pop()
                heapq.heapify(heap)
                heapq.heappush(heap, (child.f, child))
                del node
                return True
        return False

    @staticmethod
    def a_star(tiles, m, n):
        closed_list = list()
        open_list = list()
        heapq.heappush(open_list, (0, Search.get_start_node(tiles=tiles, m=m, n=n)))
        is_start = True
        while open_list:
            _, current_node = heapq.heappop(open_list)
            closed_list.append(current_node.used_tiles)
            if current_node.is_this_goal(m, n):
                return current_node.g
            children, edges = current_node.get_adjacent_nodes(is_start=is_start, m=m, n=n, tiles=tiles)
            is_start = False
            if not children:
                continue
            for child, edge in zip(children, edges):
                if child.used_tiles in closed_list:
                    continue
                child.g = current_node.g + edge
                child.h = child.get_h(tiles)
                child.f = child.get_f()
                if Search.compare(child, open_list):
                    continue
                heapq.heappush(open_list, (child.f, child))

    @classmethod
    def get_input(cls):
        tiles = list()
        m, n = list(map(int, input().split(" ")))
        for i in range(n * m):
            u, r, d, l = list(map(int, input().split(" ")))
            tiles.append((u, r, d, l))
        return tiles, m, n

    @classmethod
    def process(cls):
        tiles, m, n = Search.get_input()
        result = Search.a_star(tiles, m, n)
        print(result)


Search.process()
