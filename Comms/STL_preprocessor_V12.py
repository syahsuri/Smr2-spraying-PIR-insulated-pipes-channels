import open3d as o3d
import numpy as np
import math
import copy
import os
import datetime
import json

""""
Classes
"""
class object:
    def __init__(self,mesh):
        self.mesh = mesh
        self.pointcloud = np.asarray(self.mesh.vertices)
        self.maximums = {"X_max": np.max(self.pointcloud[:,0]),
                         "X_min": np.min(self.pointcloud[:,0]),
                         "Y_max": np.max(self.pointcloud[:,1]),
                         "Y_min": np.min(self.pointcloud[:,1]),
                         "Z_max": np.max(self.pointcloud[:,2]),
                         "Z_min": np.min(self.pointcloud[:,2]) }
    
    def vertices(self):
        return self.mesh.triangles
    def vertices_np(self):
        return np.asarray(self.mesh.triangles)

class point:
    def __init__(self,x,y,z,i):
        
        self.X = x
        self.Y = y
        self.Z = z
        self.nmb = i #number used in indexing with open3d mesh
        self.X_line = False
        self.Y_line = False
        self.Z_line = False

    def __str__(self):
     return f"point {self.nmb} - X:{self.X} Y:{self.Y} Z:{self.Z}"
    
    def np_point(self):
        return [self.X,self.Y,self.Z]

class line:
    def __init__(self,points):
        self.points = points

class surface:
    def __init__(self,lines):
        self.lines = lines


""""
Functions
"""

def mesh_to_point_cloud(mesh):
    # xyz = np.asarray(mesh.vertices)

    pcd = mesh.sample_points_poisson_disk(number_of_points=5000)
    mesh.compute_vertex_normals()
    xyz = np.append(np.asarray(mesh.vertices),np.asarray(pcd.points),axis=0)
    return xyz

def pointcloud_to_points(pointcloud):
    nmb_of_points = pointcloud.shape[0]
    pointlist = [point(pointcloud[i, 0], pointcloud[i, 1], pointcloud[i, 2],i) for i in range(nmb_of_points)]
    return pointlist

def find_unique_points(points): 
        seen = []
        unique_points = []
        for point in points:
            if point.np_point() not in seen:
                seen.append(point.np_point())
                unique_points.append(point)
        return unique_points




