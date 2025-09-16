import json
import shutil
import os
import SimpleITK as sitk


idxes = ['025',
'038',
'062',
'218',
'361',
'235',
'347',
'147',
'090',
'179',
'066',
'152',
'210',
'228',
'133',
'346',
'116']

def save_prediction(final_segmentation_as_npy, subject_id, RESULTDIR='Results/ITK_test'):
    os.makedirs(RESULTDIR, exist_ok=True)
    label_mask = sitk.GetImageFromArray(final_segmentation_as_npy)
    sitk.WriteImage(label_mask, os.path.join(RESULTDIR, subject_id + '_pred.nii.gz'))

def create_zip(RESULTDIR='Results/ITK_test'):
    
    prediction_json = []
    for i, name in enumerate(sorted(idxes)):
        # Copy the image to the output directory
        src = os.path.join(RESULTDIR, 'BraTS20_Training_' + name + '_pred.nii.gz')
        dst = './submission/item' + str(i) + '/output/images/tumor-segmentation/BraTS20_Training_' + name + '_pred.nii.gz'
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)
        prediction_json.append({
            "pk": f"item{i}",
            "inputs": [
                {
                    "image": {
                        "name": f"BraTS20_Training_{name}",
                    },
                    "interface": {
                        "slug": "brain-image",
                        "relative_path": "images/brain-mri",
                    }
                }
            ],
            "outputs": [
                {
                    "image": {
                        "name": f"BraTS20_Training_{name}"
                    },
                    "interface": {
                        "slug": "tumor-segmentation",
                        "relative_path": "images/tumor-segmentation",
                    }
                }
            ],
            })

    with open('./submission/predictions.json', "w") as f:
        json.dump(prediction_json, f, indent=4)
    shutil.make_archive('./submission', 'zip', './submission')
    # remove the submission folder
    shutil.rmtree('./submission')