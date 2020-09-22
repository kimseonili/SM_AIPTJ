from parse import load_ps
import utils
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.signal import medfilt
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from statistics import mean

# 필요한 기본 수치값 연산 클라스~
class BodyValue:
    def __init__(self,pose):
        self.pose = pose
    # 상박
    def upper_arm_vectors_r(self):
        return [self.pose.rshoulder.x - self.pose.relbow.x, self.pose.rshoulder.y - self.pose.relbow.y]
    def upper_arm_vectors_l(self):
        return [self.pose.lshoulder.x - self.pose.lelbow.x, self.pose.lshoulder.y - self.pose.lelbow.y]
    # 하박
    def lower_arm_vectors_r(self): 
        return [self.pose.relbow.x - self.pose.rwrist.x, self.pose.relbow.y - self.pose.rwrist.y]

    def lower_arm_vectors_l(self):
        return [self.pose.lelbow.x - self.pose.lwrist.x, self.pose.lelbow.y - self.pose.lwrist.y]
    # 목 - 엉덩이
    def torso_vectors(self):
        return [self.pose.neck.x - (self.pose.rhip.x + self.pose.lhip.x)/2, self.pose.neck.y - (self.pose.rhip.y + self.pose.lhip.y)/2]
    # 허벅지
    def upper_leg_vectors_r(self):
        return [self.pose.rhip.x - self.pose.rknee.x, self.pose.rhip.y - self.pose.rknee.y]
    def upper_leg_vectors_l(self):
        return [self.pose.lhip.x - self.pose.lknee.x, self.pose.lhip.y - self.pose.lknee.y]
    # 종아리
    def lower_leg_vectors_r(self):
        return [self.pose.rknee.x - self.pose.rankle.x, self.pose.rknee.y - self.pose.rankle.y]
    def lower_leg_vectors_l(self):
        return [self.pose.lknee.x - self.pose.lankle.x, self.pose.lknee.y - self.pose.lankle.y]
    # 발 사이 거리
    def between_feet_vectors(self):
        return [self.pose.rankle.x - self.pose.lankle.x, self.pose.rankle.y - self.pose.lankle.y]
    #어깨사이거리
    def between_shoulder_vectors(self):
        return [self.pose.rshoulder.x - self.pose.lshoulder.x, self.pose.rshoulder.y - self.pose.lshoulder.y]
    # 몸 - 팔 각도
    def upper_arm_torso_angle_r(self):
        return math.degrees(np.arccos(np.clip(np.dot(self.upper_arm_vectors_r(),self.torso_vectors()),-1.0,1.0)))
    def upper_arm_torso_angle_l(self):
        return math.degrees(np.arccos(np.clip(np.dot(self.upper_arm_vectors_l(),self.torso_vectors()),-1.0,1.0)))
    # 상박 - 하박 각도
    def upper_lower_arm_angle_r(self):
        return math.degrees(np.arccos(np.clip(np.dot(self.upper_arm_vectors_r(),self.lower_arm_vectors_r()),-1.0,1.0)))
    def upper_lower_arm_angle_l(self):
        return math.degrees(np.arccos(np.clip(np.dot(self.upper_arm_vectors_l(),self.lower_arm_vectors_l()),-1.0,1.0)))
    # 골반 거리
    def between_hip_vectors(self):
        return [self.pose.rhip.x - self.pose.lhip.x, self.pose.rhip.y - self.pose.lhip.y]
    # 허벅지 - 종아리 각도
    def upper_lower_leg_angle_r(self):
        return math.degrees(np.arccos(np.clip(np.dot(self.upper_leg_vectors_r(),self.lower_leg_vectors_r()),-1.0,1.0)))
    def upper_lower_leg_angle_l(self):
        return math.degrees(np.arccos(np.clip(np.dot(self.upper_leg_vectors_l(),self.lower_leg_vectors_l()),-1.0,1.0)))





# 비교할 기준
ps_std = load_ps('poses_compressed/baseball/Accurate_baseball/zbaseball_accurate1.npy')
# 인풋 데이터
ps = load_ps('input data_path')

poses_std = ps_std.poses
poses = ps.poses

# 발 사이 거리
between_feet_vectors_std = []
between_feet_vectors = []
# 어깨 사이 거리
between_shoulder_vectors_std=[]
between_shoulder_vectors=[]
# 골반 사이 거리
between_hip_vectors_std = []
between_hip_vectors = []
# 어깨, 다리사이거리 비율
shoulder_step_vectors_std=[]
shoulder_step_vectors=[]
# 몸 - 팔 각도
upper_arm_torso_angle_r_std = []
upper_arm_torso_angle_r = []

upper_arm_torso_angle_l_std = []
upper_arm_torso_angle_l = []
# 상박 - 하박 각도
upper_lower_arm_angle_r_std = []
upper_lower_arm_angle_r = []

upper_lower_arm_angle_l_std = []
upper_lower_arm_angle_l = []
# 허벅지 - 종아리 각도
upper_lower_leg_angle_r_std=[]
upper_lower_leg_angle_r=[]

upper_lower_leg_angle_l_std=[]
upper_lower_leg_angle_l=[]


