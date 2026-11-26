"""Recognise handwritten digits: machine learning with pictures (real data that comes with scikit-learn)."""
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

digits = load_digits()
print(f"{len(digits.images)} images of {digits.images[0].shape[0]}×{digits.images[0].shape[1]} pixels")
print("The first image as numbers (0 = white, 16 = black):")
print(digits.images[0].astype(int))

fig, axes = plt.subplots(1, 10, figsize=(10, 1.4))
for ax, image, label in zip(axes, digits.images, digits.target):
    ax.imshow(image, cmap="gray_r"); ax.set_title(label); ax.axis("off")
plt.savefig("digits.png", dpi=110, bbox_inches="tight")

X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.25, random_state=1)
model = SVC().fit(X_train, y_train)
predicted = model.predict(X_test)
print(f"\nRight on {accuracy_score(y_test, predicted):.1%} of {len(y_test)} digits it hasn't seen")

wrong = [i for i in range(len(y_test)) if predicted[i] != y_test[i]]
fig, axes = plt.subplots(1, len(wrong), figsize=(1.1 * len(wrong), 1.6))
for ax, i in zip(axes, wrong):
    ax.imshow(X_test[i].reshape(8, 8), cmap="gray_r"); ax.set_title(f"{y_test[i]}→{predicted[i]}"); ax.axis("off")
plt.savefig("digits_mistakes.png", dpi=110, bbox_inches="tight")
print(f"Mistakes (real→predicted): {', '.join(f'{y_test[i]}→{predicted[i]}' for i in wrong)}")
