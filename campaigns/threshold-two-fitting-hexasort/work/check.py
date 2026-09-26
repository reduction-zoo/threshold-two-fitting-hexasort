"""Independent 3-SAT and split-graph star-coloring oracles."""

import argparse
import json
import subprocess
import sys
from itertools import permutations, product
from pathlib import Path

import z3


def legal_source(source):
    if not isinstance(source, dict):
        return False
    n = source.get("num_vars")
    clauses = source.get("clauses")
    return (type(n) is int and n >= 0 and isinstance(clauses, list)
            and all(isinstance(clause, list) and len(clause) <= 3
                    and all(type(literal) is int and 1 <= abs(literal) <= n for literal in clause)
                    for clause in clauses))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal source formula")
    variables = [z3.Bool(f"x{i}") for i in range(source["num_vars"])]
    solver = z3.Solver()
    for clause in source["clauses"]:
        solver.add(z3.Or(*(variables[abs(literal) - 1] if literal > 0
                           else z3.Not(variables[-literal - 1]) for literal in clause)))
    result = solver.check()
    if result == z3.unsat:
        return {"status": "NO-SOLUTION"}
    if result != z3.sat:
        raise RuntimeError(f"Inconclusive source solver: {result}")
    model = solver.model()
    return {"assignment": [z3.is_true(model.eval(variable, model_completion=True)) for variable in variables]}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    assignment = output.get("assignment")
    if set(output) != {"assignment"} or not isinstance(assignment, list) or len(assignment) != source["num_vars"] or any(type(value) is not bool for value in assignment):
        return False
    return all(any(assignment[abs(literal) - 1] == (literal > 0) for literal in clause)
               for clause in source["clauses"])


def legal_target(target):
    if not isinstance(target,dict) or set(target) != {"vertices","edges","stacks"}:
        return False
    n,edges,stacks = target["vertices"],target["edges"],target["stacks"]
    return (type(n) is int and n >= 0 and isinstance(edges,list)
            and all(isinstance(edge,list) and len(edge) == 2
                    and all(type(v) is int and 0 <= v < n for v in edge)
                    and edge[0] < edge[1] for edge in edges)
            and len({tuple(edge) for edge in edges}) == len(edges)
            and isinstance(stacks,list)
            and all(type(color) is int and color >= 0 for color in stacks))


def neighbors(target):
    adjacent = [set() for _ in range(target["vertices"])]
    for u,v in target["edges"]:
        adjacent[u].add(v)
        adjacent[v].add(u)
    return adjacent


def move(board,vertex,color,adjacent):
    if type(vertex) is not int or not 0 <= vertex < len(board) or board[vertex] != -1:
        return None
    updated = list(board)
    matches = [v for v in adjacent[vertex] if board[v] == color]
    if matches:
        for v in matches+[vertex]:
            updated[v] = -1
    else:
        updated[vertex] = color
    return tuple(updated)


def direct_placements(target,placements):
    if (not isinstance(placements,list) or len(placements) != len(target["stacks"])):
        return False
    board = (-1,)*target["vertices"]
    adjacent = neighbors(target)
    for vertex,color in zip(placements,target["stacks"]):
        board = move(board,vertex,color,adjacent)
        if board is None:
            return False
    return True


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Illegal threshold-two fitting instance")
    adjacent = neighbors(target)
    outputs = []

    def search(index,board,placements):
        if len(outputs) >= limit:
            return
        if index == len(target["stacks"]):
            outputs.append({"placements":placements})
            return
        for vertex in range(target["vertices"]):
            new_board = move(board,vertex,target["stacks"][index],adjacent)
            if new_board is not None:
                search(index+1,new_board,placements+[vertex])

    search(0,(-1,)*target["vertices"],[])
    for answer in outputs:
        assert direct_placements(target,answer["placements"])
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return set(output) == {"placements"} and direct_placements(target,output["placements"])


def breadth_first_exists(target):
    adjacent = neighbors(target)
    states = {(-1,)*target["vertices"]}
    for color in target["stacks"]:
        states = {new for board in states for vertex in range(target["vertices"])
                  if (new := move(board,vertex,color,adjacent)) is not None}
    return bool(states)


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases
    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for n,clauses,answer in EDGE_CASES:
        assert ("assignment" in solve_source({"num_vars":n,"clauses":clauses})) == answer
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        exists = any(all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause)
                             for clause in source["clauses"])
                     for bits in product((False,True),repeat=source["num_vars"]))
        assert ("assignment" in current) == exists == ("assignment" in case["expected"])
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    import random
    yes,no = 0,0
    for seed in range(150):
        rng = random.Random(seed)
        n = rng.randint(1,5)
        edges = [[u,v] for u in range(n) for v in range(u+1,n) if rng.randrange(2)]
        stacks = [rng.randrange(3) for _ in range(rng.randint(0,8))]
        target = {"vertices":n,"edges":edges,"stacks":stacks}
        answer = solve_target(target)
        exists = breadth_first_exists(target)
        assert ("placements" in answer) == exists
        assert valid_target(target,answer)
        yes += exists
        no += not exists
    print(f"Self-test passed: {len(cases)} source formulas and {yes} YES/{no} NO target sequences")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal target: {target}")
        for output in target_solutions(target):
            assert valid_target(target,output)
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
