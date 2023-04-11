import mimetypes
# import requests
import os, shutil, errno
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from .models import ModelTrainingStatus
from .utils.support import handle_processDICOM, load_dashimage, file_upload, mobile


def main_index(request):
    if mobile(request):
        context = {'is_mobile': True}
    else:
        context = {'is_mobile': False}
    return render(request, 'index.html', context)


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def query(request):
    return render(request, 'summery.html')


@login_required
def dashimage(request):
    # working
    if request.method == "POST":
        # process file
        if request.FILES['zip_file']:

            try:
                file = request.FILES['zip_file']
                filename = str(file)
                if filename.split(".")[1] == "zip":
                    patient_id = filename.split(".")[0]
                    img_data = handle_processDICOM(file, patient_id)
                    return render(request, 'convert_dicom.html',
                                  {'image_uri': img_data['img_data'], 'patient_id': img_data['patient_id']})
                else:
                    print("Please upload valid zip")
            except Exception as e:
                print(e)
        print("Out with out processing ")
        return render(request, 'convert_dicom.html')
    else:
        return render(request, 'convert_dicom.html')


@login_required
def upload_file(request):
    # working
    if request.method == "POST":
        if request.FILES['data_file'] and request.POST["request_id"]:
            request_id = request.POST["request_id"]
            file = request.FILES['data_file']
            filename = str(file)

            try:
                if filename.split(".")[-1] == "dashimage":
                    print("process .dashimage")
                    # handle_uploaded_file(file, request_id)
                elif filename.split(".")[-1] == "zip":
                    print("process .zip")
                    # handle_uploaded_zip_file(file, filename.split(".")[0], request_id)
                else:
                    print("Wrong file format")
            except Exception as e:
                print(e)
            return render(request, 'upload_file.html')
    else:
        return render(request, 'upload_file.html')


@login_required
def upload_batch_files(request):
    if request.method == "POST":
        if request.FILES['data_file'] and request.POST["request_id"]:
            request_id = request.POST["request_id"]
            file = request.FILES['data_file']
            filename = str(file)
            try:
                if filename.split(".")[-1] == "zip":
                    print("process .dashimage")
                    # handle_batch_upload_dashimage(file, request_id)
                elif filename.split(".")[-1] == "uy":
                    print("process .zip")
                    # handle_uploaded_zip_file(file, filename.split(".")[0], request_id)
                else:
                    print("Wrong file format")
            except Exception as e:
                print(e)
        return render(request, 'upload_batch_files.html')
    else:
        return render(request, 'upload_batch_files.html')


@login_required
def download_model(request):
    # NOTE: Dropdown should contain all id's that are associated with user
    if request.method == "POST":
        if request.POST['model_id']:
            model_id = request.POST['model_id']
            model_name = model_id + "_cnn.h5"
            model_path = "models/" + model_name
            if os.path.exists(model_path):
                with open(model_path, 'rb') as model:
                    mime_type, _ = mimetypes.guess_type(model_path)
                    response = HttpResponse(model, content_type=mime_type)
                    response['Content-Disposition'] = 'attachment; filename=%s' % model_name
                    return response
            else:
                print("Model is not")
        return render(request, 'download_model.html')
    else:
        return render(request, 'download_model.html')


@login_required
def make_predictions(request):
    # NOTE: Dropdown should contain all id's that are associated with user
    if request.method == "POST":
        # Detect file type and call api based on
        print("Got it")
        return render(request, 'make_predictions.html')
    else:
        return render(request, 'make_predictions.html')


@login_required
def train_model(request):
    if request.method == 'POST':
        if request.POST['model_id'] and request.POST['epoch'] and request.POST['lr'] and request.POST['test_size'] and \
                request.POST['batch_size'] and request.POST['patience']:
            if request.FILES['label_csv']:
                csvfile = request.FILES['label_csv']
                path = os.path.join(os.getcwd(), "dashimage/data/training_csv")
                print(path)
                if file_upload(csvfile, path, "csv"):
                    # Save data into db
                    model_id = request.POST['model_id']
                    user_id = "001"
                    epoch = request.POST['epoch']
                    lr = request.POST['lr']
                    test_size = request.POST['test_size']
                    batch_size = request.POST['batch_size']
                    patience = request.POST['patience']
                    csv_file_name = str(csvfile)
                    status = "Yet to start"
                    try:
                        # NOTE: Do this properly
                        data = ModelTrainingStatus.objects.create(model_id=model_id, user_id=user_id, epoch=epoch,
                                                                  lr=lr, test_size=test_size, batch_size=batch_size,
                                                                  csv_file_name=csv_file_name, status=status)
                        data.full_clean()
                        print("Cleaning done")
                        return render(request, 'model_train.html', {'status': "Success",
                                                                    "message": "Request has been submited model training will start soon."})
                    except ValidationError as e:
                        return render(request, 'model_train.html', {'status': "Error", 'Message': e})
                else:
                    return render(request, 'model_train.html',
                                  {'status': "Error", "message": "Error while uploading label file"})

            return render(request, 'model_train.html')
    else:
        return render(request, 'model_train.html')


@login_required
def get_model_training_status(request):
    # model_training_status = ModelTrainingStatus.objects.all()
    # return render(request, 'model_training_status.html', {"model_req_list": model_training_status})
    return render(request, 'model_training_status.html')


@login_required
def view_dashimage(request):
    # NOTE: Dropdown should contain all id's that are associated with user
    if request.method == "POST":
        if request.FILES['dashimage']:
            dashimage = request.FILES['dashimage']
            img_data = load_dashimage(dashimage)
        return render(request, 'view_dashimage.html',
                      {'image_uri': img_data['img_data'], 'patient_id': img_data['patient_id']})
    else:
        return render(request, 'view_dashimage.html')


@login_required
def download_file(request, patient_id):
    if patient_id:
        image_path = os.path.join(os.getcwd(), "dashimage/data/dashimage/")
        image_path = image_path + patient_id + ".npy"
        if os.path.exists(image_path):
            with open(image_path, 'rb') as datafile:
                mime_type, _ = mimetypes.guess_type(image_path)
                response = HttpResponse(datafile, content_type=mime_type)
                response['Content-Disposition'] = 'attachment; filename=%s' % patient_id + ".dashimage"
                return response
        else:
            print(image_path)
            print("path not present")
        return render(request, 'convert_dicom.html')
    else:
        return render(request, 'convert_dicom.html')
