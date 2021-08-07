import sys

class Solver:
    df = 1.0
    min = False
    tol = 0.001
    iter = 50
    fileName = ''
    matrix = {}
    reward = {}
    probEntry = {}
    nodes = set()
    singleDestination = []
    chance = set()
    decision = set()
    
    def __init__(self, filename, df, min, tol, iter):
        with open(filename) as f:
            content = f.readlines()
            for line in content:
                if line[0] != '#' and line != "\n":
                    if ':' in line:
                        line = line.strip()
                        lis = line.split(":")
                        self.nodes.add(lis[0].strip())
                        later = lis[1].strip()
                        later = later[1:-1]
                        # print(later)
                        nextState = later.split(',')
                        nextS = [each.strip() for each in nextState]
                        self.matrix[lis[0].strip()] = nextS
                        for each in nextS:
                            self.nodes.add(each)
                        if len(nextS) == 1:
                            self.singleDestination.append(lis[0].strip())
                    elif '=' in line:
                        lis = line.split('=')
                        self.nodes.add(lis[0].strip())
                        val = float(lis[1].strip())
                        self.reward[lis[0].strip()] = val
                    elif '%' in line:
                        lis = line.split('%')
                        self.nodes.add(lis[0].strip())
                        later = lis[1].strip().split(' ')
                        problist = []
                        for each in later:
                            problist.append(float(each))
                        self.probEntry[lis[0].strip()] = problist
        self.df = df
        self.min = min
        self.tol = tol
        self.iter = iter
        for each in self.nodes:
            if each not in self.reward:
                self.reward[each] = 0.0
            # such node has edges but no probability entry
            if each in self.matrix and len(self.matrix[each]) > 1 and ((each in self.probEntry and len(self.probEntry[each]) == 1) or (each not in self.probEntry)):
                self.decision.add(each)
            elif each in self.probEntry and len(self.probEntry[each]) >= 1:
                self.chance.add(each)
            

    def solver(self):
        # print(self.reward)
        policy = {}
        for key in self.matrix:
            if key in self.decision:
                policy[key] = self.matrix[key][0]
        # print(policy)
        va = {}
        p = {}
        while True:
            i = 0
            va = self.value_iteration(policy)
            # print(va)
            p = self.policy_iteration(va)
            # print(p)
            for each in p:
                if p[each] == policy[each]:
                    i += 1
            if i == len(policy):
                break
            policy = p
        for each in p:
            print(each, '->', p[each],'')
        for each in va:
            print(each, '=', va[each], '')

    def policy_iteration(self, values):
        newp = {}
        if self.min == False:
            for current in values:
                if current in self.decision:
                    best_path = ''
                    maxvalue = 0.0
                    prob = 1.0
                    alpha = 0.0
                    if current in self.probEntry:
                        prob = self.probEntry[current][0]
                        alpha = (1 - prob) / (len(self.matrix[current]) -1)
                    
                    for child in self.matrix[current]:
                        temp = 0.0
                        val = self.reward[current]
                        for other in self.matrix[current]:
                            if child == other:
                                temp += prob * values[other]
                            else:
                                temp += alpha * values[other]
                        val += self.df * temp
                        if val > maxvalue:
                            maxvalue = val
                            best_path = child
                    # print('the best path of', current,'is', best_path)
                    newp[current] = best_path
        else:
            for current in values:
                if current in self.decision:
                    best_path = ''
                    minvalue = sys.float_info.max
                    prob = 1.0
                    alpha = 0.0
                    if current in self.probEntry:
                        prob = self.probEntry[current][0]
                        alpha = (1-prob) / (len(self.matrix[current]) -1)
                    for child in self.matrix[current]:
                        temp = 0.0
                        val = self.reward[current]
                        for other in self.matrix[current]:
                            if child == other:
                                temp += prob * values[other]
                            else:
                                temp += alpha * values[other]
                        val += self.df * temp
                        if val < minvalue:
                            minvalue = val
                            best_path = child
                    newp[current] = best_path
        return newp
            
    def value_iteration(self, policy):
        it = 0
        max_diff = sys.float_info.max
        val_temp = {}
        values = {}
        for each in self.reward:
            values[each] = self.reward[each]
        while it < self.iter and max_diff > self.tol:
            for current in self.nodes:
                val = self.reward[current]
                temp = 0.0
                if current in self.decision:
                    prob = 1.0
                    alpha = 0.0
                    if current in self.probEntry:
                        prob = self.probEntry[current][0]
                        alpha = (1 - prob) / (len(self.matrix[current]) -1)
                    # print(prob, 'prob for', current)
                    move = policy[current]
                    for child in self.matrix[current]:
                        if move == child:
                            temp += prob * values[child]
                        else:
                            temp += alpha * values[child]

                elif current in self.chance:
                    for i in range(0, len(self.matrix[current])):
                        prob = self.probEntry[current][i]
                        node = self.matrix[current][i]
                        temp += prob * values[node]
                elif current in self.singleDestination:
                    node = self.matrix[current][0]
                    temp += values[node]

                val += self.df * temp
                val_temp[current] = val
            diff = 0.0
            for key in val_temp:
                if abs(val_temp[key] - values[key]) > diff:
                    diff = abs(val_temp[key] - values[key])
            max_diff = diff
            it += 1
            for node in val_temp:
                values[node] = val_temp[node]
            # print("iter", it,"values", values)
        return values



if __name__ == "__main__":
    df = 1.0
    min = False
    tol = 0.001
    iter = 50
    fileName = ""
    if "-df" in sys.argv:
        i = sys.argv.index("-df")
        df = float(sys.argv[i+1])
    if "-min" in sys.argv:
        min = True
    if "-tol" in sys.argv:
        i = sys.argv.index("-tol")
        tol = float(sys.argv[i+1])
    if "-iter" in sys.argv:
        i = sys.argv.index("-iter")
        iter = int(sys.argv[i+1])
    for each in sys.argv:
        if each[len(each)-3: len(each)] == "txt":
            fileName = each
            # print(fileName)
    mdp = Solver(fileName, df, min, tol, iter)
    mdp.solver()
    