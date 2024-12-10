- Creation of sequence without for_identity -> CreateSeqStmt
- Usage of USING in join expression -> JoinExpr usingClause
- Usage of numbers in order by and group by - SelectStmt
- Usage of numbers in order by and group by - OrderByExpr

- naming boolean columns
- replace in view and trigger
- tests for line number, offset

-- move constants to constants.py
-- rewrite print_violations so that it can be called on violations from anywhere
-- e.g main, we don't need checker, every violation carries the violated rule
-- change paths to sources and path to source
