import os
from urllib import request
import zipfile
import pathlib
import random
import warnings
import numpy as np
import tensorflow as tf
from scipy import ndimage
from tensorflow import keras
from keras.callbacks import CSVLogger
from tensorflow.keras import layers
import matplotlib.pyplot as plt



def load_numpy(path):
    data = np.load(path)
    return data


"""
IMPORTANT:
    Add proper comments.
    Add logger
"""



@tf.function
def rotate(volume):
    """Rotate the volume by a few degrees"""

    def scipy_rotate(volume):
        # define some rotation angles
        angles = [-20, -10, -5, 5, 10, 20]
        # pick angles at random
        angle = random.choice(angles)
        # rotate volume
        volume = ndimage.rotate(volume, angle, reshape=False)
        volume[volume < 0] = 0
        volume[volume > 1] = 1
        return volume

    augmented_volume = tf.numpy_function(scipy_rotate, [volume], tf.float32)
    return augmented_volume


def train_preprocessing(volume, label):
    """Process training data by rotating and adding a channel."""
    # Rotate volume
    # volume = rotate(volume)
    volume = tf.expand_dims(volume, axis=3)
    return volume, label


def validation_preprocessing(volume, label):
    """Process validation data by only adding a channel."""
    volume = tf.expand_dims(volume, axis=3)
    return volume, label

