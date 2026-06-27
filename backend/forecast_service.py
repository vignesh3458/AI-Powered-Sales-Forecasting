from backend.database import (
    get_sales_data,
    get_model_update_time
)

from forecasting.forecast_model import (
    generate_forecast
)

import numpy as np

def get_forecast(periods=30):

    df = get_sales_data()

    model_version = get_model_update_time()

    forecast = generate_forecast(
        df,
        model_version=model_version,
        periods=periods
    )

    forecast = forecast.replace({
        np.nan: None
    })

    return {

        "status": "success",

        "model_version": str(model_version),

        "forecast": forecast[
            [
                "ds",
                "yhat",
                "yhat_lower",
                "yhat_upper"
            ]
        ].to_dict(
            orient="records"
        )

    }