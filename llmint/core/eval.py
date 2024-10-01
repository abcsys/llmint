class pcolors:
    RIGHT = '\033[92m'
    WRONG = '\033[91m'
    MISSING = '\033[33m'
    ENDC = '\033[0m'


def accuracy(output: list, test_example: list):
    correct = False
    correctIdxs = []
    numCorrect = 0
    total = 0
    
    print("Generated Mappings:", flush=True)
    for gen_mapping in output:
        for i in range(len(test_example)):
            mapping = list(gen_mapping.values())[0][0]
            reasoning = list(gen_mapping.values())[0][1]
            if mapping == str(test_example[i]).replace("'", ""):
                print(pcolors.RIGHT + mapping + pcolors.ENDC + '\n', reasoning, flush=True)
                numCorrect += 1
                correctIdxs.append(i)
                correct = True
        if not correct:
            print(pcolors.WRONG + mapping + pcolors.ENDC + '\n', reasoning, flush=True)
        correct = False
        total += 1
        
    print("Ground Truth Mappings:", flush=True)
    for i in range(len(test_example)):
        if i in correctIdxs:
            print(pcolors.RIGHT + str(test_example[i]).replace("'", "") + pcolors.ENDC,
                  flush=True)
        else:
            print(pcolors.MISSING + str(test_example[i]).replace("'", "") + pcolors.ENDC,
                  flush=True)

    precision = len(correctIdxs) / len(output)
    recall = len(correctIdxs) / len(test_example)
    if precision + recall > 0:
        f1 = 2 * ((precision * recall) / (precision + recall))
    else:
        f1 = 0
    return precision, recall, f1

def print_mappings(mappings: dict, include_reasoning=True):
    for name, response in mappings.items():
        mapping, reasoning = response
        if include_reasoning:

            print(pcolors.RIGHT + mapping + pcolors.ENDC + '\n',
                  reasoning, flush=True)
        else:
            print(pcolors.RIGHT + mapping + pcolors.ENDC,
                  flush=True)
