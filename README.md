# V8 d8 Builder

Prebuilt d8 (V8's developer shell) for vulnerability research and CTF competitions.

## Features

- **Release + Debug Symbols** - Optimized for vulnerability research (default)
- **Debug builds** - Full debug symbols for development
- **Manual trigger** - Build on-demand via GitHub Actions
- **Configurable** - Choose specific V8 versions/commits or build latest
- **Git commit support** - Build specific V8 commits for CVE reproduction

## Build Types

### Release + Symbols (Recommended)
```gn
is_debug = false
symbol_level = 2
v8_optimized_debug = false
v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true
```
Best for: Exploit development, CTF, vulnerability research

### Debug
```gn
is_debug = true
symbol_level = 2
v8_enable_sandbox = false
v8_enable_gdbjit = true
```
Best for: Development, debugging V8 internals

## Quick Start

### Download Prebuilt

1. Go to [Actions](../../actions)
2. Click "Build d8 (Release with Symbols)" workflow
3. Click "Run workflow"
4. Select build type (release/debug)
5. Enter V8 version or git commit hash (optional)
6. Wait for build to complete (~30 minutes)
7. Download artifacts from the workflow run

### Build Specific CVE Version

For reproducing CVEs, use the exact git commit hash:

```
# Example: CVE-2025-5419
V8 commit: 609a85c2a1bd77d6f6905369f4bc4fcf34c5db09
```

### Build Locally

```bash
# Clone this repository
git clone https://github.com/Fz0x00/v8-d8-builder.git
cd v8-d8-builder

# Build using Docker
docker run --rm -v $(pwd)/output:/output var77/v8-docker-build bash -c \
  "fetch v8 && cd v8 && \
   cat > args.gn << EOF
  is_component_build = false
  is_debug = false
  symbol_level = 2
  v8_optimized_debug = false
  v8_enable_backtrace = true
  v8_enable_disassembler = true
  v8_enable_object_print = true
  v8_enable_verify_heap = true
  v8_static_library = true
  v8_use_external_startup_data = false
  use_custom_libcxx = false
  treat_warnings_as_errors = false
  EOF
  gn gen out.gn/x64.release && \
  ninja -C out.gn/x64.release d8 && \
  cp out.gn/x64.release/d8 /output/"
```

## Usage with GDB

```bash
# Run d8 with GDB
gdb ./d8

# Inside GDB
(gdb) run --allow-natives-syntax --shell test.js

# Set breakpoints
(gdb) break v8::internal::Heap::AllocateRaw
(gdb) continue
```

## Debugging Tips

```bash
# Run with V8 flags for debugging
./d8 --allow-natives-syntax --shell test.js

# Enable V8 logging
./d8 --trace-opt --trace-deopt test.js

# Use with GDB
gdb --args ./d8 --allow-natives-syntax test.js
```

## Related Projects

- [var77/v8-docker-build](https://github.com/var77/v8-docker-build) - Docker-based V8 build tool
- [denoland/rusty_v8](https://github.com/denoland/rusty_v8) - Rust V8 bindings
- [kuoruan/libv8](https://github.com/kuoruan/libv8) - V8 static libraries

## License

MIT