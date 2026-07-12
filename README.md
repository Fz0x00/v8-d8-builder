# V8 d8 Builder

Prebuilt d8 (V8's developer shell) for vulnerability research and CTF competitions.

## Features

- **Auto-release** - Builds automatically published to GitHub Releases
- **V8 version tracking** - Each build tagged with V8 commit hash
- **Release + Debug Symbols** - Optimized for vulnerability research (default)
- **Debug builds** - Full debug symbols for development

## Version Tracking

### Tag Format
```
v8-{commit_short}-{build_type}
```

Examples:
```
v8-609a85c-release
v8-609a85c-debug
v8-a1b2c3d-release
```

### Release Name Format
```
V8 {version} d8 ({build_type}) - {commit_short}
```

Examples:
```
V8 13.0.0 d8 (release) - 609a85c
V8 d8 (debug) - a1b2c3d
```

## Quick Start

### Download Prebuilt

1. Go to [Releases](../../releases)
2. Find the version you need (by commit hash, date, or V8 version)
3. Download `d8` binary from the release assets

### Build Specific Version

1. Go to [Actions](../../actions)
2. Click "Build d8" workflow
3. Click "Run workflow"
4. Fill in parameters:
   - **Build type**: `release` or `debug`
   - **V8 version**: Git commit hash or version (optional)
5. Wait for build (~30 minutes)
6. Release will be created automatically

## Build Types

### Release + Symbols (Recommended)
```gn
is_debug = false
symbol_level = 2
v8_optimized_debug = false
v8_enable_backtrace = true
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

## Examples

### CVE-2025-5419

```bash
# Trigger build
gh workflow run build-d8.yml \
  -f build_type=release \
  -f v8_version=609a85c2a1bd77d6f6905369f4bc4fcf34c5db09

# Check status
gh run list --workflow=build-d8.yml

# Download from release
gh release download v8-609a85c-release
```

### Latest Debug Version

```bash
gh workflow run build-d8.yml -f build_type=debug
```

### Specific V8 Version

```bash
gh workflow run build-d8.yml \
  -f build_type=release \
  -f v8_version=13.0.0
```

## Usage

```bash
# Make executable
chmod +x d8

# Run with GDB
gdb ./d8

# Run with V8 flags
./d8 --allow-natives-syntax --shell test.js

# Enable V8 logging
./d8 --trace-opt --trace-deopt test.js
```

## Release Structure

Each release includes:
- `d8` - Main binary
- `*.so` - Shared libraries (if any)
- Release notes with:
  - V8 version and commit hash
  - Build type
  - Build configuration
  - Usage instructions

## API Access

### List all releases
```bash
gh release list
```

### Download specific release
```bash
# By tag
gh release download v8-609a85c-release

# Latest release
gh release download
```

### Get release info
```bash
gh release view v8-609a85c-release
```

## Search Releases

```bash
# Search by V8 version
gh release list | grep "V8 13.0.0"

# Search by build type
gh release list | grep "(release)"

# Search by commit
gh release list | grep "609a85c"
```

## Related Projects

- [var77/v8-docker-build](https://github.com/var77/v8-docker-build) - Docker-based V8 build tool
- [denoland/rusty_v8](https://github.com/denoland/rusty_v8) - Rust V8 bindings
- [kuoruan/libv8](https://github.com/kuoruan/libv8) - V8 static libraries

## License

MIT