def orient_mesh(mesh):
    #define some general parameters of mesh
    pointcloud = mesh_to_point_cloud(mesh)
    points = pointcloud_to_points(pointcloud)
    vertices = np.asarray(mesh.triangles)
    maximums = {"X_max": np.max(pointcloud[:,0]),
                "X_min": np.min(pointcloud[:,0]),
                "Y_max": np.max(pointcloud[:,1]),
                "Y_min": np.min(pointcloud[:,1]),
                "Z_max": np.max(pointcloud[:,2]),
                "Z_min": np.min(pointcloud[:,2]) }

    #find possible orientation planes (ground planes)
    #ground planes are defined as maximum/outside surfaces where product can stand on
    def find_ground_planes(points):
        #find maximum points in XYZ +/- directions
        TH = 0.00001 #threshold range for inaccuracies in STL model
        ground_planes = []
        ground_planes.append([[point for point in points if maximums["X_max"]-TH < point.X < maximums["X_max"]+TH],"X+"])
        ground_planes.append([[point for point in points if maximums["X_min"]-TH < point.X < maximums["X_min"]+TH],"X-"])
        ground_planes.append([[point for point in points if maximums["Y_max"]-TH < point.Y < maximums["Y_max"]+TH],"Y+"])
        ground_planes.append([[point for point in points if maximums["Y_min"]-TH < point.Y < maximums["Y_min"]+TH],"Y-"])
        ground_planes.append([[point for point in points if maximums["Z_max"]-TH < point.Z < maximums["Z_max"]+TH],"Z+"])
        ground_planes.append([[point for point in points if maximums["Z_min"]-TH < point.Z < maximums["Z_min"]+TH],"Z-"])
        
        #Delete plane if there are less than 4 points (assumed rectangle)
        ground_planes = [ plane for plane in ground_planes if len(plane[0]) >= 4]
        
        #Find connections and delete when there are is a connection between 3 points on a plane (filled surface)
        def check_connections(plane):
            points_nmb = [point.nmb for point in plane[0]]
            for row in vertices:
                if np.isin(row,points_nmb).sum()>2:
                   return True
            return False
        ground_planes = [groundplane for groundplane in ground_planes if check_connections(groundplane) == False]
        
        return ground_planes
    
    #filter gound ground planes and define ground plane
    def filter_ground_planes (ground_planes):
        #find length of diagonal acros ground plane
        def size_gnd(ground_plane):
            points = ground_plane [0]
            dir = ground_plane[1][0]
            if dir[0] == "X":
                A = [max(point.Y for point in points),max(point.Z for point in points)]
                B = [min(point.Y for point in points),min(point.Z for point in points)]
            elif dir[0] == "Y":
                A = [max(point.X for point in points),max(point.Z for point in points)]
                B = [min(point.X for point in points),min(point.Z for point in points)]
            elif dir[0] == "Z":
                A = [max(point.X for point in points),max(point.Y for point in points)]
                B = [min(point.X for point in points),min(point.Y for point in points)]
            
            size = math.dist(A, B)
            return size
        
        #find lenght up from groundplane
        def height_from_gnd (ground_plane):
            dir = ground_plane [1][0]
            match dir:
                case "X": height = maximums["X_max"] - maximums["X_min"] 
                case "Y": height = maximums["Y_max"] - maximums["Y_min"]
                case "Z": height = maximums["Z_max"] - maximums["Z_min"]  
            return height
    
        #choose plane based on size of plane and height from plane
        def filter(ground_plane):
            filter = (1*size_gnd(ground_plane) + 1*height_from_gnd(ground_plane))
            return filter
        ground_plane = max(ground_planes, key=filter)
        
        return ground_plane

    #Translate mesh to have one point of groundplane at (0,0,0)
    def translate_mesh(mesh,ground_plane):

        gnd_point = copy.copy(ground_plane[0][3]) #just get one point on groundplane 
        translate_mesh = copy.deepcopy(mesh).translate((-gnd_point.X, -gnd_point.Y, -gnd_point.Z), relative=True)
        
        #translate groundplane itself as well
        for point in ground_plane[0]:
            point.X = point.X - gnd_point.X
            point.Y = point.Y - gnd_point.Y
            point.Z = point.Z - gnd_point.Z
    
        return translate_mesh,ground_plane
    
    #Rotate mesh to have all points in positive direction and Z+ in vertical upwards
    def rotate_mesh(mesh,ground_plane):
        #rotate mesh to get positive Z direction
        dir = ground_plane[1]
        match dir:
            case "X+":R = mesh.get_rotation_matrix_from_xyz((0              ,  0.5* math.pi , 0))
            case "X-":R = mesh.get_rotation_matrix_from_xyz((0              , -0.5* math.pi , 0))
            case "Y+":R = mesh.get_rotation_matrix_from_xyz((-0.5* math.pi  , 0             , 0))
            case "Y-":R = mesh.get_rotation_matrix_from_xyz(( 0.5* math.pi  , 0             , 0))
            case "Z+":R = mesh.get_rotation_matrix_from_xyz((   1* math.pi  , 0             , 0))
            case "Z-":R = mesh.get_rotation_matrix_from_xyz((0              , 0             , 0))
        rotated_mesh_1 = copy.deepcopy(mesh).rotate(R, center=(0, 0, 0))
        
        #rotate mesh to get positive X and Y direction
        rotated_mesh_points = np.asarray(rotated_mesh_1.vertices)
        if abs(np.min(rotated_mesh_points[:,0])) < abs(np.max(rotated_mesh_points[:,0])):
              dirX = "X+"
        else: dirX = "X-"
        if abs(np.min(rotated_mesh_points[:,1])) < abs(np.max(rotated_mesh_points[:,1])):
              dirY = "Y+"
        else: dirY = "Y-"

        match [dirX, dirY]:
            case ["X+","Y+"]: R = mesh.get_rotation_matrix_from_xyz((0,0,0))
            case ["X+","Y-"]: R = mesh.get_rotation_matrix_from_xyz((0,0, 0.5* math.pi))
            case ["X-","Y+"]: R = mesh.get_rotation_matrix_from_xyz((0,0,-0.5* math.pi))
            case ["X-","Y-"]: R = mesh.get_rotation_matrix_from_xyz((0,0,   1* math.pi))
        rotated_mesh_2 = copy.deepcopy(rotated_mesh_1).rotate(R, center=(0, 0, 0))
        
        return rotated_mesh_2

    #find ground possible groundplanes (open ended maximums)
    ground_planes = find_ground_planes (points)
    #filter ground planes on different variables
    ground_plane  = filter_ground_planes (ground_planes)
    #translate part to groundpoint
    translated_mesh,ground_plane = translate_mesh(mesh,ground_plane)
    #rotate part for z+ in vertical upwards direction
    orientated_mesh = rotate_mesh(translated_mesh,ground_plane)
    # orientated_object = None
    return orientated_mesh

