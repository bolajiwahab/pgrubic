# Rules

There are **100+** rules and all rules are enabled by default. Rule are divided into 7 categories:

1. **constraint**: Rules for constraints
2. **general**: Rules for best practice
3. **naming**: Rules for naming
4. **schema**: Rules for schema
5. **security**: Rules for security
6. **typing**: Rules for typing
7. **unsafe**: Rules for unsafe migrations

## constraint (CT)

|   Code  |                      Name                                                        |      Stable        | Auto fix |
| --------| ---------------------------------------------------------------------------------|------------------- |--------------------|
| CT001 | [cascade-update](rules/constraint/cascade-update.md)                               | :white_check_mark: | :white_check_mark: |
| CT002 | [cascade-delete](rules/constraint/cascade-delete.md)                               | :white_check_mark: | :white_check_mark: |
| CT003 | [identity-generated-by-default](rules/constraint/identity-generated-by-default.md) | :white_check_mark: | :white_check_mark: |
| CT004 | [remove-constraint](rules/constraint/remove-constraint.md)                         | :white_check_mark: | :x:                |

## general (GN)

|   Code  |                      Name                                                       |      Stable        | Auto fix |
| --------| --------------------------------------------------------------------------------|------------------- |--------------------|
| GN001 | [table-inheritance](rules/general/table-inheritance.md)                           | :white_check_mark: | :x:                |
| GN002 | [create-rule](rules/general/create-rule.md)                                       | :white_check_mark: | :x:                |
| GN003 | [sql-ascii-encoding](rules/general/sql-ascii-encoding.md)                         | :white_check_mark: | :white_check_mark: |
| GN004 | [missing-primary-key](rules/general/missing-primary-key.md)                       | :white_check_mark: | :x:                |
| GN005 | [index-elements-more-than-three](rules/general/index-elements-more-than-three.md) | :white_check_mark: | :x:                |
| GN006 | [create-enum](rules/general/create-enum.md)                                       | :white_check_mark: | :x:                |
| GN007 | [missing-replace-in-function](rules/general/missing-replace-in-function.md)       | :white_check_mark: | :white_check_mark: |
| GN008 | [missing-replace-in-procedure](rules/general/missing-replace-in-procedure.md)     | :white_check_mark: | :white_check_mark: |
| GN009 | [duplicate-column](rules/general/duplicate-column.md)                             | :white_check_mark: | :x:                |
| GN010 | [table-column-conflict](rules/general/table-column-conflict.md)                   | :white_check_mark: | :x:                |
| GN011 | [missing-required-column](rules/general/missing-required-column.md)               | :white_check_mark: | :white_check_mark: |
| GN012 | [required-column-removal](rules/general/required-column-removal.md)               | :white_check_mark: | :x:                |
| GN013 | [nullable-required-column](rules/general/nullable-required-column.md)             | :white_check_mark: | :white_check_mark: |
| GN014 | [select-into](rules/general/select-into.md)                                       | :white_check_mark: | :white_check_mark: |
| GN015 | [drop-cascade](rules/general/drop-cascade.md)                                     | :white_check_mark: | :white_check_mark: |
| GN016 | [constant-generated-column](rules/general/constant-generated-column.md)           | :white_check_mark: | :x:                |
| GN017 | [id-column](rules/general/id-column.md)                                           | :white_check_mark: | :white_check_mark: |
| GN018 | [multi-column-partitioning](rules/general/multi-column-partitioning.md)           | :white_check_mark: | :x:                |
| GN019 | [unlogged-table](rules/general/unlogged-table.md)                                 | :white_check_mark: | :white_check_mark: |
| GN020 | [current-time](rules/general/current-time.md)                                     | :white_check_mark: | :white_check_mark: |
| GN021 | [null-constraint](rules/general/null-constraint.md)                               | :white_check_mark: | :white_check_mark: |
| GN022 | [update-without-where-clause](rules/general/update-without-where-clause.md)       | :white_check_mark: | :x:                |
| GN023 | [delete-without-where-clause](rules/general/delete-without-where-clause.md)       | :white_check_mark: | :x:                |
| GN024 | [null-comparison](rules/general/null-comparison.md)                               | :white_check_mark: | :white_check_mark: |
| GN025 | [duplicate-index](rules/general/duplicate-index.md)                               | :white_check_mark: | :x:                |
| GN026 | [not-in](rules/general/not-in.md)                                                 | :white_check_mark: | :x:                |
| GN027 | [yoda-condition](rules/general/yoda-condition.md)                                 | :white_check_mark: | :white_check_mark: |
| GN028 | [asterisk](rules/general/asterisk.md)                                             | :white_check_mark: | :x:                |
| GN029 | [missing-replace-in-view](rules/general/missing-replace-in-view.md)               | :white_check_mark: | :white_check_mark: |
| GN030 | [missing-replace-in-trigger](rules/general/missing-replace-in-trigger.md)         | :white_check_mark: | :white_check_mark: |

## naming (NM)

