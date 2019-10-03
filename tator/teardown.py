#!/usr/bin/env python3

import pytator
import json
import os
import sys

def uploadThumbnails(tator, dest_tator, mode, thumbnail_type_id, directory):
    for dir_element in os.listdir(directory):
        full_path=os.path.join(directory, dir_element)
        localization_id=int(os.path.splitext(dir_element)[0])
        media=dest_tator.Media.byName(dir_element)
        if not media:
            md5=pytator.md5sum.md5_sum(full_path)
            dest_tator.Media.uploadFile(thumbnail_type_id,
                               full_path,
                               waitForTranscode=True,
                               progressBars=False,
                               md5=md5,
                               section="Thumbnails")
            media=tator.Media.byMd5(md5)

        if mode == "state" or "localization_keyframe":
            #TODO: Duplicate state objects
            pass
        elif mode == "localization_thumbnail":
            localization=tator.Localization.get(localization_id)
            media_attrs=media['attributes']
            media_attrs.update(localization['attributes'])
            tator.Media.applyAttribute(media['id'], media_attrs)
            tator.Localization.update(localization_id,
                                      {"thumbnail_image": media['id']})

if __name__ == '__main__':
    rest_svc = os.getenv('TATOR_API_SERVICE')
    work_dir = os.getenv('TATOR_WORK_DIR')
    token = os.getenv('TATOR_AUTH_TOKEN')
    project_id = os.getenv('TATOR_PROJECT_ID')
    pipeline_args_str = os.getenv('TATOR_PIPELINE_ARGS')
    if pipeline_args_str:
        pipeline_args = json.loads(pipeline_args_str)
    else:
        print("ERROR: No pipeline arguments specified!")
        sys.exit(-1)
    thumbnail_type_id = pipeline_args['imageTypeId']
    dest_project_id = pipeline_args.get('destProject', project_id)
    mode = pipeline_args.get('mode', None)

    tator = pytator.Tator(rest_svc, token, project_id)
    dest_tator = pytator.Tator(rest_svc, token, dest_project_id)

    for dir_element in os.listdir(work_dir):
        full_path=os.path.join(work_dir, dir_element)
        if os.path.isdir(full_path):
            uploadThumbnails(tator, dest_tator, mode, thumbnail_type_id, full_path)
