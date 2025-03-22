import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Sample dataset: ['followers', 'following', 'tweets', 'is_bot (1=bot, 0=human)']
data = [
    [100, 10, 200, 1],  # Likely a bot
    [500, 300, 1000, 0],  # Human
    [50, 5, 20, 1],  # Bot
    [1000, 900, 5000, 0],  # Human
]

df = pd.DataFrame(data, columns=["followers", "following", "tweets", "is_bot"])
X = df[["followers", "following", "tweets"]]
y = df["is_bot"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Test accuracy
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

def predict_bot(followers, following, tweets):
    return model.predict([[followers, following, tweets]])[0]
