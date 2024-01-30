import requests

from PIL import Image
from torch.linalg import vector_norm
from torch import div
from transformers import CLIPProcessor, CLIPModel

MODEL = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
PROCESSOR = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def get_text_encoding(text):
    """ Takes in text and returns normalized CLIP encoding."""

    text_inputs = PROCESSOR(
        text=text,
        return_tensors="pt"
    )

    text_embeds = MODEL.get_text_features(**text_inputs)
    normed_text_embeds = div(text_embeds, vector_norm(text_embeds))

    return normed_text_embeds

def get_image_encoding(image_url):
    """
    Takes a URL for a JPG image and returns the image's normalized CLIP encoding.
    """

    image = Image.open(requests.get(image_url, stream=True).raw)

    image_inputs = PROCESSOR(
        images=image, 
        return_tensors="pt", 
        padding=True
    )

    image_embeds = MODEL.get_image_features(**image_inputs)
    normed_image_embeds = div(image_embeds, vector_norm(image_embeds))

    return normed_image_embeds


