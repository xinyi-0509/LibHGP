<div align="center">

# LibHGP

**A Lightweight Geometry Engine for Digital Manufacturing**

A foundational algorithm library for integrating and industrializing laboratory geometric algorithm assets, supporting **C++ / Python / Web** three calling interfaces.

</div>

## Table of Contents

- [Introduction](#introduction)
- [Architecture](#architecture)
- [Recommended Environment](#recommended-environment)
- [Quick Start](#quick-start)
- [License](#license)

<<<<<<< HEAD
## Introduction
=======
- [项目简介](#项目简介)
- [核心特性](#核心特征)
- [系统架构](#系统架构)
- [仓库目录概览](#仓库目录概览)
- [依赖与环境](#依赖与环境)
- [构建说明](#构建说明)
- [Python扩展说明](#Python 扩展说明)
- [常见配置选项](#常见配置选项)
- [发布与运行时注意事项](#发布与运行时注意事项)
- [快速开始](#快速开始)
- [贡献](#贡献)
- [许可证](#许可证)
>>>>>>> d1ee12c (更新README)

LibHGP is a geometry processing and computational geometry algorithm library that serves as the foundation for building an interactive visualization platform with good maintainability, scalability, and reusability. It supports three usage modes:

- **C++ Native Calls**: Suitable for high-performance algorithm development and system integration
- **Python Calls**: Suitable for research experiments, prototyping, and teaching
- **Web Calls**: Suitable for frontend display, interactive visualization, and online demonstrations

## Architecture

The project can be divided into the following layers:

### 1. Core Algorithm Layer
Responsible for implementing geometry processing, computational geometry, and related fundamental algorithm modules, including:

- 2D geometry algorithms
- 3D geometry algorithms
- Mesh processing
- Convex hull and spatial indexing
- Other laboratory-accumulated algorithm modules

### 2. Interface Wrapper Layer
Responsible for providing unified wrappers for underlying algorithms, exposing stable and consistent calling interfaces, including:

- C++ native interface
- Python binding interface (e.g., pybind11)
- Web calling interface (can support FastAPI / WebAssembly in the future)

### 3. Application and Presentation Layer
Targeting specific application scenarios, including:

- Research prototyping
- Teaching demonstrations
- Algorithm visualization
- Web-based interactive display

## Recommended Environment
- C++17 
- Visual Studio 2019

## Quick Start

### C++ Users

1. Copy all files from `libhgp/C++/` into your project directory
2. Include the header file: `#include "libhgp.h"`
3. Declare the namespace: `using namespace libhgp;`
4. Use the following code for a quick test:
```cpp
#include "iostream"
#include"libhgp.h"
using namespace std;
using namespace libhgp;
int main(int argc, char* argv[])
{
	char dirBuf[260] = { 0 };
	char userBuf[260] = { 0 };
	auto a = PL().HGP_2D_Distance_Point_Point_C(Vector2d(0, 0), Vector2d(1, 1));
	PL().LGP_WinGetCurDirectory_C(dirBuf, sizeof(dirBuf));
	PL().LGP_WinGetUserName_C(userBuf, sizeof(userBuf));
	std::cerr << a << std::endl;
	cerr << "WinGetCurDirectory: " << dirBuf << endl;
	cerr << "WinGetUserName: " << userBuf << endl;
	system("pause");
	return 0;
}
```
### Python Users

<<<<<<< HEAD
1. Copy all files from `libhgp/Python/` into your project directory
2. Import the module in Python: `import hgp_py`
3. Use the following code for a quick test:
=======

## 依赖与环境

- CMake >= 3.16  （CMakeLists 中使用 3.16）
- C++17 支持（CMAKE_CXX_STANDARD 17）
- 编译器：
  - Windows: MSVC 2019 / 2022（Visual Studio 2019/2022）
  - Linux: GCC 9+ / Clang 等
- 第三方库：
  - CGAL（配置为 REQUIRED，使用 CGAL::CGAL 和 CGAL::CGAL_Core）
  - pybind11（用于 Python 绑定）
  - Clipper（已内置或放在 clipper/）
- Python >= 3.8（构建/使用 Python 扩展时）
- vcpkg（推荐在 Windows 上使用以统一依赖管理）

vcpkg 示例：
- Windows:
  vcpkg install cgal[core] --triplet x64-windows-static-md
  vcpkg install pybind11 --triplet x64-windows-static-md
---

## 构建说明

本项目使用 CMake 管理构建。CMakeLists.txt 已包含如下约定（摘要）：

- cmake_minimum_required(VERSION 3.16)
- MSVC 平台上显式设置运行时为 MultiThreadedDLL（/MD）或 MultiThreadedDebugDLL（/MDd）
- 两个库目标：libhgp (SHARED) 与 libhgp_static (STATIC)
- 为静态库设置 POSITION_INDEPENDENT_CODE ON
- 可选构建项 BUILD_PYTHON_BINDINGS（默认 ON），查找 pybind11 并生成 hgp_py 模块

下面给出常见平台的构建步骤。

### Linux（建议在拥有 CGAL 等依赖的环境）
```bash
git clone https://github.com/xinyi-0509/LibHGP.git
cd LibHGP
mkdir build && cd build

cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_TOOLCHAIN_FILE=/path/to/vcpkg/scripts/buildsystems/vcpkg.cmake

cmake --build . --config Release
```

### Windows（MSVC，使用 vcpkg）
```powershell
git clone https://github.com/xinyi-0509/LibHGP.git
cd LibHGP
mkdir build; cd build

cmake .. `
  -G "Visual Studio 17 2022" -A x64 `
  -DCMAKE_TOOLCHAIN_FILE="C:/path/to/vcpkg/scripts/buildsystems/vcpkg.cmake" `
  -DVCPKG_TARGET_TRIPLET="x64-windows-static-md"

cmake --build . --config Release
```

### 仅构建/禁用 Python 绑定
默认会构建 Python 绑定（BUILD_PYTHON_BINDINGS=ON）。若希望禁用：
```bash
cmake .. -DBUILD_PYTHON_BINDINGS=OFF
cmake --build .
```

---

## Python扩展说明

- 构建选项：BUILD_PYTHON_BINDINGS（ON/OFF）
- CMake 会调用 find_package(pybind11 CONFIG REQUIRED) 并通过 pybind11_add_module(...) 生成 `hgp_py` 模块
- `hgp_py` 链接到静态库 `libhgp_static`（静态链接可以实现自包含分发）
- 推荐在构建环境中使用与目标 Python 一致的解释器与 pybind11（通过 vcpkg 或系统包安装）

示例 Python 使用（示例函数名需根据实际绑定调整）：
>>>>>>> d1ee12c (更新README)
```python
import hgp_py

# ── Test 1: 2D point-to-point distance ──────────────────────────────
p1, p2 = [0.0, 0.0], [3.0, 4.0]
dist = hgp_py.HGP_2D_Distance_Point_Point(p1, p2)
assert abs(dist - 5.0) < 1e-9
print(f"[PASS] Test 1: 2D point distance (0,0) (3,4) \n HGP_2D_Distance_Point_Point({p1}, {p2}) = {dist} (expected 5.0)")

# ── Test 2: Point-in-polygon test ────────────────────────────
polygon = [[0.0,0.0],[4.0,0.0],[4.0,4.0],[0.0,4.0]]
inside_pt, outside_pt = [2.0, 2.0], [5.0, 5.0]
assert hgp_py.HGP_2D_Location_Point_Polygon(inside_pt, polygon) == True
assert hgp_py.HGP_2D_Location_Point_Polygon(outside_pt, polygon) == False
print(f"[PASS] Test 2: Point-in-polygon test Polygon[(0,0),(4,0),(4,4),(0,4)] \n HGP_2D_Location_Point_Polygon({inside_pt}) = True")
print(f" HGP_2D_Location_Point_Polygon({outside_pt}) = False")

# ── Test 3: Polygon regular sampling ──────────────────────────────
pts = hgp_py.HGP_2D_Polygon_Regular_Sampling_C1(polygon, 0.1)
print(f"[PASS] Test 3: Polygon regular sampling Polygon[(0,0),(4,0),(4,4),(0,4)] spacing=0.1 \n HGP_2D_Polygon_Regular_Sampling_C1() → generated {len(pts)} sample points")

# ── Test 4: Line segment intersection ────────────────────────────────────
seg1_p1, seg1_p2 = [0.0,0.0],[2.0,2.0]
seg2_p1, seg2_p2 = [0.0,2.0],[2.0,0.0]
hit, inter = hgp_py.HGP_2D_Intersection_Segment_Segment(
    seg1_p1, seg1_p2, seg2_p1, seg2_p2)
assert hit == True
assert abs(inter[0] - 1.0) < 1e-9 and abs(inter[1] - 1.0) < 1e-9
print(f"[PASS] Test 4: Line segment intersection Segment A[(0,0)→(2,2)] Segment B[(0,2)→(2,0)] \n HGP_2D_Intersection_Segment_Segment() = {inter} (expected [1.0,1.0])")

# ── Test 5: Polygon area ──────────────────────────────────
area = hgp_py.HGP_2D_Polygon_Area(polygon)
print(f"[PASS] Test 5: Polygon area Polygon[(0,0),(4,0),(4,4),(0,4)] \n HGP_2D_Polygon_Area() = {area} (expected 16.0)")

# ── Test 6: 3D point-to-point distance ────────────────────────────────
p3, p4 = [0.0,0.0,0.0], [1.0,1.0,1.0]
d3 = hgp_py.HGP_3D_Distance_Point_Point(p3, p4)
expected = 3**0.5
print(f"[PASS] Test 6: 3D point distance (0,0,0) (1,1,1) \n HGP_3D_Distance_Point_Point({p3}, {p4}) = {d3:.6f} (expected √3 ≈ {expected:.6f})")

print("\n✅ All tests passed.")
"
```
### Web Users

<<<<<<< HEAD
1. Copy all files from `libhgp/Web/` into your project directory
2. Navigate to the server build directory: `cd backend`
3. Start the local server: `python -m uvicorn app:app --reload --port 8000`
4. Access the local server at: `http://127.0.0.1:8000/`
=======
部署注意：
- Windows 下如果使用静态链接（libhgp_static）并将其编译进 hgp_py，则通常不需要额外的 DLL；若使用动态库 libhgp，则需要同时部署 libhgp.dll。
>>>>>>> d1ee12c (更新README)

## License

<<<<<<< HEAD
All rights about the program are reserved by the authors of this project. The programs can only be used for research purpose. In no event shall the author be liable to any party for direct, indirect, special, inc
=======
## 常见配置与源码要点（根据当前 CMakeLists.txt）

- 强制 CMake policy CMP0091 在 project() 之前设置以控制 MSVC 运行时行为：
  cmake_policy(SET CMP0091 NEW)
- MSVC 运行时： set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
- 默认启用本地库路径（local_libs）作为 PRIVATE include
- 使用 find_package(CGAL REQUIRED COMPONENTS Core)，并将 CGAL::CGAL、CGAL::CGAL_Core 链接到目标
- pybind11 通过 CONFIG 模式查找并生成模块 hgp_py（pybind11_add_module）
- 静态库 libhgp_static 设置 POSITION_INDEPENDENT_CODE ON 以便安全地与共享对象链接

---

## 发布与运行时注意事项

- 构建时请确认使用的 vcpkg triplet 与运行时选项一致（特别是 Windows MSVC 的 /MD vs /MT）
- 若打算发布 Python wheel，请先确保 hgp_py 对应平台的运行时依赖都已静态或打包好
- 推荐使用 CI（例如 GitHub Actions）自动化构建并对 Linux/Windows 提供二进制发布包

---

## 快速开始


### C++ 用户

1. 将 libhgp/C++/ 中的所有文件复制进您的项目目录
2. 声明头文件 `#include"libhgp.h"`
3. 声明命名空间 `using namespace libhgp;`
4. 使用以下代码快速测试：
"
#include "iostream"
#include"libhgp.h"
using namespace std;
using namespace libhgp;
int main(int argc, char* argv[])
{
	char dirBuf[260] = { 0 };
	char userBuf[260] = { 0 };
	auto a = PL().HGP_2D_Distance_Point_Point_C(Vector2d(0, 0), Vector2d(1, 1));
	PL().LGP_WinGetCurDirectory_C(dirBuf, sizeof(dirBuf));
	PL().LGP_WinGetUserName_C(userBuf, sizeof(userBuf));
	std::cerr << a << std::endl;
	cerr << "WinGetCurDirectory: " << dirBuf << endl;
	cerr << "WinGetUserName: " << userBuf << endl;
	system("pause");
	return 0;
}
"

### Python 用户

1. 将 libhgp/Python/ 中的所有文件复制进您的项目目录
2. 在 Python 中导入模块 'import hgp_py'
3. 使用以下代码快速测试：
"
import hgp_py

# ── Test 1: 2D point-to-point distance ──────────────────────────────
p1, p2 = [0.0, 0.0], [3.0, 4.0]
dist = hgp_py.HGP_2D_Distance_Point_Point(p1, p2)
assert abs(dist - 5.0) < 1e-9
print(f"[PASS] Test 1: 2D point distance (0,0) (3,4) \n HGP_2D_Distance_Point_Point({p1}, {p2}) = {dist} (expected 5.0)")

# ── Test 2: Point-in-polygon test ────────────────────────────
polygon = [[0.0,0.0],[4.0,0.0],[4.0,4.0],[0.0,4.0]]
inside_pt, outside_pt = [2.0, 2.0], [5.0, 5.0]
assert hgp_py.HGP_2D_Location_Point_Polygon(inside_pt, polygon) == True
assert hgp_py.HGP_2D_Location_Point_Polygon(outside_pt, polygon) == False
print(f"[PASS] Test 2: Point-in-polygon test Polygon[(0,0),(4,0),(4,4),(0,4)] \n HGP_2D_Location_Point_Polygon({inside_pt}) = True")
print(f" HGP_2D_Location_Point_Polygon({outside_pt}) = False")

# ── Test 3: Polygon regular sampling ──────────────────────────────
pts = hgp_py.HGP_2D_Polygon_Regular_Sampling_C1(polygon, 0.1)
print(f"[PASS] Test 3: Polygon regular sampling Polygon[(0,0),(4,0),(4,4),(0,4)] spacing=0.1 \n HGP_2D_Polygon_Regular_Sampling_C1() → generated {len(pts)} sample points")

# ── Test 4: Line segment intersection ────────────────────────────────────
seg1_p1, seg1_p2 = [0.0,0.0],[2.0,2.0]
seg2_p1, seg2_p2 = [0.0,2.0],[2.0,0.0]
hit, inter = hgp_py.HGP_2D_Intersection_Segment_Segment(
    seg1_p1, seg1_p2, seg2_p1, seg2_p2)
assert hit == True
assert abs(inter[0] - 1.0) < 1e-9 and abs(inter[1] - 1.0) < 1e-9
print(f"[PASS] Test 4: Line segment intersection Segment A[(0,0)→(2,2)] Segment B[(0,2)→(2,0)] \n HGP_2D_Intersection_Segment_Segment() = {inter} (expected [1.0,1.0])")

# ── Test 5: Polygon area ──────────────────────────────────
area = hgp_py.HGP_2D_Polygon_Area(polygon)
print(f"[PASS] Test 5: Polygon area Polygon[(0,0),(4,0),(4,4),(0,4)] \n HGP_2D_Polygon_Area() = {area} (expected 16.0)")

# ── Test 6: 3D point-to-point distance ────────────────────────────────
p3, p4 = [0.0,0.0,0.0], [1.0,1.0,1.0]
d3 = hgp_py.HGP_3D_Distance_Point_Point(p3, p4)
expected = 3**0.5
print(f"[PASS] Test 6: 3D point distance (0,0,0) (1,1,1) \n HGP_3D_Distance_Point_Point({p3}, {p4}) = {d3:.6f} (expected √3 ≈ {expected:.6f})")

print("\n✅ All tests passed.")
"

### Web 用户

1. 将 libhgp/Web/ 中的所有文件复制进您的项目目录
2. 进入服务器构建目录 'cd backend'
3. 启动本地服务器 'python -m uvicorn app:app --reload --port 8000'
4. 访问本地服务器 http://127.0.0.1:8000/
## 贡献

欢迎提交 issue 或 PR。建议在贡献前先打开 Issue 讨论设计或改动点，或创建分支按功能/修复命名（例如 feature/pybind-cleanup 或 fix/cmake-runtime）。

贡献流程概览：
1. Fork 仓库
2. 新建分支并实现变更
3. 提交 PR，描述变更内容与测试情况
4. 等待 review 与合并

---

## 许可证

本项目使用 MIT 许可证（LICENSE 文件中说明）。如需其他许可或有合作事宜，请联系仓库维护者。

---

<div align="center">
  Made with ❤️ | 2025.02 – 2025.07
</div>
>>>>>>> d1ee12c (更新README)
