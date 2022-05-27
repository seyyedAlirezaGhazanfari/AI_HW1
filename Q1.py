import math


class Heap:
    def __init__(self, n, s):
        self.pq = [(s, 0), ]
        self.index = [math.inf for i in range(n)]
        self.index[s] = 0

    @staticmethod
    def insert(heap: list, item: tuple):
        heap.append(item)
        start_pos = 0
        pos = len(heap) - 1
        new_item = heap[pos]
        while pos > start_pos:
            parent_pos = (pos - 1) >> 1
            parent = heap[parent_pos]
            if new_item < parent:
                heap[pos] = parent
                pos = parent_pos
                continue
            break
        heap[pos] = new_item

    @staticmethod
    def pop(heap: list):
        last_elt = heap.pop()
        if heap:
            return_item = heap[0]
            heap[0] = last_elt
            Heap._siftup(heap, 0)
            return return_item
        return last_elt

    @staticmethod
    def _siftup(heap, pos):
        endpos = len(heap)
        startpos = pos
        newitem = heap[pos]
        childpos = 2 * pos + 1  # leftmost child position
        while childpos < endpos:
            rightpos = childpos + 1
            if rightpos < endpos and not heap[childpos] < heap[rightpos]:
                childpos = rightpos
            heap[pos] = heap[childpos]
            pos = childpos
            childpos = 2 * pos + 1
        heap[pos] = newitem
        Heap._siftdown(heap, startpos, pos)

    @staticmethod
    def _siftdown(heap, startpos, pos):
        newitem = heap[pos]
        while pos > startpos:
            parentpos = (pos - 1) >> 1
            parent = heap[parentpos]
            if newitem < parent:
                heap[pos] = parent
                pos = parentpos
                continue
            break
        heap[pos] = newitem


class Search:
    @staticmethod
    def get_one_test():
        n, m = list(map(int, input().split(" ")))
        dists = [[] for i in range(n)]
        for i in range(m):
            u, v, d = list(map(int, input().split(" ")))
            dists[u - 1].append((v, d))
            dists[v - 1].append((u, d))
        t = int(input())
        a_s = list(map(int, input().split(" ")))
        c = int(input())
        b_s = list(map(int, input().split(" ")))
        s, g = list(map(int, input().split(" ")))
        return m, n, dists, t, a_s, c, b_s, s, g

    @staticmethod
    def get_thief_cost(s, dests, n, a_s, b_s):
        visited = [False] * n
        halfed = [False] * n
        parent_map = [-1] * n
        pq = []
        node_costs = [math.inf] * n
        node_costs[s - 1] = 0
        Heap.insert(pq, (0, s))
        while pq:
            _, node = Heap.pop(pq)
            for adj_node, weight in dests[node - 1]:
                coefficient = 1
                if not (visited[adj_node - 1]):
                    if adj_node in b_s:
                        coefficient = 1 / 2
                        halfed[adj_node - 1] = True
                    if Search.this_path_had_car(parent_map, halfed, node_costs, node) is not None and adj_node in b_s:
                        new_cost = Search.this_path_had_car(parent_map, halfed, node_costs, node) + weight / 2
                    else:
                        new_cost = (node_costs[node - 1] + weight) * coefficient
                    if node_costs[adj_node - 1] <= new_cost:
                        continue
                    parent_map[adj_node - 1] = node
                    node_costs[adj_node - 1] = new_cost
                    Heap.insert(pq, (new_cost, adj_node))
            visited[node - 1] = True
        thieves_min_cost = math.inf
        for thief in a_s:
            thieves_min_cost = min(node_costs[thief - 1], thieves_min_cost)
        return thieves_min_cost

    @staticmethod
    def this_path_had_car(parent_map, halfed, node_costs, node):
        target = node
        while target != -1:
            if halfed[target - 1]:
                return (node_costs[node - 1] - node_costs[target - 1]) / 2 + node_costs[target - 1]
            target = parent_map[target - 1]

        return None

    @staticmethod
    def get_source_cost(s, g, dests, n):
        visited = [False] * n
        parent_map = [-1] * n
        pq = list()
        node_costs = [math.inf] * n
        node_costs[s - 1] = 0
        Heap.insert(pq, (0, s))
        while pq:
            _, node = Heap.pop(pq)
            visited[node - 1] = True
            for adj_node, weight in dests[node - 1]:
                if not visited[adj_node - 1]:
                    new_cost = node_costs[node - 1] + weight
                    if node_costs[adj_node - 1] < new_cost:
                        continue
                    parent_map[adj_node - 1] = node
                    node_costs[adj_node - 1] = new_cost
                    Heap.insert(pq, (new_cost, adj_node))
        result_path = Search.get_path(s, g, parent_map)
        p = len(result_path)
        t = node_costs[g - 1]

        return t, p, result_path

    @staticmethod
    def get_path(s, g, parent_map):
        target = g
        path_list = [g, ]
        while target != -1:
            target = parent_map[target - 1]
            path_list.append(target)
            if target == s:
                break
        if target == -1:
            return []
        else:
            return path_list

    @staticmethod
    def process_test(n, dests, a_s, b_s, s, g):
        time, p, path = Search.get_source_cost(g, s, dests, n)
        thieves = Search.get_thief_cost(g, dests, n, a_s, b_s)
        if thieves < time:
            print("Poor Tintin")
        else:
            print(time)
            print(p)
            print(" ".join(list(map(str, path))))

    @staticmethod
    def get_tests():
        k = int(input())
        for i in range(k):
            m, n, dests, t, a_s, c, b_s, s, g = Search.get_one_test()
            Search.process_test(n, dests, a_s, b_s, s, g)


Search.get_tests()
