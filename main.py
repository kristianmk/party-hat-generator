# Party hat generator for 3D printing. Use "spiral" - or "vase" mode for a nice result.
# Also includes sketch of lobster tag.
# Written by K. M. Knausgård 2022
import cadquery as cq

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

    solid_cone = (
        cq.Workplane("front")
        .circle(radius=radius)
        .extrude(until=150.0, taper=19.0).tag("cone")
    )

    text_pos_z = 30

    text = (
        solid_cone.copyWorkplane(
              cq.Workplane("left", origin=(100, 0, text_pos_z))
                  .transformed(offset=cq.Vector(0, 0, text_pos_z), rotate=cq.Vector(0, 0, -90))
           ).text(
            text,
            fontsize=18.0,  # mm
            distance=200.0,
            font="Sans",
            combine="cut",
            halign="center",
            valign="center",
        )

        # .circle(radius=10).cutThruAll()

    )
    #result = text.faces("-Z").shell(0.5)

    return text


def export_3mf(model, filenameWithExtension):
    cq.exporters.export(model, filenameWithExtension, tolerance=0.01, angularTolerance=0.05)


def main():
    hat = create_party_hat(radius=40.0, text="Silje")
    export_3mf(hat, "test.3mf")


if __name__ == '__main__':
    main()
