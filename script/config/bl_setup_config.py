## Setup Pink Beamline
## List of PVs and values to be set by function "pink.setup_pink"
## Format: [ PV, value, Monitor PV, deadband, timeout(sec) ]

# Remove U17-PGM mirror
group1_list = [
    ["u171pgm1:PH_0_SET", 770.0, "u171pgm1:PH_0_GET", 0.3, 180],
]

# AU1 Aperture
group2_list = [
    ["WAUY02U012L:AbsM1", -1.0, "WAUY02U012L:rdPosM1", 0.1, 60],
    ["WAUY02U012L:AbsM2", -1.6, "WAUY02U012L:rdPosM2", 0.1, 60],
    ["WAUY02U012L:AbsM3",  0.4, "WAUY02U012L:rdPosM3", 0.1, 60],
    ["WAUY02U012L:AbsM4", -1.4, "WAUY02U012L:rdPosM4", 0.1, 60],
]
# Pink Apertures U17-AU3-Pink
group3_list = [
    ["AUY01U112L:AbsM1", -18.5, "AUY01U112L:rdPosM1", 0.1, 60],
    ["AUY01U112L:AbsM2", -21.5, "AUY01U112L:rdPosM2", 0.1, 60],
    ["AUY01U112L:AbsM3",  -1.5, "AUY01U112L:rdPosM3", 0.1, 60],
    ["AUY01U112L:AbsM4",   2.5, "AUY01U112L:rdPosM4", 0.1, 60],
]
# Translate M2 mirror into the beam
group4_list = [
    ["HEX2OS12L:hexapod:setPoseY", 0.0, "HEX2OS12L:hexapod:getReadPoseY", 1.0, 120],
]

# task list format: [group of PVs, message before execute group, message after, group execute question]
task_list = [
   [group1_list, "Moving U17-PGM to home position... ", "OK"       , "Move PGM to home ?"          ],
   [group2_list, "Moving Apertures U17-AU1-Pink... "  , "OK"       , "Move Apertures for U17 AU1 ?"],
   [group3_list, "Moving Apertures U17-AU3-Pink... "  , "OK"       , "Move Apertures for U17 AU3 ?"],
   [group4_list, "Moving Hexapod Ty..."               , "OK\nDone!", "Move M2 mirror into beam ?"  ]
]
