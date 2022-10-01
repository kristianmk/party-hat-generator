# Party hat generator for 3D printing. Use "spiral" - or "vase" mode for a nice result.
#
# Written by K. M. Knausgård 2022
import cadquery as cq
import math


def create_party_hat(radius=30.0, text="☺", fontsize=28.0):
    taper = 19.0  # Smaller value <=> sharper angle <=> more pointy hat
    text_pos_z = 13.0
    text_extrusion = 0.5
    fillet_radius = 0.12
    tiedown_thickness = 2

    height = radius/math.tan(taper*math.pi/180)
    height_plus_some_margin = (radius+text_extrusion)/math.tan(taper*math.pi/180) * 1.1  # 10 % margin

    solid_cone = (  # This is the actual hat.
        cq.Workplane("front")
        .circle(radius=radius)
        .extrude(until=height_plus_some_margin, taper=taper)  # Create cone by extrusion
        .cut(cq.Workplane("front", origin=(0, 0, height)).circle(50).extrude(-2.1))  # Remove sharp tip
        .faces(">Z").fillet(1.0)  # Round off resulting circular face on tip.
    )

    solid_cone_text_cutter = (  # This cone is used for cutting text, not for the hat itself.
        cq.Workplane("front")
        .circle(radius=radius+text_extrusion)
        .extrude(until=height_plus_some_margin, taper=taper)
    )

    text = (
        cq.Workplane("left", origin=(radius, 0, text_pos_z))
            .transformed(offset=cq.Vector(0, 0, text_pos_z), rotate=cq.Vector(0, taper, -90))
            .text(
                text,
                fontsize=fontsize,  # mm
                distance=radius*5,  # Radius will be enough for a realistic hat with finite height.
                font="Sans",  # Arial
                combine=False,
                halign="center",
                valign="center",
            )
    )

    tiedown_circle_hidden_inside_hat = (
        cq.Workplane("front", origin=(0, 0, 0))
            .circle(radius=radius)
            .extrude(until=2, taper=taper)
            .faces(">Z")
            .circle(radius-3)
            .cutThruAll()
    )

    tiedown_ears_inside_hat = (
        cq.Workplane("front", origin=(radius-5, 0, 0))
            .rect(6, 20)
            .extrude(until=tiedown_thickness)
            .edges("|Z and <X")
            .fillet(2.5)
            .faces(">Z")
            .circle(radius=1.5)
            .cutThruAll()
            .mirror(mirrorPlane="YZ", union=True)
            .rotateAboutCenter(axisEndPoint=(0, 0, 1), angleDegrees=90)
    )

    tiedown_inside = tiedown_circle_hidden_inside_hat.union(tiedown_ears_inside_hat).edges("|Z").fillet(1)

    text_with_fillet = text.intersect(solid_cone_text_cutter)  #.fillet(fillet_radius)
    cone_with_extruded_filleted_text = text_with_fillet.union(solid_cone).edges().fillet(fillet_radius)

    # Removes the lower part to get rid of unnecessary fillet.
    hat = cone_with_extruded_filleted_text\
        - cq.Workplane("front").circle(radius+1).extrude(fillet_radius)\
        - cq.Workplane("front").circle(radius-1).extrude(tiedown_thickness+0.12, taper=taper) # Make a one layer gap 0.12


    return tiedown_inside.union(hat)  #.faces("<Z").shell(0.01)


def export_3mf(model, filename_with_extension):
    cq.exporters.export(model, filename_with_extension, tolerance=0.01, angularTolerance=0.05)

    message = (
                f"Slice in Cura with settings:\n"
                "   -> Normal 0.2 mm settings as starting point,\n"
                "   -> Generate support false,\n"
                "   -> Bottom thickness 2.0 mm, \n"
                "   -> Infill 0%,\n"  
                "   -> Spiralize outer contour on,\n"
                "   -> Make overhang printable on (due to problems with large fillets for text),\n"
                "   -> (Slicing tolerance Exclusive on).\n"
                "   -> (Connect infill lines ?).\n"
    )
    print(message)


def main():
    text = "☺"
    hat = create_party_hat(radius=51.0, text=text, fontsize=42.0)
    export_3mf(hat, f"partyhat_{text.lower().replace(' ', '_')}.3mf")


if __name__ == '__main__':
    main()
