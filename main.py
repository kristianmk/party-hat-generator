# Party hat generator for 3D printing. Use "spiral" - or "vase" mode for a nice result.
# Also includes sketch of lobster tag.
# Written by K. M. Knausgård 2022
import cadquery as cq
import math

if 'show_object' not in globals():
    def show_object(*args, **kwargs):
        pass


def create_lobster_tag(registration="REG-NUM-314",
                       name="Kristian Muri Knausgård",
                       address="One way 42\n3141 City",
                       phone="31 41 59 26",
                       width=80,
                       thickness=4):
    box = cq.Workplane("XY").box(80, 40, 2.0)
    text = (
        box.faces("+Z")
        .workplane()
        .text(
            name,
            fontsize=8.0,  # mm
            distance=-1.0,
            font="Sans",
            combine="cut",
            halign="center",
            valign="center",
        )
    )

def create_princess_tiara(radius=30.0, text="☺"):
    solid_cone = (
        cq.Workplane("front")
            .circle(radius=radius)
            .extrude(until=150.0, taper=19.0).tag("cone")
    )

    text = (
        solid_cone.copyWorkplane(
            cq.Workplane("front", origin=(-5, 0, 0))
        ).circle(40).cutThruAll()
    )
    result = text.faces("-Z").shell(0.5)

    return result


def create_party_hat(radius=30.0, text="☺"):

    taper = 19.0  # Smaller value <=> sharper angle <=> more pointy hat
    text_pos_z = 13.0
    text_extrusion = 0.5
    fillet_radius = 0.12

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
            fontsize=28.0,  # mm
            #kind="bold",
            #clean=True,
            distance=radius*5,  # Radius will be enough for a realistic hat with finite height.
            font="Sans",  # Arial
            combine=False,
            halign="center",
            valign="center",
        )
    )

    text_with_fillet = text.intersect(solid_cone_text_cutter)  #.fillet(fillet_radius)

    cone_with_extruded_filleted_text = text_with_fillet.union(solid_cone).edges().fillet(fillet_radius)

    #cone_with_extruded_filleted_text = cone_with_extruded_text.faces(">Z").fillet(fillet_radius).clean()

    # Removes the lower part to get rid of unnecessary fillet.
    hat = cone_with_extruded_filleted_text\
        - cq.Workplane("front").circle(radius+1).extrude(fillet_radius)

    return hat  #.faces("<Z").shell(0.01)


def export_3mf(model, filenameWithExtension):
    cq.exporters.export(model, filenameWithExtension, tolerance=0.01, angularTolerance=0.05)



    message = (
                f"Slice in Cura with settings:\n"
                "   -> Normal 0.2 mm settings as starting point\n"
                "   -> Bottom thickness 0.0 mm, \n"
                "   -> Infill 0%,\n"  
                "   -> Spiralize outer contour on,\n"
                "   -> Make overhang printable on (due to problems with large fillets for text),\n"
                "   -> (Slicing tolerance Exclusive on).\n"
    )
    print(message)


def main():
    text = "Ida"
    hat = create_party_hat(radius=55.0, text=text)
    export_3mf(hat, f"partyhat_{text.lower().replace(' ', '_')}.3mf")


if __name__ == '__main__':
    main()
