import ifcopenshell
import ifcopenshell.geom
from ifcopenshell.api import run

def create_ifc_file(rooms, building_name="My Design"):
    """Create an IFC file from room data."""
    # Create a new IFC model (IFC4)
    file = ifcopenshell.file(schema="IFC4")
    
    # 1. Create project and site
    project = run("root.create_entity", file, ifc_class="IfcProject", name=building_name)
    
    # 2. Create site
    site = run("root.create_entity", file, ifc_class="IfcSite", name="Site")
    run("aggregate.assign_object", file, product=site, relating_object=project)
    
    # 3. Create building
    building = run("root.create_entity", file, ifc_class="IfcBuilding", name=building_name)
    run("aggregate.assign_object", file, product=building, relating_object=site)
    
    # 4. Create a storey
    storey = run("root.create_entity", file, ifc_class="IfcBuildingStorey", name="Ground Floor")
    run("aggregate.assign_object", file, product=storey, relating_object=building)
    
    # 5. Create walls and slabs for each room
    for r in rooms:
        x = r["x"]
        y = r["y"]
        w = r["w"]
        h = r["h"]
        height = 3.0  # floor height
        
        # Create a slab (floor) for this room
        points = [
            (x, y, 0.0),
            (x + w, y, 0.0),
            (x + w, y + h, 0.0),
            (x, y + h, 0.0)
        ]
        slab = create_slab(file, storey, points)
        
        # Create 4 walls around each room
        wall_thickness = 0.2
        
        # Wall 1: Bottom (y = constant)
        create_wall(file, storey, 
                   (x, y, 0.0), (x + w, y, 0.0), 
                   height, wall_thickness, "EXTERIOR")
        
        # Wall 2: Top (y = y + h)
        create_wall(file, storey,
                   (x, y + h, 0.0), (x + w, y + h, 0.0),
                   height, wall_thickness, "EXTERIOR")
        
        # Wall 3: Left (x = constant)
        create_wall(file, storey,
                   (x, y, 0.0), (x, y + h, 0.0),
                   height, wall_thickness, "EXTERIOR")
        
        # Wall 4: Right (x = x + w)
        create_wall(file, storey,
                   (x + w, y, 0.0), (x + w, y + h, 0.0),
                   height, wall_thickness, "EXTERIOR")
        
        # Create a space (room volume)
        create_space(file, storey, r["name"], x, y, w, h, height)
    
    return file

def create_slab(file, storey, points):
    """Create a slab (floor) from corner points."""
    # Build polyline from points
    p1 = file.createIfcCartesianPoint(points[0])
    p2 = file.createIfcCartesianPoint(points[1])
    p3 = file.createIfcCartesianPoint(points[2])
    p4 = file.createIfcCartesianPoint(points[3])
    
    polyline = file.createIfcPolyline([p1, p2, p3, p4, p1])
    profile = file.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
    
    # Extrude to create slab
    slab = run("root.create_entity", file, ifc_class="IfcSlab", name="Slab")
    run("geometry.create_extruded_solid", file, product=slab, 
        profile=profile, depth=0.2, extruded_direction=(0, 0, 1))
    run("spatial.assign_container", file, product=slab, relating_structure=storey)
    return slab

def create_wall(file, storey, start, end, height, thickness, wall_type="INTERIOR"):
    """Create a wall between two points."""
    p1 = file.createIfcCartesianPoint(start)
    p2 = file.createIfcCartesianPoint(end)
    
    # Wall axis (line)
    axis = file.createIfcPolyline([p1, p2])
    
    # Wall profile (rectangle)
    profile = file.createIfcRectangleProfileDef("AREA", "WALL", 
                                                file.createIfcAxis2Placement2D(
                                                    file.createIfcCartesianPoint((0, 0)),
                                                    file.createIfcDirection((1, 0))),
                                                thickness, 0.3)
    
    wall = run("root.create_entity", file, ifc_class="IfcWall", name=f"Wall_{wall_type}")
    run("geometry.create_extruded_solid", file, product=wall, 
        profile=profile, depth=height, extruded_direction=(0, 0, 1),
        position=file.createIfcAxis2Placement3D(
            file.createIfcCartesianPoint(start),
            file.createIfcDirection((0, 0, 1)),
            file.createIfcDirection((1, 0, 0))
        ))
    run("spatial.assign_container", file, product=wall, relating_structure=storey)
    return wall

def create_space(file, storey, name, x, y, w, h, height):
    """Create an IfcSpace (room volume)."""
    # Create a simple box geometry for the space
    points = [
        (x, y, 0.0),
        (x + w, y, 0.0),
        (x + w, y + h, 0.0),
        (x, y + h, 0.0)
    ]
    polyline = file.createIfcPolyline([
        file.createIfcCartesianPoint(p) for p in points + [points[0]]
    ])
    profile = file.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
    
    space = run("root.create_entity", file, ifc_class="IfcSpace", name=name)
    run("geometry.create_extruded_solid", file, product=space,
        profile=profile, depth=height, extruded_direction=(0, 0, 1))
    run("spatial.assign_container", file, product=space, relating_structure=storey)
    return space

def export_ifc(rooms, filename="design.ifc"):
    """Save IFC file to disk or return bytes."""
    file = create_ifc_file(rooms)
    # Write to bytes for Streamlit download
    import io
    buffer = io.BytesIO()
    file.write(buffer)
    return buffer.getvalue()