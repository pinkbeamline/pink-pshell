#Center position
#y0=0.3
#x0=-0.4

#Scanj presets
x_0=[0.6, 0.4, 0.2, 0, -0.2, -0.4, -0.6, -0.8, -1.0, 1.2, 1.4]
y_0=[-0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1]


for i in range(0,9):
    pink.AU1(top=y_0[i]+0.1, bottom=y_0[i]-0.1, wall=-0.3, ring=-0.5)
    scan.gap(diode.IZero(), start=6., end=11, step=0.02, exposure=1)


for i in range(0,11):
    pink.AU1(top=0.4, bottom=0.2, wall=x_0[i]+0.1, ring=x_0[i]-0.1)
    scan.gap(diode.IZero(), start=6., end=11, step=0.02, exposure=1)


pink.shutter_hard_CLOSE()
#caput("PINK:PLCVAC:V11close", 1)