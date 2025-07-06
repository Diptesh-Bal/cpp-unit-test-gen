# C++ Unit Test Generator with LLM

A sophisticated automated unit test generation system for C++ projects using Large Language Models (LLMs) with strict YAML-based instructions. This tool generates, refines, and validates unit tests while providing comprehensive test coverage analysis.

## 🚀 Features

- **Automated Test Generation**: Uses LLM to generate initial unit tests for C++ source files
- **Intelligent Test Refinement**: Removes duplicates, improves coverage, and enhances test quality
- **Build Integration**: Automatically builds projects and handles compilation errors
- **Coverage Analysis**: Integrates with GNU code coverage tools (gcov/lcov)
- **YAML-Based Instructions**: Strict, repeatable prompts for consistent test generation
- **Error Recovery**: Handles build failures and provides fix suggestions
- **Cross-Platform**: Works on Windows, Linux, and macOS

## 📋 Requirements

### System Requirements

- **Python 3.7+**
- **C++ Compiler** (GCC, Clang, or MSVC)
- **CMake 3.10+**
- **Google Test Framework**
- **GNU Coverage Tools** (gcov, lcov)

### LLM Requirements

- **Ollama** running locally on `localhost:11434`
- **Recommended Models**: `phi3:mini`, `llama3.2`, or `codellama`

### Python Dependencies

```
requests>=2.25.0
```

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd cpp-unit-test-gen
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install System Dependencies

#### Windows

```bash
# Install Visual Studio Build Tools or MinGW
# Install CMake from https://cmake.org/download/
# Install Google Test (vcpkg recommended)
vcpkg install gtest
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install build-essential cmake libgtest-dev lcov
```

#### macOS

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install dependencies via Homebrew
brew install cmake googletest lcov
```

### 4. Setup Ollama

```bash
# Install Ollama (https://ollama.ai/)
# Pull a suitable model
ollama pull phi3:mini
# Start Ollama service
ollama serve
```

## 📁 Project Structure

```
cpp-unit-test-gen/
├── src/
│   ├── main.py              # Main orchestration script
│   ├── llm_client.py        # LLM API client
│   ├── build_utils.py       # Build and coverage utilities
│   └── yaml_prompts/        # YAML instruction files
│       ├── initial.yaml     # Initial test generation prompts
│       ├── refine.yaml      # Test refinement prompts
│       └── fix_build.yaml   # Build error fix prompts
├── test_projects/           # Input C++ projects
│   └── orgChartApi-master/  # Sample project
├── generated_tests/         # Output test files
├── build/                   # Build artifacts
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🎯 Usage

### Basic Usage

1. **Place your C++ project** in the `test_projects/` directory
2. **Run the test generation pipeline**:
   ```bash
   python src/main.py
   ```

### Advanced Usage

#### Custom Project Path

Modify the `project_dir` variable in `src/main.py`:

```python
project_dir = os.path.join(project_root, "test_projects", "your-project-name")
```

#### Different LLM Model

Change the model in `src/llm_client.py`:

```python
def call_llm(prompt, model="llama3.2", max_retries=3):
```

#### Custom YAML Prompts

Edit the YAML files in `src/yaml_prompts/` to customize:

- Test generation style
- Framework preferences
- Coverage requirements
- Error handling strategies

## 🔧 Configuration

### YAML Prompt Files

#### `initial.yaml` - Initial Test Generation

```yaml
task: generate_unit_tests
framework: gtest
requirements:
  - No duplicate tests
  - Add all necessary #include statements
  - Use Google Test best practices
  - One test file per input file
  - Format code strictly
  - Maximize code coverage
```

#### `refine.yaml` - Test Refinement

```yaml
task: refine_unit_tests
requirements:
  - Remove duplicate or redundant tests
  - Add missing includes or libraries
  - Improve test coverage and formatting
  - No test should be repeated
  - Use Google Test idioms
```

#### `fix_build.yaml` - Build Error Fixes

```yaml
task: fix_build_errors
requirements:
  - Analyze build error messages and identify root causes
  - Fix missing includes, libraries, or dependencies
  - Correct syntax errors, typos, or compilation issues
  - Ensure proper CMake configuration and linking
  - Provide specific fixes for each error identified
  - Maintain Google Test framework compatibility
```

### Environment Variables

```bash
# Optional: Override default Ollama URL
export OLLAMA_API_URL="http://localhost:11434/api/generate"

# Optional: Set default model
export OLLAMA_MODEL="phi3:mini"
```

## 🔄 Pipeline Process

The tool follows a 4-step pipeline:

