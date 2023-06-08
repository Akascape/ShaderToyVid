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
import pygments.lexers
from chlorophyll import CodeView

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
        self.open_video.bind("<Button-2>", lambda event: self.do_popup(event, frame=self.right_click_menu_1))
        
        self.label_1 = customtkinter.CTkLabel(master=self.frame, width=320, height=25, text="Choose Shader Effect",
                                              font=(self.font, -16)) 
        self.label_1.grid(row=1, column=0, pady=(15,0), padx=30, sticky="we", columnspan=2)

        self.check_shader_folder()
        
        # option Menu   
        self.combobox_1 = customtkinter.CTkOptionMenu(master=self.frame, width=120, height=35, button_color="#212435", hover=False,
                                                     fg_color="#212435", dropdown_fg_color="#212435", dropdown_hover_color="#181b28",
                                                     values=self.myeffects, command=self.open_script) 
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
        self.textboxes = []

        self.right_click_menu = tkinter.Menu(self.tabview, tearoff=False, background='#343e5a', fg='white', borderwidth=0, bd=0)
        self.right_click_menu.add_command(label="clear", command=self.clear_code)
        self.right_click_menu.add_command(label="copy", command=self.copy_code)
        self.right_click_menu.add_command(label="paste", command=self.paste_code)
        self.right_click_menu.add_command(label="save", command=self.save_code)
        
        # the code box for Common Tab
        self.frame_1 = customtkinter.CTkFrame(master=self.tabview.tab("Common"), fg_color="#282a36", border_width=1, corner_radius=15, height=200)
        self.frame_1.pack(fill="both", padx=5, pady=5, expand=True)
        
        self.textbox_common = CodeView(self.frame_1, lexer=pygments.lexers.CLexer, font=(self.font, 10), height=1, color_scheme="dracula", undo=True)
        
        self.scrollbar_1 = customtkinter.CTkScrollbar(self.frame_1, command=self.textbox_common.yview)
        self.scrollbar_1.pack(fill="y", padx=(0,2), pady=7, side="right")
        
        self.textbox_common.pack(fill="both", padx=(10,0), pady=10, expand=True)
        self.textbox_common.configure(yscrollcommand=lambda x,y: self.dynamic_scrollbar(x,y,self.scrollbar_1))
        self.textboxes.append(self.textbox_common)
        
        self.textbox_common.bind("<Button-3>", lambda event: self.do_popup(event, frame=self.right_click_menu))
        self.textbox_common.bind("<Button-2>", lambda event: self.do_popup(event, frame=self.right_click_menu))
        
        # the code box for Image Tab
        self.frame_2 = customtkinter.CTkFrame(master=self.tabview.tab("Image"), fg_color="#282a36", border_width=1, corner_radius=15, height=200)
        self.frame_2.pack(fill="both", padx=5, pady=5, expand=True)
        
        self.textbox = CodeView(self.frame_2, lexer=pygments.lexers.CLexer, font=(self.font, 10), height=1, color_scheme="dracula", undo=True)
        
        self.scrollbar_2 = customtkinter.CTkScrollbar(self.frame_2, command=self.textbox.yview)
        self.scrollbar_2.pack(fill="y", padx=(0,2), pady=7, side="right")
        
        self.textbox.pack(fill="both", padx=(10,0), pady=10, expand=True)
        self.textbox.configure(yscrollcommand=lambda x,y: self.dynamic_scrollbar(x,y,self.scrollbar_2))
        self.textboxes.append(self.textbox)
        
        self.textbox.bind("<Button-3>", lambda event: self.do_popup(event, frame=self.right_click_menu))
        self.textbox.bind("<Button-2>", lambda event: self.do_popup(event, frame=self.right_click_menu))
        
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
        self.frame_3 = customtkinter.CTkFrame(master=self.tabview.tab("Buf A"), fg_color="#282a36", border_width=1, corner_radius=15, height=200)
        self.frame_3.pack(fill="both", padx=5, pady=5, expand=True)
        
        self.textbox_A = CodeView(self.frame_3, lexer=pygments.lexers.CLexer, font=(self.font, 10), height=1, color_scheme="dracula", undo=True)
        
        self.scrollbar_3 = customtkinter.CTkScrollbar(self.frame_3, command=self.textbox_A.yview)
        self.scrollbar_3.pack(fill="y", padx=(0,2), pady=7, side="right")
        
        self.textbox_A.pack(fill="both", padx=(10,0), pady=10, expand=True)
        self.textbox_A.configure(yscrollcommand=lambda x,y: self.dynamic_scrollbar(x,y,self.scrollbar_3))
        self.textboxes.append(self.textbox_A)

        self.textbox_A.bind("<Button-3>", lambda event: self.do_popup(event, frame=self.right_click_menu))
        self.textbox_A.bind("<Button-2>", lambda event: self.do_popup(event, frame=self.right_click_menu))
        
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
        self.frame_4 = customtkinter.CTkFrame(master=self.tabview.tab("Buf B"), fg_color="#282a36", border_width=1, corner_radius=15, height=200)
        self.frame_4.pack(fill="both", padx=5, pady=5, expand=True)
        
        self.textbox_B = CodeView(self.frame_4, lexer=pygments.lexers.CLexer, font=(self.font, 10), height=1, color_scheme="dracula", undo=True)
        
        self.scrollbar_4 = customtkinter.CTkScrollbar(self.frame_4, command=self.textbox_B.yview)
        self.scrollbar_4.pack(fill="y", padx=(0,2), pady=7, side="right")
        
        self.textbox_B.pack(fill="both", padx=(10,0), pady=10, expand=True)
        self.textbox_B.configure(yscrollcommand=lambda x,y: self.dynamic_scrollbar(x,y,self.scrollbar_4))
        self.textboxes.append(self.textbox_B)

        self.textbox_B.bind("<Button-3>", lambda event: self.do_popup(event, frame=self.right_click_menu))
        self.textbox_B.bind("<Button-2>", lambda event: self.do_popup(event, frame=self.right_click_menu))
        
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
        self.frame_5 = customtkinter.CTkFrame(master=self.tabview.tab("Buf C"), fg_color="#282a36", border_width=1, corner_radius=15, height=200)
        self.frame_5.pack(fill="both", padx=5, pady=5, expand=True)
        
        self.textbox_C = CodeView(self.frame_5, lexer=pygments.lexers.CLexer, font=(self.font, 10), height=1, color_scheme="dracula", undo=True)
        
        self.scrollbar_5 = customtkinter.CTkScrollbar(self.frame_5, command=self.textbox_C.yview)
        self.scrollbar_5.pack(fill="y", padx=(0,2), pady=7, side="right")

        self.textbox_C.pack(fill="both", padx=(10,0), pady=10, expand=True)
        self.textbox_C.configure(yscrollcommand=lambda x,y: self.dynamic_scrollbar(x,y,self.scrollbar_5))
        self.textboxes.append(self.textbox_C)

        self.textbox_C.bind("<Button-3>", lambda event: self.do_popup(event, frame=self.right_click_menu))
        self.textbox_C.bind("<Button-2>", lambda event: self.do_popup(event, frame=self.right_click_menu))
        
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
        self.frame_6 = customtkinter.CTkFrame(master=self.tabview.tab("Buf D"), fg_color="#282a36", border_width=1, corner_radius=15, height=200)
        self.frame_6.pack(fill="both", padx=5, pady=5, expand=True)
        
        self.textbox_D = CodeView(self.frame_6, lexer=pygments.lexers.CLexer, font=(self.font, 10), height=1, color_scheme="dracula", undo=True)
        self.scrollbar_6 = customtkinter.CTkScrollbar(self.frame_6, command=self.textbox_D.yview)
        self.scrollbar_6.pack(fill="y", padx=(0,2), pady=7, side="right")
        
        self.textbox_D.pack(fill="both", padx=(10,0), pady=10, expand=True)
        self.textbox_D.configure(yscrollcommand=lambda x,y: self.dynamic_scrollbar(x,y,self.scrollbar_6))
        self.textboxes.append(self.textbox_D)

        self.textbox_D.bind("<Button-3>", lambda event: self.do_popup(event, frame=self.right_click_menu))
        self.textbox_D.bind("<Button-2>", lambda event: self.do_popup(event, frame=self.right_click_menu))
        
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

        # remove unwanted widgets:
        for i in self.textboxes:
            i._vs.grid_forget()
            i._hs.grid_forget()
            i._line_numbers.grid_forget()
            
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
        
        self.option_menus = [self.ichannel_0, self.ichannel_1, self.ichannel_2, self.ichannel_3, self.buff_A_ichannel_0, self.buff_A_ichannel_1,
                             self.buff_A_ichannel_2, self.buff_A_ichannel_3, self.buff_B_ichannel_0, self.buff_B_ichannel_1, self.buff_B_ichannel_2,
                             self.buff_B_ichannel_3, self.buff_C_ichannel_0, self.buff_C_ichannel_1, self.buff_C_ichannel_2, self.buff_C_ichannel_3,
                             self.buff_D_ichannel_0, self.buff_D_ichannel_1, self.buff_D_ichannel_2, self.buff_D_ichannel_3]
        
    def get_textbox(self):
        if self.tabview.get()=="Image":
            return self.textbox
        elif self.tabview.get()=="Common":
            return self.textbox_common
        elif self.tabview.get()=="Buf A":
            return self.textbox_A 
        elif self.tabview.get()=="Buf B":
            return self.textbox_B
        elif self.tabview.get()=="Buf C":
            return self.textbox_C
        elif self.tabview.get()=="Buf D":
            return self.textbox_D
            
    def clear_code(self):
        textbox = self.get_textbox()
        textbox.delete("1.0","end")
        
    def copy_code(self):
        textbox = self.get_textbox()
        self.clipboard_append(textbox.get(tkinter.SEL_FIRST, tkinter.SEL_LAST))
        
    def paste_code(self):
        textbox = self.get_textbox()
        try: textbox.insert(textbox.index('insert'), self.clipboard_get())
        except: pass
        
    def save_code(self):
        textbox = self.get_textbox()
        file_name = f"Untitled_{self.tabview.get().replace(' ', '_')}.glsl"
        if not os.path.isdir(self.mydir):
            os.mkdir(self.mydir)
        save_file = tkinter.filedialog.asksaveasfilename(filetypes =[('GLSL', ['*glsl']),('All Files', '*.*')], initialdir=self.mydir, initialfile=file_name)
        if save_file:
            with open(save_file, "w") as f:
                f.write(textbox.get(1.0, tkinter.END))
        self.check_shader_folder()
        self.combobox_1.configure(values=self.myeffects)
        
    def check_shader_folder(self):
        # Import some shaders from the default folder (My Shaders) if exists
        self.mydir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "My Shaders")
        self.myeffects = ["Custom"]
        if os.path.isdir(self.mydir):
            scriptfiles = os.listdir(self.mydir)
            for i in scriptfiles:
                if os.path.splitext(i)[1]==".glsl":
                    self.myeffects.append(i)
        else:
            print("No shader folder found!")
            
    def dynamic_scrollbar(self, x, y, scrollbar):
        if float(x)==0.0 and float(y)==1.0:
            scrollbar.configure(button_color=scrollbar.cget("bg_color"), button_hover_color=scrollbar.cget("bg_color"))
        else:
            scrollbar.configure(button_color="#4a4d50", button_hover_color="#6d7176")
        scrollbar.set(x,y)
        
    def add_texture(self):
        texture_file = tkinter.filedialog.askopenfilename(filetypes =[('Image', ['*jpg','*png']),('All Files', '*.*')])
        if texture_file:
            self.textures[f"texture{self.num}"] = texture_file
            self.values.append(f"texture{self.num}")
            self.num+=1
            
        for i in self.option_menus:
            i.configure(values=self.values)
            
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
        textbox = self.get_textbox()
        textbox.delete("1.0","end")
        textbox.insert(1.0, code)
            
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
            tkinter.messagebox.showinfo("No input channel", "Please import a video file!")
            return
        elif len(self.textbox.get(1.0, "end-1c"))<5:
            tkinter.messagebox.showinfo("No valid script", "Please enter some script in the textbox!")
            return
        preview = True
        
        self.saveButton.configure(state=tkinter.DISABLED)
        self.previewButton.configure(state=tkinter.DISABLED)
        self.process()
        self.saveButton.configure(state=tkinter.NORMAL)
        self.previewButton.configure(state=tkinter.NORMAL)

    def render_export(self):
        """ render out the shader """
        global preview, newdir, output_file
        if not ofile:
            tkinter.messagebox.showinfo("No input channel", "Please import a video file!")
            return
        elif len(self.textbox.get(1.0, "end-1c"))<5:
            tkinter.messagebox.showinfo("No valid script", "Please enter some script in the textbox!")
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

        self.saveButton.configure(state=tkinter.DISABLED)
        self.previewButton.configure(state=tkinter.DISABLED)
        self.process()
        self.saveButton.configure(state=tkinter.NORMAL)
        self.previewButton.configure(state=tkinter.NORMAL)
        
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
                
                try: super().__init__(width, height, title, resizable=True)
                except: 
                    window.close()
                    return
                
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
                    return
                
                try: window.shadertoy.buffer_a = window.shadertoy.create_buffer(buffer_code_A) if len(buffer_code_A)>5 else None
                except:
                    warnings.warn("Error in Buffer-A code!")
                    window.close()
                    return
                
                try: window.shadertoy.buffer_b = window.shadertoy.create_buffer(buffer_code_B) if len(buffer_code_B)>5 else None
                except:
                    warnings.warn("Error in Buffer-B code!")
                    window.close()
                    return
                
                try: window.shadertoy.buffer_c = window.shadertoy.create_buffer(buffer_code_C) if len(buffer_code_C)>5 else None
                except:
                    warnings.warn("Error in Buffer-C code!")
                    window.close()
                    return
                
                try: window.shadertoy.buffer_c = window.shadertoy.create_buffer(buffer_code_D) if len(buffer_code_D)>5 else None
                except:
                    warnings.warn("Error in Buffer-D code!")
                    window.close()
                    return
         
                window.video = cv2.VideoCapture(ofile)
                width, height = (int(window.video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                 int(window.video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                window.video_texture = window.ctx.texture((width, height), components=3)
                window.video_texture.wrap_x = window.ctx.CLAMP_TO_EDGE
                window.video_texture.wrap_y = window.ctx.CLAMP_TO_EDGE
                window.video_texture.swizzle = "BGR1"
                
                try: window.set_size(width, height)
                except:
                    warnings.warn("Not a valid video file!")
                    window.close()
                    return
                
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
        try: arcade.run()
        except: arcade.exit()
        
    def on_closing(self, event=0):
        self.destroy()
        arcade.exit()
        
    def start(self):
        self.mainloop()
        
if __name__ == "__main__":
    app = HomePage()
    app.start()
