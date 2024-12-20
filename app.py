from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import plotly
import json

app = Flask(__name__)

# Load dataset
data = pd.read_csv('data/data.csv')

# Convert categorical columns
categorical_columns = ['AIRLINE', 'ORIGIN', 'DEST']
data[categorical_columns] = data[categorical_columns].astype('category')

# Prepare features and target
X = data.drop(columns=['ARR_DELAY'])
y = data['ARR_DELAY']

# Home route
@app.route('/')
def home():
    # Dataset description and head
    dataset_description = "This dataset contains flight data with columns including airline, origin, destination, arrival delay, and other flight-related information."
    dataset_head = data.head()

    # Create initial visualizations
    delay_dist_plot = create_delay_distribution_plot()
    monthly_delay_plot = create_monthly_delay_plot()

    # Extract unique airlines
    airlines = data['AIRLINE'].cat.categories.tolist()

    return render_template('index.html', 
                           description=dataset_description, 
                           dataset_head=dataset_head.to_html(classes='table table-bordered'),
                           delay_dist_plot=delay_dist_plot,
                           monthly_delay_plot=monthly_delay_plot,
                           airlines=airlines)

# Create delay distribution plot
def create_delay_distribution_plot():
    fig = px.histogram(data, x='ARR_DELAY', nbins=50, title="Distribution of Arrival Delays")
    fig.update_layout(
        xaxis_title="Arrival Delay (minutes)",
        yaxis_title="Frequency",
        template="plotly_dark"
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Create airline-specific delay distribution plot
@app.route('/get_airline_plot', methods=['POST'])
def get_airline_plot():
    airline = request.json.get('airline')

    if airline:
        # Filter data for the selected airline
        filtered_data = data[data['AIRLINE'] == airline]
        if filtered_data.empty:
            return jsonify({'error': 'No data available for the selected airline.'}), 400
        title = f"Distribution of Arrival Delays for {airline}"
    else:
        # Use all airlines if no specific airline is selected
        filtered_data = data
        title = "Distribution of Arrival Delays for All Airlines"
    
    fig = px.histogram(filtered_data, x='ARR_DELAY', nbins=50, title=title)
    fig.update_layout(
        xaxis_title="Arrival Delay (minutes)",
        yaxis_title="Frequency",
        template="plotly_dark"
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Create monthly delay plot
def create_monthly_delay_plot():
    monthly_avg_delay = data.groupby('MONTH')['ARR_DELAY'].mean().reset_index()
    fig = px.bar(monthly_avg_delay, x='MONTH', y='ARR_DELAY', title="Monthly Average Flight Delays")
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Average Delay (minutes)",
        template="plotly_dark"
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Train the model route
@app.route('/train_model', methods=['POST'])
def train_model():
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the CatBoostRegressor model
    model = CatBoostRegressor(
        iterations=1000,
        depth=6,
        learning_rate=0.1,
        loss_function='RMSE',
        verbose=200
    )

    # Indices of categorical features
    cat_feature_indices = [X.columns.get_loc(col) for col in categorical_columns]

    # Train the model
    model.fit(
        X_train,
        y_train,
        eval_set=(X_test, y_test),
        use_best_model=True,
        cat_features=cat_feature_indices
    )

    # Extract evaluation metrics
    eval_results = model.evals_result_

    # Prepare data for visualization
    iterations = list(range(len(eval_results['validation']['RMSE'])))
    train_rmse = eval_results['learn']['RMSE']
    val_rmse = eval_results['validation']['RMSE']

    # Create training metrics plot
    training_plot = create_training_plot(iterations, train_rmse, val_rmse)

    # Final metrics
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5

    # Create feature importance plot
    feature_importance_plot = create_feature_importance_plot(model, X)

    # Create actual vs predicted plot
    actual_vs_predicted_plot = create_actual_vs_predicted_plot(y_test, y_pred)

    return jsonify({
        'rmse': rmse,
        'mse': mse,
        'training_plot': training_plot,
        'feature_importance_plot': feature_importance_plot,
        'actual_vs_predicted_plot': actual_vs_predicted_plot
    })


def create_training_plot(iterations, train_rmse, val_rmse):
    """Creates a Plotly visualization for training and validation RMSE."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=iterations, y=train_rmse, mode='lines', name='Train RMSE'))
    fig.add_trace(go.Scatter(x=iterations, y=val_rmse, mode='lines', name='Validation RMSE'))
    fig.update_layout(
        title="Training and Validation RMSE Over Iterations",
        xaxis_title="Iterations",
        yaxis_title="RMSE",
        template="plotly_dark"
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_feature_importance_plot(model, X):
    """Creates a feature importance plot."""
    feature_importances = model.get_feature_importance()
    fig = px.bar(x=X.columns, y=feature_importances, labels={'x': 'Feature', 'y': 'Importance'}, title="Feature Importance")
    fig.update_layout(template="plotly_dark")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_actual_vs_predicted_plot(y_test, y_pred):
    """Creates a scatter plot for actual vs predicted values."""
    fig = px.scatter(x=y_test, y=y_pred, labels={'x': 'Actual Delay', 'y': 'Predicted Delay'})
    fig.update_layout(title="Actual vs Predicted Arrival Delays", template="plotly_dark")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

if __name__ == '__main__':
    app.run(debug=True)
