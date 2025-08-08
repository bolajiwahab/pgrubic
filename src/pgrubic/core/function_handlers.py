"""Function-specific handlers for extracting SQL content from function parameters."""

import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from pglast import ast

from .string_parser import StringSQLContent, StringSQLParser

logger = logging.getLogger(__name__)


@dataclass
class FunctionSQLParameter:
    """Represents a function parameter that contains SQL content."""
    parameter_index: int
    parameter_content: str
    sql_contents: List[StringSQLContent]


class BaseFunctionHandler(ABC):
    """Base class for function-specific SQL extraction handlers."""
    
    @abstractmethod
    def can_handle(self, funcname: List[str]) -> bool:
        """Check if this handler can process the given function name.
        
        Args:
            funcname: Function name parts (e.g., ['pglogical', 'replicate_ddl_command'])
            
        Returns:
            True if this handler can process the function
        """
        pass
    
    @abstractmethod
    def extract_sql_from_parameters(self, func_call: ast.FuncCall) -> List[FunctionSQLParameter]:
        """Extract SQL content from function parameters.
        
        Args:
            func_call: The function call AST node
            
        Returns:
            List of parameters containing SQL content
        """
        pass


class PglogicalHandler(BaseFunctionHandler):
    """Handler for pglogical.replicate_ddl_command() calls."""
    
    def __init__(self):
        """Initialize the pglogical handler."""
        self.sql_parser = StringSQLParser()
    
    def can_handle(self, funcname: List[str]) -> bool:
        """Check if this is a pglogical function call.
        
        Args:
            funcname: Function name parts
            
        Returns:
            True if this is a pglogical function
        """
        if len(funcname) >= 2:
            return (funcname[-2].lower() == 'pglogical' and 
                   funcname[-1].lower() in ['replicate_ddl_command', 'replicate_ddl'])
        return False
    
    def extract_sql_from_parameters(self, func_call: ast.FuncCall) -> List[FunctionSQLParameter]:
        """Extract SQL from pglogical function parameters.
        
        For pglogical.replicate_ddl_command(sql_text, replication_sets),
        the first parameter typically contains the SQL/DO block content.
        
        Args:
            func_call: The pglogical function call
            
        Returns:
            List of parameters with SQL content
        """
        results = []
        
        if not func_call.args or len(func_call.args) == 0:
            return results
        
        # The first parameter usually contains the SQL content
        first_param = func_call.args[0]
        
        # Extract string content from the parameter
        param_content = self._extract_string_from_node(first_param)
        if param_content:
            sql_contents = self.sql_parser.parse_string_content(param_content)
            
            if sql_contents:
                results.append(FunctionSQLParameter(
                    parameter_index=0,
                    parameter_content=param_content,
                    sql_contents=sql_contents
                ))
                
                logger.debug(f"Found {len(sql_contents)} SQL content(s) in pglogical parameter")
        
        return results
    
    def _extract_string_from_node(self, node: ast.Node) -> Optional[str]:
        """Extract string content from an AST node.
        
        Args:
            node: The AST node to extract from
            
        Returns:
            String content if found, None otherwise
        """
        if isinstance(node, ast.A_Const) and hasattr(node.val, 'sval'):
            return node.val.sval
        elif isinstance(node, ast.String) and hasattr(node, 'sval'):
            return node.sval
        
        # Handle other node types as needed
        return None


class ExecuteHandler(BaseFunctionHandler):
    """Handler for EXECUTE statements with dynamic SQL."""
    
    def __init__(self):
        """Initialize the execute handler."""
        self.sql_parser = StringSQLParser()
    
    def can_handle(self, funcname: List[str]) -> bool:
        """Check if this is an EXECUTE statement.
        
        Note: EXECUTE statements are typically parsed differently,
        but this handler can be extended for similar patterns.
        
        Args:
            funcname: Function name parts
            
        Returns:
            False for now (EXECUTE requires special handling)
        """
        # EXECUTE statements need special handling in the AST
        # This is a placeholder for future enhancement
        return False
    
    def extract_sql_from_parameters(self, func_call: ast.FuncCall) -> List[FunctionSQLParameter]:
        """Extract SQL from EXECUTE parameters.
        
        Args:
            func_call: The function call
            
        Returns:
            Empty list for now
        """
        # Placeholder for future EXECUTE statement support
        return []


