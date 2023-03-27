import numpy as np
from pythreejs import (Renderer, Scene, PerspectiveCamera, Mesh, BoxGeometry, SphereGeometry, CylinderGeometry, ConeGeometry, PlaneGeometry,
                       MeshStandardMaterial, DirectionalLight, OrbitControls, BufferGeometry, CircleGeometry, RingGeometry, GridHelper, ArrowHelper)
from scipy.spatial.transform import Rotation as R
from IPython.display import display

# NOTE: all these functions must be used in a Jupyter notebook that is running in your browser for the display functions to work
# NOTE: you must include the following at the start of your notebook to enable the pythreejs and widgetsnbextension extensions:
#  !jupyter nbextension enable --py --sys-prefix pythreejs
#  !jupyter nbextension enable --py --sys-prefix widgetsnbextension

class GeometricPrimitive:
    def __init__(self, geometry, position, name, material_type, group_number, emissivity, specularity, rotation=None):
        print("Creating GeometricPrimitive object:"+name)
        # return error if geometry is not a pythreejs geometry object
        if not isinstance(geometry, (SphereGeometry, CylinderGeometry, CircleGeometry, RingGeometry, ConeGeometry, PlaneGeometry)):
            raise ValueError("geometry must be a supported pythreejs geometry object")
        # return error if position is not of length 3
        if not len(position) == 3:
            raise ValueError("position must be a list of length 3")
        # rotation must be None or length 3
        # if rotation is not None or not len(rotation) == 3:
        #     raise ValueError("rotation must be a list of length 3")
        # return error if name is not a string of less than 30 characters
        if not isinstance(name, str) or len(name) > 30:
            raise ValueError("name must be a string of less than 30 characters")
        # return error if material type is not 1 or 0
        if material_type not in [0, 1]:
            raise ValueError("material_type must be 0 or 1")
        # return error if group number is not an integer
        if not isinstance(group_number, int):
            raise ValueError("group_number must be an integer")
        # return error if emissivity is not a float between 0 and 1
        if not isinstance(emissivity, float) or emissivity < 0 or emissivity > 1:
            raise ValueError("emissivity must be a float between 0 and 1")
        # return error if specularity is not a float between 0 and 1
        if not isinstance(specularity, float) or specularity < 0 or specularity > 1:
            raise ValueError("specularity must be a float between 0 and 1")

        self.geometry = geometry
        self.position = position
        self.rotation= rotation
        self.name = name
        self.material_type = material_type
        self.group_number = group_number #component group number
        self.emissivity = emissivity 
        self.specularity = specularity
        self.calculate_properties()

        # if the object is a cylinder, add two circles as the cylinder must be capped with circles at each end...
        if isinstance(self.geometry, CylinderGeometry):
            # only allow cylinders that have a radius at the top and bottom that are equal
            if self.geometry.radiusTop != self.geometry.radiusBottom:
                raise ValueError("Cylinder radiusTop and radiusBottom must be equal")
            self.caps = [GeometricPrimitive(CircleGeometry(radius=self.radius), self.center_bot, self.name + '_base', self.material_type, self.group_number, self.emissivity, self.specularity),
                         GeometricPrimitive(CircleGeometry(radius=self.radius), self.center_top, self.name + '_top', self.material_type, self.group_number, self.emissivity, self.specularity)]
        
    def calculate_properties(self):
        
        if isinstance(self.geometry, SphereGeometry):
            self.radius = self.geometry.radius

        elif isinstance(self.geometry, CylinderGeometry):
            self.radius = self.geometry.radiusBottom
            # calculate rotation matrix of the cylinder
            if self.rotation is not None:
                r = R.from_euler('XYZ', self.rotation, degrees=False)
                self.rotation_matrix = r.as_matrix()
            else:
                self.rotation_matrix = np.identity(3)
            # calculate the unit verctors for the top and bottom of the cube
            z_axis = np.array([0, 0, 1])
            if self.rotation is not None:
                z_axis = np.matmul(self.rotation_matrix, z_axis)
            else:
                z_axis = np.array([0, 0, 1])
            self.base_unit_vector = -z_axis
            self.center_top = self.position + self.base_unit_vector * self.geometry.height / 2
            self.center_bot = self.position - self.base_unit_vector * self.geometry.height / 2
        
        elif isinstance(self.geometry, CircleGeometry):
            self.radius = self.geometry.radius
            
            def circum_point(theta): #calculate the coordinates of a point on the circumference of the circle
                return [self.radius * np.cos(theta), self.radius * np.sin(theta), 0]
            
            if self.rotation is not None: # apply a rotation matrix to the points if the circle is rotated
                r = R.from_euler('XYZ', self.rotation, degrees=True)
                self.rotation_matrix = r.as_matrix()
                rot_circum_point = lambda theta: np.matmul(self.rotation_matrix, circum_point(theta))
                self.circum_point1 = rot_circum_point(np.radians(45))
                self.circum_point2 = rot_circum_point(np.radians(135))
            else:
                self.circum_point1 = circum_point(np.radians(45))
                self.circum_point2 = circum_point(np.radians(135))
            
        
        elif isinstance(self.geometry, RingGeometry):
            self.outer_radius = self.geometry.outerRadius
            self.inner_radius = self.geometry.innerRadius
            self.thickness = self.outer_radius - self.inner_radius
        
        elif isinstance(self.geometry, ConeGeometry):
            self.depth = self.geometry.height
            self.radius_bottom = self.geometry.radius
            self.radius_top = 0 if not hasattr(self.geometry, 'radiusTop') else self.geometry.radiusTop
            self.base_center_coords = [0, -self.geometry.height / 2, 0]
            self.tip_coords = [0, self.geometry.height / 2, 0]
        
        elif isinstance(self.geometry, PlaneGeometry):
            self.vertices = []
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    self.vertices.append([i * self.geometry.width / 2, j * self.geometry.height / 2, 0])

