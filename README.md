<div align="center">

# LibHGP

**面向数字制造的微型几何引擎**

实验室几何算法资源整合与工程化的基础算法库，支持 **C++ / Python / Web** 三种调用接口。

</div>

## 目录

- [项目简介](#项目简介)
- [系统架构](#系统架构)
- [依赖与环境](#依赖与环境)
- [构建说明](#构建说明)
- [Python扩展说明](#python扩展说明)
- [常见配置与源码要点](#常见配置与源码要点)
- [发布与运行时注意事项](#发布与运行时注意事项)
- [快速开始](#快速开始)
- [贡献](#贡献)
- [许可证](#许可证)

---

## 项目简介

LibHGP 是一个几何处理与计算几何算法库，以可维护性、可扩展性和可复用性为设计目标，支持三种使用方式：

- **C++ 原生调用**：适合高性能算法开发与系统集成
- **Python 调用**：适合科研实验、原型验证与教学
- **Web 调用**：适合前端展示、交互式可视化与在线演示

---

## 系统架构

项目分为以下三层：

### 1. 核心算法层
负责实现几何处理、计算几何及相关基础算法模块，包括：

- 2D 几何算法
- 3D 几何算法
- 网格处理
- 凸包与空间索引
- 其他实验室积累的算法模块

### 2. 接口封装层
负责对底层算法进行统一封装，暴露稳定一致的调用接口，包括：

- C++ 原生接口
- Python 绑定接口（pybind11）
- Web 调用接口（FastAPI）

### 3. 应用与展示层
面向具体应用场景，包括：

- 科研原型验证
- 教学演示
- 算法可视化
- Web 交互式展示

---

## 依赖与环境

- CMake >= 3.16
- C++17 支持（`CMAKE_CXX_STANDARD 17`）
- 编译器：
  - Windows：MSVC 2019 / 2022（Visual Studio 2019/2022）
  - Linux：GCC 9+ / Clang 等
- 第三方库：
  - CGAL（配置为 REQUIRED，使用 `CGAL::CGAL` 和 `CGAL::CGAL_Core`）
  - pybind11（用于 Python 绑定）
  - Clipper（已内置，位于 `clipper/`）
- Python >= 3.8（构建或使用 Python 扩展时需要）
- vcpkg（推荐在 Windows 上使用以统一依赖管理）

**vcpkg 安装示例（Windows）：**

```bash
vcpkg install cgal[core] --triplet x64-windows-static-md
vcpkg install pybind11 --triplet x64-windows-static-md
```

---

## 构建说明

本项目使用 CMake 管理构建，`CMakeLists.txt` 主要约定如下：

- `cmake_minimum_required(VERSION 3.16)`
- MSVC 平台显式设置运行时为 MultiThreadedDLL（`/MD`）或 MultiThreadedDebugDLL（`/MDd`）
- 两个库目标：`libhgp`（SHARED）与 `libhgp_static`（STATIC）
- 静态库设置 `POSITION_INDEPENDENT_CODE ON`
- 可选构建项 `BUILD_PYTHON_BINDINGS`（默认 ON），查找 pybind11 并生成 `hgp_py` 模块

### Linux（需已安装 CGAL 等依赖）

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

### 禁用 Python 绑定

```bash
cmake .. -DBUILD_PYTHON_BINDINGS=OFF
cmake --build .
```

---

## Python扩展说明

- 构建选项：`BUILD_PYTHON_BINDINGS`（ON/OFF）
- CMake 会调用 `find_package(pybind11 CONFIG REQUIRED)` 并通过 `pybind11_add_module(...)` 生成 `hgp_py` 模块
- `hgp_py` 链接到静态库 `libhgp_static`，实现自包含分发，无需额外 DLL
- 推荐在构建环境中使用与目标 Python 版本一致的解释器与 pybind11（通过 vcpkg 或系统包安装）

**部署注意：**
- 使用静态链接（`libhgp_static`）编译进 `hgp_py` 时，通常不需要额外的 DLL
- 若使用动态库 `libhgp`，则需要同时部署 `libhgp.dll`

---

## 常见配置与源码要点

- 强制在 `project()` 之前设置 CMake policy CMP0091 以控制 MSVC 运行时行为：
  ```cmake
  cmake_policy(SET CMP0091 NEW)
  ```
- MSVC 运行时配置：
  ```cmake
  set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
  ```
- 默认启用本地库路径（`local_libs`）作为 PRIVATE include
- 使用 `find_package(CGAL REQUIRED COMPONENTS Core)`，并将 `CGAL::CGAL`、`CGAL::CGAL_Core` 链接到目标
- pybind11 通过 CONFIG 模式查找并生成模块 `hgp_py`（`pybind11_add_module`）
- 静态库 `libhgp_static` 设置 `POSITION_INDEPENDENT_CODE ON` 以便安全地与共享对象链接

---

## 发布与运行时注意事项

- 构建时请确认 vcpkg triplet 与运行时选项一致（特别是 Windows MSVC 的 `/MD` vs `/MT`）
- 若打算发布 Python wheel，请确保 `hgp_py` 对应平台的运行时依赖已静态链接或打包完整
- 推荐使用 CI（例如 GitHub Actions）自动化构建，并为 Linux/Windows 提供二进制发布包

---

## 快速开始

### C++ 用户

1. 将 `libhgp/C++/` 中的所有文件复制到您的项目目录
2. 引入头文件：`#include "libhgp.h"`
3. 声明命名空间：`using namespace libhgp;`
4. 使用以下代码快速测试：

```cpp
#include <iostream>
#include "libhgp.h"
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

### Python 用户

1. 将 `libhgp/Python/` 中的所有文件复制到您的项目目录
2. 在 Python 中导入模块：`import hgp_py`
3. 使用以下代码快速测试：

```python
import hgp_py

# 测试1：2D 点到点距离
p1, p2 = [0.0, 0.0], [3.0, 4.0]
dist = hgp_py.HGP_2D_Distance_Point_Point(p1, p2)
assert abs(dist - 5.0) < 1e-9
print(f"[PASS] 测试1：HGP_2D_Distance_Point_Point({p1}, {p2}) = {dist}（期望 5.0）")

# 测试2：点在多边形内判断
polygon = [[0.0,0.0],[4.0,0.0],[4.0,4.0],[0.0,4.0]]
inside_pt, outside_pt = [2.0, 2.0], [5.0, 5.0]
assert hgp_py.HGP_2D_Location_Point_Polygon(inside_pt, polygon) == True
assert hgp_py.HGP_2D_Location_Point_Polygon(outside_pt, polygon) == False
print(f"[PASS] 测试2：点在多边形内判断通过")

# 测试3：多边形均匀采样
pts = hgp_py.HGP_2D_Polygon_Regular_Sampling_C1(polygon, 0.1)
print(f"[PASS] 测试3：HGP_2D_Polygon_Regular_Sampling_C1() → 生成 {len(pts)} 个采样点")

# 测试4：线段相交
seg1_p1, seg1_p2 = [0.0,0.0],[2.0,2.0]
seg2_p1, seg2_p2 = [0.0,2.0],[2.0,0.0]
hit, inter = hgp_py.HGP_2D_Intersection_Segment_Segment(seg1_p1, seg1_p2, seg2_p1, seg2_p2)
assert hit == True
assert abs(inter[0] - 1.0) < 1e-9 and abs(inter[1] - 1.0) < 1e-9
print(f"[PASS] 测试4：线段相交点 = {inter}（期望 [1.0, 1.0]）")

# 测试5：多边形面积
area = hgp_py.HGP_2D_Polygon_Area(polygon)
print(f"[PASS] 测试5：HGP_2D_Polygon_Area() = {area}（期望 16.0）")

# 测试6：3D 点到点距离
p3, p4 = [0.0,0.0,0.0], [1.0,1.0,1.0]
d3 = hgp_py.HGP_3D_Distance_Point_Point(p3, p4)
expected = 3**0.5
print(f"[PASS] 测试6：HGP_3D_Distance_Point_Point({p3}, {p4}) = {d3:.6f}（期望 √3 ≈ {expected:.6f}）")

print("\n✅ 所有测试通过。")
```

### Web 用户

1. 将 `libhgp/Web/` 中的所有文件复制到您的项目目录
2. 进入后端目录：`cd backend`
3. 启动本地服务器：`python -m uvicorn app:app --reload --port 8000`
4. 访问：[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 贡献

欢迎提交 Issue 或 PR。建议在贡献前先开 Issue 讨论设计或改动点，分支命名建议按功能/修复命名（例如 `feature/pybind-cleanup` 或 `fix/cmake-runtime`）。

贡献流程：

1. Fork 仓库
2. 新建分支并实现变更
3. 提交 PR，描述变更内容与测试情况
4. 等待 review 与合并

---

## 许可证

本项目使用 MIT 许可证（详见 LICENSE 文件）。如需其他许可或有合作事宜，请联系仓库维护者。

---

<div align="center">
  Made with ❤️ | 2025.02 – 2025.07
</div>
