import io
import os
import re
import sys
import csv
import shutil
import zipfile
import numpy as np
# sys.path.append("..")
import urllib, base64
import matplotlib.pyplot as plt
# from ..ml.CustomCNN import CustomCNNWithSeprateLableFile
from .preprocessDICOM import preprocess


def plot_slices(num_rows, num_columns, width, height, data):
    plt.switch_backend('Agg')
    """Plot a montage of 20 CT slices"""
    data = np.rot90(np.array(data))
    data = np.transpose(data)
    data = np.reshape(data, (num_rows, num_columns, width, height))
    rows_data, columns_data = data.shape[0], data.shape[1]
    heights = [slc[0].shape[0] for slc in data]
    widths = [slc.shape[1] for slc in data[0]]
    fig_width = 12.0
    fig_height = fig_width * sum(heights) / sum(widths)
    f, axarr = plt.subplots(
        rows_data,
        columns_data,
        figsize=(fig_width, fig_height),
        gridspec_kw={"height_ratios": heights},
    )
    for i in range(rows_data):
        for j in range(columns_data):
            axarr[i, j].imshow(data[i][j], cmap="gray")
            axarr[i, j].axis("off")
    # plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
    # plt.show()
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return uri


def handle_uploaded_file(file, request_id):
    """
    Upload .dashimage in requested id folder
    """

    request_path = "data/model_training_data/" + request_id
    if not os.path.exists(request_path):
        os.makedirs(request_path)
        # os.mkdir(request_path)

    if False:
        # file.content_type != "application/zip"
        raise HTTPException(status_code=400, detail="Please upload valid zip file")
    else:
        file_location = request_path + "/" + str(file)
        try:
            # with open(file_location, "wb") as buffer:
            #     shutil.copyfileobj(file.file,buffer)
            with open(file_location, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                return {"message": "file upload done!!!"}
        except Exception as e:
            print(e)
            return {"message": "There was an error uploading the file"}


def handle_uploaded_zip_file(file, patient_id, request_id):
    print("processing started")
    # Assing paths
    data_path = "data/"

    # NOTE: Its assumed that RT Struct file will follow a naming convention of RS.<patient_id>.dcm
    RT_STRUCT_FILE_FORMAT = "RS.{:s}.dcm"

    request_path = "data/model_training_data/" + request_id
    if not os.path.exists(request_path):
        os.makedirs(request_path)
        # os.mkdir(request_path)

    zip_location = os.path.join(data_path, "dicom_requested/", str(file))
    # Uploading zip file
    with open(zip_location, "wb") as buffer:
        for chunk in file.chunks():
            buffer.write(chunk)

    dicom_path = os.path.join(data_path, "dicom/")
    with zipfile.ZipFile(zip_location, "r") as zip_ref:
        zip_ref.extractall(dicom_path)

    patient_dicom_path = os.path.join(dicom_path, patient_id)
    print(patient_dicom_path)
    patient_rt_struct_file_name = RT_STRUCT_FILE_FORMAT.format(patient_id)
    patient_numpy_file_path = os.path.join(request_path, patient_id + ".dashimage")
    print(patient_numpy_file_path)
    patient_rt_struct_file_path = os.path.join(patient_dicom_path, patient_rt_struct_file_name)
    print(patient_rt_struct_file_path)
    if os.path.exists(patient_rt_struct_file_path):
        img = preprocess(patient_dicom_path, patient_rt_struct_file_path, zero=False)
        np.save(patient_numpy_file_path, img)
        shutil.rmtree(patient_dicom_path)
        os.remove(zip_location)
        print("processing ended")
        return patient_numpy_file_path
    else:
        return {"error": "RT file is missing"}


def handle_processDICOM(file, patient_id):
    """
    Process DICOM zip and return .dashimage
    """
    print("processing started")
    data_path = os.path.join(os.getcwd(), "dashimage/data/")

    # NOTE: Its assumed that RT Struct file will follow a naming convention of RS.<patient_id>.dcm
    RT_STRUCT_FILE_FORMAT = "RS.{:s}.dcm"

    zip_location = os.path.join(data_path, "dicom_requested/", str(file))
    # Uploading zip file
    try:
        with open(zip_location, "wb") as buffer:
            for chunk in file.chunks():
                buffer.write(chunk)
    except Exception as e:
        print("Error in file upload")
        print(e)

    dicom_path = os.path.join(data_path, "dicom/")
    with zipfile.ZipFile(zip_location, "r") as zip_ref:
        zip_ref.extractall(dicom_path)
    patient_dicom_path = os.path.join(dicom_path, patient_id)

    for file in os.listdir(patient_dicom_path):
        if file.startswith('RS'):
            patient_rt_struct_file_name = file
            patient_rt_struct_file_path = os.path.join(patient_dicom_path, patient_rt_struct_file_name)
            # patient_rt_struct_file_name = RT_STRUCT_FILE_FORMAT.format(patient_id)
            patient_dashimage_file_path = os.path.join(data_path, 'dashimage/', patient_id)
            if os.path.exists(patient_rt_struct_file_path):
                img = preprocess(patient_dicom_path, patient_rt_struct_file_path, zero=False)
                np.save(patient_dashimage_file_path, img)

                print("Image saved")
                img_data = plot_slices(6, 10, 64, 64, img[:, :, :60])

                data = {
                    "patient_id": patient_id,
                    "img_data": img_data
                }
                shutil.rmtree(patient_dicom_path)
                os.remove(zip_location)
                return data
    else:
        return {"error": "RT file is missing"}


def handle_batch_upload_dashimage(file, request_id):
    request_path = "data/model_training_data/" + request_id
    if not os.path.exists(request_path):
        os.makedirs(request_path)

    zip_temp_location = os.path.join("data/", "temp/", str(file))

    with open(zip_temp_location, "wb") as buffer:
        for chunk in file.chunks():
            buffer.write(chunk)

    with zipfile.ZipFile(zip_temp_location, "r") as zip_ref:
        zip_ref.extractall(request_path)

    os.remove(zip_temp_location)

    total_file_count = len(os.listdir(request_path))
    print("total file count: " + str(total_file_count))
    return "total file count: " + str(total_file_count)


def prepare_data(request_id, csvfile):
    """
    Filter infected and clean data for model training using provided csv
    """
    data_path = "data/model_training_data/" + request_id
    filtered_data_path = "data/training_data_filtered/" + request_id
    temp_csv_location = "data/temp/" + str(csvfile)
    with open(temp_csv_location, "wb") as buffer:
        for chunk in csvfile.chunks():
            buffer.write(chunk)

    if os.path.exists(data_path):
        print("Total files for model training: " + str(len(os.listdir(data_path))))

        if not os.path.exists(filtered_data_path):
            try:
                os.mkdir(filtered_data_path)
                os.mkdir(filtered_data_path + "/clean_cases")
                os.mkdir(filtered_data_path + "/infected_cases")
            except OSError as error:
                print(error)

        # Read csv and copy files
        with open(temp_csv_location, mode='r') as file:
            csvFile = csv.reader(file)
            try:
                for lines in csvFile:
                    file = data_path + "/" + lines[0] + '.dashimage'
                    print(file)
                    if os.path.exists(file):
                        if lines[1] == "1":
                            # copy to infacted folder
                            print(file + " : -ve")
                            shutil.copy2(file, filtered_data_path + "/infected_cases")
                        elif lines[1] == "0":
                            # copy to the disinfect folder
                            # print(file + " : +ve")
                            shutil.copy2(file, filtered_data_path + "/clean_cases")
                        else:
                            print(file)
                print("Coping files done!!!")
                print("Total cleancases files for model training: " + str(
                    len(os.listdir(filtered_data_path + "/clean_cases"))))
                print("Total infectedcases files for model training: " + str(
                    len(os.listdir(filtered_data_path + "/infected_cases"))))
            except:
                print("Error")
    else:
        print("Path is not exists!!!")


def load_dashimage(dashaimage):
    temp_path = os.path.join(os.getcwd, "data/temp/")
    temp_dashimage_location = os.path.join(temp_path, str(dashaimage))

    with open(temp_dashimage_location, "wb") as buffer:
        for chunk in dashaimage.chunks():
            buffer.write(chunk)

    dashaimage_data = np.load(temp_dashimage_location)
    img_data = plot_slices(6, 10, 64, 64, dashaimage_data[:, :, :60])

    patient_id = str(dashaimage).split(".")[0]
    data = {
        "patient_id": patient_id,
        "img_data": img_data
    }

    return data


def model_train(request_id, cfg):
    """
    Train model  
    - First call process_data function 
    """
    filtered_data_path = "../data/training_data_filtered/" + request_id

    clean_cases_count = len(os.listdir(filtered_data_path + "/clean_cases"))
    infected_cases_count = len(os.listdir(filtered_data_path + "/infected_cases"))

    if clean_cases_count > 0 and infected_cases_count > 0:
        # Call 
        cnn_obj = CustomCNNWithSeprateLableFile(cfg=cfg, request_id=request_id)
        cnn_obj.train_model()
    else:
        print("Data is not sufficient for model training")
        return {"error": "Data is not sufficient for model training"}


def file_upload(file, path, filetype):
    """
    File upload on specific location
    """

    if not os.path.exists(path):
        os.makedirs(path)

    if validate_file(file, filetype):
        file_location = path + "/" + str(file)
        try:
            with open(file_location, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                return {"message": "file upload done!!!"}
        except Exception as e:
            print(e)
            return {"message": "There was an error uploading the file", "error": e}
    else:
        print("")
        return {"message": "Please upload valid file"}


def validate_file(file, filetype):
    """
    File validation process
    """
    return True


def mobile(request):
    """Return True if the request comes from a mobile device."""
    MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False
