import requests

from PIL import Image
from torch.linalg import vector_norm
from torch import div, inner
from transformers import CLIPProcessor, CLIPModel, CLIPVisionModel

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


url = "https://mf-pixly.s3.us-west-2.amazonaws.com/fuji.jpg"

image = Image.open(requests.get(url, stream=True).raw)

image_inputs = processor(
    images=image, 
    return_tensors="pt", 
    padding=True
)

image_embeds = model.get_image_features(**image_inputs)
# print("image_embeds = ", image_embeds)
normed_image_embeds = div(image_embeds, vector_norm(image_embeds))
# print("normed_image_embeds = ", normed_image_embeds)

bad_text_inputs = processor(
    text="A picture of a feather",
    return_tensors="pt"
)

good_text_embeds = model.get_text_features(**bad_text_inputs)
#print("good_text_embeds = ", good_text_embeds)
normed_good_text_embeds = div(good_text_embeds, vector_norm(good_text_embeds))
#print("normed_good_text_embeds = ", normed_good_text_embeds)

bad_text_inputs = processor(
    text="A picture of a man on a bike",
    return_tensors="pt"
)

bad_text_embeds = model.get_text_features(**bad_text_inputs)
#print("bad_text_embeds = ", bad_text_embeds)
normed_bad_text_embeds = div(bad_text_embeds, vector_norm(bad_text_embeds))
#print("normed_bad_text_embeds = ", normed_bad_text_embeds)

good_text_sim = inner(normed_good_text_embeds, normed_image_embeds)
bad_text_sim = inner(normed_bad_text_embeds, normed_image_embeds)

print("good_text_sim = ", good_text_sim)
print("bad_text_sim = ", bad_text_sim)