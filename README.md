# Python Wrapper for C++ Tool (CI-ready)

## Quick Start (local)

```bash
# Build the C++ tool
cmake -S tool -B build
cmake --build build --config Release

# Run the wrapper
python wrapper/run_tool.py --bin build/simple_tool --input tests/sample_input.txt --threshold 6
```

- Exit code `0` means pass; `1` means validation failure; `124` means timeout.
- The wrapper prints a JSON summary and can emit JUnit XML with `--junit`.

## CI (GitHub Actions)
A ready-to-use workflow is in `.github/workflows/ci.yml`:
- Builds the C++ tool with CMake
- Runs the Python wrapper for valid and invalid cases
- Uploads JUnit XML as CI artifacts
