from operator import methodcaller
from flask import Flask,render_template
from flask import request, jsonify
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from jinja2 import Template
from flask import send_file
from helper import create_image 

def create_app() :
    app = Flask(__name__)
    @app.route("/",methods=['GET','POST'])
    def show():
        capital        = request.args.get('cl_nt_cp', default = 1, type = float)
        total          = request.args.get('cl_tot_po', default = 1, type = float)
        sub_name       = request.args.get('cl_nm', default = 1, type = str)
        wealth_manager = request.args.get('wlt_mng', default = 1, type = str)
        wealth_number  = request.args.get('wlt_mng_nm', default = 1, type = str)
        wlt_mang_num   = f"+{wealth_number[0:2]} {wealth_number[2:7]} {wealth_number[7:]}"
        wealth_manager = wealth_manager + f": {wlt_mang_num}"
        full_pic = create_image(capital,total,sub_name,wealth_manager)
        full_pic.save("processed_123.jpeg", "JPEG", quality=80, optimize=True, progressive=True)
        return send_file("processed_123.jpeg")

    if __name__ == "__main__":
        app.run()
    return app 
