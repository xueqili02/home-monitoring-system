import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt




def three22(plyPath,savePath):

    # 读取PLY文件
    point_cloud = o3d.io.read_point_cloud(plyPath)

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

    # 获取点云坐标
    points = np.asarray(wall_cloud.points)

    # 计算点云的中心
    center = np.mean(points, axis=0)

    # 将点云平移到原点
    centered_points = points - center

    # 计算点云的协方差矩阵
    cov_matrix = np.cov(centered_points.T)

    # 计算协方差矩阵的特征向量
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    # 选择最小特征值对应的特征向量作为平面的法线
    plane_normal = eigenvectors[:, np.argmin(eigenvalues)]

    # 将点云投影到平面
    projected_points = centered_points - np.outer(np.dot(centered_points, plane_normal), plane_normal)

    # 绘制平面图
    plt.scatter(projected_points[:, 0], projected_points[:, 1])
    plt.axis('equal')  # Set aspect ratio
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.title('Aligned Projection')
    plt.savefig(savePath)
    plt.show()





three22('zoulang.ply','111.jpg')