class CustomCNNWithSeprateLableFile():
    '''
    cfg required parameters
    - lr, epochs, patience, 
    
    '''
    def __init__(self, cfg = None, request_id = None):
        self.cfg = cfg
        self.model = None
        self.request_id = request_id
        self.width = self.height = self.depth = 64
    
    def checkGPUStatus(self):
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            # Restrict TensorFlow to only use the first GPU
            try:
                tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
                logical_gpus = tf.config.experimental.list_logical_devices('GPU')
                print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPU")
            except RuntimeError as e:
                # Visible devices must be set before GPUs have been initialized
                print(e)
        tf.debugging.set_log_device_placement(True)
        tf.config.list_physical_devices('GPU')

    def process_data(self, clean_path, infected_cases_path):

        # Getting paths
        try:
            clean_cases_path = [os.path.join(clean_path, x) 
                        for x in os.listdir(clean_path)]
            infected_cases_path = [os.path.join(infected_cases_path, x) 
                        for x in os.listdir(infected_cases_path)]    
            # Collecting labels
            self.clean_cases_labels = np.array([0 for _ in range(len(clean_cases_path))])
            self.infected_cases_labels = np.array([1 for _ in range(len(infected_cases_path))])

            # Loading data
            self.clean_cases = np.array([load_numpy(path) for path in clean_cases_path])
            self.infected_cases = np.array([load_numpy(path) for path in infected_cases_path])

            print("Clean cases " + str(len(self.clean_cases_labels)))
            print("Infected cases " + str(len(self.infected_cases_labels)))
        except Exception as e:
            print(e)
            return {
                "Error": e
            }


    def customTrainTestSplit(self):

        test_size = int(self.cfg['test_size'] * 100) 
        test_size_clean_cases = int((len(self.clean_cases) / 100) * test_size)
        test_size_infected_cases = int((len(self.infected_cases) / 100) * test_size)

        self.x_train = np.concatenate((self.clean_cases[test_size_clean_cases:], self.infected_cases[test_size_infected_cases:]), axis=0)
        self.y_train = np.concatenate((self.clean_cases_labels[test_size_clean_cases:], self.infected_cases_labels[test_size_infected_cases:]), axis=0)

        self.x_val = np.concatenate((self.clean_cases[:test_size_clean_cases], self.infected_cases[:test_size_infected_cases]), axis=0)
        self.y_val = np.concatenate((self.clean_cases_labels[:test_size_clean_cases], self.infected_cases_labels[:test_size_infected_cases]), axis=0)

        print("Number of samples in train and validation are %d and %d." %(len(self.x_train), len(self.x_val)))

    def data_augmentation(self, dataset):
        '''
            Need to implement some method
        '''
        pass

    def prepare_dataset(self):
        self.train_loader = tf.data.Dataset.from_tensor_slices((self.x_train, self.y_train))
        self.validation_loader = tf.data.Dataset.from_tensor_slices((self.x_val, self.y_val))

        batch_size = self.cfg['batch_size']
        # Augment the on the fly during training.
        self.train_dataset = (
            self.train_loader.shuffle(len(self.x_train))
            .map(train_preprocessing)
            .batch(batch_size)
            .prefetch(2)
        )
        # Only rescale.
        self.validation_dataset = (
            self.validation_loader.shuffle(len(self.x_val))
            .map(validation_preprocessing)
            .batch(batch_size)
            .prefetch(2)
        )

    def build_model(self):

        # NOTE: Build Modular 

        # self will all model build reqirements 
        # Required parameters: data_width, height and depth of array

        inputs = keras.Input((self.width, self.height, self.depth, 1))

        x = layers.Conv3D(filters=64, kernel_size=3, activation="relu")(inputs)
        x = layers.MaxPool3D(pool_size=2)(x)
        x = layers.BatchNormalization()(x)

        x = layers.Conv3D(filters=64, kernel_size=3, activation="relu")(x)
        x = layers.MaxPool3D(pool_size=2)(x)
        x = layers.BatchNormalization()(x)

        x = layers.Conv3D(filters=128, kernel_size=3, activation="relu")(x)
        x = layers.MaxPool3D(pool_size=2)(x)
        x = layers.BatchNormalization()(x)

        x = layers.Conv3D(filters=256, kernel_size=3, activation="relu")(x)
        x = layers.MaxPool3D(pool_size=2)(x)
        x = layers.BatchNormalization()(x)

        x = layers.GlobalAveragePooling3D()(x)
        x = layers.Dense(units=512, activation="relu")(x)
        x = layers.Dropout(0.3)(x)

        outputs = layers.Dense(units=1, activation="sigmoid")(x)

        # Define the model.
        model = keras.Model(inputs, outputs, name="3dcnn")
        return model
    

    def train_model(self):
        #csv_logger = CSVLogger("../model_trainging_logs/"+self.request_id+".csv", append=True)

        # Will get from self
        lr = self.cfg['lr']
        initial_learning_rate = self.cfg['initial_learning_rate']
        decay_rate = self.cfg['decay_rate']
        decay_steps = self.cfg['decay_steps']
        epochs = self.cfg['epochs']
        patience = self.cfg['patience']

        # Call
        self.customTrainTestSplit()
        self.prepare_dataset()

        
        # Model return from build_model
        model = self.build_model()

        lr_schedule = keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate, decay_steps=decay_steps, decay_rate=decay_rate, staircase=True)

        model.compile(
            loss="binary_crossentropy",
            optimizer=keras.optimizers.Adam(learning_rate=lr_schedule),
            metrics=["acc"],
        )

        # Define callbacks.
        checkpoint_cb = keras.callbacks.ModelCheckpoint("../models/",
            self.request_id+"_cnn.h5", save_best_only=True
        )

        early_stopping_cb = keras.callbacks.EarlyStopping(monitor="val_acc", patience=patience)

        # Train the model, doing validation at the end of each epoch

        model.fit(
            self.train_dataset,
            validation_data=self.validation_dataset,
            epochs=epochs,
            shuffle=True,
            verbose=2,
            callbacks=[checkpoint_cb, early_stopping_cb],
        )
        
        self.model = model

        self.save_model_data() 
        # Call model model valication sample
        
        # return model result using function

        return model

    def model_validation(self, data):
        self.load_model_data(self, self.request_id)
        prediction = self.model.predict(np.expand_dims(data, axis=0))[0]
        scores = [1 - prediction[0], prediction[0]]

        class_names = ["clean", "infected"]
        for score, name in zip(scores, class_names):
            print(
                "This model is %.2f percent confident that CT scan is %s"
                % ((100 * score), name)
            )

    def save_model_data(self):
        path = "../models/"+self.request_id+"_cnn.h5"
        self.model.save(path)
        print("CNN model " + self.request_id+"_cnn.h5 saved")

    def load_model_data(self):
        path = "../models/"+self.request_id+"_cnn.h5"
        try:
            self.model = keras.models.load_model(path)
        except Exception as e:
            return {'msg': 'Failed to load model',
                    'error': e 
                }

    def predict(self, request_id, data):
        if self.request_id != None:
            self.load_model_data()
            prediction = self.model.predict(data)
            
            scores = [1 - prediction[0], prediction[0]]
            results = []
            class_names = ["clean", "infected"]
            for score, name in zip(scores, class_names):
                results.append(
                    "This model is %.2f percent confident that CT scan is %s"
                    % ((100 * score), name)
                )
            return results
        else:
            print("Request_id required!!")
            return{
                "error": "Request_id required!!"
            }
    
    def cal_model_metrics(self):
        pass
    
    
    def test(self, clean_path, infected_path):
        print(clean_path)