def create_mesh(primitive, material):
    geometry = primitive.geometry
    mesh = Mesh(geometry=geometry, material=material)
    mesh.position = primitive.position
    if primitive.rotation is not None:
        r = R.from_euler('XYZ', primitive.rotation, degrees=True)
        mesh.quaternion = tuple(r.as_quat())
    return mesh

def setup_scene(primitives,rotations=None):
    camera = PerspectiveCamera(position=[3, 3, 3], aspect=1.0)
    controls = OrbitControls(controlling=camera)
    light = DirectionalLight(position=[10, 10, 10])

    #add unit x,y,z vectors
    x_axis = ArrowHelper(dir=[1, 0, 0], origin=[0, 0, 0], length=1, color='red')
    y_axis = ArrowHelper(dir=[0, 1, 0], origin=[0, 0, 0], length=1, color='green')
    z_axis = ArrowHelper(dir=[0, 0, 1], origin=[0, 0, 0], length=1, color='blue')

    #add a grid
    grid = GridHelper(size=10, divisions=10, color_center_line='black', color_grid='grey')

    scene = Scene()
    scene.add(camera)
    scene.add(light)
    scene.add(x_axis)
    scene.add(y_axis)
    scene.add(z_axis)
    scene.add(grid)
    
    material = MeshStandardMaterial(color='green', roughness=0.5, metalness=0.5)

    for i, primitive in enumerate(primitives):
        mesh = create_mesh(primitive, material)
        scene.add(mesh)

    renderer = Renderer(scene, camera, [controls], width=800, height=600)
    return renderer

def plot_primitives(primitives):
    renderer = setup_scene(primitives)
    display(renderer)

