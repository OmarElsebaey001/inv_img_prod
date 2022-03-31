import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import matplotlib
import io
from random import randint
import os


matplotlib.pyplot.switch_backend('Agg')
matplotlib.use('agg')
def convertImage(img):
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] >= 230 and item[1] >= 230 and item[2] >= 230:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    return img
def create_image(capital,total,sub_name,wealth_manager):
    tot_cap_diff = int(total - capital)
    sub_name_font = ImageFont.truetype(r'Nexa Light.otf', 100)
    sub_name_loc  = (1700,850)
    sub_name_col  = (55,57,54)

    cap_inv      = "{:,}".format(capital)
    cap_inv_font = ImageFont.truetype(r'Nexa Bold.otf', 110)
    cap_inv_loc  = (1290,1255)
    cap_inv_col  = (55,57,54)

    tot_prt_val      = "{:,}".format(total)
    tot_prt_val_font = ImageFont.truetype(r'Nexa Bold.otf', 110)
    tot_prt_val_loc  = (3650,1255)
    tot_prt_val_col  = (55,57,54)

    gain_loss      = "{:,}".format(tot_cap_diff)
    gain_loss_font = ImageFont.truetype(r'Nexa Bold.otf', 110)
    gain_loss_loc  = (1370,1515)
    gain_loss_col  = "#FFFFFF"

    abs_rtn = "{:,}".format(round(100*tot_cap_diff/capital, 2)) + "%"
    abs_rtn_font = ImageFont.truetype(r'Nexa Bold.otf', 110)
    abs_rtn_loc  = (3635,1515)
    abs_rtn_col  = "#FFFFFF"

    wlt_mang = wealth_manager
    wlt_mang_font = ImageFont.truetype(r'OpenSans-SemiBold.ttf', 80)
    wlt_mang_loc  = (2060,4220)
    wlt_mang_col  = (55,57,54)

    img = Image.open("latest_template_appended.jpeg").convert('RGB')
    draw = ImageDraw.Draw(img)
    draw.text(sub_name_loc,sub_name,sub_name_col,font=sub_name_font)
    draw.text(cap_inv_loc,cap_inv,cap_inv_col,font=cap_inv_font)
    draw.text(tot_prt_val_loc,tot_prt_val,tot_prt_val_col,font=tot_prt_val_font)
    draw.text(gain_loss_loc,gain_loss,gain_loss_col,font=gain_loss_font)
    draw.text(abs_rtn_loc,abs_rtn,abs_rtn_col,font=abs_rtn_font)
    draw.text(wlt_mang_loc,wlt_mang,wlt_mang_col,font=wlt_mang_font)
    ###################
    background = img
    if (tot_cap_diff > 0): 
        first  = [capital, total, total]
        second = [0,capital,0]
        sign   = "+"
    else:
        first  = [capital, capital, total]
        second = [0,total,0]
        sign   = "-"

    df = pd.DataFrame({"Price 1": first,
                    "Price 2" : second,
                        "Day": ["Capital Invested","Total Gain/Loss","Total Portfolio Value"]})
    custom_params = {"axes.spines.right": False,"axes.spines.left": False, "axes.spines.top": False,
                    'figure.figsize':(15,8),
                    "figure.autolayout": True,
                    }
    colors = ["#25302a", "#ecfa00", "#bccbc9"]
    palette=colors
    sns.set_theme(style="white", palette=palette,rc=custom_params);
    s1 = sns.barplot(x = 'Day', y = 'Price 1', data = df)
    s_x = s1 
    ann_txt = [capital,tot_cap_diff,total]
    ann_txt = [f'{i:,}' for i in ann_txt]
    if (tot_cap_diff > 0):
        ann_txt[1] = sign + ann_txt[1]
    ann = ["yellow","black","black"]
    for index,p in enumerate(s_x.patches):
        if(index > 2) :
            break
        print(f"Now processing the patch index{index}",p)
        print("Will annotate with : " , ann_txt[index])
        s_x.annotate(f'\n{ann_txt[index]}',
                    (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='top', color=ann[index], size=30)
    sns.barplot(x = 'Day', y = 'Price 2', data = df, color = 'white')
    y_ticks = s1.get_yticks()
    y_ticks = [f'{i:,}' for i in y_ticks]
    s_x = s1
    print(s_x.patches)
    for index,p in enumerate(s_x.patches):
        if(index > 2) :
            break
        print(f"Now processing the patch index{index}",p)
        print("Will annotate with : " , ann_txt[index])
        s_x.annotate(f'\n{ann_txt[index]}',
                    (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='top', color=ann[index], size=30)
    s_x.set(xlabel=None)
    s_x.set(ylabel=None)
    s_x.set(xlabel=None)
    s_x.set(xticklabels=[])
    s_x.set_yticklabels(y_ticks, size = 30)
    f_name = str(randint(0,5000)) + ".jpeg"
    plt.savefig(f_name, format='jpeg',dpi=170)
    chart_img = Image.open(f_name)
    foreground  = convertImage(chart_img)
    background.paste(foreground, (1100,2500), foreground)
    os.remove(f_name)
    return background