### Step 1: Initial Test Generation

1. **Scans** the C++ project for source files (`.cc`, `.cpp`)
2. **Sends** each file to the LLM with `initial.yaml` instructions
3. **Generates** initial unit tests in `generated_tests/` directory

### Step 2: Test Refinement

1. **Processes** generated test files
2. **Removes** duplicate tests
3. **Improves** test coverage and formatting
4. **Adds** missing includes and libraries

### Step 3: Build and Debug

1. **Attempts** to build the project with generated tests
2. **Handles** build errors automatically
3. **Sends** error logs to LLM for fixes
4. **Iterates** until build succeeds

### Step 4: Coverage Analysis

1. **Runs** the test suite
2. **Generates** coverage reports using gcov/lcov
3. **Outputs** HTML coverage report
4. **Provides** coverage statistics

## 📊 Output

### Generated Files

- **Test Files**: `generated_tests/test_*.cc`
- **Build Artifacts**: `build/` directory
- **Coverage Report**: `build/coverage/index.html`

### Sample Output

```
🚀 Starting C++ Unit Test Generation Pipeline
📁 Project directory: C:\cpp-unit-test-gen\test_projects\orgChartApi-master
📁 Test directory: C:\cpp-unit-test-gen\generated_tests
📁 Build directory: C:\cpp-unit-test-gen\build

📝 Step 1: Generating initial unit tests...
Found 16 C++ files to process:
  - main.cc
  - controllers/AuthController.cc
  - controllers/DepartmentsController.cc
  ...

✅ Generated test: test_main.cc
✅ Generated test: test_AuthController.cc
...

🔧 Step 2: Refining generated tests...
✅ Refined test: test_main.cc
✅ Refined test: test_AuthController.cc
...

🔨 Step 3: Building project with generated tests...
✅ Build successful!

🧪 Step 4: Running tests and generating coverage...
✅ Tests passed!
📊 Coverage report generated at: build/coverage/index.html

🎉 Pipeline completed!
```

## 🐛 Troubleshooting

### Common Issues

#### 1. LLM Connection Errors

```
❌ Error: Failed to connect to Ollama
```

**Solution**: Ensure Ollama is running:

```bash
ollama serve
```

#### 2. Build Failures

```
❌ Build failed: CMake Error
```

**Solution**: Check CMake configuration and dependencies:

```bash
# Verify CMake installation
cmake --version

# Check if Google Test is available
find /usr -name "gtest" 2>/dev/null
```

#### 3. Coverage Tool Issues

```
❌ Error generating coverage: lcov not found
```

**Solution**: Install coverage tools:

```bash
# Ubuntu/Debian
sudo apt install lcov

# macOS
brew install lcov

# Windows (via vcpkg)
vcpkg install lcov
```

#### 4. Timeout Errors

```
⚠️ Request timeout, retrying...
```

**Solution**:

- Use a faster model (e.g., `phi3:mini` instead of `llama3.2`)
- Increase timeout in `llm_client.py`
- Check system resources

### Debug Mode

Enable verbose logging by modifying `main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔍 Architecture

### Core Components

1. **Main Orchestrator** (`main.py`)

   - Coordinates the entire pipeline
   - Handles file discovery and processing
   - Manages error recovery

2. **LLM Client** (`llm_client.py`)

   - Communicates with Ollama API
   - Implements retry logic and error handling
   - Supports multiple models

3. **Build Utilities** (`build_utils.py`)

   - CMake project building
   - Test execution
   - Coverage generation

4. **YAML Prompts** (`yaml_prompts/`)
   - Structured instructions for LLM
   - Ensures consistent output
   - Configurable behavior

### Data Flow

```
C++ Source Files → LLM (initial.yaml) → Raw Tests → LLM (refine.yaml) → Refined Tests → Build → Coverage Report
```

## 📈 Performance

### Benchmarks

- **Test Generation**: ~30-60 seconds per file (depending on model)
- **Build Time**: Varies by project size
- **Coverage Generation**: ~10-30 seconds

### Optimization Tips

1. **Use faster models** for large projects
2. **Process files in parallel** (future enhancement)
3. **Cache build artifacts** between runs
4. **Skip third-party libraries** in file discovery

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Include error handling

## 🙏 Acknowledgments

- **Ollama** for providing the LLM infrastructure
- **Google Test** for the testing framework
- **CMake** for build system support
- **GNU Coverage Tools** for coverage analysis

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed information
4. Include system details and error logs

---

**Note**: This tool is designed for educational and development purposes. Always review generated tests before using them in production environments.