def define_lines (points,dir,tolerance=0):
    lines = []
    match dir:
        case"X": XYZ = 0
        case"Y": XYZ = 1
        case"Z": XYZ = 2
        case _ : print("give X/Y/Z")

    #find unique points
    unique_points = find_unique_points (points)

    #find lines (match case for each axis)
    match XYZ:
        case 0:
            #loop over every point
            for point in unique_points:
                #define search fields
                search_field_Y = [point.Y * (1-tolerance),point.Y * (1+tolerance)]
                search_field_Z = [point.Z * (1-tolerance),point.Z * (1+tolerance)]
                #find matching points
                match_points = [point for point in unique_points if search_field_Y[0] <= point.Y <= search_field_Y[1] 
                                                                and search_field_Z[0] <= point.Z <= search_field_Z[1]]
                
            #set label and delete points used for line
                for point in match_points:
                    point.X_line = True
                unique_points = [point for point in unique_points if point.X_line == False]
            #check if there are points to connect and save in a new line
                if len(match_points) > 1:
                    lines.append(line(match_points))
        case 1:
            #loop over every point
            for point in unique_points:
            #define search fields
                search_field_X = [point.X * (1-tolerance),point.X * (1+tolerance)]
                search_field_Z = [point.Z * (1-tolerance),point.Z * (1+tolerance)]
            #find matching points
                match_points = [point for point in unique_points if search_field_X[0] <= point.X <= search_field_X[1] 
                                                                and search_field_Z[0] <= point.Z <= search_field_Z[1]]
                
            #set label and delete points used for line
                for point in match_points:
                    point.Y_line = True
                unique_points = [point for point in unique_points if point.Y_line == False]
            #check if there are points to connect and save in a new line
                if len(match_points) > 1:
                    lines.append(line(match_points))
        case 2:
            #loop over every point
            for point in unique_points:
            #define search fields
                search_field_X = [point.X * (1-tolerance),point.X * (1+tolerance)]
                search_field_Y = [point.Y * (1-tolerance),point.Y * (1+tolerance)]
            #find matching points
                match_points = [point for point in unique_points if search_field_X[0] <= point.X <= search_field_X[1] 
                                                                and search_field_Y[0] <= point.Y <= search_field_Y[1]]
                
            #set label and delete points used for line
                for point in match_points:
                    point.Z_line = True
                unique_points = [point for point in unique_points if point.Z_line == False]
            #check if there are points to connect and save in a new line
                if len(match_points) > 1:
                    lines.append(line(match_points))
    
    

    return lines

def define_surfaces(lines,dir,tolerance=0):
    surfaces = []
    match dir:
        case"X": XYZ = 0
        case"Y": XYZ = 1
        case"Z": XYZ = 2
        case _ : print("give X/Y/Z")

    def Find_corner(line,dir):
        match dir:
            case 0:point = min(line.points, key=lambda point: point.X)
            case 1:point = min(line.points, key=lambda point: point.Y)
            case 2:point = min(line.points, key=lambda point: point.Z)
        return point

    sorted_lines = sorted(lines, key=lambda line: Find_corner(line,XYZ).Z)

    for line in lines:
        corner_point = Find_corner(line,XYZ)



    return surfaces

