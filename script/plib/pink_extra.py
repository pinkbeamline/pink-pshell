## PINK Extra functions

def pink_save_bl_snapshot():
    import config.bl_snapshot_config as pcfg

    for dat in pcfg.pvlist:
        try:
            pval = caget(dat[1])
        except:
            print("PV is unreachable: " + dat[1])
            pval = 0
        save_dataset(dat[0], pval)

