import numpy as np
import librosa
from os import walk, path

import warnings
warnings.filterwarnings('ignore')

class DataParser:
    def __init__(self, root, duration=None, pickle=None):
        self.pickle = pickle
        self.duration = duration
        self.root = root
        genres = [x[0] for x in walk(self.root)][1:]
        self.label_mapping = {genre: index for (index, genre) in enumerate(genres)}

    def to_label(self, string):
        return self.label_mapping[string]

    def to_string(self, label):
        label_mapping = {value: key for (key,value) in self.label_mapping}
        return label_mapping[label]

    def extract_features(self, file_path):
        raw, rate = librosa.load(file_path, duration=30)
        stft = np.abs(librosa.stft(raw))
        mfcc = np.mean(librosa.feature.mfcc(y=raw,sr=rate,n_mfcc=40).T, axis=0)
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=rate).T, axis=0)
        mel = np.mean(librosa.feature.melspectrogram(y=raw, sr=rate).T, axis=0)
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=rate).T, axis=0)
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(raw), sr=rate).T, axis=0)
        return [mfcc, chroma, mel, contrast, tonnetz]

    def from_files(self):
        labels = []
        samples = []

        for glob in list(walk(self.root))[1:]:
            subdir, songs = glob[0], glob[2]
            print(f"{subdir}")
            for song in songs:
                print(song)
                features = self.extract_features(path.join(subdir, song))
                samples.append(np.hstack(features))
                labels.append(self.to_label(subdir))
        return np.array(samples), np.array(labels)

    def from_pickle(self):
        if self.pickle:
            return np.load(self.pickle, allow_pickle=True)

def main():
    root = input()
    parser = DataParser(root=root)
    samples, labels = parser.from_files()
    np.save(f"{root}_samples.npy", samples, allow_pickle=True)
    np.save(f"{root}_labels.npy", labels, allow_pickle=True)

if __name__ == "__main__":
    main()
