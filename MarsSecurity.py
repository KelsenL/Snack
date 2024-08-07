"""
API文档: https://api.nasa.gov/ (Mars Rover Photos栏中)

申请API KEY: https://api.nasa.gov/
"""
import requests
import gradio as gr

# Function to fetch Mars Rover photos
def fetch_mars_rover_photos(api_key, sol=None, earth_date=None, camera='FHAZ', page=1):
    base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
    
    if sol is not None:
        params = {
            'api_key': api_key,
            'sol': sol,
            'camera': camera,
            'page': page
        }
    elif earth_date is not None:
        params = {
            'api_key': api_key,
            'earth_date': earth_date,
            'camera': camera,
            'page': page
        }
    else:
        return None

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def mars_rover_photo_interface(sol, earth_date, camera, page):
    api_key = "Q890KsJoL60zA8Z1DWlJOol7kXSKLd9ikIoq5F9U"  # Replace with your own API key
    data = fetch_mars_rover_photos(api_key, sol=sol, earth_date=earth_date, camera=camera, page=page)
    
    if data:
        photos = data.get('photos', [])
        photo_urls = [photo['img_src'] for photo in photos]
        return photo_urls
    else:
        return []

# Define the input components for the Gradio interface
sol_input = gr.Number(label="Martian Sol", value=1000)
earth_date_input = gr.Textbox(label="Earth Date", value='2015-06-03')
camera_input = gr.Textbox(label="Camera", value='FHAZ')
page_input = gr.Number(label="Page", value=1)

# Create the Gradio interface with a description
gr.Interface(
    fn=mars_rover_photo_interface,
    inputs=[sol_input, earth_date_input, camera_input, page_input],
    outputs=gr.Gallery(label="Mars Rover Photos"),
    description="You can either query by Martian Sol or by Earth Date"
).launch()
