import open3d as o3d
import numpy as np

# 读取PLY文件
point_cloud = o3d.io.read_point_cloud('Scaniverse 2023-07-08 003927.ply')

# 去除离群点
cl, ind = point_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)

# 体素下采样
downsampled_cloud = cl.voxel_down_sample(voxel_size=0.05)

# 法线估计
downsampled_cloud.estimate_normals()

# 平面提取
plane_model, inliers = downsampled_cloud.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=100)
plane_cloud = downsampled_cloud.select_by_index(inliers)

# 墙体提取
wall_cloud = downsampled_cloud.select_by_index(inliers, invert=True)

# 投影到平面
plane_normal = plane_model[:3]
plane_origin = plane_cloud.get_center()
projected_points = np.dot(wall_cloud.points - plane_origin, plane_normal.reshape(-1, 1))[:, :2]

# # 绘制平面
# plane_cloud.paint_uniform_color([0.7, 0.7, 0.7])
#
# # 绘制墙体
# wall_cloud.paint_uniform_color([1, 1, 1])

# 可视化结果
o3d.visualization.draw_geometries([plane_cloud, wall_cloud])
