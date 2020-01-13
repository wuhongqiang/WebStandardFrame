import os
import functools
import sys
import zipfile


import sublime
import sublime_plugin


class NewModuleCommand(sublime_plugin.WindowCommand):

    def run(self, dirs):
        self.window.show_input_panel("Moudle Name:", "", functools.partial(self.on_done, dirs[0]), None, None)

    def on_done(self, dir, name):
        moudle_dir = os.path.join(dir, name)
        os.makedirs(moudle_dir, 0o775)
        os.makedirs(os.path.join(moudle_dir, "dist"), 0o775)
        os.makedirs(os.path.join(moudle_dir, "html"), 0o775)
        os.makedirs(os.path.join(moudle_dir, "css"), 0o775)
        os.makedirs(os.path.join(moudle_dir, "js"), 0o775)
        os.makedirs(os.path.join(moudle_dir, "img"), 0o775)
        #create readme.md
        self.file_create(moudle_dir,"README.md","# version1.0")


    def file_create(self,dir,name,content):
        
         file_dir=os.path.join(dir, name)
         if not os.path.isfile(file_dir):
            file=open(file_dir,mode="w",encoding="utf-8")
            file.write(content)
            file.close()   

    def is_visible(self, dirs):
        return len(dirs) > 0


class DeployModuleCommand(sublime_plugin.WindowCommand):

    def run(self, dirs):
        dirname,filename=os.path.split(dirs[0])
        self.window.show_input_panel("Version(eg:1.0.0):", "", functools.partial(self.on_done, dirs[0]), None, None)

    def on_done(self, dir, version):
        self.file_zip(dir,version)
        
    def file_zip(self,dir,version):
        dir_name,file_name=os.path.split(dir)
        dirName=dir
        zipFileName=os.path.join(dirName, "dist/")+file_name+"-"+version+".zip"
        fileList=[] 
        fileList.append(dirName)
        for root,dirs,files in os.walk(dirName):
            #dirs.remove('dist')
            for dir_str in dirs:
                fileList.append(os.path.join(root,dir_str))
            for names in files:
                fileList.append(os.path.join(root,names))
        zf=zipfile.ZipFile(zipFileName,"w",zipfile.zlib.DEFLATED)
        for tar in fileList:
            arcname=tar[len(dirName):]
            zf.write(tar,arcname)
        zf.close() 

    def is_visible(self, dirs):
        return len(dirs) >0

class NewHtmlCommand(sublime_plugin.WindowCommand):

    def run(self, dirs):
        dir_name,file_name=os.path.split(dirs[0])
        if (file_name!="html"):
            return
        else:
           self.window.show_input_panel("Html Name:", "", functools.partial(self.on_done, dirs[0]), None, None)


    def on_done(self, dir, name):
        moudle_dir = dir 
        parent_dir=os.path.abspath(os.path.dirname(moudle_dir)+os.path.sep+".")
        print(moudle_dir)
        print(parent_dir)
        #create html
        html_content="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8"> 
        <title>%s</title>
        <link rel="stylesheet" href="../css/%s.css"> 
        <script href="../js/%s.js"></script>
        </head>
        <body>
        </body>
        </html>
        """%(name,name,name)
        self.file_create(moudle_dir,name+".html",html_content)
        #create css
        css_content="""
         /* %s.css */
        """%(name)
        self.file_create(os.path.join(parent_dir, "css"),name+".css",css_content)
        #create js
        js_content="""
        /* %s.js*/
        """%(name)
        self.file_create(os.path.join(parent_dir, "js"),name+".js",js_content)
        
    def file_create(self,dir,name,content):
        
         file_dir=os.path.join(dir, name)
         if not os.path.isfile(file_dir):
            file=open(file_dir,mode="w",encoding="utf-8")
            file.write(content)
            file.close()   

    def is_visible(self, dirs):
        return len(dirs) >0



                