from odoo import api, fields, models,_
import os
from odoo.exceptions import UserError


class Wizard(models.TransientModel):
    _name = 'save.save'
    module_name = fields.Many2one(comodel_name="module.module", string="Module Name", required=True,ondelete="cascade")

    #####################################  Create init  ##########################
    def create_init_file(self,os):
        os.mknod('__init__.py')
        with open("__init__.py", mode='a')as txt:
            txt.write("from . import models" + "\n")
    #####################################  Create mainfest  ##########################
    def create_mainfest_file(self,os,Module_Name,Models):
        os.mknod('__manifest__.py')
        with open("__manifest__.py", mode='a')as txt:
            txt.write("{" +
                      "'name':" + "\"" + Module_Name + "\"" + "," + "\n" +
                      "'depends': ['base']," + "\n" +
                      "'data': [" + "'views/root_menu.xml'," + "\n")
        for model in Models:
            with open("__manifest__.py", mode='a')as txt:
                txt.write(
                    "'views/" + model['name'] + ".xml',\n")
        with open("__manifest__.py", mode='a')as txt:
            txt.writelines("],}")

    #####################################  Create models  ##########################
    def create_models(self,os,Models):
        #####################################  Create models  ##########################
        os.chdir('models')  # cd to models dir
        os.mknod('__init__.py')
        for model in Models:
            os.mknod(model['name'] + '.py')
            with open("__init__.py", mode='a')as txt:
                txt.write("from . import " + model['name'] + "\n")
        #######################################################################################

        ####################################create model#######################################
        for model in Models:
            fields = self.env['field.field'].search_read([['model_name', '=', model['name']]],
                                                         ['name', 'type', 'string', 'required', 'readonly'])
            with open(model['name'] + ".py", mode='a')as txt:
                txt.writelines("from odoo import api, fields, models\n\n")
                txt.writelines("class " + model['name'] + "(models.Model):" + "\n" + "\t" +
                               "_name" + "=" + "'" + model['name'] + "." + model['name'] + "'" + "\n" + "\t"

                               )
                for field in fields:
                    txt.writelines(
                        field['name'] + "=fields." + field['type'] + "(string='" + field['string'] + "',required=" +
                        str(field['required']) + ",readonly=" + str(field['readonly']) + ")" + "\n" + "\t")

    #########################################create views##################################
    def create_views(self,os,Models,Module_Name):
        os.chdir('../views')
        for model in Models:
            fields = self.env['field.field'].search_read([['model_name', '=', model['name']]], ['name', 'type'])
            with open(model['name'] + ".xml", mode='a')as txt:
                txt.writelines("<odoo>" + "\n" +
                               "<data>" + "\n" +

                               "<record id=" + "\"" + model['name'] + "_form" + "\"" + " model=\"ir.ui.view\">" + "\n" +
                               "<field name=\"name\">" + model['menu_name'] + "</field>" + "\n" +
                               "<field name=\"model\">" + model['name'] + "." + model['name'] + "</field>" + "\n" +
                               "<field name=\"arch\" type=\"xml\">" + "\n" +
                               "<form>" + "\n" +
                               "<sheet>" + "\n" +
                               "<group>" + "\n")
                for field in fields:
                    txt.writelines("<field name=\"" + field['name'] + "\"/>" + "\n")
                txt.writelines(
                    "</group>" + "\n" +
                    "</sheet>" + "\n" +
                    "</form>" + "\n" +
                    "</field>" + "\n" +
                    "</record>\n\n")
                txt.writelines(
                    "<record id=" + "\"" + model['name'] + "_action\"" + " model=\"ir.actions.act_window\">" + "\n" +
                    "<field name=\"name\">" + model['menu_name'] + "</field>" + "\n" +
                    "<field name=\"type\">ir.actions.act_window</field>" + "\n" +
                    "<field name=\"res_model\">" + model['name'] + "." + model['name'] + "</field>" + "\n" +
                    "<field name=\"view_mode\">tree,form</field>" + "\n" +
                    "<field name=\"help\" type=\"html\">" + "\n" +
                    "<p class=\"oe_view_nocontent_create\">" + "\n" +
                    "<!-- Add Text Here -->" + "\n" +
                    "</p><p>" + "\n" +
                    "<!-- More details about what a user can do with this object will be OK -->" + "\n" +
                    "</p>" + "\n" +
                    "</field>" + "\n" +
                    "</record>" + "\n" +
                    "<menuitem" +
                    " id =" + "\"" + model['name'] + "_menu" + "\"" + "\n" +
                    "name =" + "\"" + model['menu_name'] + "\"" + "\n" +
                    "parent =" + "\"" + Module_Name + "_root" + "\"" + "\n" +
                    "action =" + "\"" + model['name'] + "_action" + "\"" + "\n" +
                    "/>" + "\n\n" +
                    "</data>" + "\n" +
                    "</odoo>")

        os.mknod('root_menu.xml')
        with open("root_menu.xml", mode='a')as txt:
            txt.writelines("""<?xml version="1.0" encoding="utf-8"?>
        <odoo>
            <data>""" + "\n")

            txt.write(
                "<menuitem id=" + "\"" + Module_Name + "_root" + "\"" + " name=" + "\"" + Module_Name + "\"" + "/>" + "\n")
            txt.writelines("""     </data></odoo>""")
            return UserError(_("Saved"))


    def save(self):
       #################   Variables   #######################################################
       Module_Name=self.module_name.name
       Models=self.env['model.model'].search_read([['module_name', '=', Module_Name]],['name','menu_name'])
       ########################################################################################
       #####################################  Create Dirs  ####################################
       if os.path.exists(Module_Name):
          raise  UserError("File Exists!")
       os.mkdir(Module_Name)#create main dir
       os.chdir(Module_Name)#cd to main dir
       os.mkdir('models')#create models dir
       os.mkdir('views')#create views dir
       #######################################################################################
       self.create_init_file(os)
       self.create_mainfest_file(os,Module_Name,Models)
       self.create_models(os,Models)
       self.create_views(os,Models,Module_Name)