# 각 파트별 원하는 값 도출
for i, (pose_std,pose) in enumerate(zip(poses_std,poses)):
        between_feet_vectors_std.append(((BodyValue(pose_std).between_feet_vectors()[0])**2 + (BodyValue(pose_std).between_feet_vectors()[1])**2)**1/2)
        between_feet_vectors.append(((BodyValue(pose).between_feet_vectors()[0])**2 + (BodyValue(pose).between_feet_vectors()[1])**2)**1/2)

        # print(between_feet_vectors[i])
        between_hip_vectors_std.append(((BodyValue(pose_std).between_hip_vectors()[0])**2 + (BodyValue(pose_std).between_hip_vectors()[1])**2)**1/2)
        between_hip_vectors.append(((BodyValue(pose).between_hip_vectors()[0])**2 + (BodyValue(pose).between_hip_vectors()[1])**2)**1/2)

        between_shoulder_vectors_std.append(((BodyValue(pose_std).between_shoulder_vectors()[0])**2 + (BodyValue(pose_std).between_shoulder_vectors()[1])**2)**1/2)
        between_shoulder_vectors.append(((BodyValue(pose).between_shoulder_vectors()[0])**2 + (BodyValue(pose).between_shoulder_vectors()[1])**2)**1/2)
        # print(between_shoulder_vectors[i])

        
        shoulder_step_vectors_std.append(between_feet_vectors_std[i]/between_shoulder_vectors_std[i])
        shoulder_step_vectors.append(between_feet_vectors[i]/between_shoulder_vectors[i])

        upper_arm_torso_angle_r_std.append(BodyValue(pose_std).upper_arm_torso_angle_r())
        upper_arm_torso_angle_r.append(BodyValue(pose).upper_arm_torso_angle_r())

        upper_arm_torso_angle_l_std.append(BodyValue(pose_std).upper_arm_torso_angle_l())
        upper_arm_torso_angle_l.append(BodyValue(pose).upper_arm_torso_angle_l())

        upper_lower_arm_angle_r_std.append(BodyValue(pose_std).upper_lower_arm_angle_r())
        upper_lower_arm_angle_r.append(BodyValue(pose).upper_lower_arm_angle_r())

        upper_lower_arm_angle_l_std.append(BodyValue(pose_std).upper_lower_arm_angle_l())
        upper_lower_arm_angle_l.append(BodyValue(pose).upper_lower_arm_angle_l())

        upper_lower_leg_angle_r_std.append(BodyValue(pose_std).upper_lower_leg_angle_r())
        upper_lower_leg_angle_r.append(BodyValue(pose).upper_lower_leg_angle_r())

        upper_lower_leg_angle_l_std.append(BodyValue(pose_std).upper_lower_leg_angle_l())
        upper_lower_leg_angle_l.append(BodyValue(pose).upper_lower_leg_angle_l())

# 각 부위별 수치값에 필터적용    
between_feet_vectors_filtered_std = medfilt(medfilt(np.array(between_feet_vectors_std), 5), 5)
between_feet_vectors_filtered = medfilt(medfilt(np.array(between_feet_vectors), 5), 5)

between_hip_vectors_filtered_std = medfilt(medfilt(np.array(between_hip_vectors_std), 5), 5)
between_hip_vectors_filtered = medfilt(medfilt(np.array(between_hip_vectors), 5), 5)

shoulder_step_vectors_filtered_std = medfilt(medfilt(np.array(shoulder_step_vectors_std), 5), 5)
shoulder_step_vectors_filtered = medfilt(medfilt(np.array(shoulder_step_vectors), 5), 5)

upper_arm_torso_angle_r_filtered_std = medfilt(medfilt(np.array(upper_arm_torso_angle_r_std), 5), 5)
upper_arm_torso_angle_r_filtered = medfilt(medfilt(np.array(upper_arm_torso_angle_r), 5), 5)
upper_arm_torso_angle_l_filtered_std = medfilt(medfilt(np.array(upper_arm_torso_angle_l_std), 5), 5)
upper_arm_torso_angle_l_filtered = medfilt(medfilt(np.array(upper_arm_torso_angle_l), 5), 5)

upper_lower_arm_angle_r_filtered_std = medfilt(medfilt(np.array(upper_lower_arm_angle_r_std), 5), 5)
upper_lower_arm_angle_r_filtered = medfilt(medfilt(np.array(upper_lower_arm_angle_r), 5), 5)
upper_lower_arm_angle_l_filtered_std = medfilt(medfilt(np.array(upper_lower_arm_angle_l_std), 5), 5)
upper_lower_arm_angle_l_filtered = medfilt(medfilt(np.array(upper_lower_arm_angle_l), 5), 5)

upper_lower_leg_angle_r_filtered_std = medfilt(medfilt(np.array(upper_lower_leg_angle_r_std), 5), 5)
upper_lower_leg_angle_r_filtered = medfilt(medfilt(np.array(upper_lower_leg_angle_r), 5), 5)
upper_lower_leg_angle_l_filtered_std = medfilt(medfilt(np.array(upper_lower_leg_angle_l_std), 5), 5)
upper_lower_leg_angle_l_filtered = medfilt(medfilt(np.array(upper_lower_leg_angle_l), 5), 5)

