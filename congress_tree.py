import sys
import csv
import math

class Root:
    lchild = None
    rchild = None
    def __init__(self, split):
        self.split = split


def entropy(a, b):
    if a != 0 and b != 0:
        p = a/(a + b)
        return -(p * math.log(p) + (1 - p) * math.log(1 - p))
    return 0


def importance(attribute, examples):
    rep = 0
    dem = 0
    rep_y = 0
    rep_n = 0
    dem_y = 0
    dem_n = 0

    for row in examples:
        if row[-1] == 'Republican':
            rep += 1
            if row[attribute] == 'Yea':
                rep_y += 1
            else:
                rep_n += 1            
        else:
            dem += 1
            if row[attribute] == 'Yea':
                dem_y += 1
            else:
                dem_n += 1
           
    total = entropy(rep, dem)
    B_y = entropy(rep_y, dem_y)
    B_n = entropy(rep_n, dem_n)
    rem_y = (rep_y + dem_y)/(rep + dem) * B_y
    rem_n = (rep_n + dem_n)/(rep + dem) * B_n
    gain = total - rem_y - rem_n
    return gain


def plurality_value(examples):
    rep_c = 0
    dem_c = 0
    for row in examples:
        if row[-1] == 'Republican':
            rep_c += 1
        else:
            dem_c += 1
    if rep_c > dem_c:
        result = Root('Republican')
    else:
        result = Root('Democrat')
    return result

        
def same(examples):
    _c = examples[0][-1]
    for row in examples:
        if row[-1] != _c:
            return False
    return True


def decision_tree(examples, attributes, parent_examples, used, depth, level):
    if len(examples) == 0:
        return plurality_value(parent_examples)
    elif same(examples):
        return Root(examples[0][-1])
    elif len(attributes) == len(used):
        return plurality_value(examples)
    else:
        arg = []
        for each in range(len(attributes)):
            if attributes[each] not in used:
                arg.append(importance(each, examples))
        peak = arg.index(max(arg))
        root = Root(attributes[peak])
        used.append(attributes[peak])
        print('\t' * level + attributes[peak])
        level += 1
        if level == depth:
            return plurality_value(parent_examples)
        subtree_yea = []
        subtree_nay = []
        for row in examples:
            if row[peak] == 'Yea':
                subtree_yea.append(row)
            else:
                subtree_nay.append(row)
        root.lchild = decision_tree(subtree_yea, attributes, examples, used, depth, level)
        root.rchild = decision_tree(subtree_nay, attributes, examples, used, depth, level)
        return root


def accuracy(tree, test, attributes):
    count = 0
    root = tree
    for row in test:
        while root.lchild != None or root.rchild != None:
            _split = attributes.index(root.split)
            if row[_split] == "Yea":
                root = root.lchild
            else:
                root = root.rchild
        if row[-1] == root.split:
            count += 1
        root = tree
    return count/len(test)


def main():
    filename = sys.argv[1]
    depth = int(sys.argv[2])
    count = 0
    data = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for row in csv_reader:
            data.append(row)
    attributes = data[0]
    examples = data[1:-1]
    cut = int((len(data) - 1) / 5)
    data0 = data[1: cut]
    data1 = data[cut: 2 * cut]
    data2 = data[2 * cut: 3 * cut]
    data3 = data[3 * cut: 4 * cut]
    data4 = data[4 * cut: -1]
    train0 = data1 + data2 + data3 + data4
    train1 = data0 + data2 + data3 + data4
    train2 = data0 + data1 + data3 + data4
    train3 = data0 + data1 + data2 + data4
    train4 = data0 + data1 + data2 + data3

    tree = decision_tree(train0, attributes, [], [], depth, count)
    print("")
    estimate0 = accuracy(tree, data0, attributes)
    tree = decision_tree(train1, attributes, [], [], depth, count)
    print("")
    estimate1 = accuracy(tree, data1, attributes)
    tree = decision_tree(train2, attributes, [], [], depth, count)
    print("")
    estimate2 = accuracy(tree, data2, attributes)
    tree = decision_tree(train3, attributes, [], [], depth, count)
    print("")
    estimate3 = accuracy(tree, data3, attributes)
    tree = decision_tree(train4, attributes, [], [], depth, count)
    print("")
    estimate4 = accuracy(tree, data4, attributes)
    average = (estimate0 + estimate1 + estimate2 + estimate3 + estimate4) / 5
    estimate = str(round(estimate0, 2)) + " " + str(round(estimate1, 2)) + " " + str(round(estimate2, 2)) + " " + str(round(estimate3, 2)) + " " + str(round(estimate4, 2)) + " " + str(round(average, 2))
    print(estimate)
   
            
if __name__ == '__main__':
    main()
