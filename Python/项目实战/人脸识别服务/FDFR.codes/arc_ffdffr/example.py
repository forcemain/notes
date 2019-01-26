#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from arcsoft.core.manager import FaceDetectionManager, FaceRecognitionManager


if __name__ == '__main__':
    mm_img1 = 'images/limanman_first.jpeg'
    mm_img2 = 'images/limanman_second.jpeg'

    with FaceDetectionManager() as fdmanager, FaceRecognitionManager() as frmanager:
        _, mm_faces1 = fdmanager.do_still_image_detection(mm_img1)
        _, mm_faces2 = fdmanager.do_still_image_detection(mm_img2)

        _, ref_feature = frmanager.do_extract_frfeature(mm_faces1[0])
        _, pro_feature = frmanager.do_extract_frfeature(mm_faces2[0])

        frmanager.do_facepair_matching(ref_feature, pro_feature)
