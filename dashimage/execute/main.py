import sys
sys.path.append("..")
import os
import shutil
import zipfile
import numpy as np
from random import randrange
from fastapi.responses import FileResponse
from utils.preprocessDICOM import preprocess
from fastapi import FastAPI, UploadFile, File, status, HTTPException
from execute import *


app = FastAPI()

# NOTE: Its assumed that RT Struct file will follow a naming convention of RS.<patient_id>.dcm
RT_STRUCT_FILE_FORMAT = "RS.{:s}.dcm"

# Assiging paths
dicom_images_path = "../data/dicom/"
dicom_processed_path = "../data/dicom_processed/"
dicom_processed_numpy = "../data/numpy/"
dicom_requested = "../data/dicom_requested/"


@app.post("/get_pre_processed_file")
async def pre_process_file(file: UploadFile = File(...)):
    '''
    Add comment
    '''
    if file.content_type != "application/zip":
        raise HTTPException(status_code=400, detail="Please upload valid zip file")
    else:
        file_location = dicom_requested+file.filename
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
        patient_id = file.filename.split(".")[0]

        with zipfile.ZipFile(file_location,"r") as zip_ref:
            zip_ref.extractall(dicom_images_path)

        patient_id_path = os.path.join(dicom_images_path, patient_id)
        patient_numpy_file_path = os.path.join(dicom_processed_numpy, patient_id + ".npy")

        patient_rt_struct_file_name = RT_STRUCT_FILE_FORMAT.format(patient_id)
        patient_rt_struct_file_path = os.path.join(patient_id_path, patient_rt_struct_file_name)

        if os.path.exists(patient_rt_struct_file_path):
            img = preprocess(patient_id_path, patient_rt_struct_file_path, zero=False)
            np.save(patient_numpy_file_path, img)
            shutil.rmtree(patient_id_path)
            return FileResponse(path=patient_numpy_file_path, filename=patient_id+".npy")
        else:
            raise HTTPException(status_code=400, detail="RT file is missing",)

#uvicorn main:app --reload

@app.get("/download_model/{model_id}")
async def download_model(model_id):
    """
    Download CNN model using request_id
    """
    model_path = "../models/"+model_id+"_cnn.h5"
    if os.path.exists(model_path):
        return FileResponse(path=model_path,filename=model_id+"_cnn.h5")
    else:
        raise HTTPException(status_code=400, detail="Model not found")


@app.post("/predict_dicom/{model_id}")
async def predictions_from_dicom(model_id,file: UploadFile = File(...)):
    """
    make prediction from dicom zip file
    """
    model_path = "../models/"+model_id+"_cnn.h5"
    if not os.path.exists(model_path):
        raise HTTPException(status_code=400, detail="Requested model is not present")

    if file.content_type != "application/zip":
        raise HTTPException(status_code=400, detail="Please upload valid zip file")
    else:

        file_location = dicom_requested+file.filename
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
        patient_id = file.filename.split(".")[0]

        with zipfile.ZipFile(file_location,"r") as zip_ref:
            zip_ref.extractall(dicom_images_path)

        patient_id_path = os.path.join(dicom_images_path, patient_id)
        patient_numpy_file_path = os.path.join(dicom_processed_numpy, patient_id + ".npy")

        patient_rt_struct_file_name = RT_STRUCT_FILE_FORMAT.format(patient_id)
        patient_rt_struct_file_path = os.path.join(patient_id_path, patient_rt_struct_file_name)

        if os.path.exists(patient_rt_struct_file_path):
            data = preprocess(patient_id_path, patient_rt_struct_file_path, zero=False)
            prediction = predict_processed_data(model_id, data)
            shutil.rmtree(patient_id_path)
            return {"Message": prediction}
        else:
            raise HTTPException(status_code=400, detail="RT file is missing",)