def primitives_to_ucl(primitives, ucl_filename):
    #convert primitives to ucl format according to the following rules

    # Each component record in the spacecraft description file begins with a header line specifying the type of component being described by that record (e.g. GENERAL, SPHERE, CONEI etc.). Thereafter, there is a comment line consisting of a record number, two solidi (//), a material type number, a component group number, and possibly a comment about the component, e.g.,
    # 3 // 001 0010 main bus +Z face
    # In this example the record number is 3; the material type number is 1 (any leading zeros are ignored); the component group number is 10; and, the comment provides some information about the component.
    # material type 1 is "MLI"
    # material type 0 is "not MLI"

    # PlanarPolygons ("GENERAL" in ucl, "PlaneGeometry" in pythreejs)
    # Consecutive lines of the component record specify geometrical attributes and are dependent on the geometrical primitve type.
    # for a PlaneGeometry ("GENERAL" in ucl), the first line specifies the number of vertices, 
    # the next lines specify the x, y, and z coordinates of a vertex of the plane, which are listed in anticlockwise order when viewed from the positive side of the plane 
    # the final line specifies the reflectivity and specularity coefficents respectively (0-1)

    # PlanarCircles ("CIRCLE" in ucl, "CircleGeometry" in pythreejs)
    # following the comment line, the radius of the circle is specified on the next line
    #the next lines are the positions of the center of the circle and two points on the circumference of the circle (also in anticlockwise order when viewed from the positive side of the circle)
    
    # Cylinders ("CYL_X" in ucl, "CylinderGeometry" in pythreejs)
    # following the comment line, the radius of the cross section of the cylinder is specified on the next line
    # the next lines are the postiions of the end points of the cylinder (center of the cylinder is the midpoint of the end points)
    # for cylinders to appear closed in the ucl viewer, the cylinder must be capped with circles at each end

    print(f"writing ucl file to {ucl_filename}...")
    print(f"number of primitives: {len(primitives)}")
    
    all_ucl = ""
    for i, primitive in enumerate(primitives):
        record_number = i + 1

        def comment_line(primitive,record_number):
            comment = f"{record_number} // {primitive.material_type} {primitive.group_number} {primitive.name}"
            return comment

        def emiss_spec_line(primitive):
            return f"{primitive.emissivity} {primitive.specularity}"

        if isinstance(primitive.geometry, PlaneGeometry):
            print(f"primitive {i} is a PlaneGeometry") 
            ucl_format = "GENERAL\n"
            ucl_format += comment_line(primitive,record_number)+"\n"
            ucl_format += f"{len(primitive.vertices)}\n" #number of vertices
            for vertex in primitive.vertices: # specify the x, y, and z coordinates of a vertex of the plane (listed in anticlockwise order when viewed from the positive side of the plane)
                ucl_format += f"{vertex[0]} {vertex[1]} {vertex[2]}" + "\n"
            ucl_format += emiss_spec_line(primitive) + "\n"
            all_ucl += ucl_format

        elif isinstance(primitive.geometry, CircleGeometry):
            print(f"primitive {i} is a CircleGeometry")
            ucl_format = "CIRCLE\n"
            ucl_format += comment_line(primitive,record_number)+"\n"
            ucl_format += f"{primitive.radius}\n" #radius
            ucl_format += f"{primitive.position[0]} {primitive.position[1]} {primitive.position[2]}\n" #center of circle
            ucl_format += f"{primitive.circum_point1[0]} {primitive.circum_point1[1]} {primitive.circum_point1[2]}\n" # 1st point on circumference
            ucl_format += f"{primitive.circum_point2[0]} {primitive.circum_point2[1]} {primitive.circum_point2[2]}\n" # 2nd point on circumference
            ucl_format += emiss_spec_line(primitive) + "\n"
            all_ucl += ucl_format
            
        elif isinstance(primitive.geometry, CylinderGeometry):
            print(f"primitive {i} is a CylinderGeometry")
            ucl_format = "CYLINDER\n"
            ucl_format += comment_line(primitive,record_number)+"\n"
            # radius of cross section
            ucl_format += f"{primitive.radius}\n"
            # position of end points of cylinder
            ucl_format += f"{primitive.center_bot[0]} {primitive.center_bot[1]} {primitive.center_bot[2]}\n"
            ucl_format += f"{primitive.center_top[0]} {primitive.center_top[1]} {primitive.center_top[2]}\n"
            all_ucl += ucl_format

    #write each new instance of a primitive to a new line in the ucl file
    with open(ucl_filename, "a") as f:
        # clear the file
        f.truncate(0)
        # write the ucl format to the file
        f.write(all_ucl)


