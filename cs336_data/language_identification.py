import fasttext

def identify_language(text: str):
    model = fasttext.load_model("../lid.176.bin")
    labels, probs = model.predict(text.replace("\n", " "), k=1)
    if not labels:
        return "unknown", 0.0
    
    lang = labels[0].replace("__label__", "")
    score = float(probs[0]) if probs else 0.0
    return lang, score

if __name__ == "__main__":
    lang, score = identify_language("hello")
    print(f"lang={lang},score={score}")