@app.post("/predictions_from_processed/{model_id}")
async def predictions_from_processed(model_id,file: UploadFile = File(...)):
    """
    Make predictions from processed file
    """
    file_path = "../data/numpy/"
    file_location = file_path+file.filename
    model_path = "../models/"+model_id+"_cnn.h5"

    if not os.path.exists(model_path):
        raise HTTPException(status_code=400, detail="Model not found")

    if False:
        # file.content_type != "application/zip"
        # Check valid file
        raise HTTPException(status_code=400, detail="Please upload valid zip file")
    else:
        try:
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file,buffer)
            if  os.path.exists(file_location):
                prediction = predict_processed_file(request_id=model_id, file_path=file_location)
                return prediction
            else:
                raise HTTPException(status_code=400, detail="Processed file is not exists on location")   
        except Exception as e:
            print(e)
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()


@app.post("/upload_processed_file/{request_id}")
async def upload_processed_file(request_id,file: UploadFile = File(...)):
    """
    Upload one processed file at specific location
    """
    request_path = "../data/model_training_data/"+request_id
    if not os.path.exists(request_path):
        os.mkdir(request_path)
    
    if False:
        # file.content_type != "application/zip"
        raise HTTPException(status_code=400, detail="Please upload valid zip file")
    else:
        file_location = request_path + "/"+ file.filename
        try:
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file,buffer)
                return {"message": "file upload done!!!"}
        except Exception as e:
            print(e)
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()


@app.post("/upload_batch_processed_file/{request_id}")
async def upload_batch_processed_file(request_id,file: UploadFile = File(...)):
    """
    Upload zip file that contains processed files 
    """
    request_path = "../data/model_training_data/"+request_id
    if not os.path.exists(request_path):
        os.mkdir(request_path)
    if file.content_type != "application/zip":
        raise HTTPException(status_code=400, detail="Please upload valid zip file")
    else:
        temp_id = randrange(100000, 999999)
        temp_path = "../data/temp/"+str(temp_id)
        os.mkdir(temp_path)
        temp_location = temp_path + file.filename

        with open(temp_location, "wb") as buffer:
            shutil.copyfileobj(file.file,buffer)

        with zipfile.ZipFile(temp_location,"r") as zip_ref:
            zip_ref.extractall(request_path)
        
        shutil.rmtree(temp_path)
        return {"message" : "Files upload successfully!!"}



@app.post("/upload_dicom_file/{request_id}")
async def upload_dicom_file(request_id, file: UploadFile = File(...)):
    '''
    Add comment
    '''
    request_path = "../data/model_training_data/"+request_id+"/"

    if not os.path.exists(request_path):
        os.mkdir(request_path)
    if file.content_type != "application/zip":
        raise HTTPException(status_code=400, detail="Please upload valid zip file")
    else:
        file_location = dicom_requested+file.filename
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
        patient_id = file.filename.split(".")[0]

        with zipfile.ZipFile(file_location,"r") as zip_ref:
            zip_ref.extractall(dicom_images_path)

        patient_id_path = os.path.join(dicom_images_path, patient_id)
        patient_numpy_file_path = os.path.join(dicom_processed_numpy, patient_id + ".npy")

        patient_rt_struct_file_name = RT_STRUCT_FILE_FORMAT.format(patient_id)
        patient_rt_struct_file_path = os.path.join(patient_id_path, patient_rt_struct_file_name)

        if os.path.exists(patient_rt_struct_file_path):
            img = preprocess(patient_id_path, patient_rt_struct_file_path, zero=False)
            np.save(request_path+patient_id + ".npy", img)
            return {"message": "Dicom upload and processed successfully!!!"}
        else:
            raise HTTPException(status_code=400, detail="RT file is missing",)


@app.post("/upload_bulk_dicom_file/{request_id}")
async def upload_bulk_dicom_file(request_id, file: UploadFile = File(...)):
    pass


@app.post("/model_train/")
async def model_train(request_id, cfg,file: UploadFile = File(...)):
    """
    validate cfg before passing to 
    Use Thrade
    """
    training_data_path = "../data/model_training_data/"+request_id
    if not os.path.exists(training_data_path):
       raise HTTPException(status_code=400, detail="No data avaliable for model training") 
    
    try:
        file_location = "../data/temp/"+file.filename
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
    except Exception as e:
        print(e)
    prepare_data(request_id, file_location)
    # Call model training in Thread function
    # model_train(request_id, cfg)
    return {"message":"Model training in progress"}


@app.get("/model_train_status/{model_status_id}")
async def model_train_status(model_status_id):
    pass
