# 3-SAT → Threshold-two Fitting Hexasort

Category: Complexity open

## Source

A source instance is an explicitly encoded Boolean formula with at most three literals per clause. Its outputs are satisfying Boolean assignments, or NO-SOLUTION when the formula is unsatisfiable.

## Target

The target gives a graph and a sequence of colored stacks. Each move places the next stack on an empty vertex; if it has a same-color neighbor, the new stack and its same-color neighbors clear. The goal is to place every stack, not to clear the final board.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

This asks whether the lowest nontrivial clearing threshold already supports computational hardness.

## Difficulty

Every legal placement sequence must encode the source, despite clearing moves that can open unintended space.

## Literature context

The threshold-two fitting question asks whether all stacks can be placed, rather than whether the final board can be cleared.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [Hexasort — The Complexity of Stacking Colors on Graphs](https://arxiv.org/html/2603.01244v1): Klocker and Fink, Hexasort — The Complexity of Stacking Colors on Graphs, Section 1.2 and Lemma 2, supplies the rules and forced three-merge observation. Section 4 leaves Fitting complexity at constant threshold open. The FUN 2026 version retains that question. Existing numerical hardness uses a growing threshold; tractability when both threshold and color count are fixed allows unrestricted color counts here. Threshold two is a specific unresolved candidate within that broader question, not a separately stated conjecture in the paper.
- [FUN 2026 version](https://drops.dagstuhl.de/storage/00lipics/lipics-vol366-fun2026/html/LIPIcs.FUN.2026.26/LIPIcs.FUN.2026.26.html): Klocker and Fink, Hexasort — The Complexity of Stacking Colors on Graphs, Section 1.2 and Lemma 2, supplies the rules and forced three-merge observation. Section 4 leaves Fitting complexity at constant threshold open. The FUN 2026 version retains that question. Existing numerical hardness uses a growing threshold; tractability when both threshold and color count are fixed allows unrestricted color counts here. Threshold two is a specific unresolved candidate within that broader question, not a separately stated conjecture in the paper.

Fixed from board record `website/questions/threshold-two-fitting-hexasort.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
