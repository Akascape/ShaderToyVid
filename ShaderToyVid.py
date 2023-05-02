#####################------ShaderToyVid------######################
#Author: Akash Bora
#License: MIT (without any warranty)
#Version: 0.3 beta

# import the required modules
import arcade
from arcade.experimental.shadertoy import Shadertoy
import cv2
import tkinter
import customtkinter
import os
import numpy

class HomePage(customtkinter.CTk):
    
    global ofile, sfile  
    ofile = ""
    WIDTH = 400
    HEIGHT = 700

    def __init__(self):
        super().__init__()
        self.title("ShaderToyVid")
        self.geometry(f"{HomePage.WIDTH}x{HomePage.HEIGHT}+{50}+{50}")
        self.minsize(300, 700)
        self.configure(fg_color="#181b28")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<1>", lambda event: event.widget.focus_set())
        self.frame = customtkinter.CTkFrame(master=self, fg_color="#181b28", border_width=2, border_color="#10121f")
        self.frame.grid(row=0, column=0, sticky="nswe", padx=(10,10), pady=20)
        self.frame.grid_columnconfigure((0,1), weight=1)
        self.frame.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)
        
        # button for importing video
        self.open_video = customtkinter.CTkButton(master=self.frame, height=40,
                                                text="Input Video", fg_color="#212435",
                                                font=("Roboto Medium",15),
                                                command=self.open_vid)
        self.open_video.grid(row=0, column=0, padx=30, pady=(30,0),sticky="we", columnspan=2)

        self.label_1 = customtkinter.CTkLabel(master=self.frame, width=320, height=25,
                                              text="Choose a Shader Effect",
                                              font=("Roboto Medium", -16)) 
        self.label_1.grid(row=1, column=0, pady=(15,0), padx=30, sticky="we", columnspan=2)

        # Import some shaders from the default folder (My Shaders) if exists        
        myeffect=["Custom"]
        try:
            self.mydir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "My Shaders")
            scriptfiles = os.listdir(self.mydir)
            for i in scriptfiles:
                myeffect.append(i)
        except:
            print("No shaders found!")

        # option Menu   
        self.combobox_1 = customtkinter.CTkOptionMenu(master=self.frame, width=120, height=35, button_color="#212435", hover=False,
                                                fg_color="#212435", dropdown_fg_color="#212435", dropdown_hover_color="#181b28",
                                                values=myeffect, command=self.open_script) 
        self.combobox_1.grid(row=2, column=0, pady=20, padx=30, sticky="we", columnspan=2)

        # the code box
        self.textbox = customtkinter.CTkTextbox(master=self.frame, fg_color="#212435", border_width=1, corner_radius=15, height=300)
        self.textbox.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 0), sticky="nsew")

        # preview Button
        self.previewButton = customtkinter.CTkButton(master=self.frame,
                                                width=140,
                                                height=40,
                                                text="PREVIEW",
                                                fg_color="#212435",
                                                font=("Roboto Medium",15),
                                                command=self.render_show)
        self.previewButton.grid(row=4, column=0, padx=(20,5), pady=(25,10), sticky="we")

        # render Button
        self.saveButton = customtkinter.CTkButton(master=self.frame,
                                                width=140,
                                                height=40,
                                                text="RENDER",
                                                fg_color="#212435",
                                                font=("Roboto Medium",15),
                                                command=self.render_export)
        self.saveButton.grid(row=4, column=1, padx=(5,20), pady=(25,10), sticky="we")
    
        # save options
        self.option_switch = customtkinter.CTkSwitch(master=self.frame, text="Sequence",
                                                     progress_color="#4a4d50")
        self.option_switch.grid(row=5, column=0, padx=(60, 10), pady=10, sticky="w")

        self.label_2 = customtkinter.CTkLabel(master=self.frame, width=10, height=20,
                                              text="Video")
        self.label_2.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        
        # version label
        self.label_3 = customtkinter.CTkLabel(master=self.frame, width=10, height=20,
                                              text="v0.3 beta")      
        self.label_3.grid(row=5, column=1, padx=10, sticky="se")

    def open_vid(self):
        """ opens the filedialog to import a video """
        global ofile
        ofile = tkinter.filedialog.askopenfilename(filetypes =[('Video', ['*mp4','*mov','*avi','*mkv']),('All Files', '*.*')])
        if ofile:
            self.open_video.configure(text=os.path.basename(ofile))
        else:
            self.open_video.configure(text="Input Video")
            
    def open_script(self, value):
        """ opens a filedialog to import a script with the custom option """
        global sfile
        if value=="Custom":
            sfile = tkinter.filedialog.askopenfilename(filetypes =[('GLSL Script', ['*txt','*glsl','*webgl']),('All Files', '*.*')])
            if sfile:
                with open(sfile, 'r') as f:
                    self.textbox.delete("1.0","end")
                    self.textbox.insert(1.0, f.read())
                f.close()
        else:
            with open(os.path.join(self.mydir, value), 'r') as f:
                    self.textbox.delete("1.0","end")
                    self.textbox.insert(1.0, f.read())
            f.close()

    def render_show(self):
        """ preview the rendered window """
        global preview
        if not ofile:
            tkinter.messagebox.showinfo("No Input Channel", "Please Import a Video!")
            return
        elif self.textbox.get(1.0, "end-1c")=="":
            tkinter.messagebox.showinfo("No Script", "Please enter your script in the textbox!")
            return
        preview = True
        
        try:
            self.saveButton.configure(state=tkinter.DISABLED)
            self.previewButton.configure(state=tkinter.DISABLED)
            self.process()
            #import threading #Live Preview Test (Unstable)
            #threading.Thread(target=self.process).start()
            self.saveButton.configure(state=tkinter.NORMAL)
            self.previewButton.configure(state=tkinter.NORMAL)
        except:
            self.saveButton.configure(state=tkinter.NORMAL)
            self.previewButton.configure(state=tkinter.NORMAL)
            print("Shader Error")
            arcade.exit()
            return

    def render_export(self):
        """ render out the shader """
        global preview, newdir, output_file
        if not ofile:
            tkinter.messagebox.showinfo("No input channel found", "Please import a video file!")
            return
        elif self.textbox.get(1.0, "end-1c")=="":
            tkinter.messagebox.showinfo("No script found", "Please enter some script in the textbox!")
            return
        res = tkinter.messagebox.askquestion("Export","Do you want to render the video with this shader?")
        
        if res=="yes":
            pass
        elif res=="no":
            return
        
        preview = False
        
        if self.option_switch.get()==1:
            newdir = os.path.splitext(ofile)[0]+"_"+os.path.splitext(self.combobox_1.get())[0]
            nf = 0
            while os.path.exists(newdir):
                nf = nf+1
                newdir = os.path.splitext(ofile)[0]+"_"+os.path.splitext(self.combobox_1.get())[0]+"("+str(nf)+")"
            os.mkdir(newdir) # make a new folder where the png image sequence will be saved
        else:
            output_file = tkinter.filedialog.asksaveasfilename(filetypes =[('Video', ['*.mp4','*.avi','*.mov','*.mkv']),('All Files', '*.*')],
                                                 initialfile=os.path.splitext(ofile)[0]+os.path.splitext(self.combobox_1.get())[0]+".mp4")
            if not output_file:
                return
        try:
            self.saveButton.configure(state=tkinter.DISABLED)
            self.previewButton.configure(state=tkinter.DISABLED)
            self.process()
            self.saveButton.configure(state=tkinter.NORMAL)
            self.previewButton.configure(state=tkinter.NORMAL)
        except:
            self.saveButton.configure(state=tkinter.NORMAL)
            self.previewButton.configure(state=tkinter.NORMAL)   
            print("Shader Error")
            if preview==False:
                print("Error loading the frames, please retry!")
            arcade.exit()
            return
        
        if self.option_switch.get()==0 and preview==False:
            self.out.release() # incase the render window is closed forcefully
            
    def process(self):
        """ connect the shadertoy process from arcade """
        global preview, currentframe, newdir, output_file
        SCREEN_WIDTH = 100
        SCREEN_HEIGHT = 100
        SCREEN_TITLE = "ShaderToy Video"
        currentframe = 0
        
        class ShadertoyVideo(arcade.Window):
            global currentframe
            def __init__(self2, width, height, title):
                super().__init__(width, height, title, resizable=True)
                try:
                    self2.shadertoy = Shadertoy(
                            self2.get_framebuffer_size(),
                            self.textbox.get(1.0, "end-1c"))
                except:
                    self2.close()
                self2.video = cv2.VideoCapture(ofile)
                width, height = (
                    int(self2.video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self2.video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                self2.video_texture = self2.ctx.texture((width, height), components=3)
                self2.video_texture.wrap_x = self2.ctx.CLAMP_TO_EDGE
                self2.video_texture.wrap_y = self2.ctx.CLAMP_TO_EDGE
                self2.video_texture.swizzle = "BGR1"
                self2.shadertoy.channel_0 = self2.video_texture
                self2.set_size(width, height)
                if self.option_switch.get()==0 and preview==False:
                    self.out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), self2.video.get(cv2.CAP_PROP_FPS), (width, height))
                
            def on_draw(self2):
                self2.clear()
                self2.shadertoy.render()
                
            def on_update(self2, delta_time: float):
                self2.shadertoy.time += delta_time
                self2.next_frame()
                self2.shadertoy.resize(self2.get_framebuffer_size())
                
            def on_resize(self2, width: float, height: float):
                super().on_resize(width, height)
                
            def next_frame(self2):
                global currentframe
                exists, frame = self2.video.read()
                frame = cv2.flip(frame, 0)
                if frame is not None:
                    self2.video_texture.write(frame)
                    if preview==False:
                        if currentframe!=0:
                            image = arcade.get_image()
                            if self.option_switch.get()==1:
                                name = os.path.join(newdir, 'Frame-' + (str(currentframe)).zfill(6) + ".png")
                                image.save(name,'PNG')
                            else:
                                self.out.write(cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR))
                        currentframe +=1    
                else:
                    if preview==False:
                        arcade.finish_render()
                        arcade.exit()
                        self2.close()
                        if self.option_switch.get()==1:
                            tkinter.messagebox.showinfo("Done!", "PNG Sequence saved: "+str(newdir))
                        else:
                            self.out.release()
                            tkinter.messagebox.showinfo("Done!", "Video saved: "+os.path.basename(output_file))
                    else:
                        self2.video.set(1, 0)
                #self2.shadertoy.reload(self.textbox.get(1.0, "end-1c")) #Live Preview Test (Unstable)
                            
        if __name__ == "__main__":
            ShadertoyVideo(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
            arcade.run()
            
    def on_closing(self, event=0):
        self.destroy()
        arcade.exit()
        
    def start(self):
        self.mainloop()
        
if __name__ == "__main__":
    app = HomePage()
    app.start()
