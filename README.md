# V8 d8 Builder

Prebuilt d8 (V8's developer shell) debug versions for vulnerability research and CTF competitions.

## Features

- **Debug builds** with full symbols for vulnerability analysis
- **Manual trigger** - Build on-demand via GitHub Actions
- **Configurable** - Choose specific V8 versions or build latest
- **Automated** - Uses proven Docker-based build environment

## Quick Start

### Download Prebuilt (Recommended)

1. Go to [Actions](../../actions)
2. Click "Build d8 (Debug)" workflow
3. Click "Run workflow"
4. Enter V8 version (or leave empty for latest)
5. Wait for build to complete (~30 minutes)
6. Download artifacts from the workflow run

### Build Locally

```bash
# Clone this repository
git clone https://github.com/YOUR_USERNAME/v8-d8-builder.git
cd v8-d8-builder

# Build using Docker
docker run --rm -v $(pwd)/output:/output var77/v8-docker-build bash -c \
  "fetch v8 && cd v8 && \
   cat > args.gn << EOF
  is_debug = true
  is_component_build = false
  v8_static_library = true
  symbol_level = 2
  v8_enable_sandbox = false
  v8_optimized_debug = false
  v8_enable_gdbjit = true
  treat_warnings_as_errors = false
  v8_use_external_startup_data = false
  use_custom_libcxx = false
  EOF
  gn gen out.gn/x64.debug && \
  ninja -C out.gn/x64.debug d8 && \
  cp out.gn/x64.debug/d8 /output/"
```

## Build Configuration

The debug build includes:

- `is_debug = true` - Debug symbols and assertions
- `symbol_level = 2` - Full debug symbols
- `v8_enable_sandbox = false` - Disable sandbox for easier exploitation
- `v8_optimized_debug = false` - Disable optimizations for predictable behavior
- `v8_enable_gdbjit = true` - Enable GDB JIT interface

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

## Versions

Builds are available for various V8 versions. Check the [Actions](../../actions) page for available builds.

## Related Projects

- [var77/v8-docker-build](https://github.com/var77/v8-docker-build) - Docker-based V8 build tool
- [denoland/rusty_v8](https://github.com/denoland/rusty_v8) - Rust V8 bindings
- [kuoruan/libv8](https://github.com/kuoruan/libv8) - V8 static libraries

## License

MIT