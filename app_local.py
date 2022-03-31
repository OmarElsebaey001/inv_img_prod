from operator import methodcaller
from flask import Flask,make_response
from flask import request, jsonify
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from jinja2 import Template
from flask import send_file,make_response
from helper import create_image 
import io 
from random import randint
import os

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
    capital = int(capital)
    total = int(total)
    print(f"processing {capital} and {total}")
    f_name_1 = str(randint(0,5000))+".jpeg"
    full_pic = create_image(capital,total,sub_name,wealth_manager)
    full_pic.save(f_name_1, "JPEG", quality=80, optimize=True, progressive=True)
    return send_file(f_name_1,mimetype='image/jpeg')
if __name__ == "__main__":
    app.run()
