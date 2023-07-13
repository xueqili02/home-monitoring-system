import torch

from model.image_caption.models import caption
from model.image_caption.datasets import coco
from service.preload import config, model, tokenizer, start_token, end_token, caption, cap_mask

@torch.no_grad()
def evaluate(image):
    model.eval()
    for i in range(config.max_position_embeddings - 1):
        predictions = model(image, caption, cap_mask)
        predictions = predictions[:, i, :]
        predicted_id = torch.argmax(predictions, axis=-1)

        if predicted_id[0] == 102:
            return caption

        caption[:, i+1] = predicted_id[0]
        cap_mask[:, i+1] = False

    return caption


def describe_image(image):
    image = coco.val_transform(image)
    image = image.unsqueeze(0)
    output = evaluate(image)
    result = tokenizer.decode(output[0].tolist(), skip_special_tokens=True)
    #result = tokenizer.decode(output[0], skip_special_tokens=True)
    # print(result.capitalize())
    return result.capitalize()


# print(describe_image('bath.jpg'))