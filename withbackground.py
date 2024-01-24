import json
import requests

from flask import Flask, request, send_file, jsonify

from io import BytesIO
import PIL.Image
import PIL.ImageSequence
from PIL import ImageDraw, ImageFont

_margin_left_right = 25
_margin_top_bottom = 70

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'gif'}
DEFAULT_X = "center"
DEFAULT_Y = "top"
DEFAULT_POSITION =  {"x" : DEFAULT_X, "y": DEFAULT_Y}

app = Flask(__name__)
@app.route('/public/generate-meme', methods=['POST'])
def generate_meme():

  req = json.loads(request.data)
  img_url = req.get('img_url')
  properties = req.get('properties')
  # Validate request
  error_message = validate_gif_properties(properties)
  if error_message is not None:
    response = jsonify({
      'status': 400,
      'message': error_message,
    })
    response.status_code = 400
    return response
  
  response = requests.get(img_url, stream=True)
  print(response)
  img = BytesIO(response.content)
  with PIL.Image.open(img) as gif_image, PIL.Image.open('./white-backgound.jpeg') as bg_image:
    W,H = gif_image.size
    
    bg_image = bg_image.convert(mode='RGBA').resize((W + (_margin_left_right*2), H + (_margin_top_bottom*2)))
    back_width, back_height = bg_image.size
    for property in properties:
      position_text(bg_image, back_width, H, property=property)

    frames = tuple(create_frames(bg_image, gif_image))
    buffered = BytesIO()
    frames[0].save(
      buffered,
      format = "GIF",
      save_all = True,
      append_images = frames[1:],
      duration = 100,loop = 0
    )
    buffered.seek(0)

    return send_file(
      buffered,
      as_attachment=True,
      download_name='test.gif',
      mimetype='image/gif'
    )

def position_text(img, width, height, property):
  text = property.get("text")
  font_size = property.get("fontSize")
  is_upper_case = property.get("upperCase")
  color = property.get("color")
  position = property.get("position") or DEFAULT_POSITION

  if is_upper_case:
    text = text.upper()
  W = width
  H = height
  Im = ImageDraw.Draw(img)
  font = ImageFont.truetype("./font/Roboto-Black.ttf", size=font_size)
  #if position == "top center":
  _, _, w, h = Im.textbbox((0, 0), text, font=font)
  write_text(Im, text, font, color, get_coordinates(position.get("x") or DEFAULT_X, W, H, w, h), get_coordinates(position.get("y") or DEFAULT_Y, W, H, w, h))
  
  # elif position == "bottom center":
  #   _, _, w, h = Im.textbbox((0, 0), text, font=font)
  #   write_text(Im, text, font, color, get_center_x(W, w), get_bottom_y(H, h))

# def get_position_coordinates()

def get_coordinates(position: str, img_width:int, img_height:int, text_width:int,  text_height: int):
  match position:
    case "top":
      return get_top_y(text_height)
    case "bottom":
      return get_bottom_y(img_height, text_height)
    case "center":
      return get_center_x(img_width, text_width)
    case "left":
      return get_left()
    case "right":
      return get_right(img_width, text_width)
    
def get_left():
  return _margin_left_right

def get_right(img_width, text_width):
  return img_width - _margin_left_right - text_width


def get_center_x(img_width, text_width):
  return (img_width - text_width) / 2

def get_top_y(text_height):
  return (_margin_top_bottom - text_height) / 2

def get_bottom_y(img_height, text_height):
  return _margin_top_bottom + img_height + (_margin_top_bottom - text_height)/2

def write_text(img_draw, text, font, color, x, y):
  img_draw.multiline_text((x, y), text, fill = color, font=font)

def create_frames(bg_image, gif_image):
  for current_frame in PIL.ImageSequence.Iterator(gif_image):
    current_background = bg_image.copy()
    current_foreground = current_frame.convert(mode='RGBA')
    current_background.alpha_composite(current_foreground, dest=(_margin_left_right, _margin_top_bottom))
    yield current_background

def validate_gif_properties(properties):
  all_positions = []
  for property in properties:
    position = property.get("position")
    if position is None:
      return "Every poperty should contain position key."
    
    current_position = position.get("x") + position.get("y")
    if current_position in all_positions:
      return "Each poperty should have different position."
    
    all_positions.append(position.get("x") + position.get("y"))