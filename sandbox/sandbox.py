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

good_text_inputs = processor(
    text="A feather",
    return_tensors="pt"
)

good_text_embeds = model.get_text_features(**good_text_inputs)
#print("good_text_embeds = ", good_text_embeds)
normed_good_text_embeds = div(good_text_embeds, vector_norm(good_text_embeds))
#print("normed_good_text_embeds = ", normed_good_text_embeds)

okay_text_inputs = processor(
    text="A long skinny object",
    return_tensors="pt"
)

okay_text_embeds = model.get_text_features(**okay_text_inputs)
#print("okay_text_embeds = ", okay_text_embeds)
normed_okay_text_embeds = div(okay_text_embeds, vector_norm(okay_text_embeds))
#print("normed_okay_text_embeds = ", normed_okay_text_embeds)

bad_text_inputs = processor(
    text="A man on a bike",
    return_tensors="pt"
)

bad_text_embeds = model.get_text_features(**bad_text_inputs)
#print("bad_text_embeds = ", bad_text_embeds)
normed_bad_text_embeds = div(bad_text_embeds, vector_norm(bad_text_embeds))
#print("normed_bad_text_embeds = ", normed_bad_text_embeds)

terrible_text_inputs = processor(
    text="Two people standing in front of a big beautiful rainbow",
    return_tensors="pt"
)

terrible_text_embeds = model.get_text_features(**terrible_text_inputs)
#print("terrible_text_embeds = ", terrible_text_embeds)
normed_terrible_text_embeds = div(terrible_text_embeds, vector_norm(terrible_text_embeds))
#print("normed_terrible_text_embeds = ", normed_terrible_text_embeds)

good_text_sim = inner(normed_good_text_embeds, normed_image_embeds)
okay_text_sim = inner(normed_okay_text_embeds, normed_image_embeds)
bad_text_sim = inner(normed_bad_text_embeds, normed_image_embeds)
terrible_text_sim = inner(normed_terrible_text_embeds, normed_image_embeds)

print("good_text_sim = ", good_text_sim)
print("okay_text_sim = ", okay_text_sim)
print("bad_text_sim = ", bad_text_sim)
print("terrible_text_sim = ", terrible_text_sim)