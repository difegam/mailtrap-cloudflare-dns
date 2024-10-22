# Python Project Template 🐍

This is a template for a Python project. It includes a basic project structure, a Justfile with some useful commands, and a README.md template.

## Packages management
This project uses [uv](https://docs.astral.sh/uv/) as a package manager. To install it, please follow the instructions in the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

Here are some useful commands to manage dependencies:

### Install Python version
To install a specific Python version, run the following command:

```bash
uv python install <version>
```

### Create a virtual environment
To create a virtual environment, run the following command:

```bash
uv venv
```


### Add dependencies
To add a new dependency, run the following command:

```bash
uv add <package>
```

### Remove dependencies
To remove a dependency, run the following command:

```bash
uv remove <package>
```

### Development dependencies
To add a development dependency, run the following command:

```bash
uv add  <package> --dev
```

See the [uv documentation](https://docs.astral.sh/uv/) for more information.

## Resources
- https://github.com/asmitul/python-package-template/tree/main
- https://github.com/alvarobartt/python-package-template
- https://github.com/Diapolo10/python-poetry-template/tree/main
- https://github.com/smarlhens/python-boilerplate/tree/main
