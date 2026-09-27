# Research instructions

Read the [fixed question](campaigns/threshold-two-fitting-hexasort/question.md), [prior state](campaigns/threshold-two-fitting-hexasort/state.md) and [preparation notes](campaigns/threshold-two-fitting-hexasort/work/preparation.md). The fixed [test corpus](campaigns/threshold-two-fitting-hexasort/work/cases.json) and [verifier](campaigns/threshold-two-fitting-hexasort/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/threshold-two-fitting-hexasort/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
