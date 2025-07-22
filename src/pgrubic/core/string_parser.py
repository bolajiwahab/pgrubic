"""String parsing utilities for extracting SQL content from string literals."""

import logging
import re
from typing import Iterator, List, Optional, Tuple, Dict, Pattern
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class StringSQLContent:
    """Represents SQL content found within a string."""
    sql_content: str
    start_line_offset: int
    content_type: str  # 'do_block', 'sql_statement', 'unknown'
    confidence_score: float  # 0.0 to 1.0, higher = more confident it's SQL


class StringSQLParser:
    """Parser for detecting and extracting SQL content from string literals."""
    
    # Regex patterns for different SQL content types
    DO_BLOCK_PATTERN: Pattern[str] = re.compile(
        r'DO\s+\$(\w*)\$(.*?)\$\1\$\s+LANGUAGE\s+plpgsql',
        re.IGNORECASE | re.DOTALL
    )
    
    # Pattern for SQL keywords that suggest SQL content
    SQL_KEYWORDS_PATTERN: Pattern[str] = re.compile(
        r'\b(CREATE|ALTER|DROP|INSERT|UPDATE|DELETE|SELECT|GRANT|REVOKE|TRUNCATE|COMMENT|ANALYZE|VACUUM|EXPLAIN|LOCK|SET|RESET|SHOW|COPY|NOTIFY)\b',
        re.IGNORECASE
    )
    
    # Pattern for detecting dollar-quoted strings
    DOLLAR_QUOTE_PATTERN: Pattern[str] = re.compile(
        r'\$(\w*)\$(.*?)\$\1\$',
        re.DOTALL
    )
    
    def __init__(self):
        """Initialize the string SQL parser."""
        self.confidence_thresholds = {
            'do_block': 0.9,      # Very high confidence for DO blocks
            'sql_statement': 0.7,  # High confidence for SQL statements
            'unknown': 0.3         # Low confidence threshold
        }
    
    def parse_string_content(self, content: str) -> List[StringSQLContent]:
        """Parse string content to find SQL elements.
        
        Args:
            content: The string content to parse
            
        Returns:
            List of found SQL content with metadata
        """
        results = []
        
        # First, look for DO blocks (highest priority)
        do_blocks = self._extract_do_blocks(content)
        results.extend(do_blocks)
        
        # Then look for other SQL content not already covered by DO blocks
        other_sql = self._extract_other_sql_content(content, do_blocks)
        results.extend(other_sql)
        
        return results
    
    def _extract_do_blocks(self, content: str) -> List[StringSQLContent]:
        """Extract DO blocks from string content.
        
        Args:
            content: The string content to search
            
        Returns:
            List of DO block content found
        """
        results = []
        
        for match in self.DO_BLOCK_PATTERN.finditer(content):
            do_body = match.group(2).strip()
            start_line_offset = content[:match.start()].count('\n') + 1
            
            # Build the full DO block for processing
            full_do_block = f"DO ${match.group(1)}$\n{do_body}\n${match.group(1)}$ LANGUAGE plpgsql;"
            
            results.append(StringSQLContent(
                sql_content=full_do_block,
                start_line_offset=start_line_offset,
                content_type='do_block',
                confidence_score=0.95  # Very high confidence for DO blocks
            ))
            
            logger.debug(f"Found DO block at line offset {start_line_offset}")
        
        return results
    
    def _extract_other_sql_content(self, content: str, existing_blocks: List[StringSQLContent]) -> List[StringSQLContent]:
        """Extract other SQL content that's not already in DO blocks.
        
        Args:
            content: The string content to search
            existing_blocks: Already found DO blocks to avoid double-processing
            
        Returns:
            List of other SQL content found
        """
        results = []
        
        # For now, we'll focus on DO blocks as they're the most common case
        # Future enhancement could include standalone SQL statements
        
        return results
    
    def calculate_sql_confidence(self, content: str) -> float:
        """Calculate confidence score that content is SQL.
        
        Args:
            content: The content to evaluate
            
        Returns:
            Confidence score from 0.0 to 1.0
        """
        if not content.strip():
            return 0.0
        
        # Count SQL keywords
        sql_matches = len(self.SQL_KEYWORDS_PATTERN.findall(content))
        
        # Basic heuristics
        lines = content.split('\n')
        total_lines = len(lines)
        
        # Calculate keyword density
        keyword_density = sql_matches / max(total_lines, 1)
        
        # Look for SQL patterns
        has_semicolons = ';' in content
        has_sql_keywords = sql_matches > 0
        has_quotes = '"' in content or "'" in content
        
        # Calculate confidence
        confidence = 0.0
        
        if keyword_density > 0.3:  # High keyword density
            confidence += 0.4
        elif keyword_density > 0.1:
            confidence += 0.2
        
        if has_sql_keywords:
            confidence += 0.3
        
        if has_semicolons:
            confidence += 0.2
        
        if has_quotes:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def is_likely_sql_content(self, content: str) -> bool:
        """Quick check if content is likely to contain SQL.
        
        Args:
            content: The content to check
            
        Returns:
            True if content likely contains SQL
        """
        return self.calculate_sql_confidence(content) >= self.confidence_thresholds['unknown']


def extract_sql_from_dollar_quoted_string(content: str) -> List[StringSQLContent]:
    """Extract SQL content from dollar-quoted strings.
    
    This is a convenience function that uses StringSQLParser.
    
    Args:
        content: Dollar-quoted string content to parse
        
    Returns:
        List of SQL content found
    """
    parser = StringSQLParser()
    return parser.parse_string_content(content)


def detect_nested_do_blocks(string_content: str) -> Iterator[Tuple[str, int]]:
    """Detect nested DO blocks within a string and extract their content.
    
    Args:
        string_content: The string content to search
        
    Yields:
        Tuples of (do_block_sql, line_offset)
    """
    parser = StringSQLParser()
    sql_contents = parser.parse_string_content(string_content)
    
    for sql_content in sql_contents:
        if sql_content.content_type == 'do_block':
            yield (sql_content.sql_content, sql_content.start_line_offset)