Simple solution for cariad transformation problem.

# Prerequisites:
- Bazel installation on your system. 


### Linux

#### 1. Install Bazelisk

bash wget https://github.com/bazelbuild/bazelisk/releases/latest/download/bazelisk-linux-amd64 -O bazelisk chmod +x bazelisk sudo

### Windows

#### 1. Install Bazelisk

**Option A: Using Chocolatey**

powershell choco install bazelisk

**Option B: Manual Installation**

powershell

### Download Bazelisk
ProgressPreference = 'SilentlyContinue' Invoke-WebRequest -Uri "https://github.com/bazelbuild/bazelisk/releases/latest/download/bazelisk-windows-amd64.exe" -OutFile "env:USERPROFILE\bazelisk.exe"

### Add to PATH (run as Administrator or add manually to user PATH)

userPath = [Environment]::GetEnvironmentVariable("Path", "User") [Environment]::SetEnvironmentVariable("Path", "userPath;$env:USERPROFILE", "User")

### Rename to bazel.exe for convenience

Rename-Item "env:USERPROFILE\bazelisk.exe" "env:USERPROFILE\bazel.exe"

## Run Test
```shell
bazel run //test:test_transformation
```
