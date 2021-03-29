import os
from io import BytesIO

from flask import ( current_app, Blueprint, request, send_from_directory, send_file, safe_join, abort )
from PIL import Image, ImageFont, ImageDraw

from .utils.eptools import get_season

bp = Blueprint('meme', __name__)

#nthframe=6

IMPACT = 'Impact.ttf'

def ep_to_thumbnail_dir(static_folder, ep):
    #TODO: confirm that ep is of SxxExx format!!
    season = get_season(ep)
    img_dir = os.path.join(static_folder, 'thumbnails', season, ep)
    return img_dir


@bp.route('/<ep>/<int:frame>.jpg', methods=(['GET']))
def generate_meme(ep, frame):
    """
    dynamically generate the meme
        potentially: store the meme on disk and cron will kill cached ones
        that haven't been accessed in a while?
    """
    txt = request.args.get('txt', '')
    #find path to image
    img_dir = ep_to_thumbnail_dir(current_app.static_folder,ep)
    img_name = f'{frame:05}.jpg'
    img_path = safe_join(img_dir, img_name)

    pil_img=None
    try:
        #read img into memory, then draw on image
        pil_img = Image.open(img_path)
    except FileNotFoundError:
        abort(404)

    margin_bottom = 20 #pixels
    font = ImageFont.truetype(IMPACT, 32)
    img_w, img_h = pil_img.size
    draw = ImageDraw.Draw(pil_img)
    text_w, text_h = draw.textsize(txt, font)
    textpos = ((img_w - text_w) // 2, img_h - text_h - margin_bottom)
    draw.text(textpos, txt,
        align='center',
        font=font,
        fill='white',
        stroke_width=2,
        stroke_fill='black',
    )

    #save image in memory
    img_bytes = BytesIO()
    pil_img.save(img_bytes, 'JPEG', quality=95)
    img_bytes.seek(0)

    #return it
    return send_file(img_bytes, mimetype='image/jpeg')
