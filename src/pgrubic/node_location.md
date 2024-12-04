-- For node which do not carry location e.g literals,
especially the things we use in our rules such as literals
we need to build the location manually

1. Get the statement location
2. Tokenise for literal values
3. If the position of the literal falls with the location of the start and end locations of our
statement, we return the literal location. What of cases with multiple literals?
