## PINKPLOT
class PINKPLOT():
    def plot(self, filepath):
        path = filepath.split('|')
        if len(path)!=2 or len(path[1])>1:
            print("Error: Path invalid")
            return
        pname = path[0].split('_')
        pname = pname[2]

        ## load data from file
        try:
            title = load_data(filepath+"plot/title")
            xlabel = load_data(filepath+"plot/xlabel")
            ylabel = load_data(filepath+"plot/ylabel")
            x = load_data(filepath+"plot/x")
            y = load_data(filepath+"plot/y")
            y_desc = load_data(filepath+"plot/y_desc")
        except:
            print("Error loading data")
            return

        p1h=plot(None, y_desc[0], title=pname)
        p1 = p1h.get(0)
        p1.setTitle(title)
        p1.getAxis(p1.AxisId.X).setLabel(xlabel)
        p1.getAxis(p1.AxisId.Y).setLabel(ylabel)

        for i in range(len(y)):
            if i>0:
                p1.addSeries(LinePlotSeries(y_desc[i]))
            p1.getSeries(i).setData(x, y[i])

        #if len(y)>1:
        p1.setLegendVisible(True)
