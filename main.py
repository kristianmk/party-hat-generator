# Party hat generator for 3D printing. Use "spiral" - or "vase" mode for a nice result.
#
# Written by K. M. Knausgård 2022
import cadquery as cq
import math

# Get from Google: https://fonts.google.com/noto/specimen/Noto+Emoji
emoji_font_path = "Noto_Emoji/NotoEmoji-VariableFont_wght.ttf"


def create_party_hat(radius=30.0, text="☺", emoji=False, fontsize=28.0, with_tiedown=True, halloween_mode=False):
    taper = 19.0 if not halloween_mode else 17.0  # Smaller value <=> sharper angle <=> more pointy hat
    text_pos_z = 13.0 if not halloween_mode else fontsize/2
    text_extrusion = 0.5
    fillet_radius = 0.12  # 0.12 works for most text, but filleting with cadquery is not robust. 0.2 looks better.
    tiedown_thickness = 2
    brim_width = radius/2.0

    layer_height = 0.2  # 3D printer setting.

    height = radius / math.tan(taper * math.pi / 180)
    height_plus_some_margin = (radius + text_extrusion) / math.tan(taper * math.pi / 180) * 1.1  # 10 % margin

    solid_cone = (  # This is the actual hat.
        cq.Workplane("front", origin=(0, 0, 0))
            .circle(radius=radius)
            .extrude(until=height_plus_some_margin, taper=taper)  # Create cone by extrusion
            .cut(cq.Workplane("front", origin=(0, 0, height)).circle(50).extrude(-2.1))  # Remove sharp tip
            .faces(">Z").fillet(0.7)  # Round off resulting circular face on tip.
    )

    solid_cone_text_cutter = (  # This cone is used for cutting text, not for the hat itself.
        cq.Workplane("front", origin=(0, 0, 0))
            .circle(radius=radius + text_extrusion)
            .extrude(until=height_plus_some_margin, taper=taper)
    )

    text = (
        cq.Workplane("left", origin=(0, 0, text_pos_z))
            .transformed(offset=cq.Vector(0, 0, text_pos_z), rotate=cq.Vector(180, taper, -90))  # az, pitch, roll
            .text(
            text,
            fontsize=fontsize,  # mm
            distance=radius * 2.0,  # 2.0 should give sufficient margin, but this is not a calculated value.
            font="Noto Emoji" if emoji else "Arial",  # Arial
            fontPath=emoji_font_path if emoji else None,
            combine=False,
            halign="center",
            valign="center",
        )
    )

    tiedown_circle_hidden_inside_hat = (
        cq.Workplane("front", origin=(0, 0, 0))
            .circle(radius=radius)
            .extrude(until=tiedown_thickness, taper=taper)
            .faces(">Z")
            .circle(radius - 3)
            .cutThruAll()
            .combine()
    )

    tiedown_ears_inside_hat = (
        cq.Workplane("front", origin=(radius - 5, 0, 0))
            .rect(6, 20)
            .extrude(until=tiedown_thickness)
            .edges("|Z and <X")
            .fillet(2.5)
            .faces(">Z")
            .circle(radius=1.5)
            .cutThruAll()
            .mirror(mirrorPlane="YZ", union=True)
            .rotateAboutCenter(axisEndPoint=(0, 0, 1), angleDegrees=90)
            .combine()
    )

    tiedown_hidden_inside = (  # Reinforced ring inside hat to make tiedown ears less vulnerable to cracking.
        cq.Workplane("front", origin=(0, 0, 0))
            .add(tiedown_circle_hidden_inside_hat)
            .union(tiedown_ears_inside_hat)
            .edges("|Z").fillet(1.0)
            .combine()
    )

    cutted_text = text.intersect(solid_cone_text_cutter)
    cone_with_extruded_filleted_text = cutted_text.union(solid_cone).edges().fillet(fillet_radius)

    # Removes the lower part to get rid of unnecessary fillet.
    hat = (
        cq.Workplane("front", origin=(0, 0, 0))
        .add(cone_with_extruded_filleted_text).faces("<Z")
        .circle(radius + 1).extrude(fillet_radius, combine="cut")
        .translate((0, 0, -fillet_radius)).faces("<Z")  # Remove fillet
        .circle(radius-1).extrude(tiedown_thickness + layer_height, combine="cut", taper=taper).combine()
    )


    hat_brim = (
        cq.Workplane("front", origin=(0, 0, 0))
        .circle(radius=radius+brim_width)
        .extrude(until=tiedown_thickness/2)
        .faces(">Z")
        .circle(radius)
        .cutThruAll()
        .combine()
    )

    if halloween_mode:
        hat = hat.union(hat_brim)

    # tiedown_inside.union(hat)  #.faces("<Z").shell(0.01)#Shelling and fillets did not work well together.
    return hat.union(tiedown_hidden_inside) if with_tiedown else hat


def export_3mf(model, filename_with_extension):
    cq.exporters.export(model, filename_with_extension, tolerance=0.01, angularTolerance=0.05)

    print(f"Hat saved as {filename_with_extension}.")

    message = (
        f"Slice in Cura with settings:\n"
        "   -> Normal 0.2 mm settings as starting point,\n"
        "   -> Generate support false,\n"
        "   -> Bottom thickness 2.0 mm, \n"
        "   -> Infill 0%,\n"
        "   -> Spiralize outer contour on,\n"
        #"   -> Make overhang printable on (due to problems with large fillets for text),\n"
        "   -> (Slicing tolerance Exclusive or Inclusive on could help if spiderweb appears inside).\n"
        "   -> (Connect infill lines ?).\n"
    )
    print(message)


def main():
    # Select hat size, 95.0 cm diameter looks like a "normal" party hat.
    diameter = 170.0  # 102.0

    # Generate multiple hats using a list of tuples.
    names = [  # ("☺", 48, False),  # This character is available in the Arial font.
               # ("🌟", 43, True),    # Emoji
               # ("♥", 38, True),    # Emoji
               # ("©", 42, True),    # Emoji
               ("🎃", 85, True),
               # ("J&T", 28, False),
               # ("K", 48, False),
               # ("20!", 24, False),
               # ("Test", 25, False),
            ]

    # ... and a simple loop:
    for name in names:
        print(f"Working on hat {name[0]}, text size={name[1]}")
        text = name[0]

        # Halloween-hat
        hat = create_party_hat(radius=0.5 * diameter, text=text, fontsize=name[1], emoji=name[2], halloween_mode=True)

        # Normal party hat
        #hat = create_party_hat(radius=0.5 * diameter, text=text, fontsize=name[1], emoji=name[2])

        export_3mf(hat, f"partyhat_{text.lower().replace(' ', '_')}_diameter_{round(diameter)}_fontsize_{name[1]}.3mf")


if __name__ == '__main__':
    main()
