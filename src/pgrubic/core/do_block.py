"""DO block handling utilities for extracting and processing procedural code."""

import logging
import re
from typing import Iterator, List, Optional, Tuple

import pglast
from pglast import ast

# Import at runtime to avoid circular imports

logger = logging.getLogger(__name__)


def extract_do_block_body(do_stmt: ast.DoStmt) -> Optional[str]:
    """Extract the body code from a DO statement.
    
    Args:
        do_stmt: The DO statement AST node
        
    Returns:
        The body code as a string, or None if not found
    """
    if not do_stmt.args:
        return None
        
    for arg in do_stmt.args:
        if isinstance(arg, ast.DefElem) and arg.defname == 'as':
            # Extract string value from the arg
            if hasattr(arg.arg, 'sval'):
                return arg.arg.sval
            elif isinstance(arg.arg, tuple) and len(arg.arg) > 0:
                # Handle tuple case where the string is the first element
                if hasattr(arg.arg[0], 'sval'):
                    return arg.arg[0].sval
    
    return None


def extract_sql_statements_from_plpgsql(body: str) -> List[Tuple[str, int]]:
    """Extract SQL statements from PL/pgSQL code.
    
    This function identifies SQL statements within PL/pgSQL code by looking for
    common SQL keywords and extracting statements up to their semicolons.
    
    Args:
        body: The PL/pgSQL code body
        
    Returns:
        List of tuples containing (sql_statement, line_offset)
    """
    statements = []
    lines = body.split('\n')
    
    # SQL statement keywords that we want to extract
    sql_keywords = {
        'CREATE', 'ALTER', 'DROP', 'INSERT', 'UPDATE', 'DELETE', 'SELECT',
        'GRANT', 'REVOKE', 'TRUNCATE', 'COMMENT', 'ANALYZE', 'VACUUM',
        'EXPLAIN', 'LOCK', 'SET', 'RESET', 'SHOW', 'COPY', 'NOTIFY'
    }
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('--'):
            i += 1
            continue
            
        # Check if this line starts with a SQL keyword
        first_word = line.split()[0].upper() if line.split() else ''
        
        if first_word in sql_keywords:
            # Extract the full statement
            statement_lines = []
            line_offset = i
            
            # Collect lines until we find a semicolon at the statement level
            paren_depth = 0
            quote_char = None
            dollar_quote = None
            
            while i < len(lines):
                current_line = lines[i]
                statement_lines.append(current_line)
                
                # Track nesting to handle semicolons inside parentheses/strings
                j = 0
                while j < len(current_line):
                    char = current_line[j]
                    
                    # Handle dollar quotes
                    if dollar_quote:
                        if current_line[j:].startswith(dollar_quote):
                            j += len(dollar_quote)
                            dollar_quote = None
                            continue
                    elif char == '$' and j + 1 < len(current_line):
                        # Check for dollar quote start
                        match = re.match(r'\$([a-zA-Z_]*)\$', current_line[j:])
                        if match:
                            dollar_quote = match.group(0)
                            j += len(dollar_quote)
                            continue
                    
                    # Handle regular quotes
                    if quote_char:
                        if char == quote_char:
                            # Check for escaped quote
                            if j + 1 < len(current_line) and current_line[j + 1] == quote_char:
                                j += 2
                                continue
                            quote_char = None
                    elif char in ('"', "'"):
                        quote_char = char
                    
                    # Track parentheses depth
                    elif not quote_char and not dollar_quote:
                        if char == '(':
                            paren_depth += 1
                        elif char == ')':
                            paren_depth -= 1
                        elif char == ';' and paren_depth == 0:
                            # Found end of statement
                            statement = '\n'.join(statement_lines)
                            statements.append((statement, line_offset + 1))  # 1-based line numbers
                            i += 1
                            break
                    
                    j += 1
                else:
                    # Move to next line if we didn't find a semicolon
                    i += 1
                    if i >= len(lines):
                        # Add incomplete statement if we reached end
                        if statement_lines:
                            statement = '\n'.join(statement_lines)
                            statements.append((statement, line_offset + 1))
                        break
            else:
                continue
        else:
            i += 1
    
    return statements


def lint_do_block(linter: 'Linter', do_stmt: ast.DoStmt, source: str, filename: str, base_line: int = 1) -> Iterator['Violation']:
    """Lint SQL statements within a DO block.
    
    Args:
        linter: The linter instance to use
        do_stmt: The DO statement AST node
        source: The original source code
        filename: The filename being linted
        base_line: The line number where the DO block starts
        
    Yields:
        Violations found within the DO block
    """
    # Extract the body code
    body = extract_do_block_body(do_stmt)
    if not body:
        logger.debug("No body found in DO statement")
        return
    
    # Extract SQL statements from the body
    statements = extract_sql_statements_from_plpgsql(body)
    
    logger.debug(f"Found {len(statements)} SQL statements in DO block")
    
    # Lint each extracted statement
    for sql, line_offset in statements:
        try:
            # Run the linter on the extracted SQL statement
            result = linter.run(source_file=filename, source_code=sql)
            
            # Yield violations with adjusted line numbers
            for violation in result.violations:
                # Adjust the line number to account for the DO block offset
                # We need to add the base_line and the offset within the DO block
                adjusted_line = base_line + line_offset + violation.line_number - 2
                
                # Import here to avoid circular dependency
                from pgrubic.core.linter import Violation
                
                yield Violation(
                    rule_code=violation.rule_code,
                    rule_name=violation.rule_name,
                    rule_category=violation.rule_category,
                    line_number=adjusted_line,
                    column_offset=violation.column_offset,
                    line=violation.line,
                    statement_location=violation.statement_location,
                    description=violation.description,
                    is_auto_fixable=violation.is_auto_fixable,
                    is_fix_enabled=violation.is_fix_enabled,
                    help=violation.help
                )
                
        except Exception as e:
            logger.debug(f"Failed to parse SQL statement in DO block: {e}")
            # Continue with other statements
            continue