class CustomFunctionHandler(BaseFunctionHandler):
    """Handler for custom functions that take SQL as string parameters."""
    
    def __init__(self, function_patterns: List[str]):
        """Initialize with custom function patterns.
        
        Args:
            function_patterns: List of function name patterns to match
        """
        self.function_patterns = function_patterns
        self.sql_parser = StringSQLParser()
    
    def can_handle(self, funcname: List[str]) -> bool:
        """Check if this matches any custom function pattern.
        
        Args:
            funcname: Function name parts
            
        Returns:
            True if matches a configured pattern
        """
        full_name = '.'.join(funcname)
        
        for pattern in self.function_patterns:
            if pattern.lower() in full_name.lower():
                return True
        
        return False
    
    def extract_sql_from_parameters(self, func_call: ast.FuncCall) -> List[FunctionSQLParameter]:
        """Extract SQL from custom function parameters.
        
        This is a generic implementation that checks all string parameters
        for potential SQL content.
        
        Args:
            func_call: The function call
            
        Returns:
            List of parameters with SQL content
        """
        results = []
        
        if not func_call.args:
            return results
        
        for i, param in enumerate(func_call.args):
            param_content = self._extract_string_from_node(param)
            if param_content and self.sql_parser.is_likely_sql_content(param_content):
                sql_contents = self.sql_parser.parse_string_content(param_content)
                
                if sql_contents:
                    results.append(FunctionSQLParameter(
                        parameter_index=i,
                        parameter_content=param_content,
                        sql_contents=sql_contents
                    ))
        
        return results
    
    def _extract_string_from_node(self, node: ast.Node) -> Optional[str]:
        """Extract string content from an AST node."""
        if isinstance(node, ast.A_Const) and hasattr(node.val, 'sval'):
            return node.val.sval
        elif isinstance(node, ast.String) and hasattr(node, 'sval'):
            return node.sval
        
        return None


class FunctionHandlerRegistry:
    """Registry for managing function-specific SQL extraction handlers."""
    
    def __init__(self):
        """Initialize the registry with default handlers."""
        self.handlers: List[BaseFunctionHandler] = []
        
        # Register default handlers
        self.register_handler(PglogicalHandler())
        self.register_handler(ExecuteHandler())
    
    def register_handler(self, handler: BaseFunctionHandler):
        """Register a new function handler.
        
        Args:
            handler: The handler to register
        """
        self.handlers.append(handler)
        logger.debug(f"Registered handler: {handler.__class__.__name__}")
    
    def register_custom_functions(self, function_patterns: List[str]):
        """Register custom function patterns.
        
        Args:
            function_patterns: List of function name patterns
        """
        if function_patterns:
            custom_handler = CustomFunctionHandler(function_patterns)
            self.register_handler(custom_handler)
            logger.debug(f"Registered custom function patterns: {function_patterns}")
    
    def find_handler(self, funcname: List[str]) -> Optional[BaseFunctionHandler]:
        """Find a handler for the given function name.
        
        Args:
            funcname: Function name parts
            
        Returns:
            Handler if found, None otherwise
        """
        for handler in self.handlers:
            if handler.can_handle(funcname):
                return handler
        
        return None
    
    def extract_sql_from_function_call(self, func_call: ast.FuncCall) -> List[FunctionSQLParameter]:
        """Extract SQL content from a function call using appropriate handler.
        
        Args:
            func_call: The function call AST node
            
        Returns:
            List of parameters with SQL content
        """
        # Extract function name from the AST
        funcname = self._extract_function_name(func_call)
        if not funcname:
            return []
        
        # Find appropriate handler
        handler = self.find_handler(funcname)
        if not handler:
            return []
        
        # Extract SQL content
        return handler.extract_sql_from_parameters(func_call)
    
    def _extract_function_name(self, func_call: ast.FuncCall) -> List[str]:
        """Extract function name parts from function call.
        
        Args:
            func_call: The function call AST node
            
        Returns:
            List of name parts
        """
        if not func_call.funcname:
            return []
        
        name_parts = []
        for name_node in func_call.funcname:
            if isinstance(name_node, ast.String) and hasattr(name_node, 'sval'):
                name_parts.append(name_node.sval)
        
        return name_parts


# Global registry instance
function_handler_registry = FunctionHandlerRegistry()