import json
import os


class SpacecraftManager(object):
    def __init__(self):  # constructor

        self.directory = os.getcwd()
        self.spacecraft_dir = self.directory + '/SpaceCraft/'
        self.json_dir = self.directory + '/JSON/'
        print(self.spacecraft_dir)
        print(self.json_dir)

    def load_userfile(self, userfilename):
        pass

    def parse_optical_property(self, line_str):
        
        optical_property_array = []
        line_split = line_str.split()

        if len(line_split) == 2:
            optical_property_array.append({'reflectivity': line_split[0]})
            optical_property_array.append({'specularity': line_split[1]})
            optical_property_array.append({'emissivity': 0.000})
            optical_property_array.append({'emissivity_effective': 0.000})

        elif len(line_split) == 4:  # the new format
            optical_property_array.append({'reflectivity': line_split[0]})
            optical_property_array.append({'specularity': line_split[1]})
            optical_property_array.append({'emissivity': line_split[2]})
            optical_property_array.append({'emissivity_effective': line_split[3]})

        else:
            print("user file format error: " + str(len(line_split)) + "  " + line_str)

        return optical_property_array

    def convert_userfile2JSON(self, spacecraftname):
        wrapper = {}
        objects = []

        userfile = open(self.spacecraft_dir + spacecraftname + "/" + spacecraftname + '.txt', 'r')
        jsonfile = open(self.json_dir + spacecraftname + '.json', 'w')

        print("writing " + self.json_dir + spacecraftname + '.json')

        lines = userfile.readlines()

        for i in range(0, len(lines)):
            line = lines[i]
            if line[:3] == "GEN":
                object = {}
                vertexlist, parameterlist = [], []
                vertices = int(lines[i + 2])

                for j in range(0, vertices):
                    l = lines[i + 3 + j].split()
                    vertexlist.append({"vertex": [l[0], l[1], l[2]]})

                namestring = ' '.join(lines[i + 1][:-1].split()).translate(str.maketrans('', '', '/-'))

                mli = lines[i + 1].split()[2]
                optical_property = self.parse_optical_property(lines[i + 3 + vertices])

                parameterlist.append({"vertices": vertexlist})
                parameterlist.append({"name": namestring})

                parameterlist.append({"mli": mli})

                for i in range(len(optical_property)):
                    parameterlist.append(optical_property[i])

                object['polygon'] = parameterlist
                objects.append(object)

            if line[:3] == "CYL":
                object = {}
                parameterlist = []

                vertex1 = lines[i + 3].split()
                vertex2 = lines[i + 4].split()
                radius = lines[i + 2].split()[0]

                namestring = ' '.join(lines[i + 1][:-1].split()).translate(str.maketrans('', '', '/-'))

                optical_property = self.parse_optical_property(lines[i + 5])
                mli = lines[i + 1].split()[2]

                parameterlist.append(
                    {"vertex1":
                    [float(vertex1[0]), float(vertex1[1]), float(vertex1[2])]}
                    )
                parameterlist.append(
                    {"vertex2":
                    [float(vertex2[0]), float(vertex2[1]), float(vertex2[2])]}
                )
                parameterlist.append({"radius": float(radius)})
                parameterlist.append({"name": namestring})

                parameterlist.append({"mli": mli})

                for i in range(len(optical_property)):
                    parameterlist.append(optical_property[i])

                object['cylinder'] = parameterlist
                objects.append(object)

            if line[:3] == "PAR":
                object = {}
                parameterlist = []
                vertex1 = lines[i + 4].split()
                vertex2 = lines[i + 5].split()
                depth = lines[i + 2].split()[0]
                radius = lines[i + 3].split()[0]
                namestring = ' '.join(lines[i + 1][:-1].split()).translate(str.maketrans('', '', '/-'))
                optical_property = self.parse_optical_property(lines[i + 6])
                mli = lines[i + 1].split()[2]
                parameterlist.append(
                    {"vertex1":
                    [float(vertex1[0]), float(vertex1[1]), float(vertex1[2])]}
                )
                parameterlist.append(
                    {"vertex2":
                    [float(vertex2[0]), float(vertex2[1]), float(vertex2[2])]}
                )

                parameterlist.append({"depth": float(depth)})
                parameterlist.append({"radius": float(radius)})
                parameterlist.append({"name": namestring})
                parameterlist.append({"mli": mli})

                for i in range(len(optical_property)):
                    parameterlist.append(optical_property[i])

                object['paraboloid'] = parameterlist
                objects.append(object)

            if line[:3] == "RIN":
                object = {}
                parameterlist = []

                namestring = ' '.join(lines[i + 1][:-1].split()).translate(str.maketrans('', '', '/-'))
                radius1 = lines[i + 2].split()[0]
                radius2 = lines[i + 3].split()[0]
                vertex1 = lines[i + 4].split()
                vertex2 = lines[i + 5].split()
                vertex3 = lines[i + 6].split()

                optical_property = self.parse_optical_property(lines[i + 7])
                mli = lines[i + 1].split()[2]

                parameterlist.append({"name": namestring})
                parameterlist.append({"radius1": float(radius1)})
                parameterlist.append({"radius2": float(radius2)})
                parameterlist.append({"vertex1": [float(vertex1[0]), float(vertex1[1]), float(vertex1[2])]})
                parameterlist.append({"vertex2": [float(vertex2[0]), float(vertex2[1]), float(vertex2[2])]})
                parameterlist.append({"vertex3": [float(vertex3[0]), float(vertex3[1]), float(vertex3[2])]})
                parameterlist.append({"mli": mli})

                for i in range(len(optical_property)):
                    parameterlist.append(optical_property[i])

                object['ring'] = parameterlist
                objects.append(object)

            if line[:3] == "CON":
                object = {}
                parameterlist = []

                namestring = ' '.join(lines[i + 1][:-1].split()).translate(str.maketrans('', '', '/-'))
                coneheight = lines[i + 2].split()[0]
                baseradius = lines[i + 3].split()[0]
                basevertex = lines[i + 4].split()
                peakvertex = lines[i + 5].split()

                optical_property = self.parse_optical_property(lines[i + 6])

                mli = lines[i + 1].split()[2]

                parameterlist.append({"name": namestring})
                parameterlist.append({"coneheight": float(coneheight)})
                parameterlist.append({"baseradius": float(baseradius)})
                parameterlist.append({"basevertex": [float(basevertex[0]), float(basevertex[1]), float(basevertex[2])]})
                parameterlist.append({"peakvertex": [float(peakvertex[0]), float(peakvertex[1]), float(peakvertex[2])]})

                parameterlist.append({"mli": mli})

                for i in range(len(optical_property)):
                    parameterlist.append(optical_property[i])

                object['cone'] = parameterlist
                objects.append(object)

            if line[:3] == "TCO":
                object = {}
                parameterlist = []
                namestring = ' '.join(lines[i + 1][:-1].split()).translate(str.maketrans('', '', '/-'))
                coneheight = lines[i + 2].split()[0]
                baseradius = lines[i + 3].split()[0]
                truncatedconeheight = lines[i + 4].split()[0]
                basevertex = lines[i + 5].split()
                peakvertex = lines[i + 6].split()

                optical_property = self.parse_optical_property(lines[i + 7])

                mli = lines[i + 1].split()[2]

                parameterlist.append({"name": namestring})
                parameterlist.append({"coneheight": float(coneheight)})
                parameterlist.append({"baseradius": float(baseradius)})
                parameterlist.append({"truncatedconeheight": float(truncatedconeheight)})
                parameterlist.append({"basevertex": [float(basevertex[0]), float(basevertex[1]), float(basevertex[2])]})
                parameterlist.append({"peakvertex": [float(peakvertex[0]), float(peakvertex[1]), float(peakvertex[2])]})

                parameterlist.append({"mli": mli})

                for i in range(len(optical_property)):
                    parameterlist.append(optical_property[i])

                object['cone'] = parameterlist
                objects.append(object)
            if line[:3] == "CIR":
                obj = {}
                parameterlist = []
                namestring = ' '.join(str.split(lines[i+1][:-1])).translate(str.maketrans('', '', '/-'))
                radius = str.split(lines[i+2])[0]
                vertex1 = str.split(lines[i+3])
                vertex2 = str.split(lines[i+4])
                vertex3 = str.split(lines[i+5])
                # reflec = str.split(lines[i+6])[0]
                # spec = str.split(lines[i+6])[1]
                optical_property = self.parse_optical_property(lines[i+6])

                mli = str.split(lines[i+1])[2]

                parameterlist.append({"name": namestring})
                parameterlist.append({"radius": float(radius)})
                parameterlist.append({"vertex1": [float(vertex1[0]), float(vertex1[1]), float(vertex1[2])]})
                parameterlist.append({"vertex2": [float(vertex2[0]), float(vertex2[1]), float(vertex2[2])]})
                parameterlist.append({"vertex3": [float(vertex3[0]), float(vertex3[1]), float(vertex3[2])]})

                # for key in optical_property:
                #     parameterlist.append({key: optical_property[key]})

                parameterlist.append({"mli": mli})

                for i in range(len(optical_property)):
                    parameterlist.append(optical_property[i])

                # parameterlist.append({"reflectivity": float(reflec)})
                # parameterlist.append({"specularity": float(spec)})

                obj['circle'] = parameterlist
                objects.append(obj)


        wrapper['geometry'] = objects

        jsonfile.write(json.dumps(objects, indent=4))
        jsonfile.close()

