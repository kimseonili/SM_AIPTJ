import json
import numpy as np
import os

      
 
json_file = os.path.join('json_dir')
json_file=str(json_file)

with open(json_file) as f:
        json_obj = json.load(f)
        num_frames = len(json_obj)
        # print(num_frames)
        all_keypoints = np.zeros((num_frames, 18, 3))
        for i in range(num_frames):
            distances=[]
            number_str = str(i+1)
            zero_filled_number = number_str.zfill(3)
            for k in range(len(json_obj[str(+1)+' '+zero_filled_number+'.jpg']['people'])):
                nose_x=json_obj[str(+1)+' '+zero_filled_number+'.jpg']['people'][k]['pose_keypoints_2d'][0]
                nose_y=json_obj[str(+1)+' '+zero_filled_number+'.jpg']['people'][k]['pose_keypoints_2d'][1]
                lankle_x=json_obj[str(+1)+' '+zero_filled_number+'.jpg']['people'][k]['pose_keypoints_2d'][39]
                lankle_y=json_obj[str(+1)+' '+zero_filled_number+'.jpg']['people'][k]['pose_keypoints_2d'][40]
                nl_distence=((nose_x-lankle_x)**2 + (nose_y-lankle_y)**2)**(1/2)
                distances.append(nl_distence)
                
            index_ = distances.index(max(distances))
                

                  
            keypoints = np.array(json_obj[str(+1)+' '+zero_filled_number+'.jpg']['people'][index_]['pose_keypoints_2d'])#Alphapose 형식
            all_keypoints[i] = keypoints.reshape((18, 3))
                
        output_dir ='npy_dir'
        np.save(output_dir, all_keypoints)