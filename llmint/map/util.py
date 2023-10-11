def format_output(prediction):
    """Convert the prediction format to match the desired ground-truth format."""
    formatted_predictions = []
    for i in range(0, len(prediction), 3):
        entry = {
            pred.split(": ")[0].replace("'", "").strip(): pred.split(": ")[1].replace("'", "").strip()
            for pred in prediction[i:i + 3]
        }
        formatted_predictions.append(entry)
    return formatted_predictions