#creating line set for displaying lines
def create_line_set(lines,color):
    draw_points = []
    draw_lines = []
    i=0
    for line in lines:
        for point in line.points:
            draw_points.append([point.X,point.Y,point.Z])
        draw_lines.append([i,i+1])
        i += 2

    colors = [color for i in range(len(draw_lines))]
    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(draw_points)
    line_set.lines = o3d.utility.Vector2iVector(draw_lines)
    line_set.colors = o3d.utility.Vector3dVector(colors)
    return line_set
    # o3d.visualization.draw_geometries([line_set])

#create image to check orientation in 
def create_orientation_image(path,mesh):
    # Create a visualizer object
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible=False,width = 900,height = 900) # Set to True if you want to see the windows

    #change render options
    opt = vis.get_render_option()
    opt.mesh_show_back_face = True

    #draw geometrys
    coordination = o3d.geometry.TriangleMesh.create_coordinate_frame(size = 150)
    vis.add_geometry(coordination)

    carrier_top = o3d.geometry.TriangleMesh.create_box(600,600,6,True)
    carrier_top.paint_uniform_color([1,0.706,0])
    carrier_bottom = o3d.geometry.TriangleMesh.create_box(450,450,70,True)
    carrier_bottom.translate((75,75,-76))
    carrier_bottom.paint_uniform_color([0.7,0.7,0.7])

    carrier = carrier_top + carrier_bottom

    carrier.translate((-20,-20,-20))
    carrier.compute_vertex_normals()
    vis.add_geometry(carrier)


    mesh.compute_vertex_normals()
    vis.add_geometry(mesh)
    vis.update_geometry(mesh)

    #change camera view
    ctr = vis.get_view_control()
    parameters = o3d.io.read_pinhole_camera_parameters("\Camera_settings.json")
    ctr.convert_from_pinhole_camera_parameters(parameters)    
    vis.update_renderer()

    #save picture
    vis.capture_screen_image(path,True)

    # Destroy the window
    vis.destroy_window()

def create_meta_data(mesh,name):
    meta_data = {}
    
    meta_data["time"]   = str(datetime.datetime.now())
    meta_data["name"]   = name
    meta_data["origin"] = [0,0,0] #origin of STL

    bounding_box = o3d.geometry.AxisAlignedBoundingBox.create_from_points(mesh.vertices)
    box_points = np.absolute(np.round(np.asarray(bounding_box.get_box_points()),0))
    meta_data["max_X"], meta_data["max_Y"], meta_data["max_Z"] = box_points.max(axis=0)
    meta_data["min_X"], meta_data["min_Y"], meta_data["min_Z"] = box_points.min(axis=0)
    
    box_points = box_points[np.lexsort((box_points[:,0], box_points[:,1],box_points[:,2]))]
    box_points = box_points.tolist()
    
    #find number of faces:

    if (np.asarray(mesh.triangle_normals)[:,2]>0.8).any():
        if (np.asarray(mesh.triangle_normals)[:,2]<-0.8).any():
            meta_data["Nmb_of_faces_to_spray"] = 6
        else:
            meta_data["Nmb_of_faces_to_spray"] = 5
    else: 
        meta_data["Nmb_of_faces_to_spray"] = 4
    
    meta_data["face_0"] = [box_points[0],box_points[3],box_points[4],box_points[7]]
    meta_data["face_1"] = [box_points[0],box_points[1],box_points[4],box_points[5]]
    meta_data["face_2"] = [box_points[1],box_points[2],box_points[5],box_points[6]]
    meta_data["face_3"] = [box_points[2],box_points[3],box_points[6],box_points[7]]
    meta_data["face_4"] = [box_points[4],box_points[5],box_points[6],box_points[7]]
    meta_data["face_5"] = [box_points[0],box_points[1],box_points[2],box_points[3]]

    return meta_data  

def save_meta_data_to_json(path,data):
    with open(path, "w") as outfile: 
        json.dump(data, outfile)
    return None


