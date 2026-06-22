# RA Programming Language

RA is a modern, beginner-friendly programming language with built-in AI integration, interactive debugging, package management, and first-class VS Code support. Designed for developers building AI-augmented applications, RA combines a clean syntax with a powerful local toolchain.

---

## Key Features

- **Simple, readable syntax** -- Concise notation with familiar control flow and data types.
- **Built-in package manager (RAPM)** -- Install, publish, and manage packages with dependency resolution, signing, and trust models.
- **AI integration** -- Local AI assistance via Ollama for code explanation, review, error analysis, and documentation generation. Fully offline, no data leaves your machine.
- **Interactive debugger** -- Set breakpoints, step through code, inspect variables and scope with execution tracing.
- **VS Code extension** -- Syntax highlighting, code snippets, project validation, build/run commands, and LSP-powered diagnostics, hover, completion, references, and rename.
- **Pattern analysis (RARG)** -- Deterministic, rule-based AST analysis for structural insights, relationship analysis, and cross-system correlation.
- **Multi-paradigm** -- Procedural and object-oriented programming with classes, constructors, encapsulation, and method dispatch.
- **Data structures & algorithms** -- Built-in stack, queue, dequeue, graph, tree, sorting, and searching engines.
- **Cross-platform** -- Windows native executables and portable distribution.

---

## Quick Start

```bash
# Create a new project from a template
ra create myapp

# Build and run the project
ra run myapp

# Install a package
rapm install package-name

# Launch the interactive debugger
ra debug myapp

# Start the graphical IDE
RA.IDE
```

---

## Installation

See [docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) for detailed setup instructions covering:

- **Windows installer** -- Automatic setup via the RA Installer.
- **Portable release** -- Extract `RA_Portable/` to any location, no installation required.
- **VS Code extension** -- Install `ra-language` from the VS Code Marketplace or side-load from `vscode-extension/`.
- **RAPM setup** -- The package manager is included with the runtime; initialize a local registry with `rapm init`.
- **Ollama setup (optional)** -- Install Ollama from [ollama.com](https://ollama.com) and pull a model to enable AI features.

---

## Example Program

```ra
# Hello World in RA

import "io" as io

# Read user input and print a greeting
name = io.readln "Enter your name: " l
io.print "Hello, " name "! Welcome to RA." l
```

```ra
# Object-oriented example

@Cls Greeter
    M SayHello
        p "Hello from RA!"
    /
/

# Primary syntax
Obj.Greeter.g

# Alias syntax (equivalent)
g : Obj.Greeter

g.SayHello.run
```

---

## RAPM Usage

RAPM (RA Package Manager) manages dependencies for RA projects.

| Command | Description |
|---------|-------------|
| `rapm init` | Initialize a new package structure |
| `rapm pack` | Create a `.rapkg` archive from a package directory |
| `rapm publish` | Publish a package to the local registry |
| `rapm install <name>` | Install a package and its dependencies |
| `rapm remove <name>` | Remove an installed package |
| `rapm update <name>` | Update a package to the latest version |
| `rapm list` | List all installed packages |
| `rapm search <query>` | Search the registry for packages |
| `rapm info <name>` | Show detailed package information |

Packages use `.rapkg` format (ZIP archives containing `ra-package.toml` manifest and source files). See [docs/RAPM_SPEC.md](docs/RAPM_SPEC.md) for the full specification.

---

## VS Code Setup

1. Install the RA VS Code extension (`ra-language`) from the marketplace, or load it manually from `vscode-extension/`.
2. The extension provides:
   - **Syntax highlighting** -- Full TextMate grammar for `.ra` files.
   - **Code snippets** -- 35+ snippets for common patterns.
   - **Project commands** -- Validate, build, run, and manage projects from the command palette.
   - **LSP integration** -- Diagnostics, hover information, code completion, go-to-definition, find references, and rename symbols (requires the LSP server at `src/lsp/`).
   - **Problems panel** -- Real-time error and warning display on save.

See [docs/RA_VSCODE_EXTENSION.md](docs/RA_VSCODE_EXTENSION.md) for the full feature reference.

---

## AI Features

RA integrates with [Ollama](https://ollama.com) to provide local AI-powered development tools:

- **Code explanation** -- Select code and ask RA to explain what it does.
- **Error explanation** -- Get natural-language explanations of runtime and compile errors.
- **Code review** -- Receive suggestions for improvement and best practices.
- **Documentation generation** -- Auto-generate documentation for your code.

All AI features run fully offline. No data is sent to external servers.

To enable AI features, install Ollama, pull a model (e.g., `ollama pull llama3.2`), and start the Ollama service. See [docs/OLLAMA_INTEGRATION.md](docs/OLLAMA_INTEGRATION.md) for setup details.

---

## Debugger Features

The RA debugger provides runtime inspection capabilities:

- **Breakpoints** -- Set, clear, list, and enable/disable breakpoints on specific source lines.
- **Step execution** -- Step into, step over, and continue execution with pause/resume control.
- **Variable inspection** -- View all variables in the current scope with names, types, and values.
- **Scope inspection** -- Traverse the call stack and inspect nested scopes.
- **Execution tracing** -- Record and review execution events for post-mortem analysis.

Launch the debugger with `ra debug <project>` or attach it to a running script.

See [docs/RA_DEBUGGER_SPEC.md](docs/RA_DEBUGGER_SPEC.md) for architecture details.

---

## Documentation

| Document | Description |
|----------|-------------|
| [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) | Step-by-step introduction to RA |
| [docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) | Detailed installation instructions |
| [docs/RA_CLI_STANDARD.md](docs/RA_CLI_STANDARD.md) | CLI command reference for RA and RADK |
| [docs/RA_PROJECT_STRUCTURE.md](docs/RA_PROJECT_STRUCTURE.md) | Standard project layout and conventions |
| [docs/RA_EXECUTION_PIPELINE.md](docs/RA_EXECUTION_PIPELINE.md) | How RA bytecode is loaded and executed |
| [docs/RAPM_SPEC.md](docs/RAPM_SPEC.md) | Package manager specification |
| [docs/RA_VSCODE_EXTENSION.md](docs/RA_VSCODE_EXTENSION.md) | VS Code extension features and configuration |
| [docs/RA_LSP_ARCHITECTURE.md](docs/RA_LSP_ARCHITECTURE.md) | Language Server Protocol implementation |
| [docs/RA_DEBUGGER_SPEC.md](docs/RA_DEBUGGER_SPEC.md) | Debugger architecture and API |
| [docs/OLLAMA_INTEGRATION.md](docs/OLLAMA_INTEGRATION.md) | AI integration setup and usage |
| [docs/RA_PUBLIC_BETA_SPEC.md](docs/RA_PUBLIC_BETA_SPEC.md) | Public beta scope and deliverables |

---

## Roadmap

- **Cloud registry service** -- Community package registry with authentication and publishing workflows.
- **CI/CD integration** -- Build and test automation for RA projects.
- **Expanded LSP features** -- Code actions, inlay hints, and signature help.
- **Cross-platform compiler** -- Native compilation targets for Linux and macOS.
- **Standard library expansion** -- Additional modules for networking, file I/O, and concurrency.
- **Performance optimizations** -- JIT compilation and improved bytecode execution.

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on reporting bugs, suggesting features, and submitting pull requests. All contributors must follow the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## License

RA Language is released under the MIT License. See [LICENSE](LICENSE) for details.

---

## Community

- [GitHub Issues](https://github.com/RA-Language/RA.lang/issues) -- Report bugs and request features.
- See [COMMUNITY.md](COMMUNITY.md) for community guidelines and [SUPPORT.md](SUPPORT.md) for support resources.