def parse_optical_property(self, line):
    optical_property = []
    for i in range(int(line.split()[0])):
        property = {}
        property["wavelength"] = float(line.split()[i * 2 + 1])
        property["reflectance"] = float(line.split()[i * 2 + 2])
        optical_property.append(property)
    return optical_property

    def decode_GEN(self):
        pass

if __name__ == '__main__':

    spacecraftMgr = SpacecraftManager()
    spacecraftlist = ["Cryosat2", "Cryosat2EADS", "GPSIIA","GPSIIRNAP","GPSIIR",
								"JASON-2", "SPOT4", "SPOT5",
								"JASON-1","Envisat","Envisat_with_panel","ufo",
								"testobject1", "spot4_test", "SolO", "paintedsprite", "plateX",
								"plateY", "plateZ","Beidou-IGSO","Beidou-GEO","GalileoIOV","GalileoFOC",
								"GalileoIOV_full","GalileoIOV_box","GalileoFOC_full","SolarPanels_Gal","sentinel1",
                                "Inmarsat4-F1","TB1_EG3","TB2_EG3","TB3_EG3","TB4_EG3","Sentinel-1_v01",
                                "Sentinel-1_v02","Sentinel-1_v03","Sentinel-1_v04","GPSIIF_v01","GPSIIF_v02","GPSIIF_v03","PotatoSat"]
    
    for spacecraftname in spacecraftlist:
        spacecraftMgr.convert_userfile2JSON(spacecraftname)