"""
temporary functions
"""
def ABC (mesh):
    def stringify(point):
        point = [point[0],point[1],point[2]] 
        match point:
            case [-400,0,-300]: return "A"
            case [400 ,0,-300]: return"B"
            case [400,0,300]: return"C"
            case [-400 ,0,300]: return"D"
            case [-400,1000,-300]: return"E"
            case [400 ,1000,-300]: return"F"
            case [400,1000,300]: return"G"
            case [-400 ,1000,300]: return"H"
 
    puntlist = [stringify(point) for point in np.asarray(mesh.vertices)]
    return puntlist


"""
External use functions
"""
def process_STL(file_dir,save_orientated_stl,save_meta_data,save_image,save_dir):
    
    #orientate mesh    
    orientated_mesh = orient_mesh (o3d.io.read_triangle_mesh(file_dir))
    #create meta_data
    meta_data = create_meta_data(orientated_mesh,"Product")
    
    if save_orientated_stl == True:
        #save orientated mesh
        o3d.io.write_triangle_mesh(os.path.join(save_dir, "Product.stl"), orientated_mesh)

    if save_meta_data == True:
        #save meta_data
        save_meta_data_to_json(os.path.join(save_dir, "Product_metadata.json"),meta_data)

    if save_image == True:
        #create and save image of mesh
        create_orientation_image(os.path.join(save_dir, "Render.png"),orientated_mesh)
    
def main(file_dir):
    #open file
    # file_dir = "Objects/test part3 Corner.STL"
    # file_dir = "Objects/test part4 surface duct.STL"
    # file_dir = "Objects/test part5 straight.STL"
    # file_dir = "Objects/test part6 duct.STL"
    # file_dir = "Objects/test part7 Corner.STL"
    # file_dir = "Objects/test part8 Corner.STL"

    #orientate mesh    
    orientated_mesh = orient_mesh (o3d.io.read_triangle_mesh(file_dir))
    #create image of mesh
    create_orientation_image(os.path.join(save_dir, "Render.png"),orientated_mesh)
    #save orientated mesh
    o3d.io.write_triangle_mesh("RoboDK path/TEMP_FILES/Product.stl", orientated_mesh)

    o3d_bbox = o3d.geometry.OrientedBoundingBox



    #create product from orientated mesh
    Product = object(orientated_mesh)
   


    points = pointcloud_to_points(Product.pointcloud)

    lines_X =define_lines(points,"X")
    lines_Y =define_lines(points,"Y")
    lines_Z =define_lines(points,"Z")





    Visualize = True
    if Visualize == True:
        Draw_lines_X = create_line_set(lines_X,[1,0,0])
        Draw_lines_Y = create_line_set(lines_Y,[0,1,0])
        Draw_lines_Z = create_line_set(lines_Z,[0,0,1])

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(Product.pointcloud)
        coordination = o3d.geometry.TriangleMesh.create_coordinate_frame(size = 150)
        orientated_mesh.compute_vertex_normals()
        Product.mesh.compute_vertex_normals()
        
        vis = o3d.visualization.Visualizer()
        vis.create_window(width=900,height=900, left=50,top=50)
        vis.add_geometry(coordination)
        vis.add_geometry(pcd)
        vis.add_geometry(Draw_lines_X)
        vis.add_geometry(Draw_lines_Y)
        vis.add_geometry(Draw_lines_Z)
        vis.add_geometry(Product.mesh)

        opt = vis.get_render_option()
        opt.line_width = 10
        opt.point_size = 5
        opt.mesh_show_back_face = True

        vis.run()




""""
Program
"""
if __name__ == "__main__":
    # file_dir = "Final products\Duct_1_Straight_small.STL"
    # file_dir = "Final products\Duct_2_Straight_large.STL"
    # file_dir = "Final products\Duct_3_Funnel.STL"
    file_dir = "Final products\Duct_4_Jump.STL"
   
    save_dir = "C:/Users/tieme/Documents/School/Semester_7 (Minor)/SMR2/Code/RoboDK_python/Process_files"
    process_STL(file_dir,True,True,True,save_dir)
    # main(file_dir)