|   Code  |                      Name                                                            |      Stable        | Auto fix           |
| --------| -------------------------------------------------------------------------------------|------------------- |--------------------|
| NM001 | [invalid-index-name](rules/naming/invalid-index-name.md)                               | :white_check_mark: | :x:                |
| NM002 | [invalid-primary-key-name](rules/naming/invalid-primary-key-name.md)                   | :white_check_mark: | :x:                |
| NM003 | [invalid-unique-key-name](rules/naming/invalid-unique-key-name.md)                     | :white_check_mark: | :x:                |
| NM004 | [invalid-foreign-key-name](rules/naming/invalid-foreign-key-name.md)                   | :white_check_mark: | :x:                |
| NM005 | [invalid-check-constraint-name](rules/naming/invalid-check-constraint-name.md)         | :white_check_mark: | :x:                |
| NM006 | [invalid-exclusion-constraint-name](rules/naming/invalid-exclusion-constraint-name.md) | :white_check_mark: | :x:                |
| NM007 | [invalid-sequence-name](rules/naming/invalid-sequence-name.md)                         | :white_check_mark: | :x:                |
| NM008 | [implicit-constraint-name](rules/naming/implicit-constraint-name.md)                   | :white_check_mark: | :x:                |
| NM009 | [invalid-partition-name](rules/naming/invalid-partition-name.md)                       | :white_check_mark: | :x:                |
| NM010 | [non-snake-case-identifier](rules/naming/non-snake-case-identifier.md)                 | :white_check_mark: | :x:                |
| NM011 | [keyword-identifier](rules/naming/keyword-identifier.md)                               | :white_check_mark: | :x:                |
| NM012 | [special-character-in-identifier](rules/naming/special-character-in-identifier.md)     | :white_check_mark: | :x:                |
| NM013 | [pg-prefix-identifier](rules/naming/pg-prefix-identifier.md)                           | :white_check_mark: | :x:                |
| NM014 | [single-letter-identifier](rules/naming/single-letter-identifier.md)                   | :white_check_mark: | :x:                |
| NM015 | [timestamp-column-without-suffix](rules/naming/timestamp-column-without-suffix.md)     | :white_check_mark: | :white_check_mark: |
| NM016 | [date-column-without-suffix](rules/naming/date-column-without-suffix.md)               | :white_check_mark: | :white_check_mark: |

## schema (SM)

|   Code  |                      Name                                            |      Stable        | Auto fix           |
| --------| ---------------------------------------------------------------------|------------------- |--------------------|
| SM001 | [schema-unqualified-object](rules/schema/schema-unqualified-object.md) | :white_check_mark: | :x:                |
| SM002 | [disallowed-schema](rules/schema/disallowed-schema.md)                 | :white_check_mark: | :white_check_mark: |

## security (ST)

|   Code  |                      Name                                                      |      Stable        | Auto fix |
| --------| -------------------------------------------------------------------------------|------------------- |----------|
| ST001 | [extension-whitelist](rules/security/extension-whitelist.md)                     | :white_check_mark: | :x:      |
| ST002 | [procedural-language-whitelist](rules/security/procedural-language-whitelist.md) | :white_check_mark: | :x:      |

## typing (TP)

|   Code  |                      Name                                                                      |      Stable        | Auto fix |
| --------| -----------------------------------------------------------------------------------------------|------------------- |--------------------|
| TP001 | [timestamp-without-timezone](rules/typing/timestamp-without-timezone.md)                         | :white_check_mark: | :white_check_mark: |
| TP002 | [time-with-time-zone](rules/typing/time-with-time-zone.md)                                       | :white_check_mark: | :white_check_mark: |
| TP003 | [timestamp-with-timezone-with-precision](rules/typing/timestamp-with-timezone-with-precision.md) | :white_check_mark: | :white_check_mark: |
| TP004 | [char](rules/typing/char.md)                                                                     | :white_check_mark: | :white_check_mark: |
| TP005 | [varchar](rules/typing/varchar.md)                                                               | :white_check_mark: | :white_check_mark: |
| TP006 | [money](rules/typing/money.md)                                                                   | :white_check_mark: | :white_check_mark: |
| TP007 | [serial](rules/typing/serial.md)                                                                 | :white_check_mark: | :white_check_mark: |
| TP008 | [json](rules/typing/json.md)                                                                     | :white_check_mark: | :white_check_mark: |
| TP009 | [integer](rules/typing/integer.md)                                                               | :white_check_mark: | :white_check_mark: |
| TP010 | [smallint](rules/typing/smallint.md)                                                             | :white_check_mark: | :white_check_mark: |
| TP011 | [float](rules/typing/float.md)                                                                   | :white_check_mark: | :white_check_mark: |
| TP012 | [xml](rules/typing/xml.md)                                                                       | :white_check_mark: | :white_check_mark: |
| TP013 | [hstore](rules/typing/hstore.md)                                                                 | :white_check_mark: | :white_check_mark: |
| TP014 | [disallowed-data-type](rules/typing/disallowed-data-type.md)                                     | :white_check_mark: | :white_check_mark: |
| TP015 | [wrongly-typed-required-column](rules/typing/wrongly-typed-required-column.md)                   | :white_check_mark: | :white_check_mark: |
| TP016 | [numeric-with-precision](rules/typing/numeric-with-precision.md)                                 | :white_check_mark: | :white_check_mark: |
| TP017 | [nullable-boolean-field](rules/typing/nullable-boolean-field.md)                                 | :white_check_mark: | :white_check_mark: |