# Example use 
# # spacecraft bus
# bus_face_x_pos = GeometricPrimitive(PlaneGeometry(width=1, height=3), position=[0.5, 0, 0], name = "potato bus_face_x+", material_type = 0, group_number = 1, emissivity = 0.2, specularity = 0.1, rotation=[90, 90, 0])
# bus_face_x_neg = GeometricPrimitive(PlaneGeometry(width=1, height=3), position=[-0.5, 0, 0], name = "potato bus_face_x-", material_type = 0, group_number = 1, emissivity = 0.2, specularity = 0.1, rotation=[-90, -90, 0])
# bus_face_y_neg = GeometricPrimitive(PlaneGeometry(width=3, height=1), position=[0, -0.5, 0], name = "potato bus_face_y-", material_type = 0, group_number = 1, emissivity = 0.2, specularity = 0.1, rotation=[90, 0, 90])
# bus_face_y_pos = GeometricPrimitive(PlaneGeometry(width=3, height=1), position=[0, 0.5, 0], name = "potato bus_face_y+", material_type = 0, group_number = 1, emissivity = 0.2, specularity = 0.1, rotation=[-90, 0, 90])
# bus_face_z_pos = GeometricPrimitive(PlaneGeometry(width=1, height=1), position=[0, 0, 1.5], name = "potato bus_face_z+", material_type = 0, group_number = 1, emissivity = 0.2, specularity = 0.1, rotation=[0, 0, 0])
# bus_face_z_neg = GeometricPrimitive(PlaneGeometry(width=1, height=1), position=[0, 0, -1.5], name = "potato bus_face_z-", material_type = 0, group_number = 1, emissivity = 0.2, specularity = 0.1, rotation=[0, 180, 180])

# #spacecraft solar array (place these facing the y-axis) and along side the spacecraft bus
# array1_face_y_pos = GeometricPrimitive(PlaneGeometry(width=5, height=1), position= [3, 0.05, 0], name = "potato array1_face_y+", material_type = 0, group_number = 3, emissivity = 0.3, specularity = 0.4, rotation=[-90, 0, 0])
# array1_face_y_neg = GeometricPrimitive(PlaneGeometry(width=5, height=1), position= [3, 0.05, 0], name = "potato array1_face_y+", material_type = 0, group_number = 3, emissivity = 0.3, specularity = 0.4, rotation=[90, 0, 0])

# # spacecraft antennae
# # antenna1 = GeometricPrimitive(CylinderGeometry(radiusTop=0.02, radiusBottom=0.02, height=0.4), position=[-0.3, 0.5, 1], name = "potato antenna1", material_type = 0, group_number = 2, emissivity = 0.4, specularity = 0.8)
# # antenna2 = GeometricPrimitive(CylinderGeometry(radiusTop=0.02, radiusBottom=0.02, height=0.4), position=[0.3, 0.5, 1], name = "potato antenna2", material_type = 0, group_number = 2, emissivity = 0.4, specularity = 0.8)
# # antenna3 = GeometricPrimitive(CylinderGeometry(radiusTop=0.02, radiusBottom=0.02, height=0.4), position=[0.0, 0.5, 1], name = "potato antenna3", material_type = 0, group_number = 2, emissivity = 0.4, specularity = 0.8)

# potato_sc_primitives = [bus_face_x_pos, bus_face_x_neg, bus_face_y_neg, bus_face_y_pos,bus_face_z_pos,bus_face_z_neg, array1_face_y_pos, array1_face_y_neg]

# plot_primitives(potato_sc_primitives) ## only works in jupyter notebook
# primitives_to_ucl(potato_sc_primitives, "/Users/charlesc/Documents/GitHub/SRP_tools/potato_sc.txt")