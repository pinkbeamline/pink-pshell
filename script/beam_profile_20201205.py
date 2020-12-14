bpm.BPM2_Vertical_Profile()
bpm.BPM4_Vertical_Profile()
bpm.BPM3_Vertical_Profile()
bpm.BPM2_Horizontal_Profile()
bpm.BPM4_Horizontal_Profile()
bpm.BPM3_Horizontal_Profile()
blade.Slit_Scan(slit.bottom(), source.IZero(), start=-200, end=-50, step=3., exposure=1.0)
blade.Sample_Env_Blade_Scan(source.TFY(), axis.vertical(), start=2850, end=3100, step=4., exposure=1.0)
caput("PINK:SMA01:m9.VAL", -5500.) #Y