# 리스트로 변환
between_feet_vectors_list_std = between_feet_vectors_filtered_std.tolist()
between_feet_vectors_list = between_feet_vectors_filtered.tolist()

between_hip_vectors_list_std = between_hip_vectors_filtered_std.tolist()
between_hip_vectors_list = between_hip_vectors_filtered.tolist()

shoulder_step_vectors_list_std = shoulder_step_vectors_filtered_std.tolist()
shoulder_step_vectors_list = shoulder_step_vectors_filtered.tolist()

upper_arm_torso_angle_r_list_std = upper_arm_torso_angle_r_filtered_std.tolist()
upper_arm_torso_angle_r_list = upper_arm_torso_angle_r_filtered.tolist()

upper_arm_torso_angle_l_list_std = upper_arm_torso_angle_l_filtered_std.tolist()
upper_arm_torso_angle_l_list = upper_arm_torso_angle_l_filtered.tolist()

upper_lower_arm_angle_r_list_std = upper_lower_arm_angle_r_filtered_std.tolist()
upper_lower_arm_angle_r_list = upper_lower_arm_angle_r_filtered.tolist()

upper_lower_arm_angle_l_list_std = upper_lower_arm_angle_l_filtered_std.tolist()
upper_lower_arm_angle_l_list = upper_lower_arm_angle_l_filtered.tolist()

upper_lower_leg_angle_r_list_std = upper_lower_leg_angle_r_filtered_std.tolist()
upper_lower_leg_angle_r_list = upper_lower_leg_angle_r_filtered.tolist()

upper_lower_leg_angle_l_list_std = upper_lower_leg_angle_l_filtered_std.tolist()
upper_lower_leg_angle_l_list = upper_lower_leg_angle_l_filtered.tolist()

# 넘파이로 변환
between_feet_np_std = np.array(between_feet_vectors_list_std)
between_feet_np = np.array(between_feet_vectors_list)

between_hip_np_std = np.array(between_hip_vectors_list_std)
between_hip_np = np.array(between_hip_vectors_list)

shoulder_step_np_std = np.array(shoulder_step_vectors_list_std)
shoulder_step_np = np.array(shoulder_step_vectors_list)

upper_arm_torso_r_np_std = np.array(upper_arm_torso_angle_r_list_std)
upper_arm_torso_r_np = np.array(upper_arm_torso_angle_r_list)

upper_arm_torso_l_np_std = np.array(upper_arm_torso_angle_l_list_std)
upper_arm_torso_l_np = np.array(upper_arm_torso_angle_l_list)

upper_lower_arm_r_np_std = np.array(upper_lower_arm_angle_r_list_std)
upper_lower_arm_r_np = np.array(upper_lower_arm_angle_r_list)

upper_lower_arm_l_np_std = np.array(upper_lower_arm_angle_l_list_std)
upper_lower_arm_l_np = np.array(upper_lower_arm_angle_l_list)

upper_lower_leg_r_np_std = np.array(upper_lower_leg_angle_r_list_std)
upper_lower_leg_r_np = np.array(upper_lower_leg_angle_r_list)

upper_lower_leg_l_np_std = np.array(upper_lower_leg_angle_l_list_std)
upper_lower_leg_l_np = np.array(upper_lower_leg_angle_l_list)

#dtw값 도출
distance_list=[]
parts_std=['between_feet_np_std','between_hip_np_std','shoulder_step_np_std','upper_arm_torso_r_np_std','upper_arm_torso_l_np_std','upper_lower_arm_r_np_std','upper_lower_arm_l_np_std','upper_lower_leg_r_np_std','upper_lower_leg_l_np_std']

parts=['between_feet_np','between_hip_np','shoulder_step_np','upper_arm_torso_r_np','upper_arm_torso_l_np','upper_lower_arm_r_np','upper_lower_arm_l_np','upper_lower_leg_r_np','upper_lower_leg_l_np']
for (part_std,part) in zip(parts_std,parts):
# def dtw():
    
    
    x = vars()[part_std]
    y = vars()[part]
  
    
    distance, path = fastdtw(x, y, dist=euclidean)
    distance_list.append(distance)
    # print(distance_list)
    # print(distance)
    # print(path)

if distance_list[0] > 49.0 and distance_list[2] >  500.0:
    print("하체가 불안정합니다. 타격시 다리사이간격 좀 더 벌려주세요")

if distance_list[1] > 1.245:
    print("타격시 허리의 회전이 부족합니다. 앞발에 무게중심을 실고 허리를 회전시켜야합니다")

if distance_list[3] > 608.0 :
    print("스윙 전 배트를 들고있는 팔이 몸에서 너무 뒤로 빠져있습니다 몸쪽으로 더 당겨주세요")

if distance_list[5] > 360.0 and distance_list[6] > 323.0:
    print("스윙시 배트를 들고있는 팔은 최대한 몸에 붙혀서 끝까지뻗어서 스윙해주세요")