from random import shuffle


class ExamClass:
    """

    code_name different values : Amphi_1_G, Amphi_1_D, ISEL1_G, ISEL1_D, ISE2_G, ISE2_D,
                                 AS1_G, AS1_D, ISEL2_G, ISEL2_D, Amphi_2_G, Amphi_2_D.
    """

    def __init__(self, code_name: str, nrows: int, ncols: int):
        if code_name in ['Amphi_1_G', 'Amphi_1_D', 'ISEL1_G', 'ISEL1_D',
                         'ISE2_G', 'ISE2_D', 'AS1_G', 'AS1_D',
                         'ISEL2_G', 'ISEL2_D', 'Amphi_2_G', 'Amphi_2_D']:
            self.code_name = code_name
        else:
            raise "Nom de code de la classe d'examen invalide!"

        self.nrows = nrows
        self.ncols = ncols

        S = [(i, j) for i in range(nrows) for j in range(ncols)]
        Adj = []
        for p in S:
            Adj.append(self.ori_neighbors(p, nrows, ncols))
        self.graph = dict(S=S, A=Adj, places=[["" for j in range(ncols)] for i in range(nrows)])

    @staticmethod
    def ori_neighbors(place: tuple[int, int], n: int, m: int):
        i = place[0]
        j = place[1]
        neighborhood = []

        if (i > n) or (j > m):
            raise "Erreur des coordonnees!" \
                  "L'indiçage comme à partir de 0"

        if i == 0:
            if j < m - 1:
                neighborhood.append((i + 1, j))
                neighborhood.append((i, j + 1))
            else:
                neighborhood.append((i + 1, j))
        elif i == n - 1:
            if j < m - 1:
                neighborhood.append((i, j + 1))
            else:
                pass
        else:
            if j < m - 1:
                neighborhood.append((i + 1, j))
                neighborhood.append((i, j + 1))
            else:
                neighborhood.append((i + 1, j))
        return neighborhood

    @staticmethod
    def adj_ij(p: tuple[int, int], nrows: int, ncols: int):
        i = p[0]
        j = p[1]
        n = nrows
        m = ncols
        return i * m + j

    def depth_first_search(self):
        """
        color : White : -1
                Gray : 0
                Black : 1
        """
        dates = [0]
        color = dict()
        parent = dict()
        d = dict()
        f = dict()

        def visit_dsf(u):
            color[u] = 0
            dates.append(dates[-1] + 1)
            d[u] = dates[-1]
            for v in self.graph['A'][self.adj_ij(u, self.nrows, self.ncols)]:
                parent[v].append(u)
                if color[v] == -1:
                    visit_dsf(v)
            color[u] = 1
            dates.append(dates[-1] + 1)
            f[u] = dates[-1]

        for u in self.graph['S']:
            color[u] = -1
            parent[u] = []

        for u in self.graph['S']:
            if color[u] == -1:
                visit_dsf(u)

        return dict(parents=parent, f=f)

    def attributes_places(self, db: list[tuple[str, ...]]):
        dfs = self.depth_first_search()
        topo_order = sorted(dfs['f'], key=lambda i: dfs['f'][i], reverse=True)
        shuffle(db)
        for v in topo_order:
            if db:
                if not dfs['parents'][v]:
                    self.graph['places'][v[0]][v[1]] = db.pop()[1]
                else:
                    prev = [self.graph['places'][u[0]][u[1]][0] for u in dfs['parents'][v]]
                    x = 0
                    while db[-1][0] in prev and x < 5:
                        x += 1
                        shuffle(db)
                    self.graph['places'][v[0]][v[1]] = db.pop()[1]
                    print(x)

    def print_names(self, context: dict[str, str]):
        for i in range(self.nrows):
            for j in range(self.ncols):
                context[f"{self.code_name}_{i + 1}_{j + 1}"] = self.graph['places'][i][j]

