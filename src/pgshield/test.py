import pglast
# Assuming you have the AST tuple
ast_tuple = (
    (pglast.DefElem(defname='full', defaction=pglast.DefElemAction.DEFELEM_UNSPEC),),
    # Other elements...
)

# Check if defname='full' is contained in the tuple
defname_full_exists = any(
    defelem.defname == 'full'  # Check if defname is 'full'
    for tuple_element in ast_tuple  # Iterate over each tuple element
    for defelem in tuple_element  # Iterate over each DefElem in the tuple element
)

# Print the result
if defname_full_exists:
    print("The tuple contains a DefElem where defname='full'.")
else:
    print("The tuple does not contain a DefElem where defname='full'.")
