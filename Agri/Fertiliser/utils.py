import pickle

def load_fertilizer_model():
    """Load and return the fertilizer recommendation model."""
    with open('E:/SAMS/Agri/Fertiliser/Model/fertilizer.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

def preprocess_input(input_data):
    """
    Prepare input data for prediction.
    Assumes soil and crop values are directly received as encoded integers.
    """
    temp, humi, mois, soil, crop, nitro, pota, phosp = input_data

    # Combine all features into a single list for the model
    processed_data = [temp, humi, mois, soil, crop, nitro, pota, phosp]

    return processed_data
