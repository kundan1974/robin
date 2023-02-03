# from execute import *

# from random import randrange


# request_id = "00123"
# numpy_file = "/Users/niteshwaghmare/Documents/WorkSpace/Project/oncology/QARC-E002/data/numpy/201489.npy"

# # predict_processed_file(id, numpy_file)

# dicom_path = "/Users/niteshwaghmare/Documents/WorkSpace/Project/oncology/QARC-E002/data/prediction_dicom/201489.zip"

# #predict_dicom_file(id, dicom_path)

# csv = "hello"

# csvfile = "/Users/niteshwaghmare/Documents/WorkSpace/Project/oncology/QARC-E002/execute/csvfile.csv"

# # prepare_data(request_id, csvfile)

# cfg = {
#     'epoch': 3000
# }
# #model_train(request_id, cfg)

# id = randrange(100000, 999999)
# print(id)


import os 

print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

models_path = os.path.join(BASE_PATH, "models/")

print(models_path)