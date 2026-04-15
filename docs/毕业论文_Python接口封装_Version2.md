## Python 接口封装：基于 pybind11 的 C++ 库绑定

为使 C++ 几何处理库 `libhgp` 能在 Python 环境中调用，采用 pybind11 框架完成绑定层开发。整体工作分为三个环节：绑定文件编写、CMake 构建配置、以及 Python 功能验证。

---

### 一、绑定文件编写（`hgp_py.cpp`）

绑定层的核心工作包括两部分：类型转换辅助函数的实现，以及对 `libhgp.h` 中全部 HGP 系列函数的逐一绑定。

#### 1. 类型转换辅助函数

由于 `libhgp` 使用自定义向量类型（`Vector2d`、`Vector3d`、`Vector2d1`、`Vector3d1` 等），而 Python 侧使用嵌套 `list`，需编写一组双向转换函数：

```cpp name=hgp_py.cpp url=https://github.com/xinyi-0509/dev-retry/blob/4159cac727ec8a5cbef56917dd329575bb0587bf/hgp_py.cpp#L14-L57
// 标量向量互转
static inline Vector2d  to_vec2d (const std::vector<double>& v) {
    if (v.size()<2) throw std::runtime_error("need >=2 doubles for Vector2d");
    return Vector2d(v[0],v[1]);
}
static inline Vector3d  to_vec3d (const std::vector<double>& v) {
    if (v.size()<3) throw std::runtime_error("need >=3 doubles for Vector3d");
    return Vector3d(v[0],v[1],v[2]);
}
static inline std::vector<double> from_vec2d(const Vector2d& v){ return {v.x,v.y}; }
static inline std::vector<double> from_vec3d(const Vector3d& v){ return {v.x,v.y,v.z}; }

// 向量列表互转（Vector2d1 ↔ list[list[float]]）
static inline Vector2d1 to_vec2d1(const std::vector<std::vector<double>>& vs){
    Vector2d1 r; r.reserve(vs.size());
    for(auto& v:vs) r.push_back(to_vec2d(v)); return r;
}
static inline std::vector<std::vector<double>> from_vec2d1(const Vector2d1& vs){
    std::vector<std::vector<double>> r; r.reserve(vs.size());
    for(auto& v:vs) r.push_back(from_vec2d(v)); return r;
}
```

#### 2. 函数绑定

在 `PYBIND11_MODULE` 宏中，对 `libhgp.h` 声明的全部 HGP 函数完成绑定。每个绑定以 lambda 包装器实现类型转换，示例如下：

```cpp name=hgp_py.cpp url=https://github.com/xinyi-0509/dev-retry/blob/4159cac727ec8a5cbef56917dd329575bb0587bf/hgp_py.cpp#L65-L70
PYBIND11_MODULE(hgp_py, m) {

    // 2D 两点距离
    m.def("HGP_2D_Distance_Point_Point",
        [](const std::vector<double>& p0,
           const std::vector<double>& p1) -> double {
            return HGP_2D_Distance_Point_Point(to_vec2d(p0), to_vec2d(p1));
        }, py::arg("p_0"), py::arg("p_1"), "2D两点欧氏距离。");

    // 判断点是否在多边形内
    m.def("HGP_2D_Location_Point_Polygon",
        [](const std::vector<double>& p,
           const std::vector<std::vector<double>>& py_) -> bool {
            return HGP_2D_Location_Point_Polygon(to_vec2d(p), to_vec2d1(py_));
        }, py::arg("p"), py::arg("py"), "判断2D点是否在多边形内。");

    // 3D 平面拟合
    m.def("HGP_3D_Plane_Fitting",
        [](const std::vector<std::vector<double>>& points)
           -> std::pair<std::vector<double>, std::vector<double>> {
            Vector3d plane_p, plane_n;
            HGP_3D_Plane_Fitting(to_vec3d1(points), plane_p, plane_n);
            return {from_vec3d(plane_p), from_vec3d(plane_n)};
        }, py::arg("points"), "3D点集平面拟合，返回平面点与法向量。");

    // ... 其余函数同法绑定
}
```

绑定覆盖的函数类别如下表所示：

