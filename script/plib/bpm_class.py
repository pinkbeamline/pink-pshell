from mathutils import *
from plotutils import *

class BPM():
    bpm1_vert_CF=49
    bpm1_hor_CF=49*0.793
    bpm2_vert_CF=13
    bpm2_hor_CF=13*0.707
    bpm3_vert_CF=8.6
    bpm3_hor_CF=8.6*0.707
    bpm4_vert_CF=9.5
    bpm4_hor_CF=9.5*0.707
    roiposx=0
    roiposy=0
    roisizex=0
    roisizey=0
    cam_exposure=0
    cam_gain=0
    sig2fwmh=2.355

    def __print_info(self, label, a, b, amp, com, sigma, conv_fact, comabs):
        print("*** " + label + " Gaussian Fit ***:")
        print("   Inclination: " + '{:.3e}'.format(a))
        print("    Background: " + '{:.3f}'.format(b))
        print("     Amplitude: " + '{:.3f}'.format(amp))
        print("         Sigma: " + '{:.3f}'.format(sigma))
        print("          FWHM: " + '{:.3f}'.format(self.sig2fwmh*sigma))
        print("          Mean: " + '{:.3f}'.format(comabs))
        print("     Sigma(um): " + '{:.3f}'.format(sigma*conv_fact))
        print("      FWHM(um): " + '{:.3f}'.format(sigma*conv_fact*self.sig2fwmh))

    def BPM1_Vertical_Profile(self):
        label = "BPM1 Vertical Profile"
        print("Analysing...")
        self.__grabdata_bpm1()
        vec = caget("PINK:PG01:Stats2:ProfileAverageY_RBV")
        N = int(self.roisizey)
        pos0 = self.roiposy
        pos1 = self.roiposy+self.roisizey
        myCF = self.bpm1_vert_CF
        filename="bpm1_ver"
        self.__bpmanalysis(vec, pos0, pos1, N, label, filename, myCF)

    def BPM1_Horizontal_Profile(self):
        label = "BPM1 Horizontal Profile"
        print("Analysing...")
        self.__grabdata_bpm1()
        vec = caget("PINK:PG01:Stats2:ProfileAverageX_RBV")
        N = int(self.roisizex)
        pos0 = self.roiposx
        pos1 = self.roiposx+self.roisizex
        myCF = self.bpm1_hor_CF
        filename="bpm1_hor"
        self.__bpmanalysis(vec, pos0, pos1, N, label, filename, myCF)

    def BPM2_Vertical_Profile(self):
        label = "BPM2 Vertical Profile"
        print("Analysing...")
        self.__grabdata_bpm2()
        vec = caget("PINK:PG04:Stats2:ProfileAverageY_RBV")
        N = int(self.roisizey)
        pos0 = self.roiposy
        pos1 = self.roiposy+self.roisizey
        myCF = self.bpm2_vert_CF
        filename="bpm2_ver"
        self.__bpmanalysis(vec, pos0, pos1, N, label, filename, myCF)

    def BPM2_Horizontal_Profile(self):
        label = "BPM2 Horizontal Profile"
        print("Analysing...")
        self.__grabdata_bpm2()
        vec = caget("PINK:PG04:Stats2:ProfileAverageX_RBV")
        N = int(self.roisizex)
        pos0 = self.roiposx
        pos1 = self.roiposx+self.roisizex
        myCF = self.bpm2_hor_CF
        filename="bpm2_hor"
        self.__bpmanalysis(vec, pos0, pos1, N, label, filename, myCF)

    def BPM3_Vertical_Profile(self):
        label = "BPM3 Vertical Profile"
        print("Analysing...")
        self.__grabdata_bpm3()
        vec = caget("PINK:PG03:Stats2:ProfileAverageY_RBV")
        N = int(self.roisizey)
        pos0 = self.roiposy
        pos1 = self.roiposy+self.roisizey
        myCF = self.bpm3_vert_CF
        filename="bpm3_ver"
        self.__bpmanalysis(vec, pos0, pos1, N, label, filename, myCF)

    def BPM3_Horizontal_Profile(self):
        label = "BPM3 Horizontal Profile"
        print("Analysing...")
        self.__grabdata_bpm3()
        vec = caget("PINK:PG03:Stats2:ProfileAverageX_RBV")
        N = int(self.roisizex)
        pos0 = self.roiposx
        pos1 = self.roiposx+self.roisizex
        myCF = self.bpm3_hor_CF
        filename="bpm3_hor"
        self.__bpmanalysis(vec, pos0, pos1, N, label, filename, myCF)

    def BPM4_Vertical_Profile(self):
        label = "BPM4 Vertical Profile"
        print("Analysing...")
        self.__grabdata_bpm4()
        vec = caget("PINK:PG02:Stats2:ProfileAverageY_RBV")
        N = int(self.roisizey)
        pos0 = self.roiposy
        pos1 = self.roiposy+self.roisizey
        myCF = self.bpm4_vert_CF
        filename="bpm4_ver"
        self.__bpmanalysis(vec, pos0, pos1, N, label, filename, myCF)

    def BPM4_Horizontal_Profile(self):
        label = "BPM4 Horizontal Profile"
        print("Analysing...")
        self.__grabdata_bpm4()
        vec = caget("PINK:PG02:Stats2:ProfileAverageX_RBV")
        N = int(self.roisizex)
        pos0 = self.roiposx
        pos1 = self.roiposx+self.roisizex
        myCF = self.bpm4_hor_CF
        filename="bpm4_hor"
        self.__bpmanalysis(vec, pos0, pos1, N, label, filename, myCF)

    def __grabdata_bpm1(self):
        self.roiposx = caget("PINK:PG01:ROI1:MinX_RBV")
        self.roiposy = caget("PINK:PG01:ROI1:MinY_RBV")
        self.roisizex = caget("PINK:PG01:ROI1:SizeX_RBV")
        self.roisizey = caget("PINK:PG01:ROI1:SizeY_RBV")
        self.cam_exposure = caget("PINK:PG01:AcquireTime_RBV")
        self.cam_gain = caget("PINK:PG01:Gain_RBV")

    def __grabdata_bpm2(self):
        self.roiposx = caget("PINK:PG04:ROI1:MinX_RBV")
        self.roiposy = caget("PINK:PG04:ROI1:MinY_RBV")
        self.roisizex = caget("PINK:PG04:ROI1:SizeX_RBV")
        self.roisizey = caget("PINK:PG04:ROI1:SizeY_RBV")
        self.cam_exposure = caget("PINK:PG04:AcquireTime_RBV")
        self.cam_gain = caget("PINK:PG04:Gain_RBV")

    def __grabdata_bpm3(self):
        self.roiposx = caget("PINK:PG03:ROI1:MinX_RBV")
        self.roiposy = caget("PINK:PG03:ROI1:MinY_RBV")
        self.roisizex = caget("PINK:PG03:ROI1:SizeX_RBV")
        self.roisizey = caget("PINK:PG03:ROI1:SizeY_RBV")
        self.cam_exposure = caget("PINK:PG03:AcquireTime_RBV")
        self.cam_gain = caget("PINK:PG03:Gain_RBV")

    def __grabdata_bpm4(self):
        self.roiposx = caget("PINK:PG02:ROI1:MinX_RBV")
        self.roiposy = caget("PINK:PG02:ROI1:MinY_RBV")
        self.roisizex = caget("PINK:PG02:ROI1:SizeX_RBV")
        self.roisizey = caget("PINK:PG02:ROI1:SizeY_RBV")
        self.cam_exposure = caget("PINK:PG02:AcquireTime_RBV")
        self.cam_gain = caget("PINK:PG02:Gain_RBV")

    def __bpmanalysis(self, vec, pos0, pos1, N, label, filename, myCF):

        vecb = vec[0:N]
        xvecabs = range(pos0,pos1)
        xvec = range(0,N)
        weights = [ 1.0] * len(xvec)
        #pl = plot(vecb, label , xvec)[0]
        pl = plot(vecb, label, xvecabs)[0]
        pl.setLegendVisible(True)
        (a, b, amp, com, sigma) = fit_gaussian_linear(vecb, xvec, None, weights)
        self.__print_info(label, a, b, amp, com, sigma, myCF, com+pos0)
        ff = Gaussian(amp, com, sigma)
        gauss = [ff.value(i) + a*i + b for i in xvec]
        ss = LinePlotSeries("Gaussian Fit")
        pl.addSeries(ss)
        #ss.setData(xvec, gauss)
        ss.setData(xvecabs, gauss)
        self.__setup_file(fname=filename)
        self.__Save_Data(label, myCF, a, b, amp, com, com+pos0, sigma, sigma*self.sig2fwmh, sigma*myCF, sigma*self.sig2fwmh*myCF, xvecabs, vecb, gauss)


    def __setup_file(self, fname="bpm"):
        set_exec_pars(open=False, name=fname, reset=True)

    def __Save_Data(self, label, CV, ga, gb, gamp, gmean, gmeanabs, gsigma, gfwhm, gsigmaum, gfwhmum, xdata, yprofile, ygauss):
        save_dataset("info/bpm", label)
        save_dataset("camera/exposure", self.cam_exposure)
        save_dataset("camera/gain", self.cam_gain)
        save_dataset("camera/conv_factor", CV)
        save_dataset("ROI/MinX", self.roiposx)
        save_dataset("ROI/MinY", self.roiposy)
        save_dataset("ROI/SizeX", self.roisizex)
        save_dataset("ROI/SizeY", self.roisizey)
        save_dataset("gaussian/inclination", ga)
        save_dataset("gaussian/background", gb)
        save_dataset("gaussian/amplitude", gamp)
        save_dataset("gaussian/mean_roi", gmean)
        save_dataset("gaussian/mean_absolute", gmeanabs)
        save_dataset("gaussian/sigma", gsigma)
        save_dataset("gaussian/FWHM", gfwhm)
        save_dataset("gaussian/sigma_um", gsigmaum)
        save_dataset("gaussian/FWHM_um", gfwhmum)
        save_dataset("plot/xdata", xdata)
        save_dataset("plot/profile", yprofile)
        save_dataset("plot/gauss_fit", ygauss)

