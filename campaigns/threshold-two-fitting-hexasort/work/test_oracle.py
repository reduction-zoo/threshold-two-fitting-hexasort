from check import legal_target,solve_target,valid_target


def test_hand_cases():
    one = {"vertices":1,"edges":[],"stacks":[0]}
    assert valid_target(one,{"placements":[0]})
    assert solve_target({**one,"stacks":[0,1]}) == {"status":"NO-SOLUTION"}
    edge = {"vertices":2,"edges":[[0,1]],"stacks":[0,0,1]}
    assert valid_target(edge,{"placements":[0,1,0]})
    assert not valid_target(edge,{"placements":[0,0,1]})
    assert not legal_target({"vertices":2,"edges":[[1,0]],"stacks":[0]})


if __name__ == "__main__":
    test_hand_cases()
