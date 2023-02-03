import os
import sys
import csv
import shutil
import numpy as np
sys.path.append("..")
# import zipfile
# from random import randrange
from ml.CustomCNN import CustomCNNWithSeprateLableFile
from utils.preprocessDICOM import preprocess



def load_numpy(path):
    data = np.load(path)
    return data


def predict_processed_file(request_id, file_path):
    """
    Make predictions from request_id and numpy file
    """
    model_path = "../models/"+str(request_id)+"_cnn.h5"
    if os.path.exists(model_path):
        if os.path.exists(file_path):
            cnn_obj = CustomCNNWithSeprateLableFile(request_id=request_id)
            data = load_numpy(file_path)
            prediction = cnn_obj.predict(request_id=request_id, data=data)
            return prediction
    else:
        print("msg: " + str(request_id)+"_cnn.h5 model is not present")
        return {"msg": str(request_id)+"_cnn.h5 model is not present"}


def predict_processed_data(request_id, data):
    """
    Make predictions from request_id and numpy file
    """
    model_path = "../models/"+str(request_id)+"_cnn.h5"
    if os.path.exists(model_path):
        cnn_obj = CustomCNNWithSeprateLableFile(request_id=request_id)
        prediction = cnn_obj.predict(request_id=request_id, data = data)
        print(prediction)
        return prediction
    else:
        print("msg: " + str(request_id)+"_cnn.h5 model is not present")
        return {"msg": str(request_id)+"_cnn.h5 model is not present"}


# Same API is predict_processed_data
def predict_dicom_file(request_id, dicom_path):
    """
    Make predictions from request_id and dicom zip file
    """
    model_path = "../models/"+str(request_id)+"_cnn.h5"
    if os.path.exists(model_path):
        if os.path.exists(dicom_path):
            # Pass dicom_path for producing numpy
            # Pass numpy path to load file
            # Pass numpy file and request_id for CNN prediction 
            pass
    else:
        print("msg: " + str(request_id)+"_cnn.h5 model is not present")
        return {"msg": str(request_id)+"_cnn.h5 model is not present"}


def model_train(request_id, cfg):
    """
    Train model  
    - First call process_data function 
    """
    filtered_data_path = "../data/training_data_filtered/"+request_id

    clean_cases_count = len(os.listdir(filtered_data_path+"/clean_cases"))
    infected_cases_count = len(os.listdir(filtered_data_path+"/infected_cases"))

    if clean_cases_count > 0 and infected_cases_count > 0:
        # Call 
        cnn_obj = CustomCNNWithSeprateLableFile(cfg=cfg, request_id=request_id)
        cnn_obj.train_model()
    else:
        print("Data is not sufficient for model training")
        return {"error": "Data is not sufficient for model training"}



def prepare_data(request_id, csvfile):
    """
    Filter infected and clean data for model training using provided csv
    """
    data_path = "../data/model_training_data/"+request_id
    filtered_data_path = "../data/training_data_filtered/"+request_id
    if os.path.exists(data_path):
        print("Total files for model training: " +  str(len(os.listdir(data_path))))

        if not os.path.exists(filtered_data_path):
            try:
                os.mkdir(filtered_data_path)
                os.mkdir(filtered_data_path+"/clean_cases")
                os.mkdir(filtered_data_path+"/infected_cases")
            except OSError as error: 
                print(error)
        
        # Read csv and copy files
        with open(csvfile, mode ='r')as file:
            csvFile = csv.reader(file)
            try:
                for lines in csvFile:
                    file = data_path +"/"+ lines[0] + '.npy'
                    if os.path.exists(file):
                        if lines[1] == "1":
                            # copy to infacted folder
                            #print(file + " : -ve")
                            shutil.copy2(file, filtered_data_path+"/infected_cases")
                        elif lines[1] == "0":
                            # copy to the disinfect folder
                            #print(file + " : +ve")
                            shutil.copy2(file, filtered_data_path+"/clean_cases")
                        else:
                            print(file)
                print("Coping files done!!!")
                print("Total cleancases files for model training: " +  str(len(os.listdir(filtered_data_path+"/clean_cases"))))
                print("Total infectedcases files for model training: " +  str(len(os.listdir(filtered_data_path+"/infected_cases"))))
            except:
                print("Error")
    else: 
        print("Path is not exists!!!")

def batch_dicom_process(request_id, path):
    pass



def model_training_test(csvfile):
    try:
        with open(csvfile, mode ='r')as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                print(lines)
    except Exception as e:
        print(e)
        return "Error"
    return "All okey!!!"