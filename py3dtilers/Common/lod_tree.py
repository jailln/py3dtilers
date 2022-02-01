from ..Common import GeometryTree, GeometryNode, Lod1Node, LoaNode, Groups


class LodTree(GeometryTree):
    """
    The LodTree contains the root node(s) of the LOD hierarchy and the centroid of the whole tileset
    """

    def __init__(self, objects_to_tile, create_lod1=False, create_loa=False, polygons_path=None, with_texture=False):
        """
        LodTree takes an instance of ObjectsToTile (which contains a collection of ObjectToTile) and creates nodes.
        In order to reduce the number of .b3dm, it also distributes the geometries into a list of Group.
        A Group contains geometries and an optional polygon that will be used for LoaNodes.
        """
        root_nodes = list()

        groups = self.group_features(objects_to_tile, polygons_path)

        for group in groups:
            node = GeometryNode(group.objects_to_tile, 1, with_texture)
            root_node = node
            if create_lod1:
                lod1_node = Lod1Node(group.objects_to_tile, 5)
                lod1_node.add_child_node(root_node)
                root_node = lod1_node
            if group.with_polygon:
                loa_node = LoaNode(group.objects_to_tile, 20, group.additional_points, group.points_dict)
                loa_node.add_child_node(root_node)
                root_node = loa_node

            root_nodes.append(root_node)

        super().__init__(objects_to_tile, root_nodes)

    def group_features(self, objects_to_tile, polygons_path=None):
        """
        Group objects_to_tile to reduce the number of tiles
        """
        groups = Groups(objects_to_tile, polygons_path)
        return groups.get_groups_as_list()
