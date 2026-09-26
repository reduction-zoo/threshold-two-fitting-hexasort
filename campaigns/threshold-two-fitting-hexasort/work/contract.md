# Prepared contract

Source: `{"num_vars":n,"clauses":[[signed_literal,...],...]}` with at most three literals per clause. Output a satisfying Boolean `{"assignment":[...]}` or `{"status":"NO-SOLUTION"}`.

Target: `{"vertices":n,"edges":[[u,v],...],"stacks":[color,...]}` for a simple graph and a fixed sequence of nonnegative integer colors. A positive output `{"placements":[vertex,...]}` chooses an empty vertex for each stack in order. After placement, if at least one occupied neighbor has the new color, the new stack and every same-color neighbor clear simultaneously. Success means every stack was placed; the final board need not be empty. `NO-SOLUTION` is valid exactly if no complete sequence exists.

`algorithm.py` reads source JSON from stdin and emits legal target JSON. `algorithm.py --extract` reads `{"source":source,"target_solution":output}` and emits a valid source output. Both commands are deterministic, polynomial time, independent subprocesses. Errors exit nonzero; diagnostics go to stderr. Recovery must handle every valid target output.
