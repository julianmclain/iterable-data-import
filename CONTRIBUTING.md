# Contributing

Style guide:
- Public methods require a docstring. Use restructured text format. 

Formatting
- Formatting with black. Use `tox -e format` to automatically format python files in the project.

Running the tests
- `tox` will run the test suite and linter
- To run the integration tests create a .env file and supply `ITERABLE_API_KEY`. Must be a standard API key.