## unsafe (US)

|   Code  |                      Name                                                                                                        |      Stable        | Auto fix  |
| --------| ---------------------------------------------------------------------------------------------------------------------------------|------------------- |-----------|
| US001 | [drop-column](rules/unsafe/drop-column.md)                                                                                         | :white_check_mark: | :x:       |
| US002 | [column-data-type-change](rules/unsafe/column-data-type-change.md)                                                                 | :white_check_mark: | :x:       |
| US003 | [column-rename](rules/unsafe/column-rename.md)                                                                                     | :white_check_mark: | :x:       |
| US004 | [adding-auto-increment-column](rules/unsafe/adding-auto-increment-column.md)                                                       | :white_check_mark: | :x:       |
| US005 | [adding-auto-increment-identity-column](rules/unsafe/adding-auto-increment-identity-column.md)                                     | :white_check_mark: | :x:       |
| US006 | [adding-stored-generated-column](rules/unsafe/adding-stored-generated-column.md)                                                   | :white_check_mark: | :x:       |
| US007 | [drop-tablespace](rules/unsafe/drop-tablespace.md)                                                                                 | :white_check_mark: | :x:       |
| US008 | [drop-database](rules/unsafe/drop-database.md)                                                                                     | :white_check_mark: | :x:       |
| US009 | [drop-schema](rules/unsafe/drop-schema.md)                                                                                         | :white_check_mark: | :x:       |
| US010 | [not-null-constraint-on-existing-column](rules/unsafe/not-null-constraint-on-existing-column.md)                                   | :white_check_mark: | :x:       |
| US011 | [not-null-constraint-on-new-column-with-volatile-default](rules/unsafe/not-null-constraint-on-new-column-with-volatile-default.md) | :white_check_mark: | :x:       |
| US012 | [validating-foreign-key-constraint-on-existing-rows](rules/unsafe/validating-foreign-key-constraint-on-existing-rows.md)           | :white_check_mark: | :white_check_mark:                                                                                                                                                            |
| US013 | [validating-check-constraint-on-existing-rows](rules/unsafe/validating-check-constraint-on-existing-rows.md)                       | :white_check_mark: | :white_check_mark:                                                                                                                                                            |
| US014 | [unique-key-constraint-creating-index](rules/unsafe/unique-key-constraint-creating-index.md)                                       | :white_check_mark: | :x:       |
| US015 | [primary-key-constraint-creating-index](rules/unsafe/primary-key-constraint-creating-index.md)                                     | :white_check_mark: | :x:       |
| US016 | [non-concurrent-index-creation](rules/unsafe/non-concurrent-index-creation.md)                                                     | :white_check_mark: | :white_check_mark:                                                                                                                                                            |
| US017 | [index-movement-to-tablespace](rules/unsafe/index-movement-to-tablespace.md)                                                       | :white_check_mark: | :x:       |
| US018 | [indexes-movement-to-tablespace](rules/unsafe/indexes-movement-to-tablespace.md)                                                   | :white_check_mark: | :x:       |
| US019 | [non-concurrent-index-drop](rules/unsafe/non-concurrent-index-drop.md)                                                             | :white_check_mark: | :white_check_mark:                                                                                                                                                            |
| US020 | [non-concurrent-reindex](rules/unsafe/non-concurrent-reindex.md)                                                                   | :white_check_mark: | :white_check_mark:                                                                                                                                                            |
| US021 | [drop-table](rules/unsafe/drop-table.md)                                                                                           | :white_check_mark: | :x:       |
| US022 | [rename-table](rules/unsafe/rename-table.md)                                                                                       | :white_check_mark: | :x:       |
| US023 | [table-movement-to-tablespace](rules/unsafe/table-movement-to-tablespace.md)                                                       | :white_check_mark: | :x:       |
| US024 | [tables-movement-to-tablespace](rules/unsafe/tables-movement-to-tablespace.md)                                                     | :white_check_mark: | :x:       |
| US025 | [cluster](rules/unsafe/cluster.md)                                                                                                 | :white_check_mark: | :x:       |
| US026 | [vacuum-full](rules/unsafe/vacuum-full.md)                                                                                         | :white_check_mark: | :x:       |
| US027 | [non-concurrent-detach-partition](rules/unsafe/non-concurrent-detach-partition.md)                                                 | :white_check_mark: | :white_check_mark:                                                                                                                                                            |
| US028 | [non-concurrent-refresh-materialized-view](rules/unsafe/non-concurrent-refresh-materialized-view.md)                               | :white_check_mark: | :white_check_mark:                                                                                                                                                            |
| US029 | [truncate-table](rules/unsafe/truncate-table.md)                                                                                   | :white_check_mark: | :x:       |
| US030 | [mismatch-column-in-data-type-change](rules/unsafe/mismatch-column-in-data-type-change.md)                                         | :white_check_mark: | :x:       |