| 类别 | 函数数量 | 代表函数 |
|------|:-------:|---------|
| IO | 2 | `HGP_Vector_Base`、`HGP_Test_PGL` |
| 2D 距离计算 | 8 | `HGP_2D_Distance_Point_Point`、`HGP_2D_Distance_Polygon_Polygon`、`HGP_2D_Distance_Point_Polygons` |
| 2D 位置判断 | 2 | `HGP_2D_Location_Point_Polygon`、`HGP_2D_Location_Points_Polygon` |
| 2D 采样 | 7 | `HGP_2D_Polygon_Dart_Sampling`、`HGP_2D_Polygon_Regular_Sampling_C1/C2/C3`、`HGP_2D_Square_Regular_Sampling_C1/C2/C3` |
| 2D 求交 | 6 | `HGP_2D_Intersection_Segment_Segment`、`HGP_2D_Intersection_Line_Line`、`HGP_2D_Intersection_Segment_Polygon`、`HGP_2D_Intersection_Polygon_Polygon` |
| 2D 多边形操作 | 33 | `HGP_2D_Polygon_Area`、`HGP_2D_Detect_Polygon_Inside_C1~C5`、`HGP_2D_Convex_Hulls`、`HGP_2D_OBB_Box`、`HGP_2D_Polygon_Triangulation_C1/C2/C3` |
| 3D 距离计算 | 6 | `HGP_3D_Distance_Point_Point`、`HGP_3D_Distance_Point_Plane`、`HGP_3D_Distance_Segment_Segment` |
| 3D 投影与平面 | 15 | `HGP_3D_Plane_Fitting`、`HGP_3D_Projection_Point_Plane_C1/C2`、`HGP_3D_Plane_3D_to_2D_Points` |
| 3D 求交 | 4 | `HGP_3D_Intersection_Segment_Plane`、`HGP_3D_Intersection_Line_Plane`、`HGP_3D_Intersection_Segment_Segment` |
| 3D 其他 | 2 | `HGP_Face_Normal`、`HGP_3D_One_Triangle_Area` |
| 网格操作（HGPMESH） | 62 | `HGP_3D_Intersection_Ray_Mesh`、`HGP_3D_Mesh_Curvature_C1~C6`、`HGP_Shortest_Geodesic_Path_C1/C3/C4`、`HGP_Cut_Surface` |
| **合计** | **147** | |

---

### 二、CMake 构建配置

项目使用 CMake 管理构建流程，`CMakeLists.txt` 按照以下逻辑顺序组织各项配置工作。

#### 1. 声明 CMP0091 策略

`MSVC_RUNTIME_LIBRARY` 属性（用于控制 `/MD`、`/MDd` 等运行时库选项）依赖 CMake 策略 `CMP0091`。该策略**必须在 `project()` 之前声明**，否则后续的运行时库设置将不生效：

```cmake name=CMakeLists.txt url=https://github.com/xinyi-0509/dev-retry/blob/4159cac727ec8a5cbef56917dd329575bb0587bf/CMakeLists.txt#L1-L11
cmake_minimum_required(VERSION 3.16)

# CMP0091 必须在 project() 之前声明！
cmake_policy(SET CMP0091 NEW)

project(libhgp)

# 统一所有目标的运行时库，与 vcpkg x64-windows-static-md triplet 保持一致
if(MSVC)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
endif()
```

#### 2. 设置 UTF-8 编译选项

MSVC 默认以系统代码页（GBK）解析源文件，导致中文字符串字面量在编译时报错（C2001）。在 `project()` 之后、任何 `add_library` 之前，通过 `add_compile_options(/utf-8)` 全局启用 UTF-8，使所有后续目标均继承该选项：

```cmake name=CMakeLists.txt url=https://github.com/xinyi-0509/dev-retry/blob/4159cac727ec8a5cbef56917dd329575bb0587bf/CMakeLists.txt#L13-L18
set(CMAKE_CXX_STANDARD 17)

if(MSVC)
    add_definitions(-D_CRT_SECURE_NO_WARNINGS)
    add_compile_options(/utf-8)   # 修复中文字符串编译错误
endif()
```

#### 3. 构建 libhgp 静态库

将 `libhgp` 的全部源文件编译为静态库 `libhgp_static`，供后续的 Python 扩展模块静态链接。静态链接的目的是使最终生成的 `.pyd` 文件自包含，分发时无需携带 `libhgp.dll`：

```cmake name=CMakeLists.txt url=https://github.com/xinyi-0509/dev-retry/blob/4159cac727ec8a5cbef56917dd329575bb0587bf/CMakeLists.txt#L59-L75
# 静态库版本，用于 hgp_py 静态链接
add_library(libhgp_static STATIC ${LIBHGP_SOURCES})

# 启用位置无关代码（PIC），兼容 pybind11 模块的共享库要求
set_target_properties(libhgp_static PROPERTIES POSITION_INDEPENDENT_CODE ON)

target_include_directories(libhgp_static
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}/local_libs
)

target_link_libraries(libhgp_static
    PRIVATE
        CGAL::CGAL
        CGAL::CGAL_Core
)
```

#### 4. 通过 vcpkg 寻找 pybind11 并链接静态库

在确认静态库已定义之后，通过 vcpkg 的 CMake 工具链查找 pybind11，再使用 `pybind11_add_module` 创建 Python 扩展模块目标，最后将 `libhgp_static` 以 `PRIVATE` 方式链接进去。`PRIVATE` 保证静态库的符号不会传递暴露给 Python 层，符合扩展模块的封装要求：

