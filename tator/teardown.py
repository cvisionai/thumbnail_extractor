#!/usr/bin/env python3

import pytator
import json
import os

def uploadThumbnails(tator, thumbnail_type_id, directory):
    for dir_element in os.listdir(directory):
        full_path=os.path.join(directory, dir_element)
        localization_id=int(os.path.splitext(dir_element)[0])
        md5=pytator.md5sum.md5_sum(full_path)
        tator.Media.uploadFile(thumbnail_type_id,
                               full_path,
                               waitForTranscode=True,
                               progressBars=False,
                               md5=md5,
                               section="Thumbnails")
        media=tator.Media.byMd5(md5)
        tator.Localization.update(localization_id,
                                  {"thumbnail_image": media['id']})

if __name__ == '__main__':
    rest_svc = os.getenv('TATOR_API_SERVICE')
    work_dir = os.getenv('TATOR_WORK_DIR')
    token = os.getenv('TATOR_AUTH_TOKEN')
    project_id = os.getenv('TATOR_PROJECT_ID')
    pipeline_args_str = os.getenv('TATOR_PIPELINE_ARGS')
    pipeline_args = json.loads(pipeline_args_str)
    thumbnail_type_id = pipeline_args['imageTypeId']

    tator = pytator.Tator(rest_svc, token, project_id)

    for dir_element in os.listdir(work_dir):
        full_path=os.path.join(work_dir, dir_element)
        if os.path.isdir(full_path):
            uploadThumbnails(tator, thumbnail_type_id, full_path)
