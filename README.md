## Pgrubic

Pgrubic is a PostgreSQL linter and formatter for schema migrations and design best practices.

## Features
- Over 100+ rules.
- Automatic violation correction (e.g., automatically add `concurrently` to index create statements).
- River style code formatting.

## Getting Started
For more, see the [documentation](https://bolajiwahab.github.io/pgrubic/).

## Installation
```bash
pip install pgrubic
```
**<span style="color:red">Pgrubic is only supported on Python 3.12+</span>**.


## Usage
```bash
pgrubic *.sql
test.sql:1:38: TP017: Boolean field should be not be nullable:

ALTER TABLE public.example ADD COLUMN foo boolean DEFAULT false;
```

```bash
pgrubic test.sql
test.sql:1:38: TP017: Boolean field should be not be nullable:

ALTER TABLE public.example ADD COLUMN foo boolean DEFAULT false;
```

## Configuration

## Rules

## Contributing

## Support

## Acknowledgments

## License
