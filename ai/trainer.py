import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from joblib import dump

def load_and_prepare_data(filepath: str, shift_steps: int = 30):
    df = pd.read_csv(filepath)
    df['x_next'] = df['x'].shift(-shift_steps)
    df['y_next'] = df['y'].shift(-shift_steps)
    df.dropna(inplace=True)
    return df

def split_features_targets(df):
    X = df[['x', 'y', 'vx', 'vy', 'timestamp']]
    y_x = df['x_next']
    y_y = df['y_next']
    return X, y_x, y_y

def train_models(X, y_x, y_y, test_size=0.2):
    X_train, _, yx_train, _ = train_test_split(X, y_x, test_size=test_size)
    _, _, yy_train, _ = train_test_split(X, y_y, test_size=test_size)
    
    model_x = RandomForestRegressor(n_estimators=100)
    model_y = RandomForestRegressor(n_estimators=100)
    
    model_x.fit(X_train, yx_train)
    model_y.fit(X_train, yy_train)
    
    return model_x, model_y

def save_models(model_x, model_y, directory="ai/models"):
    os.makedirs(directory, exist_ok=True)
    dump(model_x, os.path.join(directory, "model_x.joblib"))
    dump(model_y, os.path.join(directory, "model_y.joblib"))

def main():
    df = load_and_prepare_data('data/player_moves.csv')
    X, y_x, y_y = split_features_targets(df)
    model_x, model_y = train_models(X, y_x, y_y)
    save_models(model_x, model_y)
    print("Models trained and saved successfully.")

if __name__ == "__main__":
    main()
