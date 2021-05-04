import tkinter as tk
from tkinter import messagebox
from canvasvg import saveall
from xcanvas import XCanvas


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_gene_info(self):
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)
        leftframe = tk.Frame(frame)
        leftframe.pack(side="left", padx=10, pady=10)
        lbl = tk.Label(leftframe, text="Gene Sequence", width=20)
        lbl.pack(side="top", padx =10, pady=10)
        lbl2 = tk.Label(leftframe, text="(Fasta Only)", width=20)
        lbl2.pack(side="bottom", padx = 10 , pady=5)
        self.genetxt = tk.Text(frame)
        self.genetxt.pack(fill="both", pady=10, padx=10, expand=True)

    def create_highlight_info(self):
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)
        leftframe = tk.Frame(frame)
        leftframe.pack(side="left", padx=10, pady=10)
        lbl = tk.Label(leftframe, text="(option)Highlight", width=20)
        lbl.pack(side="top", padx =10, pady=10)
        lbl2 = tk.Label(leftframe, text="ex)\n(1208..1310, 1520..1600)", width=20)
        lbl2.pack(side="bottom", padx = 10 , pady=5)
        self.highlighttxt = tk.Text(frame)
        self.highlighttxt.pack(fill="both", pady=10, padx=10, expand=True)

    def create_widgets(self):
        self.create_gene_info()
        self.create_highlight_info()
        frame = tk.Frame(self)
        frame.pack(side="bottom")
        process_btn = tk.Button(frame)
        process_btn["text"] = "Process"
        process_btn["command"] = self.create_compass_figuration
        process_btn.pack(side="left", padx=10)

        process_btn = tk.Button(frame)
        process_btn["text"] = "Process & Save"
        process_btn["command"] = self.create_compass_figuration_and_save
        process_btn.pack(side="left", padx=10)

    def calc_compass(self):
        all_gene = self.genetxt.get("1.0","end-1c")
        self.name = ">EmptyName"
        if all_gene.startswith('>') : 
            self.name ,sep,all_gene = all_gene.partition("\n")
            self.topLevel.title(self.name[1:])
            print("fasta 포맷에 의해 유전자 이름을 도출해 냈습니다. ", self.name[1:])

        range_list = []
        highlight = self.highlighttxt.get("1.0", "end-1c").replace("(", "").replace(")", ",").replace("\n", "").replace("\r", "")
        if highlight != "" :
            raw_ranges = highlight.split(",")
            #print(raw_ranges)
            for range_str in raw_ranges :
                if range_str != "":
                    rans = range_str.split("..")
                    range_list.append((int(rans[0]), int(rans[1])))
            print("총 ", len(range_list), "개의 하이라이트 유전자가 검색 되었습니다.")
        #print(range_list)
        x = 0
        y = 0
        n = -1
        high_lines = {}
        lines = [x,y]
        width = (0,0)
        height = (0,0)
        for c in all_gene:
            n = n + 1
            if c == "A":
                y = y - 1
            elif c == "T":
                y = y + 1
            elif c == "C":
                x = x - 1
            elif c == "G":
                x = x + 1
            else :
                continue
            lines.append(x)
            lines.append(y)
            width = (min(x, width[0]), max(x,width[1]))
            height = (min(y, height[0]), max(y,height[1]))
            # highlight 
            for r in range_list:
                if r[0] <= n and r[1] >= n:
                    if high_lines.get(r[0], None) == None:
                        high_lines[r[0]] = []
                    high_lines[r[0]].append(x)
                    high_lines[r[0]].append(y)

        return lines, high_lines, width, height

    def create_canvas(self):
        self.topLevel = tk.Toplevel(self.master)
        self.topLevel.geometry("1024x720+100+100")
        self.topLevel.title("Compass Figuration")
        lines , high_lines, width, height = self.calc_compass()
        canvas = XCanvas(self.topLevel, width = width[1]- width[0]+150, height=height[1]-height[0] , bg="white", bd=2)
        canvas.pack(fill="both", expand=True)
        l = canvas.create_line(tuple(lines), fill="black")
        canvas.move(l, -width[0]+150, -height[0])

        for highlines in high_lines.values() :            
            hl = canvas.create_line(tuple(highlines), fill="red", width=1)
            canvas.move(hl, -width[0]+150, -height[0])
        canvas.scalewidget.place(x=0, y=0)
        
        print("그리기 완료 : 캔버스가 성공적으로 그려졌습니다.")
        return canvas

    def create_compass_figuration(self):
        self.create_canvas()
        

    def create_compass_figuration_and_save(self):
        saveall(self.name[1:] + '.svg', self.create_canvas())
        print("저장완료 : ", self.name[1:] + ".svg 파일에 저장되었습니다.")


root = tk.Tk()
root.title("BICME")
print("BICME 프로그램을 가동 합니다.")
app = Application(master=root)
app.mainloop()