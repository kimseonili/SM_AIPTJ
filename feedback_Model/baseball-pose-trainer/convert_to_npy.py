import json
import numpy as np
import os

class npyConverter :
    def startConvert():      
        json_file = os.path.join('alphapose-results.json')
        json_file=str(json_file)

        with open(json_file) as f:
                json_obj = json.load(f)
                num_frames = len(json_obj)
                # print(num_frames)
                all_keypoints = np.zeros((num_frames, 18, 3))
                for i in range(num_frames):
                    distances=[]
                    number_str = str(i)
                    zero_filled_number = number_str.zfill(3)
                    for k in range(len(json_obj[zero_filled_number+'.jpg']['people'])):
                        # print(len(json_obj['swing_'+zero_filled_number+'.jpg']['people']))
                        nose_x=json_obj[zero_filled_number+'.jpg']['people'][k]['pose_keypoints_2d'][0]
                        nose_y=json_obj[zero_filled_number+'.jpg']['people'][k]['pose_keypoints_2d'][1]
                        lankle_x=json_obj[zero_filled_number+'.jpg']['people'][k]['pose_keypoints_2d'][39]
                        lankle_y=json_obj[zero_filled_number+'.jpg']['people'][k]['pose_keypoints_2d'][40]
                        # print(nose_x,nose_y,lankle_x,lankle_y)
                        nl_distence=((nose_x-lankle_x)**2 + (nose_y-lankle_y)**2)**(1/2)
                        distances.append(nl_distence)
                        # np.array(['swing_'+zerofiled_number+'.jpg']['people'][k]['pose_keypoints_2d'])[40]
                    index_ = distances.index(max(distances))
                        # print(distances)
                        

                        
                    keypoints = np.array(json_obj[zero_filled_number+'.jpg']['people'][index_]['pose_keypoints_2d'])#Alphapose 형식
                    all_keypoints[i] = keypoints.reshape((18, 3))
                    # print(all_keypoints[i])
                        
                output_dir ='my_npy.npy'
                np.save(output_dir, all_keypoints)