import numpy as np
import scipy.io as sio
import os
from tqdm import tqdm


def zero_crossing_rate(signal):
    return ((signal[:-1] * signal[1:]) < 0).sum()

def extract_features_from_file(filepath):
    mat = sio.loadmat(filepath)
    data = mat["newData"][:, 1:10]  # Ignora a coluna do tempo e a última coluna (zero)

    features = []
    for i in range(data.shape[1]):
        sig = data[:, i]
        features.extend([
            np.mean(sig),
            np.std(sig),
            np.max(sig),
            zero_crossing_rate(sig)
        ])
    return features

def load_dataset(root_path):
    X, y = [], []
    for label_name, label in [('nonfall', 0), ('fall', 1)]:
        folder = os.path.join(root_path, label_name)
        for fname in tqdm(os.listdir(folder), desc=f"Lendo {label_name}"):
            if fname.endswith(".mat"):
                fpath = os.path.join(folder, fname)
                feat = extract_features_from_file(fpath)
                X.append(feat)
                y.append(label)
    return np.array(X), np.array(y)
