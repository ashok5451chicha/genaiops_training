# Missing pieces (search the code for "TODO (missing piece")

| Id | Where | What to write | Status |
|---|---|---|---|
| M1 | vector_math.py: dot() | multiply matching numbers and add them up | Done |
| M2 | vector_math.py: normalize() | scale a vector to length 1; zero vector raises ValueError | Done |
| M3 | kyc_pipeline.py: mask_id() | keep the prefix and the last 3 characters; mask the rest; short numbers fully masked | Done (a number of length ≤ 3 is fully masked) |
| M4 | kyc_pipeline.py: write_csv() | create the folder, write header and rows | Done |
| M5 | run_pipeline.py: main() | classify, find duplicates, evaluate, print two tables, write the three output files | Done, plus a raw-ID privacy guard |
| M6 | tests/test_pipeline.py | write the missing pipeline tests | Done (30 tests) |
