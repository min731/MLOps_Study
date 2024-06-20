# -*- coding: utf-8 -*-

import pandas as pd
from pycaret.classification import load_model, predict_model
from fastapi import FastAPI
import uvicorn
from pydantic import create_model

# Create the app
app = FastAPI()

# Load trained Pipeline
model = load_model("first_api")

# Create input/output pydantic models
input_model = create_model("first_api_input", **{'Id': 121, 'WeekofPurchase': 260, 'StoreID': 2, 'PriceCH': 1.8600000143051147, 'PriceMM': 2.180000066757202, 'DiscCH': 0.0, 'DiscMM': 0.699999988079071, 'SpecialCH': 0, 'SpecialMM': 0, 'LoyalCH': 0.9593049883842468, 'SalePriceMM': 1.4800000190734863, 'SalePriceCH': 1.8600000143051147, 'PriceDiff': -0.3799999952316284, 'Store7': 'No', 'PctDiscMM': 0.32110100984573364, 'PctDiscCH': 0.0, 'ListPriceDiff': 0.3199999928474426, 'STORE': 2})
output_model = create_model("first_api_output", prediction='CH')


# Define predict function
@app.post("/predict", response_model=output_model)
def predict(data: input_model):
    data = pd.DataFrame([data.dict()])
    predictions = predict_model(model, data=data)
    return {"prediction": predictions["prediction_label"].iloc[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
