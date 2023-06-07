#####################------ShaderToyVid------######################

#Author: Akash Bora
#License: MIT (without any warranty)
#Version: 0.5 beta
#HomePage: https://github.com/Akascape/ShaderToyVid

import arcade
from arcade.experimental.shadertoy import Shadertoy
import cv2
import tkinter
import customtkinter
import os
import numpy
import warnings

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
        self.font = customtkinter.ThemeManager.theme["CTkFont"]["family"]
        
        self.frame = customtkinter.CTkFrame(master=self, fg_color="#181b28", border_width=2, border_color="#10121f")
        self.frame.grid(row=0, column=0, sticky="nswe", padx=(10,10), pady=20)
        self.frame.grid_columnconfigure((0,1), weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        
        # button for importing video
        self.open_video = customtkinter.CTkButton(master=self.frame, height=40, text="Input Video", fg_color="#212435",
                                                font=(self.font,15,"bold"), command=self.open_vid)
        self.open_video.grid(row=0, column=0, padx=30, pady=(30,0),sticky="we", columnspan=2)
        
        self.click_menu = tkinter.Menu(self.frame, tearoff=False, background='#343e5a', fg='white', borderwidth=0, bd=0)
        self.click_menu.add_command(label="import texture", command=lambda: self.add_texture())
        
        self.open_video.bind("<Button-3>", lambda event: self.do_popup(event, frame=self.click_menu))
        
        self.label_1 = customtkinter.CTkLabel(master=self.frame, width=320, height=25, text="Choose Shader Effect",
                                              font=(self.font, -16)) 
        self.label_1.grid(row=1, column=0, pady=(15,0), padx=30, sticky="we", columnspan=2)

        # Import some shaders from the default folder (My Shaders) if exists        
        myeffect=["Custom"]
        try:
            self.mydir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "My Shaders")
            scriptfiles = os.listdir(self.mydir)
            for i in scriptfiles:
                if os.path.splitext(i)[1]==".glsl":
                    myeffect.append(i)
        except:
            print("No shaders found!")
    
        # option Menu   
        self.combobox_1 = customtkinter.CTkOptionMenu(master=self.frame, width=120, height=35, button_color="#212435", hover=False,
                                                     fg_color="#212435", dropdown_fg_color="#212435", dropdown_hover_color="#181b28",
                                                     values=myeffect, command=self.open_script) 
        self.combobox_1.grid(row=2, column=0, pady=20, padx=30, sticky="we", columnspan=2)

        self.tabview = customtkinter.CTkTabview(self.frame, fg_color="#181b28", height=400,
                                                segmented_button_fg_color="#0e1321",
                                                segmented_button_unselected_color="#0e1321")
        self.tabview.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 0), sticky="nsew")
        self.tabview.add("Common")
        self.tabview.add("Image")
        self.tabview.add("Buf A")
        self.tabview.add("Buf B")
        self.tabview.add("Buf C")
        self.tabview.add("Buf D")
        self.tabview.set("Image")
        
        self.values = ["None", "Video", "Buf A", "Buf B", "Buf C", "Buf D"]
        self.textures = {}
        self.num = 0
        # the code box for Common Tab
        self.textbox_common = customtkinter.CTkTextbox(master=self.tabview.tab("Common"), fg_color="#212435", border_width=1, corner_radius=15, height=200)
        self.textbox_common.pack(fill="both",padx=5, pady=5, expand=True)
        
        # the code box for Image Tab
        self.textbox = customtkinter.CTkTextbox(master=self.tabview.tab("Image"), fg_color="#212435", border_width=1, corner_radius=15, height=200)
        self.textbox.pack(fill="both",padx=5, pady=5, expand=True)

        self.ichannel_0 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Image"), fg_color="#0e1321", button_color="#212435",
                                                      values=self.values, height=20, width=10)
        self.ichannel_0.pack(padx=5, pady=5, side="left", expand=True, fill="x")
        self.ichannel_0.set("Video")
        
        self.ichannel_1 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Image"), fg_color="#0e1321", button_color="#212435",
                                                      values=self.values, height=20, width=10)
        self.ichannel_1.pack(padx=5, pady=5, side="left", expand=True, fill="x")
        
        self.ichannel_2 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Image"), fg_color="#0e1321", button_color="#212435",
                                                      values=self.values, height=20, width=10)
        self.ichannel_2.pack(padx=5, pady=5, side="left", expand=True, fill="x")
        
        self.ichannel_3 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Image"), fg_color="#0e1321", button_color="#212435",
                                                      values=self.values, height=20, width=10)
        self.ichannel_3.pack(padx=5, pady=5, side="left", expand=True, fill="x")

        # the code box for Buf A Tab
        self.textbox_A = customtkinter.CTkTextbox(master=self.tabview.tab("Buf A"), fg_color="#212435", border_width=1, corner_radius=15, height=200)
        self.textbox_A.pack(fill="both",padx=5, pady=5, expand=True)

        self.buff_A_ichannel_0 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf A"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_A_ichannel_0.pack(padx=5, pady=5, side="left", expand=True, fill="x")
        
        self.buff_A_ichannel_1 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf A"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_A_ichannel_1.pack(padx=5, pady=5, side="left", expand=True, fill="x")
        
        self.buff_A_ichannel_2 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf A"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_A_ichannel_2.pack(padx=5, pady=5, side="left", expand=True, fill="x")
    
        self.buff_A_ichannel_3 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf A"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_A_ichannel_3.pack(padx=5, pady=5, side="left", expand=True, fill="x")

        # the code box for Buf B Tab
        self.textbox_B = customtkinter.CTkTextbox(master=self.tabview.tab("Buf B"), fg_color="#212435", border_width=1, corner_radius=15, height=200)
        self.textbox_B.pack(fill="both",padx=5, pady=5, expand=True)

        self.buff_B_ichannel_0 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf B"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_B_ichannel_0.pack(padx=5, pady=5, side="left", expand=True, fill="x")
        
        self.buff_B_ichannel_1 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf B"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_B_ichannel_1.pack(padx=5, pady=5, side="left", expand=True, fill="x")
    
        self.buff_B_ichannel_2 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf B"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_B_ichannel_2.pack(padx=5, pady=5, side="left", expand=True, fill="x")
        
        self.buff_B_ichannel_3 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf B"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_B_ichannel_3.pack(padx=5, pady=5, side="left", expand=True, fill="x")

        # the code box for Buf C Tab
        self.textbox_C = customtkinter.CTkTextbox(master=self.tabview.tab("Buf C"), fg_color="#212435", border_width=1, corner_radius=15, height=200)
        self.textbox_C.pack(fill="both",padx=5, pady=5, expand=True)

        self.buff_C_ichannel_0 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf C"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_C_ichannel_0.pack(padx=5, pady=5, side="left", expand=True, fill="x")
        
        self.buff_C_ichannel_1 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf C"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_C_ichannel_1.pack(padx=5, pady=5, side="left", expand=True, fill="x")
    
        self.buff_C_ichannel_2 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf C"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_C_ichannel_2.pack(padx=5, pady=5, side="left", expand=True, fill="x")
        
        self.buff_C_ichannel_3 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf C"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_C_ichannel_3.pack(padx=5, pady=5, side="left", expand=True, fill="x")

        # the code box for Buf D Tab
        self.textbox_D = customtkinter.CTkTextbox(master=self.tabview.tab("Buf D"), fg_color="#212435", border_width=1, corner_radius=15, height=200)
        self.textbox_D.pack(fill="both",padx=5, pady=5, expand=True)

        self.buff_D_ichannel_0 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf D"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_D_ichannel_0.pack(padx=5, pady=5, side="left", expand=True, fill="x")
        
        self.buff_D_ichannel_1 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf D"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_D_ichannel_1.pack(padx=5, pady=5, side="left", expand=True, fill="x")
    
        self.buff_D_ichannel_2 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf D"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_D_ichannel_2.pack(padx=5, pady=5, side="left", expand=True, fill="x")
        
        self.buff_D_ichannel_3 = customtkinter.CTkOptionMenu(master=self.tabview.tab("Buf D"), fg_color="#0e1321", button_color="#212435",
                                                             values=self.values, height=20, width=10)
        self.buff_D_ichannel_3.pack(padx=5, pady=5, side="left", expand=True, fill="x")
        
        # preview Button
        self.previewButton = customtkinter.CTkButton(master=self.frame, width=140, height=40, text="PREVIEW", fg_color="#212435", font=(self.font,15,"bold"),
                                                     command=self.render_show)
        self.previewButton.grid(row=4, column=0, padx=(20,5), pady=(25,10), sticky="we")

        # render Button
        self.saveButton = customtkinter.CTkButton(master=self.frame, width=140, height=40, text="RENDER", fg_color="#212435", font=(self.font,15,"bold"),
                                                  command=self.render_export)
        self.saveButton.grid(row=4, column=1, padx=(5,20), pady=(25,10), sticky="we")

        # save options
        self.option_switch = customtkinter.CTkSwitch(master=self.frame, text="Sequence", progress_color="#4a4d50")
        self.option_switch.grid(row=5, column=0, padx=(60, 10), pady=10, sticky="w")

        self.label_2 = customtkinter.CTkLabel(master=self.frame, width=10, height=20, text="Video")
        self.label_2.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        
        # version label
        self.label_3 = customtkinter.CTkLabel(master=self.frame, width=10, height=20, text="v0.5 beta")      
        self.label_3.grid(row=5, column=1, padx=10, pady=5, sticky="se")
        
    def add_texture(self):
        texture_file = tkinter.filedialog.askopenfilename(filetypes =[('Image', ['*jpg','*png']),('All Files', '*.*')])
        if texture_file:
            self.textures[f"texture{self.num}"] = texture_file
            self.values.append(f"texture{self.num}")
            self.num+=1
            
            self.ichannel_0.configure(values=self.values)
            self.ichannel_1.configure(values=self.values)
            self.ichannel_2.configure(values=self.values)
            self.ichannel_3.configure(values=self.values)
            
            self.buff_A_ichannel_0.configure(values=self.values)
            self.buff_A_ichannel_1.configure(values=self.values)
            self.buff_A_ichannel_2.configure(values=self.values)
            self.buff_A_ichannel_3.configure(values=self.values)
            
            self.buff_B_ichannel_0.configure(values=self.values)
            self.buff_B_ichannel_1.configure(values=self.values)
            self.buff_B_ichannel_2.configure(values=self.values)
            self.buff_B_ichannel_3.configure(values=self.values)

            self.buff_C_ichannel_0.configure(values=self.values)
            self.buff_C_ichannel_1.configure(values=self.values)
            self.buff_C_ichannel_2.configure(values=self.values)
            self.buff_C_ichannel_3.configure(values=self.values)

            self.buff_D_ichannel_0.configure(values=self.values)
            self.buff_D_ichannel_1.configure(values=self.values)
            self.buff_D_ichannel_2.configure(values=self.values)
            self.buff_D_ichannel_3.configure(values=self.values)             
            
    def do_popup(self, event, frame):
            try: frame.tk_popup(event.x_root, event.y_root)
            finally: frame.grab_release()
            
    def open_vid(self):
        """ opens the filedialog to import a video """
        global ofile
        ofile = tkinter.filedialog.askopenfilename(filetypes =[('Video', ['*mp4','*mov','*avi','*mkv']),('All Files', '*.*')])
        if ofile:
            self.open_video.configure(text=os.path.basename(ofile))
        else:
            self.open_video.configure(text="Input Video")
            
    def add_code(self, code):
        if self.tabview.get()=="Image":
            self.textbox.delete("1.0","end")
            self.textbox.insert(1.0, code)
        elif self.tabview.get()=="Common":
            self.textbox_common.delete("1.0","end")
            self.textbox_common.insert(1.0, code)
        elif self.tabview.get()=="Buf A":
            self.textbox_A.delete("1.0","end")
            self.textbox_A.insert(1.0, code)
        elif self.tabview.get()=="Buf B":
            self.textbox_B.delete("1.0","end")
            self.textbox_B.insert(1.0, code)
        elif self.tabview.get()=="Buf C":
            self.textbox_C.delete("1.0","end")
            self.textbox_C.insert(1.0, code)
        elif self.tabview.get()=="Buf D":
            self.textbox_D.delete("1.0","end")
            self.textbox_D.insert(1.0, code)
            
    def open_script(self, value):
        """ opens a filedialog to import a script with the custom option """
        global sfile
        if value=="Custom":
            sfile = tkinter.filedialog.askopenfilename(filetypes =[('GLSL Script', ['*txt','*glsl','*webgl']),('All Files', '*.*')])
            if sfile:
                with open(sfile, 'r') as f:             
                    self.add_code(f.read())
                f.close()
        else:
            with open(os.path.join(self.mydir, value), 'r') as f:
                    self.add_code(f.read())          
            f.close()

    def render_show(self):
        """ preview the rendered window """
        global preview
        if not ofile:
            tkinter.messagebox.showinfo("No Input Channel", "Please Import a Video!")
            return
        elif len(self.textbox.get(1.0, "end-1c"))<5:
            tkinter.messagebox.showinfo("No Script", "Please enter your script in the textbox!")
            return
        preview = True
        
        try:
            self.saveButton.configure(state=tkinter.DISABLED)
            self.previewButton.configure(state=tkinter.DISABLED)
            self.process()
            self.saveButton.configure(state=tkinter.NORMAL)
            self.previewButton.configure(state=tkinter.NORMAL)
        except:
            self.saveButton.configure(state=tkinter.NORMAL)
            self.previewButton.configure(state=tkinter.NORMAL)
            warnings.warn("Shader Error")
            arcade.exit()
            return

    def render_export(self):
        """ render out the shader """
        global preview, newdir, output_file
        if not ofile:
            tkinter.messagebox.showinfo("No input channel found", "Please import a video file!")
            return
        elif len(self.textbox.get(1.0, "end-1c"))<5:
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
            warnings.warn("Shader Error")
            if preview==False:
                warnings.warn("Error loading the frames, please retry!")
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
            
            def add_channels(window, self, channel, buffer, boxes):
                box = eval(f"{boxes}_{channel}")
                buf_channel = eval(f"buffer.channel_{channel}")
                
                if box.get()=="Video":
                    buf_channel = window.video_texture
                elif box.get()=="Buf A":
                    buf_channel = window.shadertoy.buffer_a.texture if window.shadertoy.buffer_a is not None else None
                elif box.get()=="Buf B":
                    buf_channel = window.shadertoy.buffer_b.texture if window.shadertoy.buffer_b is not None else None
                elif box.get()=="Buf C":
                    buf_channel = window.shadertoy.buffer_c.texture if window.shadertoy.buffer_c is not None else None
                elif box.get()=="Buf D":
                    buf_channel = window.shadertoy.buffer_d.texture if window.shadertoy.buffer_d is not None else None
                elif box.get() in self.textures.keys():
                    buf_channel = window.ctx.load_texture(self.textures[box.get()])
                    
                if not buf_channel: return
                if channel==0:
                    buffer.channel_0 = buf_channel
                elif channel==1:
                    buffer.channel_1 = buf_channel
                elif channel==2:
                    buffer.channel_2 = buf_channel
                elif channel==3:
                    buffer.channel_3 = buf_channel

            def __init__(window, width, height, title):
                super().__init__(width, height, title, resizable=True)

                main_image_code = self.textbox.get(1.0, "end-1c")
                buffer_code_A = self.textbox_A.get(1.0, "end-1c")
                buffer_code_B = self.textbox_B.get(1.0, "end-1c")
                buffer_code_C = self.textbox_C.get(1.0, "end-1c")
                buffer_code_D = self.textbox_D.get(1.0, "end-1c")

                common_code = self.textbox_common.get(1.0, "end-1c")
        
                if len(common_code)>10:
                    main_image_code = f"{common_code} \n{main_image_code}"
                    buffer_code_A = f"{common_code} \n{buffer_code_A}" if len(buffer_code_A)>5 else buffer_code_A
                    buffer_code_B = f"{common_code} \n{buffer_code_B}" if len(buffer_code_B)>5 else buffer_code_B
                    buffer_code_C = f"{common_code} \n{buffer_code_C}" if len(buffer_code_C)>5 else buffer_code_C
                    buffer_code_D = f"{common_code} \n{buffer_code_D}" if len(buffer_code_D)>5 else buffer_code_D
                
                try:
                    window.shadertoy = Shadertoy(window.get_framebuffer_size(), main_image_code)
                except:
                    warnings.warn("Error in Image code!")
                    window.close()
                    
                window.video = cv2.VideoCapture(ofile)
                width, height = (int(window.video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                 int(window.video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                window.video_texture = window.ctx.texture((width, height), components=3)
                window.video_texture.wrap_x = window.ctx.CLAMP_TO_EDGE
                window.video_texture.wrap_y = window.ctx.CLAMP_TO_EDGE
                window.video_texture.swizzle = "BGR1"
                
                try: window.shadertoy.buffer_a = window.shadertoy.create_buffer(buffer_code_A) if len(buffer_code_A)>5 else None
                except:
                    warnings.warn("Error in Buffer-A code!")
                    window.close()
                      
                try: window.shadertoy.buffer_b = window.shadertoy.create_buffer(buffer_code_B) if len(buffer_code_B)>5 else None
                except:
                    warnings.warn("Error in Buffer-B code!")
                    window.close()
         
                try: window.shadertoy.buffer_c = window.shadertoy.create_buffer(buffer_code_C) if len(buffer_code_C)>5 else None
                except:
                    warnings.warn("Error in Buffer-C code!")
                    window.close()
              
                try: window.shadertoy.buffer_c = window.shadertoy.create_buffer(buffer_code_D) if len(buffer_code_D)>5 else None
                except:
                    warnings.warn("Error in Buffer-D code!")
                    window.close()
                    
                for i in range(4):
                    window.add_channels(self, channel=i, buffer=window.shadertoy, boxes="self.ichannel")
                    
                if window.shadertoy.buffer_a:
                    for i in range(4):
                        window.add_channels(self, channel=i, buffer=window.shadertoy.buffer_a, boxes="self.buff_A_ichannel")
                        
                if window.shadertoy.buffer_b:
                    for i in range(4):
                        window.add_channels(self, channel=i, buffer=window.shadertoy.buffer_b, boxes="self.buff_B_ichannel")

                if window.shadertoy.buffer_c:
                    for i in range(4):
                        window.add_channels(self, channel=i, buffer=window.shadertoy.buffer_c, boxes="self.buff_C_ichannel")

                if window.shadertoy.buffer_d:
                    for i in range(4):
                        window.add_channels(self, channel=i, buffer=window.shadertoy.buffer_d, boxes="self.buff_D_ichannel")
                        
                window.set_size(width, height)

                if self.option_switch.get()==0 and preview==False:
                    self.out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), window.video.get(cv2.CAP_PROP_FPS), (width, height))
                
            def on_draw(window):
                window.clear()
                window.shadertoy.render()
                
            def on_update(window, delta_time: float):
                window.shadertoy.time += delta_time
                window.next_frame()
                window.shadertoy.resize(window.get_framebuffer_size())
                
            def on_resize(window, width: float, height: float):
                super().on_resize(width, height)
                
            def next_frame(window):
                global currentframe
                exists, frame = window.video.read()
                frame = cv2.flip(frame, 0)
                if frame is not None:
                    window.video_texture.write(frame)
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
                        window.close()
                        if self.option_switch.get()==1:
                            tkinter.messagebox.showinfo("Done!", "PNG Sequence saved: "+str(newdir))
                        else:
                            self.out.release()
                            tkinter.messagebox.showinfo("Done!", "Video saved: "+os.path.basename(output_file))
                    else:
                        window.video.set(1, 0)
                            
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
