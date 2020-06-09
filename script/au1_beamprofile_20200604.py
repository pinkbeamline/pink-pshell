y0=0.2
x0=-0.3
y_t=y0+0.1
y_b=y0-0.1
x_w=x0+0.1
x_r=x0-0.1
pink.AU1(top=y_t, bottom=y_b, wall=x_w, ring=x_r)
print("AU1 0.2x0.2")
bpm.BPM4_Horizontal_Profile()
bpm.BPM4_Vertical_Profile()
blade.Slit_Scan(slit.bottom(), start=-670, end=-870, step=5.0, exposure=1.0)

y_t=y0+0.2
y_b=y0-0.2
x_w=x0+0.5
x_r=x0-0.5
pink.AU1(top=y_t, bottom=y_b, wall=x_w, ring=x_r)
print("AU1 0.4x0.1")
bpm.BPM4_Horizontal_Profile()
bpm.BPM4_Vertical_Profile()
blade.Slit_Scan(slit.bottom(), start=-670, end=-870, step=5.0, exposure=1.0)

y_t=y0+0.4
y_b=y0-0.4
x_w=x0+0.8
x_r=x0-0.8
pink.AU1(top=y_t, bottom=y_b, wall=x_w, ring=x_r)
print("AU1 0.8x1.6")
bpm.BPM4_Horizontal_Profile()
bpm.BPM4_Vertical_Profile()
blade.Slit_Scan(slit.bottom(), start=-670, end=-870, step=5.0, exposure=1.0)

y_t=y0+0.5
y_b=y0-0.5
x_w=x0+1
x_r=x0-1
pink.AU1(top=y_t, bottom=y_b, wall=x_w, ring=x_r)
print("AU1 1x2")
bpm.BPM4_Horizontal_Profile()
bpm.BPM4_Vertical_Profile()
blade.Slit_Scan(slit.bottom(), start=-670, end=-870, step=5.0, exposure=1.0)

y_t=y0+0.2
y_b=y0-0.2
x_w=x0+0.5
x_r=x0-0.5
pink.AU1(top=y_t, bottom=y_b, wall=x_w, ring=x_r)