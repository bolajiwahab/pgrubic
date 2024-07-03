"""Handling noqa comments."""

import re
import typing
import functools
from collections import abc

from pglast import parser

from pgshield.core import errors, linter


def replace_comments_with_spaces(sql: str) -> str:
    """Replace comments with spaces."""
    # Regex pattern for single-line comments at the start of a line
    single_line_pattern = re.compile(r"^--.*$", re.MULTILINE)
    # Regex pattern for multi-line comments at the start of a line
    multi_line_pattern = re.compile(r"^\s*/\*[\s\S]*?\*/\s*$", re.MULTILINE)

    # Function to replace matches with spaces of the same length
    def replace_with_spaces(match):
        return " " * len(match.group(0))

    # Replace single-line comments with spaces
    sql = single_line_pattern.sub(replace_with_spaces, sql)
    # Replace multi-line comments with spaces
    return multi_line_pattern.sub(replace_with_spaces, sql)


def remove_sql_comments(statement: str) -> str:
    """Remove comments from SQL statement."""
    # We remove only comments that start a line, not inline comments
    comment_pattern = r"\s*--.*|^\s*\/[*][\S\s]*?[*]\/"
    return re.sub(
        comment_pattern,
        lambda match: match.group(0).replace(";", ""),
        statement,
        flags=re.MULTILINE,
    )
    # return re.sub(
    #     r"^\s*--.*|^\s*\/[*][\S\s]*?[*]\/",
    #     "",
    #     statement,
    #     flags=re.MULTILINE,
    # )


def _split_sql(statement: str) -> list[tuple[int, int, str]]:
    """Split SQL statement into lines."""
    lines: list[tuple[int, int, str]] = []
    line_offset = 0

    for line in statement.split(";"):

        line_length = len(line)
        lines.append((line_offset, line_offset + line_length, line))
        line_offset += line_length + 1

    # print(lines)

    return lines


# def _extract_comments(statement):
#     lines = []
#     lofs = 0
#     for line in statement.splitlines(True):
#         llen = len(line)
#         lines.append((lofs, lofs+llen, line))
#         lofs += llen
#     comments = []
#     continue_previous = False
#     for token in scan(statement):
#         if token.name in ('C_COMMENT', 'SQL_COMMENT'):
#             for bol_ofs, eol_ofs, line in lines:
#                 if bol_ofs <= token.start < eol_ofs:
#                     break
#             else:  # pragma: no cover
#                 raise RuntimeError('Uhm, logic error!')
#             at_start_of_line = not line[:token.start - bol_ofs].strip()
#             text = statement[token.start:token.end+1]
#             comments.append(Comment(token.start, text, at_start_of_line, continue_previous))
#             continue_previous = True
#         else:
#             continue_previous = False
#     return comments


def extract(statement: str) -> list[tuple[int, str]]:
    """Extract noqa from inline SQL comment."""
    # statement = remove_sql_comments(statement)

    lines = _split_sql(statement)

    comments: list[tuple[int, str]] = []

    for token in parser.scan(statement):

        msg = f"Malformed 'noqa' section in line {token.start}. Expected 'noqa: <rule>"

        if token.name == "SQL_COMMENT":

            # print(token)

            for beginning_of_line_offset, end_of_line_offset, _ in lines:
                if beginning_of_line_offset <= token.start < end_of_line_offset:
                    break
            # print(beginning_of_line_offset)

            comment = statement[token.start : (token.end + 1)]
            # print(comment)
            # is_sql_comment = comment.text.startswith('--')
            # if is_sql_comment:
            #     text = comment.text[2:].strip()
            # else:
            #     text = comment.text[2:-2].strip()

            # Normal comment lines can also have noqa e.g. --new table -- noqa: UNS05
            # Therefore extract last possible inline ignore.
            comment = [c.strip() for c in comment.split("--")][-1]
            # print(comment)

            if comment.startswith("noqa"):
                # This is an ignore identifier
                comment_remainder = comment[4:]

                if comment_remainder:
                    if not comment_remainder.startswith(":"):
                        raise errors.SQLParseError(
                            msg,
                        )

                    comment_remainder = comment_remainder[1:].strip()

                [
                    comments.append((beginning_of_line_offset, rule.strip()))  # type: ignore[func-returns-value]
                    for rule in comment_remainder.split(",")
                ]

    return comments


def directive(func: abc.Callable[..., typing.Any]) -> abc.Callable[..., typing.Any]:
    """Handle application of noqa on rules."""

    @functools.wraps(func)
    def wrapper(
        self: typing.Any,  # noqa: ANN401
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> typing.Any:  # noqa: ANN401

        statement_index: int = linter.get_statement_index(args[0])

        # print(args[0][statement_index].stmt_location)

        if args[0][statement_index].stmt_location == 0:
            location = args[0][statement_index].stmt_len
        #    print(location)

        # statement_location = args[0][statement_index].stmt_location == 0
        total_statement_location = (
            args[0][statement_index].stmt_location + args[0][statement_index].stmt_len
        )

        print(args[0][statement_index].stmt_location)

        if (
            args[0][statement_index].stmt_location,
            self.code,
        ) in self.noqa_ignore_rules:

            return None

        return func(self, *args, **kwargs)

    return wrapper
