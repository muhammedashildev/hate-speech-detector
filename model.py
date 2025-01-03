import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load tokenizer
tokenizer = BertTokenizer.from_pretrained("https://huggingface.co/bert-base-uncased/resolve/main/tokenizer.json")

# Load model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased")
model.eval()  # Set model to evaluation mode

# Define function for offensive language detection
def detect_offensive_language(text):
    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    # Forward pass through the model
    with torch.no_grad():
        outputs = model(**inputs)

    # Interpret model output
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    offensive_probability = probabilities[:, 1].item()  # Probability of being offensive

    # Define a threshold for determining if the text is offensive
    threshold = 0.5
    if offensive_probability >= threshold:
        return "Offensive"
    else:
        return "Non-offensive"

# Example usage
def main():
    text = "you look good"
    result = detect_offensive_language(text)
    print("Text is:", result)

if __name__ == "__main__":
    main()
