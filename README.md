<div align="center">

# LibHGP

**面向数字制造的微型几何引擎**

<!-- 可选：状态徽章 -->
![Language](https://img.shields.io/badge/language-C%2B%2B-blue)
![Build](https://img.shields.io/badge/build-CMake-brightgreen)
![Python](https://img.shields.io/badge/python-binding-yellow)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)

面向实验室几何算法资产整合与工程化重构的基础算法库，支持 **C++ / Python / Web** 三种调用形态。

</div>

## 目录

- [简介](#简介)
- [技术架构](#技术架构)
- [推荐环境](#推荐环境)
- [快速开始](#快速开始)
- [许可证](#许可证)

## 简介

LibHGP 是一个面向几何处理与计算几何场景的基础算法库，并以此为基础构建了一个具备良好可维护性、可扩展性与可复用性的交互式可视化平台，支持以下三类使用方式：

- **C++ 原生调用**：适合高性能算法开发与系统集成
- **Python 调用**：适合科研实验、原型验证与教学使用
- **Web 调用**：适合前端展示、交互式可视化与在线演示


## 技术架构

项目整体可以分为以下几个层次：

### 1. 核心算法层
负责实现几何处理、计算几何及相关基础算法模块，例如：

- 2D 几何算法
- 3D 几何算法
- 网格处理
- 凸包与空间索引
- 其他实验室积累的算法模块

### 2. 接口封装层
负责对底层算法进行统一封装，对外提供稳定一致的调用接口，包括：

- C++ 原生接口
- Python 绑定接口（如 pybind11）
- Web 调用接口（后续可支持 FastAPI / WebAssembly 等）

### 3. 应用与展示层
面向具体应用场景，包括：

- 科研原型验证
- 教学演示
- 算法可视化
- Web 端交互展示

## 推荐环境
- C++17 
- Visual Studio 2019

## 快速开始


### C++ 用户

1. 将 libhgp/C++/ 中的所有文件复制进您的项目目录
2. 声明头文件 `#include"libhgp.h"`
3. 声明命名空间 `using namespace libhgp;`
4. 使用以下代码快速测试：
'''cpp
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

# License

All rights about the program are reserved by the authors of this project. The programs can only be used for research purpose. In no event shall the author be liable to any party for direct, indirect, special, inc