```cmake name=CMakeLists.txt url=https://github.com/xinyi-0509/dev-retry/blob/4159cac727ec8a5cbef56917dd329575bb0587bf/CMakeLists.txt#L77-L91
option(BUILD_PYTHON_BINDINGS "Build Python bindings with pybind11" ON)
if(BUILD_PYTHON_BINDINGS)
    find_package(pybind11 CONFIG REQUIRED)   # 通过 vcpkg 工具链查找
    pybind11_add_module(hgp_py hgp_py.cpp)

    # 将 libhgp_static 全部代码打包进 .pyd，运行时无需外部 dll
    target_link_libraries(hgp_py PRIVATE libhgp_static)

    # 隐藏非必要符号，减小 .pyd 体积并避免符号冲突
    set_target_properties(hgp_py PROPERTIES
        CXX_VISIBILITY_PRESET hidden
        VISIBILITY_INLINES_HIDDEN ON
    )
endif()
```

四步配置的依赖关系如下：

```
① 声明 CMP0091（project 前）
        ↓
  project() + 运行时库统一
        ↓
② 全局 /utf-8（作用于所有后续目标）
        ↓
③ 编译 libhgp_static（依赖 /utf-8 已设置）
        ↓
④ find pybind11 → pybind11_add_module → 链接 libhgp_static
```

#### 5. Release 构建命令

构建 Release 版本的完整 CMake 命令如下：

```bash name=build_release.bat
cmake -S . -B build ^
  -G "Visual Studio 16 2019" -A x64 ^
  -DCMAKE_TOOLCHAIN_FILE=D:/devtools/vcpkg/scripts/buildsystems/vcpkg.cmake ^
  -DVCPKG_TARGET_TRIPLET=x64-windows-static-md

cmake --build build --config Release --target hgp_py
```

构建成功后，在 `build/Release/` 目录下生成扩展模块文件：

```
hgp_py.cp312-win_amd64.pyd
```

该文件为自包含模块，已将 `libhgp_static.lib`、CGAL 等全部依赖静态链接进 `.pyd` 内部，分发时无需附带任何额外动态库。

---

### 三、Python 功能验证

构建完成后，编写测试脚本验证核心几何接口的正确性：

```python name=test_hgp.py
import sys
sys.path.insert(0, r"D:\GP\dev-retry\build\Release")

import hgp_py

# ── 测试1：2D 两点距离 ──────────────────────────────────
dist = hgp_py.HGP_2D_Distance_Point_Point([0.0, 0.0], [3.0, 4.0])
assert abs(dist - 5.0) < 1e-9
print(f"[PASS] HGP_2D_Distance_Point_Point: {dist}")        # 期望 5.0

# ── 测试2：点是否在多边形内 ──────────────────────────────
polygon = [[0.0,0.0],[4.0,0.0],[4.0,4.0],[0.0,4.0]]
assert hgp_py.HGP_2D_Location_Point_Polygon([2.0, 2.0], polygon) == True
assert hgp_py.HGP_2D_Location_Point_Polygon([5.0, 5.0], polygon) == False
print("[PASS] HGP_2D_Location_Point_Polygon")

# ── 测试3：多边形规则采样 ────────────────────────────────
pts = hgp_py.HGP_2D_Polygon_Regular_Sampling_C1(polygon, 0.1)
assert len(pts) > 0
print(f"[PASS] HGP_2D_Polygon_Regular_Sampling_C1: {len(pts)} 个采样点")

# ── 测试4：线段求交 ──────────────────────────────────────
hit, inter = hgp_py.HGP_2D_Intersection_Segment_Segment(
    [0.0,0.0],[2.0,2.0],[0.0,2.0],[2.0,0.0])
assert hit == True
assert abs(inter[0] - 1.0) < 1e-9 and abs(inter[1] - 1.0) < 1e-9
print(f"[PASS] HGP_2D_Intersection_Segment_Segment: 交点 {inter}")

# ── 测试5：多边形面积 ────────────────────────────────────
area = hgp_py.HGP_2D_Polygon_Area(polygon)
assert abs(area - 16.0) < 1e-9
print(f"[PASS] HGP_2D_Polygon_Area: {area}")

# ── 测试6：3D 两点距离 ───────────────────────────────────
d3 = hgp_py.HGP_3D_Distance_Point_Point([0.0,0.0,0.0],[1.0,1.0,1.0])
assert abs(d3 - 3**0.5) < 1e-9
print(f"[PASS] HGP_3D_Distance_Point_Point: {d3:.6f}")

print("\n全部测试通过。")
```

运行结果如下：

```
[PASS] HGP_2D_Distance_Point_Point: 5.0
[PASS] HGP_2D_Location_Point_Polygon
[PASS] HGP_2D_Polygon_Regular_Sampling_C1: 121 个采样点
[PASS] HGP_2D_Intersection_Segment_Segment: 交点 [1.0, 1.0]
[PASS] HGP_2D_Polygon_Area: 16.0
[PASS] HGP_3D_Distance_Point_Point: 1.732051

全部测试通过。
```

上述测试验证了 2D/3D 距离计算、点面位置判断、多边形采样、线段求交及面积计算等核心几何功能均能通过 Python 接口正确调用，结果与理论值误差在 $10^{-9}$ 量级以内，满足精度要求。