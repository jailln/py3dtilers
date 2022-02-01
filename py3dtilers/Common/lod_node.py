from ..Common import ObjectsToTile, ObjectToTile, GeometryNode
from ..Common import ExtrudedPolygon


class LodNode(GeometryNode):
    """
    Each node contains a collection of objects to tile
    and a list of child nodes
    A node will correspond to a tile of the 3dtiles tileset
    """

    def __init__(self, objects_to_tile=None, geometric_error=50, with_texture=False):
        """
        :param objects_to_tile: an instance ObjectsToTile containing the list of geometries contained in the node
        :param geometric_error: the distance to display the 3D tile that will be created from this node.
        """
        super().__init__(objects_to_tile, with_texture)
        self.geometric_error = geometric_error


class Lod1Node(LodNode):
    """
    Creates 3D extrusions of the footprint of each geometry in the objects_to_tile parameter of the constructor.
    """

    def __init__(self, objects_to_tile, geometric_error=50):
        lod1_list = list()
        for object_to_tile in objects_to_tile:
            extruded_polygon = ExtrudedPolygon(object_to_tile)
            lod1_list.append(extruded_polygon.get_extruded_object())
        super().__init__(objects_to_tile=ObjectsToTile(lod1_list), geometric_error=geometric_error)


class LoaNode(LodNode):
    """
    Creates 3D extrusions of the polygons given as parameter.
    The LoaNode also takes a dictionary stocking the indexes of the geometries contained in each polygon.
    """
    loa_index = 0

    def __init__(self, objects_to_tile, geometric_error=50, additional_points=list(), points_dict=dict()):
        loas = list()
        for key in points_dict:
            contained_objects = ObjectsToTile([objects_to_tile[i] for i in points_dict[key]])
            loa = self.create_loa_from_polygon(contained_objects, additional_points[key], LoaNode.loa_index)
            loas.append(loa)
            LoaNode.loa_index += 1
        super().__init__(objects_to_tile=ObjectsToTile(loas), geometric_error=geometric_error)

    def create_loa_from_polygon(self, objects_to_tile, polygon_points, index=0):
        loa_geometry = ObjectToTile("loa_" + str(index))
        for object_to_tile in objects_to_tile:
            loa_geometry.geom.triangles.append(object_to_tile.geom.triangles[0])

        extruded_polygon = ExtrudedPolygon(loa_geometry, override_points=True, polygon=polygon_points)
        return extruded_polygon.get_extruded_object()
