"""
LibHGP Web 服务
后端：FastAPI
调用：hgp_py（pybind11 扩展模块）
"""

from fastapi import FastAPI,Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import hgp_py
import json

app = FastAPI(title="LibHGP Web Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 静态文件（Three.js 前端）──
app.mount("/static", StaticFiles(directory="web/static"), name="static")

@app.get("/")
async def root():
    return FileResponse("web/index.html")

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

# ════════════════════════════════════════════════
# 请求/响应模型
# ════════════════════════════════════════════════

class PointsRequest(BaseModel):
    points: list[list[float]]   # [[x,y,z], ...]

class MeshRequest(BaseModel):
    vertices:  list[list[float]]  # [[x,y,z], ...]
    face_id_0: list[int]
    face_id_1: list[int]
    face_id_2: list[int]

class SmoothRequest(BaseModel):
    vertices:  list[list[float]]
    face_id_0: list[int]
    face_id_1: list[int]
    face_id_2: list[int]
    iterations: int = 5           # 拉普拉斯迭代次数

class GeodesicRequest(BaseModel):
    mesh_path: str                # 服务端 .obj 文件路径
    source:    list[float]        # [x,y,z]
    target:    list[float]        # [x,y,z]

class SlicerRequest(BaseModel):
    mesh_path:    str
    plane_normal: list[float]     # [nx, ny, nz]
    plane_ds:     list[float]     # 一组平面偏移量

class CurvatureRequest(BaseModel):
    mesh_path:    str
    input_points: list[list[float]]

class PolygonRequest(BaseModel):
    polygon: list[list[float]]    # [[x,y], ...]  2D 点

class PolygonOffsetRequest(BaseModel):
    polygon: list[list[float]]
    distance: float


# ════════════════════════════════════════════════
# 工具函数：打包 mesh 为 JSON
# ════════════════════════════════════════════════

def mesh_response(vertices, face_id_0, face_id_1, face_id_2):
    """把顶点+面片索引打包成 Three.js BufferGeometry 友好的字典"""
    return {
        "vertices":  [coord for v in vertices for coord in v],  # 展平
        "faces":     [i for triple in zip(face_id_0, face_id_1, face_id_2)
                      for i in triple],
    }

def points_response(points):
    return {"points": [[p[0], p[1], p[2]] for p in points]}


# ════════════════════════════════════════════════
# 接口 1：3D 凸包（含面片，可直接渲染）
# 对应 HGP_3D_Convex_Hulls_C2
# ════════════════════════════════════════════════

@app.post("/api/convex_hull_3d")
def convex_hull_3d(req: PointsRequest):
    """
    输入：点云 [[x,y,z], ...]
    输出：凸包三角网格（可直接渲染）
    """
    hull_verts, fi0, fi1, fi2 = hgp_py.HGP_3D_Convex_Hulls_C2(req.points)
    return mesh_response(hull_verts, fi0, fi1, fi2)


# ════════════════════════════════════════════════
# 接口 2：拉普拉斯网格平滑
# 对应 HGP_Mesh_Laplace_Smooth_C2
# ════════════════════════════════════════════════

@app.post("/api/smooth")
def smooth(req: SmoothRequest):
    """
    输入：三角网格 + 迭代次数
    输出：平滑后的顶点（面片索引不变）
    """
    verts_out, fi0, fi1, fi2 = hgp_py.HGP_Mesh_Laplace_Smooth_C2(
        req.vertices, req.face_id_0, req.face_id_1, req.face_id_2, req.iterations
    )
    return mesh_response(verts_out, fi0, fi1, fi2)


# ════════════════════════════════════════════════
# 接口 3：网格曲率计算
# 对应 HGP_Curvature_Mesh
# ════════════════════════════════════════════════

@app.post("/api/curvature")
def curvature(req: CurvatureRequest):
    """
    输入：mesh 文件路径 + 待查询点列表
    输出：每个点的 max/min 曲率及方向（用于前端热力图着色）
    """
    max_curs, min_curs, max_dirs, min_dirs = hgp_py.HGP_Curvature_Mesh(
        req.mesh_path, req.input_points
    )
    return {
        "max_curvatures": max_curs,
        "min_curvatures": min_curs,
        "max_directions": [[d[0], d[1], d[2]] for d in max_dirs],
        "min_directions": [[d[0], d[1], d[2]] for d in min_dirs],
    }


# ════════════════════════════════════════════════
# 接口 4：最短测地路径
# 对应 HGP_Shortest_Geodesic_Path_C3
# ════════════════════════════════════════════════

@app.post("/api/geodesic_path")
def geodesic_path(req: GeodesicRequest):
    """
    输入：mesh 路径 + source/target 点
    输出：路径上的点序列（前端渲染为 THREE.Line）
    """
    path_points = hgp_py.HGP_Shortest_Geodesic_Path_C3(
        req.mesh_path, req.source, req.target
    )
    return {"path": [[p[0], p[1], p[2]] for p in path_points]}


# ════════════════════════════════════════════════
# 接口 5：网格切片（3D打印切层风格）
# 对应 HGP_Slicer_Mesh
# ════════════════════════════════════════════════

@app.post("/api/slicer")
def slicer(req: SlicerRequest):
    """
    输入：mesh路径 + 切割平面法向量 + 一组偏移量
    输出：每个平面的截面轮廓（前端渲染为 THREE.LineLoop）
    """
    offsetses, offsets = hgp_py.HGP_Slicer_Mesh(
        req.mesh_path, req.plane_normal, req.plane_ds
    )
    # offsets: List[List[Vector3d]] — 每个平面一条轮廓
    return {
        "slices": [
            {"contour": [[p[0], p[1], p[2]] for p in contour]}
            for contour in offsets
        ]
    }


# ════════════════════════════════════════════════
# 接口 6：网格分割（SDF 区域分解）
# 对应 HGP_Surface_Decomposition
# ════════════════════════════════════════════════

@app.post("/api/surface_decomposition")
def surface_decomposition(mesh_path: str):
    """
    输入：mesh 文件路径
    输出：每个面的 SDF 值 + 区域编号（前端按区域分配颜色）
    """
    face_sdf, regions_nb, face_segments = hgp_py.HGP_Surface_Decomposition(mesh_path)
    return {
        "regions_count": regions_nb,
        "face_sdf":      face_sdf,
        "face_segments": face_segments,
    }


# ════════════════════════════════════════════════
# 接口 7：2D 多边形 Offset
# 对应 HGP_2D_Polygon_One_Offsets
# ════════════════════════════════════════════════

@app.post("/api/polygon_offset_2d")
def polygon_offset_2d(req: PolygonOffsetRequest):
    """
    输入：2D 多边形顶点 + offset 距离（正=外扩，负=内缩）
    输出：offset 后的多边形组（可能分裂为多个）
    """
    result_polys = hgp_py.HGP_2D_Polygon_One_Offsets(req.polygon, req.distance)
    return {"polygons": result_polys}


# ════════════════════════════════════════════════
# 接口 8：2D 凸包
# 对应 HGP_2D_Convex_Hulls
# ════════════════════════════════════════════════

@app.post("/api/convex_hull_2d")
def convex_hull_2d(req: PolygonRequest):
    """
    输入：2D 点集
    输出：凸包顶点（按序）
    """
    hull = hgp_py.HGP_2D_Convex_Hulls(req.polygon)
    return {"hull": hull}


# ════════════════════════════════════════════════
# 接口 9：多边形采样
# 对应 HGP_2D_Polygon_Regular_Sampling_C1
# ════════════════════════════════════════════════

@app.post("/api/polygon_sampling_2d")
def polygon_sampling_2d(req: PolygonRequest, density: float = 0.05):
    """
    输入：2D 多边形 + 采样密度（对角线长度百分比）
    输出：采样点列表
    """
    pts = hgp_py.HGP_2D_Polygon_Regular_Sampling_C1(req.polygon, density)
    return {"points": pts}