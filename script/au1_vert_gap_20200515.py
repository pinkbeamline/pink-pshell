pink.AU1(top=1.3, bottom=1.3, wall=1.5, ring=1.5)
y_t=[1.2, 1.0, 0.8, 0.6, 0.4, 0.2, 0, -0.2, -0.4, -0.6]
y_b=[1.0, 0.8, 0.6, 0.4, 0.2, 0, -0.2, -0.4, -0.6, -0.8]

for i in range(0,10):
    pink.AU1(top=y_t[i], bottom=y_b[i], wall=-0.6, ring=-0.8)
    scan.gap(diode.IZero(), start=6., end=10, step=0.02, exposure=1)

for i in range(0,10):
    pink.AU1(top=y_t[i], bottom=y_b[i], wall=-0.9, ring=-1.1)
    scan.gap(diode.IZero(), start=6., end=10, step=0.02, exposure=1)

for i in range(0,10):
    pink.AU1(top=y_t[i], bottom=y_b[i], wall=-1.1, ring=-1.3)
    scan.gap(diode.IZero(), start=6., end=10, step=0.02, exposure=1)