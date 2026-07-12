# V8 d8 Debug Builder

Prebuilt d8 (V8's developer shell) **debug versions** for vulnerability research and CTF competitions.

## Why Debug?

- **Google 官方提供 release 版本**: https://storage.googleapis.com/chromium-v8/official/canary/
- **Debug 版本优势**:
  - 完整的调试符号
  - 禁用沙箱 (`v8_enable_sandbox = false`)
  - 禁用优化调试 (`v8_optimized_debug = false`)
  - 启用 GDB JIT 接口
  - 更适合漏洞分析和利用开发

## Features

- **Auto-release** - Debug builds automatically published to GitHub Releases
- **V8 version tracking** - Each build tagged with V8 commit hash
- **On-demand builds** - Build any V8 version via GitHub Actions

## Version Tracking

### Tag Format
```
v8-{commit_short}-debug
```

Examples:
```
v8-609a85c-debug
v8-a1b2c3d-debug
```

### Release Name Format
```
V8 {version} d8 (debug) - {commit_short}
```

Examples:
```
V8 13.0.0 d8 (debug) - 609a85c
V8 d8 (debug) - a1b2c3d
```

## Quick Start

### Download Prebuilt

1. Go to [Releases](../../releases)
2. Find the version you need (by commit hash, date, or V8 version)
3. Download `d8` binary from the release assets

### Build Specific Version

1. Go to [Actions](../../actions)
2. Click "Build d8 (Debug)" workflow
3. Click "Run workflow"
4. Enter V8 version (optional)
5. Wait for build (~30 minutes)
6. Release will be created automatically

## Build Configuration

```gn
is_debug = true
symbol_level = 2
v8_enable_sandbox = false
v8_optimized_debug = false
v8_enable_gdbjit = true
v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true
```

## Examples

### CVE-2025-5419

```bash
# Trigger build
gh workflow run build-d8.yml \
  -f v8_version=609a85c2a1bd77d6f6905369f4bc4fcf34c5db09

# Check status
gh run list --workflow=build-d8.yml

# Download from release
gh release download v8-609a85c-debug
```

### Latest Debug Version

```bash
gh workflow run build-d8.yml
```

### Specific V8 Version

```bash
gh workflow run build-d8.yml -f v8_version=13.0.0
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

## API Access

### List all releases
```bash
gh release list
```

### Download specific release
```bash
# By tag
gh release download v8-609a85c-debug

# Latest release
gh release download
```

### Get release info
```bash
gh release view v8-609a85c-debug
```

## Search Releases

```bash
# Search by V8 version
gh release list | grep "V8 13.0.0"

# Search by commit
gh release list | grep "609a85c"
```

## Related Projects

- [var77/v8-docker-build](https://github.com/var77/v8-docker-build) - Docker-based V8 build tool
- [denoland/rusty_v8](https://github.com/denoland/rusty_v8) - Rust V8 bindings
- [kuoruan/libv8](https://github.com/kuoruan/libv8) - V8 static libraries

## License

MIT