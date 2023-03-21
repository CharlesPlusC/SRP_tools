import open3d as o3d

path_to_analyse = "/Users/charlesc/Documents/GitHub/SRP_tools/GOCE_sag50.stl"
path_to_save = "/Users/charlesc/Documents/GitHub/SRP_tools/GOCE_sag50_inhouse.stc"

### First function attempt

def stl_to_inhouse(file_path, output_path, max_shapes=200):
    # Load the STL file
    o3d_mesh = o3d.io.read_triangle_mesh(file_path)
    
    # Perform mesh simplification using open3d
    simplified_o3d_mesh = o3d_mesh.simplify_quadric_decimation(target_number_of_triangles=max_shapes)
    
    # Visualize the simplified mesh
    visualize_mesh(simplified_o3d_mesh)

    # Initialize an empty list to store the components in the in-house format
    components = []

    # Convert the simplified mesh to the in-house format
    for face in simplified_o3d_mesh.faces:
        # Extract the relevant information from the face
        # (e.g., vertices, normal vector, etc.)

        # Convert the information into the in-house format
        # (e.g., component header, geometry, etc.)

        # Append the component to the components list
        pass

    # Write the components to the output file
    # with open(output_path, "w") as output_file:
    #     for component in components:
    #         output_file.write(component + "\n")

    # Save the simplified mesh as an STL file
    # o3d.io.write_triangle_mesh(output_path, simplified_o3d_mesh)

def visualize_mesh(mesh):
    o3d.visualization.draw_geometries([mesh])

# Call the stl_to_inhouse function
stl_to_inhouse(path_to_analyse, "path/to/your/output/file.stl")


# ### Second function attempt
# import pyvista
# import pyVHACD

# mesh = pyvista.examples.download_bunny().triangulate()

# outputs = pyVHACD.compute_vhacd(mesh.points, mesh.faces)

# plotter = pyvista.Plotter(window_size=(1500, 1100))
# for i, (mesh_points, mesh_faces) in enumerate(outputs):
#      plotter.add_mesh(pyvista.PolyData(mesh_points, mesh_faces), color=list(pyvista.hexcolors.keys())[i])

# plotter.show()

# if __name__ == "__main__":