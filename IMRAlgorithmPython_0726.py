#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
IMRecruitable Matchmaking Algorithm
asa277@cornell.edu
'''
'''
RESTATEMENT:
    Calculate a quantification of 'likeness' of a particular school given a
    student's criteria
OUTPUT:
    perc_academic (int)
    perc_enroll (int)
    perc_cost (int)
    perc_major (int)
    perc_athletic (int)
    overall_perc (int)

GIVEN:
    percentiles for all statistical criteria

FORMULA:
    overall_perc = (perc_academic * 0.25) + (perc_enroll* 0.05) +
    (perc_cost * 0.20) + (perc_major * 0.30) + (perc_athletic * 0.20)

'''


# In[2]:


import numpy as np
import ipywidgets as widgets
from ipywidgets import interactive, interact, interactive_output
from IPython.display import display
import time
from tkinter import *


# # Defining Constants -- can be changed accordingly 

# In[3]:


# WEIGHTS
WGT_ACADEM = 0.25
WGT_ENROLL = 0.05
WGT_COST = 0.20
WGT_MAJ = 0.30
WGT_ATH = 0.20

WGT1_SAT = 0.20
WGT1_ACT = 0.20
WGT1_GPA = 0.30
WGT1_ACR = 0.30

WGT2_ENRO = 0.10
WGT2_CAMP = 0.10
WGT2_SETT = 0.30
WGT2_STATE = 0.50

WGT3_TUIT = 0.75
WGT3_PNM = 0.25

#WGT_4_MAJ

WGT5_DIV = 1




# CONSTANTS - ACADEMIC CRITERIA
# GPA
GPA_0 = 2.230
GPA_10 = 2.678
GPA_20 = 2.800
GPA_30 = 2.900
GPA_40 = 3.000
GPA_50 = 3.100
GPA_60 = 3.200
GPA_70 = 3.300
GPA_80 = 3.410
GPA_90 = 3.592
GPA_100 = 4.00

# AVG SAT
SAT_NA = 0
SAT_0 = 490
SAT_10 = 970
SAT_20 = 1010
SAT_30 = 1040
SAT_40 = 1070
SAT_50 = 1110
SAT_60 = 1130
SAT_70 = 1170
SAT_80 = 1230
SAT_90 = 1330
SAT_95 = 1450
SAT_100 = 1560

# AVG ACT
ACT_NA = 0
ACT_0 = 15
ACT_10 = 19
ACT_20 = 21
ACT_30 = 22
ACT_40 = 23
ACT_50 = 24
ACT_60 = 25
ACT_70 = 26
ACT_80 = 28
ACT_90 = 30
ACT_95 = 32
ACT_100 = 35

# AVG ACCEPTANCE RATE
'''
ACR_0 = 0.04
ACT_01 = 0.12
ACT_025 = 0.2355
ACR_5 = 0.34
ACR_10 = 0.46
ACR_15 = 0.52
ACR_20 = 0.57
ACR_25 = 0.61
ACR_30 = 0.64
ACR_40 = 0.71
ACR_50 = 0.78
ACR_100 = 1.00

'''
ACR_0 = 0.0
ACR_1 = 0.05
ACR_2 = 0.15
ACR_3 = 0.35
ACR_4 = 0.50
ACR_5 = 0.65
ACR_6 = 0.75
ACR_7 = 1.0


# In[4]:


# CONSTANTS - ENROLLMENT SCHOOL SIZE
# ENROLLMENT
ENRO_0 = 100
ENRO_1 = 1000
ENRO_2 = 1500
ENRO_3 = 3000
ENRO_4 = 5000
ENRO_5 = 8500
ENRO_6 = 10000
ENRO_7 = 15000
ENRO_8 = 25000
ENRO_9 = 75000

# CAMPUS CITY POPULATION 
CITY_1 = 50
CITY_2 = 2500
CITY_3 = 7500
CITY_4 = 12500
CITY_5 = 25000
CITY_6 = 50000
CITY_7 = 100000
CITY_8 = 200000
CITY_9 = 350000
CITY_10 = 750000
CITY_11 = 1250000
CITY_12 = 8500000


# In[5]:


# CONSTANTS AFFORDABILITY
# TUITION - SELECT IS/OS ----- CHOICE BOX
TUIT_0 = 0
TUIT_1 = 1500
TUIT_2 = 5000
TUIT_3 = 7500
TUIT_4 = 10000
TUIT_5 = 15000
TUIT_6 = 30000
TUIT_7 = 45000
TUIT_8 = 55000

# PERC NEED MET
PNM_0 = 0
PNM_1 = 25
PNM_2 = 50
PNM_3 = 60
PNM_4 = 70
PNM_5 = 80
PNM_6 = 90
PNM_7 = 100


# In[6]:


# CONSTANTS -- MAJOR/STUDENT LIFE


# OUT OF STATE
OOS_0 = 0
OOS_1 = 5
OOS_2 = 10
OOS_3 = 25
OOS_4 = 35
OOS_5 = 50
OOS_6 = 65
OOS_7 = 75
OOS_8 = 99


# # Sorting of Input Information/UI Buttons-Widgets - Assignment to Bins 

# ## Validating Input

# In[7]:


def validate_SAT(user_SAT_str):
    valid = True
    if not (user_SAT_str.isdigit() and int(user_SAT_str) >= 0 and int(user_SAT_str) <= 1600):
      valid = False
    if int(user_SAT_str) % 10 != 0 or int(user_SAT_str) < 400:
      valid = False
    return valid

def validate_ACT(user_ACT_str):
    return user_ACT_str.isdigit() and int(user_ACT_str) >=0 and int(user_ACT_str) <=36
def validate_GPA(user_GPA_str):
    return (user_GPA_str.replace('.', '', 1).isdigit() or user_GPA_str.isdigit()) and ((float(user_GPA_str) >=0 and float(user_GPA_str) <= 4.0)) or (int(user_GPA_str) >= 0 and int(user_GPA_str) <= 4)

def validate_weights(weight1, weight2, weight3, weight4, weight5):
    valid = True
    weights = [weight1, weight2, weight3, weight4, weight5]
    for weight in weights:
      if str(weight).isnumeric() == False:
        valid = False
    if int(weight1) + int(weight2) + int(weight3) + int(weight4) + int(weight5) != 100:
      valid = False
    return valid


# ## Academic Criteria - Bin Creation based off entered SAT SCORE

# In[8]:


# SAT / ACT Range
def sat_bin(score):
    if score == '0':
        sat_range = 0
        bin_val = "VOID"
    elif SAT_NA < float(score) <= SAT_0:
        sat_range = np.arange(SAT_NA + 1, SAT_0 + 1, 1)
        bin_val = 1
    elif SAT_0 < float(score) <= SAT_10:
        sat_range = np.arange(SAT_0 + 1, SAT_10 + 1, 1)
        bin_val = 2
    elif SAT_10 < float(score) <= SAT_20:
        sat_range = np.arange(SAT_10 + 1, SAT_20 + 1, 1)
        bin_val = 3
    elif SAT_20 < float(score) <= SAT_30:
        sat_range = np.arange(SAT_20 + 1, SAT_30 + 1, 1)
        bin_val = 4
    elif SAT_30 < float(score) <= SAT_40:
        sat_range = np.arange(SAT_30 + 1, SAT_40 + 1, 1)
        bin_val = 5
    elif SAT_40 < float(score) <= SAT_50:
        sat_range = np.arange(SAT_40 + 1, SAT_50 + 1, 1)
        bin_val = 6
    elif SAT_50 < float(score) <= SAT_60:
        sat_range = np.arange(SAT_50 + 1, SAT_60 + 1, 1)
        bin_val = 7
    elif SAT_60 < float(score) <= SAT_70:
        sat_range = np.arange(SAT_60 + 1, SAT_70 + 1, 1)
        bin_val = 8
    elif SAT_70 < float(score) <= SAT_80:
        sat_range = np.arange(SAT_70 + 1, SAT_80 + 1, 1)
        bin_val = 9
    elif SAT_80 < float(score) <= SAT_90:
        sat_range = np.arange(SAT_80 + 1, SAT_90 + 1, 1)
        bin_val = 10
    elif SAT_90 < float(score) <= SAT_100:
        sat_range = np.arange(SAT_90 + 1, SAT_100 + 1, 1)
        bin_val = 11
    else:
        sat_range = 0
        bin_val = "VOID"
    return bin_val

def act_bin(score):
    if score == '0':
        act_range = 0
        bin_val = "VOID"
    elif ACT_NA < float(score) <= ACT_0:
        act_range = np.arange(ACT_NA + 1, ACT_0 + 1, 1)
        bin_val = 1
    elif ACT_0 < float(score) <= ACT_10:
        act_range = np.arange(ACT_0 + 1, ACT_10 + 1, 1)
        bin_val = 2
    elif ACT_10 < float(score) <= ACT_20:
        act_range = np.arange(ACT_10 + 1, ACT_20 + 1, 1)
        bin_val = 3
    elif ACT_20 < float(score) <= ACT_30:
        act_range = np.arange(ACT_20 + 1, ACT_30 + 1, 1)
        bin_val = 4
    elif ACT_30 < float(score) <= ACT_40:
        act_range = np.arange(ACT_30 + 1, ACT_40 + 1, 1)
        bin_val = 5
    elif ACT_40 < float(score) <= ACT_50:
        act_range = np.arange(ACT_40 + 1, ACT_50 + 1, 1)
        bin_val = 6
    elif ACT_50 < float(score) <= ACT_60:
        act_range = np.arange(ACT_50 + 1, ACT_60 + 1, 1)
        bin_val = 7
    elif ACT_60 < float(score) <= ACT_70:
        act_range = np.arange(ACT_60 + 1, ACT_70 + 1, 1)
        bin_val = 8
    elif ACT_70 < float(score) <= ACT_80:
        act_range = np.arange(ACT_70 + 1, ACT_80 + 1, 1)
        bin_val = 9
    elif ACT_80 < float(score) <= ACT_90:
        act_range = np.arange(ACT_80 + 1, ACT_90 + 1, 1)
        bin_val = 10
    elif ACT_90 < float(score) <= ACT_95:
        act_range = np.arange(ACT_90 + 1, ACT_95 + 1, 1)
        bin_val = 11
    elif ACT_95 < float(score) <= ACT_100:
        act_range = np.arange(ACT_95 + 1, ACT_100 + 1, 1)
        bin_val = 12
    else:
        act_range = 0
        bin_val = "VOID"
    return bin_val


# In[9]:


# GPA RANGE
def gpa_bin(score):
    if score == '0':
        gpa_range = 0
        bin_val = "VOID"
    elif 0 < float(score) < GPA_0:
        gpa_range = np.arange(0, GPA_0 + .1, .1)
        bin_val = "VOID"
    elif GPA_0 <= float(score) <= GPA_10:
        gpa_range = np.arange(GPA_0 + .1, GPA_10 + .1, .1)
        bin_val = 1
    elif GPA_10 < float(score) <= GPA_20:
        gpa_range = np.arange(GPA_10 + .1, GPA_20 + .1, .1)
        bin_val = 2
    elif GPA_20 < float(score) <= GPA_30:
        gpa_range = np.arange(GPA_20 + .1, GPA_30 + .1, .1)
        bin_val = 3
    elif GPA_30 < float(score) <= GPA_40:
        gpa_range = np.arange(GPA_30 + .1, GPA_40 + .1, .1)
        bin_val = 4
    elif GPA_40 < float(score) <= GPA_50:
        gpa_range = np.arange(GPA_40 + .1, GPA_50 + .1, .1)
        bin_val = 5
    elif GPA_50 < float(score) <= GPA_60:
        gpa_range = np.arange(GPA_50 + .1, GPA_60 + .1, .1)
        bin_val = 6
    elif GPA_60 < float(score) <= GPA_70:
        gpa_range = np.arange(GPA_60 + .1, GPA_70 + .1, .1)
        bin_val = 7
    elif GPA_70 < float(score) <= GPA_80:
        gpa_range = np.arange(GPA_70 + .1, GPA_80 + .1, .1)
        bin_val = 8
    elif GPA_80 < float(score) <= GPA_90:
        gpa_range = np.arange(GPA_80 + .1, GPA_90 + .1, .1)
        bin_val = 9
    elif GPA_90 < float(score) <= GPA_100:
        gpa_range = np.arange(GPA_90 + .1, GPA_100 + .1, .1)
        bin_val = 10
    else:
        gpa_range = 0
        bin_val = "VOID"
    return bin_val


# In[10]:


# ACCEPTANCE RATE RANGE

acr_widget = widgets.SelectionSlider(
    options=["Don't Report", '0 - 5%', '6 - 15%', '16 - 35%', '36 - 50%', '51 - 65%', '66 - 75%', '76 - 100%'],
    value="Don't Report",
    description='Choose Acceptance Rate Range: ',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True)


def acceptance_rate_bin(rate):
    if rate == "Don't Report":
        acr_range = 0
        bin_val = "VOID"
    elif rate == '0 - 5%':
        acr_range = np.arange(ACR_0, ACR_1 + 0.01, 0.01)
        bin_val = 1
    elif rate == '6 - 15%':
        acr_range = np.arange(ACR_1 + 0.01, ACR_2 + 0.01 , 0.01)
        bin_val = 2
    elif rate == '16 - 35%':
        acr_range = np.arange(ACR_2 + 0.01, ACR_3 + 0.01 , 0.01)
        bin_val = 3
    elif rate == '36 - 50%':
        acr_range = np.arange(ACR_3 + 0.01, ACR_4 + 0.01 , 0.01)
        bin_val = 4
    elif rate == '51 - 65%':
        acr_range = np.arange(ACR_4 + 0.01, ACR_5 + 0.01, 0.01)
        bin_val = 5
    elif rate == '66 - 75%':
        acr_range = np.arange(ACR_5 + 0.01, ACR_6 + 0.01 , 0.01)
        bin_val = 6
    elif rate == '76 - 100%':
        acr_range = np.arange(ACR_6 + 0.01, ACR_7 + 0.01 , 0.01)
        bin_val = 7
    else:
        acr_range = 0
    return bin_val
        
    


# ## Enrollment Criteria - based of button, selected value 

# In[11]:


# ENROLLMENT SIZE - CAMPUS SIZE

# ENROLLMENT
enroll_widget = widgets.Dropdown(
    options = ["0-100", "101-1000", "1001-1500", "1501-3000", "3001-5000", "5001-8500", "8501-10000", "10001-15000", "15001-25000", "25001-75000"],
    value = "0-100",
    description = 'Choose Enrollment Size: ',
    disabled = False,
    )

def enrollment_bin(val):
    if val == "0-100":
        enr_range = np.arange(0, ENRO_0 + 1, 1)
        bin_val = 1
    elif val == "101-1000":
        enr_range = np.arange(ENRO_0 + 1, ENRO_1 + 1, 1)
        bin_val = 2
    elif val == "1001-1500":
        enr_range = np.arange(ENRO_1 + 1, ENRO_2 + 1, 1)
        bin_val = 3
    elif val == "1501-3000":
        enr_range = np.arange(ENRO_2 + 1, ENRO_3 + 1, 1)
        bin_val = 4
    elif val == "3001-5000":
        enr_range = np.arange(ENRO_3 + 1, ENRO_4 + 1, 1)
        bin_val = 5
    elif val == "5001-8500":
        enr_range = np.arange(ENRO_4 + 1, ENRO_5 + 1, 1)
        bin_val = 6
    elif val == "8501-10000":
        enr_range = np.arange(ENRO_5 + 1, ENRO_6 + 1, 1)
        bin_val = 7
    elif val == "10001-15000":
        enr_range = np.arange(ENRO_6 + 1, ENRO_7 + 1, 1)
        bin_val = 8
    elif val == "15001-25000":
        enr_range = np.arange(ENRO_7 + 1, ENRO_8 + 1, 1)
        bin_val = 9
    elif val == "25001-75000":
        enr_range = np.arange(ENRO_8 + 1, ENRO_9 + 1, 1)
        bin_val = 10
    else:
        enr_range = 0
        bin_val = "VOID"
    return bin_val

# CAMPUS SIZE

campsize_widget = widgets.Dropdown(
    options = ["0-50", "51-2500", "2501-7500", "7501-12500", "12501-25000", "25001-50000", "50001-100000", "100001-200000", "200001-350000", "350001-750000", "750001-1250000", "1250001-8500000"],
    value = "0-50",
    description = 'Choose Campus City Population Size: ',
    disabled = False,
    )

def campsize_bin(val):
    if val == "0-50":
        camp_range = np.arange(0, CITY_1 + 1, 1)
        bin_val = 1
    elif val == "51-2500":
        camp_range = np.arange(CITY_1 + 1, CITY_2 + 1, 1)
        bin_val = 2
    elif val == "2501-7500":
        camp_range = np.arange(CITY_2 + 1, CITY_3 + 1, 1)
        bin_val = 3
    elif val == "7501-12500":
        camp_range = np.arange(CITY_3 + 1, CITY_4 + 1, 1)
        bin_val = 4
    elif val == "12501-25000":
        camp_range = np.arange(CITY_4 + 1, CITY_5 + 1, 1)
        bin_val = 5
    elif val == "25001-50000":
        camp_range = np.arange(CITY_5 + 1, CITY_6 + 1, 1)
        bin_val = 6
    elif val == "50001-100000":
        camp_range = np.arange(CITY_6 + 1, CITY_7 + 1, 1)
        bin_val = 7
    elif val == "100001-200000":
        camp_range = np.arange(CITY_7 + 1, CITY_8 + 1, 1)
        bin_val = 8
    elif val == "200001-350000":
        camp_range = np.arange(CITY_8 + 1, CITY_9 + 1, 1)
        bin_val = 9
    elif val == "350001-750000":
        camp_range = np.arange(CITY_9 + 1, CITY_10 + 1, 1)
        bin_val = 10
    elif val == "750001-1250000":
        camp_range = np.arange(CITY_10 + 1, CITY_11 + 1, 1)
        bin_val = 11
    elif val == "1250001-8500000":
        camp_range = np.arange(CITY_11 + 1, CITY_12 + 1, 1)
        bin_val = 12
    else:
        camp_range = 0
        bin_val = "VOID"
    return bin_val

# URBAN/RURAL/SUBURBAN

setting_widget = widgets.Dropdown(
    options = ["Don't Report", "Urban", "Rural", "Suburban"],
    value = "Don't Report",
    description = 'Choose College Setting: ',
    disabled = False,
    )

def setting_bin(val):
    if val == 'Urban':
        bin_val = 1
    elif val == 'Rural':
        bin_val = 2
    else:
        bin_val = 3
    return bin_val

        


# ## Cost Affordability Criteria - based off button selections for tuition preferences

# In[12]:


# COST/AFFORDABILITY 
check_tuition_widget = widgets.SelectionSlider(
    options = ["In-State", "Out-of-State"],
    value = "In-State",
    description = 'Choose Tuition Option: ',
    disabled = False,
    continuous_update = False,
    oreintation ='horizontal',
    readout=True
    )


def check_tuition(t):
    global ttype
    ttype = 1
    if t == "In-State":
        ttype=1
    elif t=="Out-of-State":
        ttype=2
    return ttype

tuitcost_widget = widgets.SelectionSlider(
    options = ["Don't Report", '0-1500', '1501-5000', '5001-7500', '7501-10000', '10001-15000', '15001-30000', '30001-45000', '45001-55000'],
    value = "Don't Report",
    description = "Choose Tuition Range: ",
    continuous_update = False,
    oreintation = 'horizontal',
    disabled = False
    )
#l = widgets.link(check_tuition_widget, tuitcost_widget)
def tuition_bin(val):
    if val == "Don't Report":
        tuit_range = 0
        bin_val = "VOID"
    elif val == '0-1500':
        tuit_range = np.arange(TUIT_0, TUIT_1 + 1, 1)
        bin_val = 1
    elif val == '15001-5000':
        tuit_range = np.arange(TUIT_1 + 1, TUIT_2 + 1, 1)
        bin_val = 2
    elif val == '5001-7500':
        tuit_range = np.arange(TUIT_2 + 1, TUIT_3 + 1, 1)
        bin_val = 3
    elif val == '7501-10000':
        tuit_range = np.arange(TUIT_3 + 1, TUIT_4 + 1, 1)
        bin_val = 3
    elif val == '10001-15000':
        tuit_range = np.arange(TUIT_4 + 1, TUIT_5 + 1, 1)
        bin_val = 4
    elif val == '15001-30000':
        tuit_range = np.arange(TUIT_5 + 1, TUIT_6 + 1, 1)
        bin_val = 5
    elif val == '30001-45000':
        tuit_range = np.arange(TUIT_6 + 1, TUIT_7 + 1, 1)
        bin_val = 6
    elif val == '45001-55000':
        tuit_range = np.arange(TUIT_7 + 1, TUIT_8 + 1, 1)
        bin_val = 7
    else:
        tuit_range = 0
        bin_val = 8
    return bin_val
        
pnm_widget = widgets.SelectionSlider(
    options = ["Don't Report", '0-25%', '26-50%', '51-60%', '61-70%', '71-80%', '81-90%', '91-100%'],
    value = "Don't Report",
    continuous_update = False,
    description = "Choose Percent Need Met: ",
    disabled = False,
    oreintation = 'horizontal',
    readout=True
    )

def pnm_bin(val):
    if val == "Don't Report":
        pnm_range = 0
        bin_val = "VOID"
    elif val == '0-25%':
        pnm_range = np.arange(PNM_0, PNM_1 + 1, 1)
        bin_val = 1
    elif val == '26-50%':
        pnm_range = np.arange(PNM_1 + 1, PNM_2 + 1, 1)
        bin_val = 2
    elif val == '51-60%':
        pnm_range = np.arange(PNM_2 + 1, PNM_3 + 1, 1)
        bin_val = 3
    elif val == '61-70%':
        pnm_range = np.arange(PNM_3 + 1, PNM_4 + 1, 1)
        bin_val = 4
    elif val == '71-80%':
        pnm_range = np.arange(PNM_4 + 1, PNM_5 + 1, 1)
        bin_val = 5
    elif val == '81-90%':
        pnm_range = np.arange(PNM_5 + 1, PNM_6 + 1, 1)
        bin_val = 6
    elif val == '91-100%':
        pnm_range = np.arange(PNM_6 + 1, PNM_7 + 1, 1)
        bin_val = 7
    else:
        pnm_range = 0
        bin_val = "VOID"
    return bin_val
        
    


# ## Athletic Criteria - based of preferntial division level selection

# In[13]:


# Athletic Selectivity
division_widget = widgets.Dropdown(
    options = ["Don't Report", "NCAA Division I", "NCAA Division II", "NCAA Division III", "NAIA", "NJCAA"],
    value = "Don't Report",
    description = "Choose Preferred Division: ",
    disabled=False
    )
def division_bin(div):
    if div == "Don't Report":
        val = 0
    elif div == "NCAA Division I":
        val = 1
    elif div == "NCAA Division II":
        val = 3
    elif div == "NCAA Division III":
        val = 2
    elif div == "NAIA":
        val = 4
    elif div == "NJCAA":
        val = 5
    else:
        val = 0
    return val


# # Organizing Schools into according bins - iteration over database

# In[14]:


import pandas as pd
import os
# from google.colab import files
import io
os.getcwd()


# To download the college data, use this CSV: https://drive.google.com/file/d/1natIQ0hHeRRsl8MM0u78moYefkp3g_Gq/view?usp=sharing.
# 
# The CSV contains all of the data from the Excel's college database without the formatting (percent signs, etc)

# In[15]:


# uploaded = files.upload()
# college_database = pd.read_csv(io.BytesIO(uploaded['college_5282021.csv']), error_bad_lines=False)

#Code used with Jupyter Notebook:
#college_database = pd.read_csv(r'/Users/aaronangeles/Desktop/IMRecruitableFILES/IMRCOLLEGEDATA.csv', encoding = 'latin-1')
college_database = pd.read_excel('college_5282021.xlsx')


# In[16]:


#Show database
college_dat = pd.DataFrame(college_database)
print(college_dat)


# ## Academic Selecitvity Organization of Schools into Bins based on Constant percentiles

# In[17]:


# ACADEMIC SELECTIVITY BINS

# AVG SAT ------------------------------------------------------------------------------------------------

cd_sat = pd.DataFrame(college_dat, columns = ['name', 'avg_sat_1'])

sat_schools_na = []
sat_schools_1 = []
sat_schools_2 = []
sat_schools_3 = []
sat_schools_4 = []
sat_schools_5 = []
sat_schools_6 = []
sat_schools_7 = []
sat_schools_8 = []
sat_schools_9 = []
sat_schools_10 = []
sat_schools_11 = []


for ind in cd_sat.index:
    if str(cd_sat['avg_sat_1'][ind]).isnumeric() == False:
        sat_schools_na.append(cd_sat['name'][ind])
    elif SAT_10 >= float(cd_sat['avg_sat_1'][ind]) >= SAT_0:
        sat_schools_1.append(cd_sat['name'][ind])
    elif SAT_20 >= float(cd_sat['avg_sat_1'][ind]) > SAT_10:
        sat_schools_2.append(cd_sat['name'][ind])
    elif SAT_30 >= float(cd_sat['avg_sat_1'][ind]) > SAT_20:
        sat_schools_3.append(cd_sat['name'][ind])
    elif SAT_40 >= float(cd_sat['avg_sat_1'][ind]) > SAT_30:
        sat_schools_4.append(cd_sat['name'][ind])
    elif SAT_50 >= float(cd_sat['avg_sat_1'][ind]) > SAT_40:
        sat_schools_5.append(cd_sat['name'][ind])
    elif SAT_60 >= float(cd_sat['avg_sat_1'][ind]) > SAT_50:
        sat_schools_6.append(cd_sat['name'][ind])
    elif SAT_70 >= float(cd_sat['avg_sat_1'][ind]) > SAT_60:
        sat_schools_7.append(cd_sat['name'][ind])
    elif SAT_80 >= float(cd_sat['avg_sat_1'][ind]) > SAT_70:
        sat_schools_8.append(cd_sat['name'][ind])
    elif SAT_90 >= float(cd_sat['avg_sat_1'][ind]) > SAT_80:
        sat_schools_9.append(cd_sat['name'][ind])
    elif SAT_95 >= float(cd_sat['avg_sat_1'][ind]) > SAT_90:
        sat_schools_10.append(cd_sat['name'][ind])
    elif SAT_100 >= float(cd_sat['avg_sat_1'][ind]) > SAT_95:
        sat_schools_11.append(cd_sat['name'][ind])
    else:
        sat_schools_na.append(cd_sat['name'][ind])

d_sat_schools_na = dict(zip(sat_schools_na, ["VOID"] * len(sat_schools_na)))
d_sat_schools_1 = dict(zip(sat_schools_1, [1] * len(sat_schools_1)))
d_sat_schools_2 = dict(zip(sat_schools_2, [2] * len(sat_schools_2)))
d_sat_schools_3 = dict(zip(sat_schools_3, [3] * len(sat_schools_3)))
d_sat_schools_4 = dict(zip(sat_schools_4, [4] * len(sat_schools_4)))
d_sat_schools_5 = dict(zip(sat_schools_5, [5] * len(sat_schools_5)))
d_sat_schools_6 = dict(zip(sat_schools_6, [6] * len(sat_schools_6)))
d_sat_schools_7 = dict(zip(sat_schools_7, [7] * len(sat_schools_7)))
d_sat_schools_8 = dict(zip(sat_schools_8, [8] * len(sat_schools_8)))
d_sat_schools_9 = dict(zip(sat_schools_9, [9] * len(sat_schools_9)))
d_sat_schools_10 = dict(zip(sat_schools_10, [10] * len(sat_schools_10)))
d_sat_schools_11 = dict(zip(sat_schools_11, [11] * len(sat_schools_11)))

dict_sat_schools = {**d_sat_schools_na, **d_sat_schools_1, **d_sat_schools_2, 
                    **d_sat_schools_3, **d_sat_schools_4, **d_sat_schools_5, **d_sat_schools_6, 
                    **d_sat_schools_7, **d_sat_schools_8, **d_sat_schools_9, **d_sat_schools_10, 
                    **d_sat_schools_11}


# In[18]:


# AVG ACT -------------------------------------------------------------------------------------------------------

cd_act = pd.DataFrame(college_dat, columns = ['name', 'avg_act_comp'])

act_schools_na = []
act_schools_1 = []
act_schools_2 = []
act_schools_3 = []
act_schools_4 = []
act_schools_5 = []
act_schools_6 = []
act_schools_7 = []
act_schools_8 = []
act_schools_9 = []
act_schools_10 = []
act_schools_11 = []
act_schools_12 = []


for ind in cd_act.index:
    if str(cd_act['avg_act_comp'][ind]).isnumeric() == False:
        act_schools_na.append(cd_act['name'][ind])
    elif ACT_0 >= float(cd_act['avg_act_comp'][ind]) >= ACT_NA:
        act_schools_2.append(cd_act['name'][ind])   
    elif ACT_10 >= float(cd_act['avg_act_comp'][ind]) > ACT_0:
        act_schools_2.append(cd_act['name'][ind])
    elif ACT_20 >= float(cd_act['avg_act_comp'][ind]) > ACT_10:
        act_schools_3.append(cd_act['name'][ind])
    elif ACT_30 >= float(cd_act['avg_act_comp'][ind]) > ACT_20:
        act_schools_4.append(cd_act['name'][ind])
    elif ACT_40 >= float(cd_act['avg_act_comp'][ind]) > ACT_30:
        act_schools_5.append(cd_act['name'][ind])
    elif ACT_50 >= float(cd_act['avg_act_comp'][ind]) > ACT_40:
        act_schools_6.append(cd_act['name'][ind])
    elif ACT_60 >= float(cd_act['avg_act_comp'][ind]) > ACT_50:
        act_schools_7.append(cd_act['name'][ind])
    elif ACT_70 >= float(cd_act['avg_act_comp'][ind]) > ACT_60:
        act_schools_8.append(cd_act['name'][ind])
    elif ACT_80 >= float(cd_act['avg_act_comp'][ind]) > ACT_70:
        act_schools_9.append(cd_act['name'][ind])
    elif ACT_90 >= float(cd_act['avg_act_comp'][ind]) > ACT_80:
        act_schools_10.append(cd_act['name'][ind])
    elif ACT_95 >= float(cd_act['avg_act_comp'][ind]) > ACT_90:
        act_schools_11.append(cd_act['name'][ind])
    elif ACT_100 >= float(cd_act['avg_act_comp'][ind]) > ACT_95:
        act_schools_12.append(cd_act['name'][ind])
    else:
        act_schools_na.append(cd_act['name'][ind])
        
d_act_schools_na = dict(zip(act_schools_na, ["VOID"] * len(act_schools_na)))
d_act_schools_1 = dict(zip(act_schools_1, [1] * len(act_schools_1)))
d_act_schools_2 = dict(zip(act_schools_2, [2] * len(act_schools_2)))
d_act_schools_3 = dict(zip(act_schools_3, [3] * len(act_schools_3)))
d_act_schools_4 = dict(zip(act_schools_4, [4] * len(act_schools_4)))
d_act_schools_5 = dict(zip(act_schools_5, [5] * len(act_schools_5)))
d_act_schools_6 = dict(zip(act_schools_6, [6] * len(act_schools_6)))
d_act_schools_7 = dict(zip(act_schools_7, [7] * len(act_schools_7)))
d_act_schools_8 = dict(zip(act_schools_8, [8] * len(act_schools_8)))
d_act_schools_9 = dict(zip(act_schools_9, [9] * len(act_schools_9)))
d_act_schools_10 = dict(zip(act_schools_10, [10] * len(act_schools_10)))
d_act_schools_11 = dict(zip(act_schools_11, [11] * len(act_schools_11)))
d_act_schools_12 = dict(zip(act_schools_11, [12] * len(act_schools_12)))

dict_act_schools = {**d_act_schools_na, **d_act_schools_1, **d_act_schools_2, **d_act_schools_3, **d_act_schools_4,
                    **d_act_schools_5, **d_act_schools_6, **d_act_schools_7, **d_act_schools_8,
                    **d_act_schools_9, **d_act_schools_10, **d_act_schools_11, **d_act_schools_12}


# In[19]:


# GPA ------------------------------------------------------------------------------------------------------
cd_gpa = pd.DataFrame(college_dat, columns = ['name', 'avg_fresh_gpa'])

gpa_schools_na = []
gpa_schools_1 = []
gpa_schools_2 = []
gpa_schools_3 = []
gpa_schools_4 = []
gpa_schools_5 = []
gpa_schools_6 = []
gpa_schools_7 = []
gpa_schools_8 = []
gpa_schools_9 = []
gpa_schools_10 = []


for ind in cd_gpa.index:
    if str(cd_gpa['avg_fresh_gpa'][ind]).isnumeric() == False:
        gpa_schools_na.append(cd_gpa['name'][ind])
    elif GPA_10 >= float(cd_gpa['avg_fresh_gpa'][ind]) >= GPA_0:
        gpa_schools_1.append(cd_gpa['name'][ind])
    elif GPA_20 >= float(cd_gpa['avg_fresh_gpa'][ind]) > GPA_10:
        gpa_schools_2.append(cd_gpa['name'][ind])
    elif GPA_30 >= float(cd_gpa['avg_fresh_gpa'][ind]) > GPA_20:
        gpa_schools_3.append(cd_gpa['name'][ind])
    elif GPA_40 >= float(cd_gpa['avg_fresh_gpa'][ind]) > GPA_30:
        gpa_schools_4.append(cd_gpa['name'][ind])
    elif GPA_50 >= float(cd_gpa['avg_fresh_gpa'][ind]) > GPA_40:
        gpa_schools_5.append(cd_gpa['name'][ind])
    elif GPA_60 >= float(cd_gpa['avg_fresh_gpa'][ind]) > GPA_50:
        gpa_schools_6.append(cd_gpa['name'][ind])
    elif GPA_70 >= float(cd_gpa['avg_fresh_gpa'][ind]) > GPA_60:
        gpa_schools_7.append(cd_gpa['name'][ind])
    elif GPA_80 >= float(cd_gpa['avg_fresh_gpa'][ind]) > GPA_70:
        gpa_schools_8.append(cd_gpa['name'][ind])
    elif GPA_90 >= float(cd_gpa['avg_fresh_gpa'][ind]) > GPA_80:
        gpa_schools_9.append(cd_gpa['name'][ind])
    elif GPA_100 >= float(cd_gpa['avg_fresh_gpa'][ind]) > GPA_90:
        gpa_schools_10.append(cd_gpa['name'][ind])
    else:
        gpa_schools_na.append(cd_gpa['name'][ind])
        
d_gpa_schools_na = dict(zip(gpa_schools_na, ["VOID"] * len(gpa_schools_na)))
d_gpa_schools_1 = dict(zip(gpa_schools_1, [1] * len(gpa_schools_1)))
d_gpa_schools_2 = dict(zip(gpa_schools_2, [2] * len(gpa_schools_2)))
d_gpa_schools_3 = dict(zip(gpa_schools_3, [3] * len(gpa_schools_3)))
d_gpa_schools_4 = dict(zip(gpa_schools_4, [4] * len(gpa_schools_4)))
d_gpa_schools_5 = dict(zip(gpa_schools_5, [5] * len(gpa_schools_5)))
d_gpa_schools_6 = dict(zip(gpa_schools_6, [6] * len(gpa_schools_6)))
d_gpa_schools_7 = dict(zip(gpa_schools_7, [7] * len(gpa_schools_7)))
d_gpa_schools_8 = dict(zip(gpa_schools_8, [8] * len(gpa_schools_8)))
d_gpa_schools_9 = dict(zip(gpa_schools_9, [9] * len(gpa_schools_9)))
d_gpa_schools_10 = dict(zip(gpa_schools_10, [10] * len(gpa_schools_10)))

dict_gpa_schools = {**d_gpa_schools_na, **d_gpa_schools_1, **d_gpa_schools_2, **d_gpa_schools_3, **d_gpa_schools_4,
                    **d_gpa_schools_5, **d_gpa_schools_6, **d_gpa_schools_7, **d_gpa_schools_8,
                    **d_gpa_schools_9, **d_gpa_schools_10}


# In[20]:


# Acceptance Rate  ------------------------------------------------------------------------------------------------------
cd_acceptrate = pd.DataFrame(college_dat, columns = ['name', 'accept_rate'])

acceptrate_schools_na = []
acceptrate_schools_1 = []
acceptrate_schools_2 = []
acceptrate_schools_3 = []
acceptrate_schools_4 = []
acceptrate_schools_5 = []
acceptrate_schools_6 = []
acceptrate_schools_7 = []


for ind in cd_acceptrate.index:
    if cd_acceptrate['accept_rate'][ind] == 'N/A':
        acceptrate_schools_na.append(cd_acceptrate['name'][ind])
    if cd_acceptrate['accept_rate'][ind] == 'Not Listed':
        acceptrate_schools_na.append(cd_acceptrate['name'][ind])
    if cd_acceptrate['accept_rate'][ind] == 'not reported':
        acceptrate_schools_na.append(cd_acceptrate['name'][ind])
    elif ACR_1 >= float(cd_acceptrate['accept_rate'][ind]) >= ACR_0:
        acceptrate_schools_1.append(cd_acceptrate['name'][ind])
    elif ACR_2 >= float(cd_acceptrate['accept_rate'][ind]) > ACR_1:
        acceptrate_schools_2.append(cd_acceptrate['name'][ind])
    elif ACR_3 >= float(cd_acceptrate['accept_rate'][ind]) > ACR_2:
        acceptrate_schools_3.append(cd_acceptrate['name'][ind])
    elif ACR_4 >= float(cd_acceptrate['accept_rate'][ind]) > ACR_3:
        acceptrate_schools_4.append(cd_acceptrate['name'][ind])
    elif ACR_5 >= float(cd_acceptrate['accept_rate'][ind]) > ACR_4:
        acceptrate_schools_5.append(cd_acceptrate['name'][ind])
    elif ACR_6 >= float(cd_acceptrate['accept_rate'][ind]) > ACR_5:
        acceptrate_schools_6.append(cd_acceptrate['name'][ind])
    elif ACR_7 >= float(cd_acceptrate['accept_rate'][ind]) > ACR_6:
        acceptrate_schools_7.append(cd_acceptrate['name'][ind])
    else:
        acceptrate_schools_na.append(cd_acceptrate['name'][ind])
        
d_acceptrate_schools_na = dict(zip(acceptrate_schools_na, ["VOID"] * len(acceptrate_schools_na)))
d_acceptrate_schools_1 = dict(zip(acceptrate_schools_1, [1] * len(acceptrate_schools_1)))
d_acceptrate_schools_2 = dict(zip(acceptrate_schools_2, [2] * len(acceptrate_schools_2)))
d_acceptrate_schools_3 = dict(zip(acceptrate_schools_3, [3] * len(acceptrate_schools_3)))
d_acceptrate_schools_4 = dict(zip(acceptrate_schools_4, [4] * len(acceptrate_schools_4)))
d_acceptrate_schools_5 = dict(zip(acceptrate_schools_5, [5] * len(acceptrate_schools_5)))
d_acceptrate_schools_6 = dict(zip(acceptrate_schools_6, [6] * len(acceptrate_schools_6)))
d_acceptrate_schools_7 = dict(zip(acceptrate_schools_7, [7] * len(acceptrate_schools_7)))

dict_acceptrate_schools = {**d_acceptrate_schools_na, **d_acceptrate_schools_1, **d_acceptrate_schools_2, **d_acceptrate_schools_3, **d_acceptrate_schools_4,
                    **d_acceptrate_schools_5, **d_acceptrate_schools_6, **d_acceptrate_schools_7}


# ## Enrollment Criteria Organization based on Percentile Bin Constant Values

# In[21]:


# ENROLLMENT/SIZE -----------------------------------------------------------------------------------------------
cd_enroll = pd.DataFrame(college_dat, columns = ['name', 'college_enrollment'])

enroll_schools_na = []
enroll_schools_1 = []
enroll_schools_2 = []
enroll_schools_3 = []
enroll_schools_4 = []
enroll_schools_5 = []
enroll_schools_6 = []
enroll_schools_7 = []
enroll_schools_8 = []
enroll_schools_9 = []
enroll_schools_10 = []

for ind in cd_enroll.index:
    if str(cd_enroll['college_enrollment'][ind]).isnumeric() == False:
        enroll_schools_na.append(cd_enroll['name'][ind])
#     elif cd_enroll['college_enrollment'][ind] == 'per credit hour':
#         enroll_schools_na.append(cd_enroll['name'][ind])
    elif ENRO_0 >= float(cd_enroll['college_enrollment'][ind]) >= 0:
        enroll_schools_1.append(cd_enroll['name'][ind])
    elif ENRO_1 >= float(cd_enroll['college_enrollment'][ind]) > ENRO_0:
        enroll_schools_2.append(cd_enroll['name'][ind])
    elif ENRO_2 >= float(cd_enroll['college_enrollment'][ind]) > ENRO_1:
        enroll_schools_3.append(cd_enroll['name'][ind])
    elif ENRO_3 >= float(cd_enroll['college_enrollment'][ind]) > ENRO_2:
        enroll_schools_4.append(cd_enroll['name'][ind])
    elif ENRO_4 >= float(cd_enroll['college_enrollment'][ind]) > ENRO_3:
        enroll_schools_5.append(cd_enroll['name'][ind])
    elif ENRO_5 >= float(cd_enroll['college_enrollment'][ind]) > ENRO_4:
        enroll_schools_6.append(cd_enroll['name'][ind])
    elif ENRO_6 >= float(cd_enroll['college_enrollment'][ind]) > ENRO_5:
        enroll_schools_7.append(cd_enroll['name'][ind])
    elif ENRO_7 >= float(cd_enroll['college_enrollment'][ind]) > ENRO_6:
        enroll_schools_8.append(cd_enroll['name'][ind])
    elif ENRO_8 >= float(cd_enroll['college_enrollment'][ind]) > ENRO_7:
        enroll_schools_9.append(cd_enroll['name'][ind])
    elif ENRO_9 >= float(cd_enroll['college_enrollment'][ind]) > ENRO_8:
        enroll_schools_10.append(cd_enroll['name'][ind])
    else:
        enroll_schools_na.append(cd_enroll['name'][ind])

d_enroll_schools_na = dict(zip(enroll_schools_na, ["VOID"] * len(enroll_schools_na)))
d_enroll_schools_1 = dict(zip(enroll_schools_1, [1] * len(enroll_schools_1)))
d_enroll_schools_2 = dict(zip(enroll_schools_2, [2] * len(enroll_schools_2)))
d_enroll_schools_3 = dict(zip(enroll_schools_3, [3] * len(enroll_schools_3)))
d_enroll_schools_4 = dict(zip(enroll_schools_4, [4] * len(enroll_schools_4)))
d_enroll_schools_5 = dict(zip(enroll_schools_5, [5] * len(enroll_schools_5)))
d_enroll_schools_6 = dict(zip(enroll_schools_6, [6] * len(enroll_schools_6)))
d_enroll_schools_7 = dict(zip(enroll_schools_7, [7] * len(enroll_schools_7)))
d_enroll_schools_8 = dict(zip(enroll_schools_8, [8] * len(enroll_schools_8)))
d_enroll_schools_9 = dict(zip(enroll_schools_9, [9] * len(enroll_schools_9)))
d_enroll_schools_10 = dict(zip(enroll_schools_10, [10] * len(enroll_schools_10)))

dict_enroll_schools = {**d_enroll_schools_na, **d_enroll_schools_1, **d_enroll_schools_2, **d_enroll_schools_3, **d_enroll_schools_4,
                    **d_enroll_schools_5, **d_enroll_schools_6, **d_enroll_schools_7, **d_enroll_schools_8,
                    **d_enroll_schools_9, **d_enroll_schools_10}

# CAMPUS SIZE/POPULATION ----------------------------------------------------------------------------------------
cd_campsize = pd.DataFrame(college_dat, columns = ['name', 'population'])

campsize_schools_na = []
campsize_schools_1 = []
campsize_schools_2 = []
campsize_schools_3 = []
campsize_schools_4 = []
campsize_schools_5 = []
campsize_schools_6 = []
campsize_schools_7 = []
campsize_schools_8 = []
campsize_schools_9 = []
campsize_schools_10 = []
campsize_schools_11 = []
campsize_schools_12 = []


for ind in cd_campsize.index:
    current_pop = str(cd_campsize['population'][ind]).replace(',', '').replace(' ', '')
    current_name = cd_campsize['name'][ind]
    
    if cd_campsize['population'][ind] == 'N/A':
        campsize_schools_na.append(cd_campsize['name'][ind])
    elif CITY_1 >= float(current_pop) > 0:
        campsize_schools_1.append(cd_campsize['name'][ind])
    elif CITY_2 >= float(current_pop) > CITY_1:
        campsize_schools_2.append(cd_campsize['name'][ind])
    elif CITY_3 >= float(current_pop) > CITY_2:
        campsize_schools_3.append(cd_campsize['name'][ind])
    elif CITY_4 >= float(current_pop) > CITY_3:
        campsize_schools_4.append(cd_campsize['name'][ind])
    elif CITY_5 >= float(current_pop) > CITY_4:
        campsize_schools_5.append(cd_campsize['name'][ind])
    elif CITY_6 >= float(current_pop) > CITY_5:
        campsize_schools_6.append(cd_campsize['name'][ind])
    elif CITY_7 >= float(current_pop) > CITY_6:
        campsize_schools_7.append(cd_campsize['name'][ind])
    elif CITY_8 >= float(current_pop) > CITY_7:
        campsize_schools_8.append(cd_campsize['name'][ind])
    elif CITY_9 >= float(current_pop) > CITY_8:
        campsize_schools_9.append(cd_campsize['name'][ind])
    elif CITY_10 >= float(current_pop) > CITY_9:
        campsize_schools_10.append(cd_campsize['name'][ind])
    elif CITY_11 >= float(current_pop) > CITY_10:
        campsize_schools_11.append(cd_campsize['name'][ind])
    elif CITY_12 >= float(current_pop) > CITY_11:
        campsize_schools_12.append(cd_campsize['name'][ind])
    else:
        campsize_schools_na.append(cd_campsize['name'][ind])
        
d_campsize_schools_na = dict(zip(campsize_schools_na, ["VOID"] * len(campsize_schools_na)))
d_campsize_schools_1 = dict(zip(campsize_schools_1, [1] * len(campsize_schools_1)))
d_campsize_schools_2 = dict(zip(campsize_schools_2, [2] * len(campsize_schools_2)))
d_campsize_schools_3 = dict(zip(campsize_schools_3, [3] * len(campsize_schools_3)))
d_campsize_schools_4 = dict(zip(campsize_schools_4, [4] * len(campsize_schools_4)))
d_campsize_schools_5 = dict(zip(campsize_schools_5, [5] * len(campsize_schools_5)))
d_campsize_schools_6 = dict(zip(campsize_schools_6, [6] * len(campsize_schools_6)))
d_campsize_schools_7 = dict(zip(campsize_schools_7, [7] * len(campsize_schools_7)))
d_campsize_schools_8 = dict(zip(campsize_schools_8, [8] * len(campsize_schools_8)))
d_campsize_schools_9 = dict(zip(campsize_schools_9, [9] * len(campsize_schools_9)))
d_campsize_schools_10 = dict(zip(campsize_schools_10, [10] * len(campsize_schools_10)))
d_campsize_schools_11 = dict(zip(campsize_schools_11, [11] * len(campsize_schools_11)))
d_campsize_schools_12 = dict(zip(campsize_schools_12, [12] * len(campsize_schools_12)))

dict_campsize_schools = {**d_campsize_schools_na, **d_campsize_schools_1, **d_campsize_schools_2, **d_campsize_schools_3, **d_campsize_schools_4,
                    **d_campsize_schools_5, **d_campsize_schools_6, **d_campsize_schools_7, **d_campsize_schools_8,
                    **d_campsize_schools_9, **d_campsize_schools_10, **d_campsize_schools_11, **d_campsize_schools_12}


# In[22]:


cd_setting = pd.DataFrame(college_dat, columns = ['name', 'setting'])

setting_schools_na = []
setting_schools_1 = []
setting_schools_2 = []
setting_schools_3 = []

for ind in cd_setting.index:
    current_setting = str(cd_setting['setting'][ind]).replace(',', '').replace(' ', '')
    current_name = cd_setting['name'][ind]
    
    if cd_setting['setting'][ind] == 'Unknown':
        setting_schools_na.append(cd_setting['name'][ind])
    elif current_setting == 'Urban':
        setting_schools_1.append(cd_setting['name'][ind])
    elif current_setting == 'Rural':
        setting_schools_2.append(cd_setting['name'][ind])
    elif current_setting == 'Suburban':
        setting_schools_3.append(cd_setting['name'][ind])
    else:
        setting_schools_na.append(cd_setting['name'][ind])
        
d_setting_schools_na = dict(zip(setting_schools_na, ["VOID"] * len(setting_schools_na)))
d_setting_schools_1 = dict(zip(setting_schools_1, [1] * len(setting_schools_1)))
d_setting_schools_2 = dict(zip(setting_schools_2, [2] * len(setting_schools_2)))
d_setting_schools_3 = dict(zip(setting_schools_3, [3] * len(setting_schools_3)))

dict_setting_schools = {**d_setting_schools_na, **d_setting_schools_1, **d_setting_schools_2, **d_setting_schools_3}


# In[23]:


cd_state = pd.DataFrame(college_dat, columns = ['name', 'state'])

state_schools = []
states = []

for ind in cd_state.index:
    current_state = str(cd_state['state'][ind]).replace(',', '').replace(' ', '')
    current_name = cd_state['name'][ind]

    state_schools.append(cd_state['name'][ind])
    states.append(current_state)
        
dict_state_schools = dict(zip(state_schools, states))


# ## Cost and Affordability Organization based of percentile bin constants

# In[24]:


# COST/AFFORDABILITY BINS

# Percent Need Met ------------------------------------------------------------------------------------------------
cd_pnm = pd.DataFrame(college_dat, columns = ['name', 'perc_stud_met'])

pnm_na = []
pnm_schools_1 = []
pnm_schools_2 = []
pnm_schools_3 = []
pnm_schools_4 = []
pnm_schools_5 = []
pnm_schools_6 = []
pnm_schools_7 = []
for ind in cd_pnm.index:
    if str(cd_pnm['perc_stud_met'][ind]).isnumeric() == False:
        pnm_na.append(cd_pnm['name'][ind])
    elif PNM_1 >= float(cd_pnm['perc_stud_met'][ind]) >= PNM_0:
        pnm_schools_1.append(cd_pnm['name'][ind])
    elif PNM_2 >= float(cd_pnm['perc_stud_met'][ind]) > PNM_1:
        pnm_schools_2.append(cd_pnm['name'][ind])
    elif PNM_3 >= float(cd_pnm['perc_stud_met'][ind]) > PNM_2:
        pnm_schools_3.append(cd_pnm['name'][ind])
    elif PNM_4 >= float(cd_pnm['perc_stud_met'][ind]) > PNM_3:
        pnm_schools_4.append(cd_pnm['name'][ind])
    elif PNM_5 >= float(cd_pnm['perc_stud_met'][ind]) > PNM_4:
        pnm_schools_5.append(cd_pnm['name'][ind])
    elif PNM_6 >= float(cd_pnm['perc_stud_met'][ind]) > PNM_5:
        pnm_schools_6.append(cd_pnm['name'][ind])
    elif PNM_7 >= float(cd_pnm['perc_stud_met'][ind]) > PNM_6:
        pnm_schools_7.append(cd_pnm['name'][ind])
    else:
        pnm_na.append(cd_pnm['name'][ind])

d_pnm_schools_na = dict(zip(pnm_na, ["VOID"] * len(pnm_na)))
d_pnm_schools_1 = dict(zip(pnm_schools_1, [1] * len(pnm_schools_1)))
d_pnm_schools_2 = dict(zip(pnm_schools_2, [2] * len(pnm_schools_2)))
d_pnm_schools_3 = dict(zip(pnm_schools_3, [3] * len(pnm_schools_3)))
d_pnm_schools_4 = dict(zip(pnm_schools_4, [4] * len(pnm_schools_4)))
d_pnm_schools_5 = dict(zip(pnm_schools_5, [5] * len(pnm_schools_5)))
d_pnm_schools_6 = dict(zip(pnm_schools_6, [6] * len(pnm_schools_6)))
d_pnm_schools_7 = dict(zip(pnm_schools_7, [7] * len(pnm_schools_7)))

dict_pnm_schools = {**d_pnm_schools_na, **d_pnm_schools_1, **d_pnm_schools_2, **d_pnm_schools_3, **d_pnm_schools_4,
                    **d_pnm_schools_5, **d_pnm_schools_6, **d_pnm_schools_7}

# Tuition -----------------------------------------------------------------------------------------------------

cd_tuit_in = pd.DataFrame(college_dat, columns = ['name', 'tuition_in'])

tuit_schools_inna = []
tuit_schools_in1 = []
tuit_schools_in2 = []
tuit_schools_in3 = []
tuit_schools_in4 = []
tuit_schools_in5 = []
tuit_schools_in6 = []
tuit_schools_in7 = []
tuit_schools_in8 = []

for ind in cd_tuit_in.index:
    if str(cd_tuit_in['tuition_in'][ind]).isnumeric() == False:
        tuit_schools_inna.append(cd_tuit_in['name'][ind])
#     elif cd_tuit_in['tuition_in'][ind] == 'per credit hour':
#         tuit_schools_inna.append(cd_tuit_in['name'][ind])
    elif TUIT_1 >= int(cd_tuit_in['tuition_in'][ind]) >= TUIT_0:
        tuit_schools_in1.append(cd_tuit_in['name'][ind])
    elif TUIT_2 >= int(cd_tuit_in['tuition_in'][ind]) > TUIT_1:
        tuit_schools_in2.append(cd_tuit_in['name'][ind])
    elif TUIT_3 >= int(cd_tuit_in['tuition_in'][ind]) > TUIT_2:
        tuit_schools_in3.append(cd_tuit_in['name'][ind])
    elif TUIT_4 >= int(cd_tuit_in['tuition_in'][ind]) > TUIT_3:
        tuit_schools_in4.append(cd_tuit_in['name'][ind])
    elif TUIT_5 >= int(cd_tuit_in['tuition_in'][ind]) > TUIT_4:
        tuit_schools_in5.append(cd_tuit_in['name'][ind])
    elif TUIT_6 >= int(cd_tuit_in['tuition_in'][ind]) > TUIT_5:
        tuit_schools_in6.append(cd_tuit_in['name'][ind])
    elif TUIT_7 >= int(cd_tuit_in['tuition_in'][ind]) > TUIT_6:
        tuit_schools_in7.append(cd_tuit_in['name'][ind])
    elif TUIT_8 >= int(cd_tuit_in['tuition_in'][ind]) > TUIT_7:
        tuit_schools_in8.append(cd_tuit_in['name'][ind])
    else:
        tuit_schools_inna.append(cd_tuit_in['name'][ind])
        
d_tuit_schools_inna = dict(zip(tuit_schools_inna, ["VOID"] * len(tuit_schools_inna)))
d_tuit_schools_in1 = dict(zip(tuit_schools_in1, [1] * len(tuit_schools_in1)))
d_tuit_schools_in2 = dict(zip(tuit_schools_in2, [2] * len(tuit_schools_in2)))
d_tuit_schools_in3 = dict(zip(tuit_schools_in3, [3] * len(tuit_schools_in3)))
d_tuit_schools_in4 = dict(zip(tuit_schools_in4, [4] * len(tuit_schools_in4)))
d_tuit_schools_in5 = dict(zip(tuit_schools_in5, [5] * len(tuit_schools_in5)))
d_tuit_schools_in6 = dict(zip(tuit_schools_in6, [6] * len(tuit_schools_in6)))
d_tuit_schools_in7 = dict(zip(tuit_schools_in7, [7] * len(tuit_schools_in7)))
d_tuit_schools_in8 = dict(zip(tuit_schools_in8, [8] * len(tuit_schools_in8)))

dict_tuit_schools_in = {**d_tuit_schools_inna, **d_tuit_schools_in1, **d_tuit_schools_in2, **d_tuit_schools_in3, **d_tuit_schools_in4,
                    **d_tuit_schools_in5, **d_tuit_schools_in6, **d_tuit_schools_in7, **d_tuit_schools_in8}


cd_tuit_out = pd.DataFrame(college_dat, columns = ['name', 'tuition_out'])

tuit_schools_outna = []
tuit_schools_out1 = []
tuit_schools_out2 = []
tuit_schools_out3 = []
tuit_schools_out4 = []
tuit_schools_out5 = []
tuit_schools_out6 = []
tuit_schools_out7 = []
tuit_schools_out8 = []

for ind in cd_tuit_out.index:
    if str(cd_tuit_out['tuition_out'][ind]).isnumeric() == False:
        tuit_schools_outna.append(cd_tuit_out['name'][ind])
#     elif cd_tuit_out['tuition_out'][ind] == 'per credit hour':
#         tuit_schools_outna.append(cd_tuit_out['name'][ind])
    elif TUIT_1 >= int(cd_tuit_out['tuition_out'][ind]) >= TUIT_0:
        tuit_schools_out1.append(cd_tuit_out['name'][ind])
    elif TUIT_2 >= int(cd_tuit_out['tuition_out'][ind]) > TUIT_1:
        tuit_schools_out2.append(cd_tuit_out['name'][ind])
    elif TUIT_3 >= int(cd_tuit_out['tuition_out'][ind]) > TUIT_2:
        tuit_schools_out3.append(cd_tuit_out['name'][ind])
    elif TUIT_4 >= int(cd_tuit_out['tuition_out'][ind]) > TUIT_3:
        tuit_schools_out4.append(cd_tuit_out['name'][ind])
    elif TUIT_5 >= int(cd_tuit_out['tuition_out'][ind]) > TUIT_4:
        tuit_schools_out5.append(cd_tuit_out['name'][ind])
    elif TUIT_6 >= int(cd_tuit_out['tuition_out'][ind]) > TUIT_5:
        tuit_schools_out6.append(cd_tuit_out['name'][ind])
    elif TUIT_7 >= int(cd_tuit_out['tuition_out'][ind]) > TUIT_6:
        tuit_schools_out7.append(cd_tuit_out['name'][ind])
    elif TUIT_8 >= int(cd_tuit_out['tuition_out'][ind]) > TUIT_7:
        tuit_schools_out8.append(cd_tuit_out['name'][ind])
    else:
        tuit_schools_outna.append(cd_tuit_out['name'][ind])

d_tuit_schools_outna = dict(zip(tuit_schools_outna, ["VOID"] * len(tuit_schools_outna)))
d_tuit_schools_out1 = dict(zip(tuit_schools_out1, [1] * len(tuit_schools_out1)))
d_tuit_schools_out2 = dict(zip(tuit_schools_out2, [2] * len(tuit_schools_out2)))
d_tuit_schools_out3 = dict(zip(tuit_schools_out3, [3] * len(tuit_schools_out3)))
d_tuit_schools_out4 = dict(zip(tuit_schools_out4, [4] * len(tuit_schools_out4)))
d_tuit_schools_out5 = dict(zip(tuit_schools_out5, [5] * len(tuit_schools_out5)))
d_tuit_schools_out6 = dict(zip(tuit_schools_out6, [6] * len(tuit_schools_out6)))
d_tuit_schools_out7 = dict(zip(tuit_schools_out7, [7] * len(tuit_schools_out7)))
d_tuit_schools_out8 = dict(zip(tuit_schools_out8, [8] * len(tuit_schools_out8)))

dict_tuit_schools_out = {**d_tuit_schools_outna, **d_tuit_schools_out1, **d_tuit_schools_out2, **d_tuit_schools_out3, **d_tuit_schools_out4,
                    **d_tuit_schools_out5, **d_tuit_schools_out6, **d_tuit_schools_out7, **d_tuit_schools_out8}


# In[ ]:





# ## Major Selectivity Organization Based on Percentile Bin Constants

# In[25]:


# MAJORS ---

# LEAVE BLANK FOR NOW


# ## Athletic Selectivity Organization Based on Percentile Bin Constants

# In[26]:


# ATHLETIC SELECTIVITY
cd_division = pd.DataFrame(college_dat, columns = ['name', 'division'])

division_schools_1 = []
division_schools_2 = []
division_schools_3 = []
division_schools_NAIA = []
division_schools_NJCAA = []

for ind in cd_division.index:
    if cd_division['division'][ind] == 'NCAA I':
        division_schools_1.append(cd_division['name'][ind])
    elif cd_division['division'][ind] == 'NCAA II':
        division_schools_2.append(cd_division['name'][ind])
    elif cd_division['division'][ind] == 'NCAA III':
        division_schools_3.append(cd_division['name'][ind])
    elif cd_division['division'][ind] == 'NAIA':
        division_schools_NAIA.append(cd_division['name'][ind])
    elif cd_division['division'][ind] == 'NJCAA':
        division_schools_NJCAA.append(cd_division['name'][ind])

d_division_schools_NJCAA = dict(zip(division_schools_NJCAA, [5] * len(division_schools_NJCAA)))
d_division_schools_1 = dict(zip(division_schools_1, [1] * len(division_schools_1)))
d_division_schools_2 = dict(zip(division_schools_2, [3] * len(division_schools_2)))
d_division_schools_3 = dict(zip(division_schools_3, [2] * len(division_schools_3)))
d_division_schools_NAIA = dict(zip(division_schools_NAIA, [4] * len(division_schools_NAIA)))

dict_division_schools = {**d_division_schools_1, **d_division_schools_2, **d_division_schools_3, **d_division_schools_NAIA, **d_division_schools_NAIA}


# # MATCHING FUNCTIONS

# ## ACADEMIC CRITERIA

# In[27]:


# SAT MATCH

def sat_match(bin_val):
    sat_dict_weights = {}
    for key, value in dict_sat_schools.items():
        if bin_val == "VOID":
            sat_dict_weights[key] = 15
        elif bin_val == value:
            sat_dict_weights[key] = 100
        elif ((bin_val + 1) == value) or (bin_val - 1 == value):
            sat_dict_weights[key] = 85
        elif ((bin_val + 2) == value) or (bin_val - 2 == value):
            sat_dict_weights[key] = 70
        elif ((bin_val + 3) == value) or (bin_val - 3 == value):
            sat_dict_weights[key] = 50
        elif ((bin_val + 4) == value) or (bin_val - 4 == value):
            sat_dict_weights[key] = 35
        elif ((bin_val + 5) == value) or (bin_val - 5 == value):
            sat_dict_weights[key] = 0
        else:
            #sat_dict_weights[key] = 0
            x=0
    return sat_dict_weights


# In[28]:


# ACT MATCH
def act_match(bin_val):
    act_dict_weights = {}
    for key, value in dict_act_schools.items():
        if bin_val == "VOID":
            act_dict_weights[key] = 15
        elif bin_val == value:
            act_dict_weights[key] = 100
        elif ((bin_val + 1) == value) or (bin_val - 1 == value):
            act_dict_weights[key] = 90
        elif ((bin_val + 2) == value) or (bin_val - 2 == value):
            act_dict_weights[key] = 75
        elif ((bin_val + 3) == value) or (bin_val - 3 == value):
            act_dict_weights[key] = 60
        elif ((bin_val + 4) == value) or (bin_val - 4 == value):
            act_dict_weights[key] = 45
        elif ((bin_val + 5) == value) or (bin_val - 5 == value):
            act_dict_weights[key] = 15
        elif ((bin_val + 6) == value) or (bin_val - 6 == value):
            act_dict_weights[key] = 0
        else:
            x = 0
    return act_dict_weights


# In[29]:


# GPA MATCH
def gpa_match(bin_val):
    gpa_dict_weights = {}
    for key, value in dict_gpa_schools.items():
        if bin_val == "VOID":
            gpa_dict_weights[key] = 15
        elif bin_val == value:
            gpa_dict_weights[key] = 100
        elif ((bin_val + 1) == value) or (bin_val - 1 == value):
            gpa_dict_weights[key] = 90
        elif ((bin_val + 2) == value) or (bin_val - 2 == value):
            gpa_dict_weights[key] = 75
        elif ((bin_val + 3) == value) or (bin_val - 3 == value):
            gpa_dict_weights[key] = 60
        elif ((bin_val + 4) == value) or (bin_val - 4 == value):
            gpa_dict_weights[key] = 45
        elif ((bin_val + 5) == value) or (bin_val - 5 == value):
            gpa_dict_weights[key] = 15
        elif ((bin_val + 6) == value) or (bin_val - 6 == value):
            gpa_dict_weights[key] = 0
        else:
            x = 0
    return gpa_dict_weights


# In[30]:


# ACCEPTANCE RATE MATCH
def acceptance_rate_match(bin_val):
    acr_dict_weights = {}
    for key, value in dict_acceptrate_schools.items():
        if bin_val == "VOID":
            acr_dict_weights[key] = 10
        elif bin_val == value:
            acr_dict_weights[key] = 100
        elif ((bin_val + 1) == value) or (bin_val - 1 == value):
            acr_dict_weights[key] = 90
        elif ((bin_val + 2) == value) or (bin_val - 2 == value):
            acr_dict_weights[key] = 60
        elif ((bin_val + 3) == value) or (bin_val - 3 == value):
            acr_dict_weights[key] = 45
        elif ((bin_val + 4) == value) or (bin_val - 4 == value):
            acr_dict_weights[key] = 35
        elif ((bin_val + 5) == value) or (bin_val - 5 == value):
            acr_dict_weights[key] = 10
        elif ((bin_val + 6) == value) or (bin_val - 6 == value):
            acr_dict_weights[key] = 0
        else:
            x = 0
    return acr_dict_weights


# ## ENROLLMENT CRITERIA

# In[31]:


# Enrollment Match
def enrollment_match(bin_val):
    enroll_dict_weights = {}
    for key, value in dict_enroll_schools.items():
        if bin_val == "VOID":
            enroll_dict_weights[key] = 20
        elif bin_val == value:
            enroll_dict_weights[key] = 100
        elif ((bin_val + 1) == value) or (bin_val - 1 == value):
            enroll_dict_weights[key] = 85
        elif ((bin_val + 2) == value) or (bin_val - 2 == value):
            enroll_dict_weights[key] = 80
        elif ((bin_val + 3) == value) or (bin_val - 3 == value):
            enroll_dict_weights[key] = 65
        elif ((bin_val + 4) == value) or (bin_val - 4 == value):
            enroll_dict_weights[key] = 35
        elif ((bin_val + 5) == value) or (bin_val - 5 == value):
            enroll_dict_weights[key] = 10
        elif ((bin_val + 6) == value) or (bin_val - 6 == value):
            enroll_dict_weights[key] = 0
        else:
            x = 0
    return enroll_dict_weights

    


# In[32]:


# Enrollment Match
def campsize_match(bin_val):
    campsize_dict_weights = {}
    for key, value in dict_campsize_schools.items():
        if bin_val == "VOID":
            campsize_dict_weights[key] = 15
        elif bin_val == value:
            campsize_dict_weights[key] = 100
        elif ((bin_val + 1) == value) or (bin_val - 1 == value):
            campsize_dict_weights[key] = 80
        elif ((bin_val + 2) == value) or (bin_val - 2 == value):
            campsize_dict_weights[key] = 65
        elif ((bin_val + 3) == value) or (bin_val - 3 == value):
            campsize_dict_weights[key] = 50
        elif ((bin_val + 4) == value) or (bin_val - 4 == value):
            campsize_dict_weights[key] = 30
        elif ((bin_val + 5) == value) or (bin_val - 5 == value):
            campsize_dict_weights[key] = 10
        elif ((bin_val + 6) == value) or (bin_val - 6 == value):
            campsize_dict_weights[key] = 0
        else:
            x = 0
    return campsize_dict_weights


# In[33]:


def setting_match(bin_val):
    setting_dict_weights = {}
    for key, value in dict_setting_schools.items():
        if bin_val == "VOID":
            setting_dict_weights[key] = 25
        elif bin_val == value:
            setting_dict_weights[key] = 100
        else:
            setting_dict_weights[key] = 0
    return setting_dict_weights


# In[34]:


def state_match(states_values):
    state_dict_weights = {}
    for key, value in dict_state_schools.items():
        if value in states_values:
            state_dict_weights[key] = 100
        else:
            state_dict_weights[key] = 0
    return state_dict_weights


# ## COST/AFFORDABILITY CRITERIA

# In[35]:


# Enrollment Match
def pnm_match(bin_val):
    pnm_dict_weights = {}
    for key, value in dict_pnm_schools.items():
        if bin_val == "VOID":
            pnm_dict_weights[key] = 15
        elif bin_val == value:
            pnm_dict_weights[key] = 100
        elif ((bin_val + 1) == value) or (bin_val - 1 == value):
            pnm_dict_weights[key] = 80
        elif ((bin_val + 2) == value) or (bin_val - 2 == value):
            pnm_dict_weights[key] = 60
        elif ((bin_val + 3) == value) or (bin_val - 3 == value):
            pnm_dict_weights[key] = 50
        elif ((bin_val + 4) == value) or (bin_val - 4 == value):
            pnm_dict_weights[key] = 35
        elif ((bin_val + 5) == value) or (bin_val - 5 == value):
            pnm_dict_weights[key] = 5
        elif ((bin_val + 6) == value) or (bin_val - 6 == value):
            pnm_dict_weights[key] = 0
        else:
            x = 0
    return pnm_dict_weights


# In[36]:


# Tuition Match
# Tuition IS
def tuition_in_match(bin_val):
    tuition_in_dict_weights = {}
    for key, value in dict_tuit_schools_in.items():
        if bin_val == "VOID":
            tuition_in_dict_weights[key] = 15
        elif bin_val == value:
            tuition_in_dict_weights[key] = 100
        elif ((bin_val + 1) == value) or (bin_val - 1 == value):
            tuition_in_dict_weights[key] = 75
        elif ((bin_val + 2) == value) or (bin_val - 2 == value):
            tuition_in_dict_weights[key] = 60
        elif ((bin_val + 3) == value) or (bin_val - 3 == value):
            tuition_in_dict_weights[key] = 35
        elif ((bin_val + 4) == value) or (bin_val - 4 == value):
            tuition_in_dict_weights[key] = 20
        elif ((bin_val + 5) == value) or (bin_val - 5 == value):
            tuition_in_dict_weights[key] = 5
        elif ((bin_val + 6) == value) or (bin_val - 6 == value):
            tuition_in_dict_weights[key] = 0
        else:
            x = 0
    return tuition_in_dict_weights

# Tuition OS
def tuition_out_match(bin_val):
    tuition_out_dict_weights = {}
    for key, value in dict_tuit_schools_out.items():
        if bin_val == "VOID":
            tuition_out_dict_weights[key] = 15
        elif bin_val == value:
            tuition_out_dict_weights[key] = 100
        elif ((bin_val + 1) == value) or (bin_val - 1 == value):
            tuition_out_dict_weights[key] = 75
        elif ((bin_val + 2) == value) or (bin_val - 2 == value):
            tuition_out_dict_weights[key] = 60
        elif ((bin_val + 3) == value) or (bin_val - 3 == value):
            tuition_out_dict_weights[key] = 35
        elif ((bin_val + 4) == value) or (bin_val - 4 == value):
            tuition_out_dict_weights[key] = 20
        elif ((bin_val + 5) == value) or (bin_val - 5 == value):
            tuition_out_dict_weights[key] = 5
        elif ((bin_val + 6) == value) or (bin_val - 6 == value):
            tuition_out_dict_weights[key] = 0
        else:
            x = 0
    return tuition_out_dict_weights


# In[37]:


# def tuition_match(bin_val):
#     tuition_dict_weights = {}
#     for key, value in dict_tuit_schools_in.items():
#         if bin_val == "VOID":
#             tuition_dict_weights[key] = 15
#         else:
#             if state matches:
#                 set_bin = dict_tuit_schools_in[key]
                
#                 if bin_val == set_bin:
#                     tuition_dict_weights[key] = 100
#                 if ((bin_val + 1) == set_bin) or (bin_val - 1 == set_bin):
#                     tuition_in_dict_weights[key] = 75
#                 if ((bin_val + 2) == set_bin) or (bin_val - 2 == set_bin):
#                     tuition_in_dict_weights[key] = 60
#                 if ((bin_val + 3) == set_bin) or (bin_val - 3 == set_bin):
#                     tuition_in_dict_weights[key] = 35
#                 if ((bin_val + 4) == set_bin) or (bin_val - 4 == set_bin):
#                     tuition_in_dict_weights[key] = 20
#                 if ((bin_val + 5) == set_bin) or (bin_val - 5 == set_bin):
#                     tuition_in_dict_weights[key] = 5
#                 if ((bin_val + 6) == set_bin) or (bin_val - 6 == set_bin):
#                     tuition_in_dict_weights[key] = 0
#                 else:
#                     x = 0
#     return tuition_in_dict_weights


# ## MAJOR CRITERIA

# In[38]:


# TO BE REVISITED LATER


# ## ATHLETIC SELECTIVITY

# In[39]:


# Divsion 1 - 1, Divison 2 - 3, Division 3 - 2, NAIA - 4, NJCAA - 5
# with assumption that Division 3 is more highly viewed/more desirable to student athletes
def division_match(bin_val):
    division_dict_weights = {}
    for key, value in dict_division_schools.items():
        if bin_val == "VOID":
            division_dict_weights[key] = 15
        elif bin_val == value:
            division_dict_weights[key] = 100
        elif ((bin_val + 1) == value) or (bin_val - 1 == value):
            division_dict_weights[key] = 25
        elif ((bin_val + 2) == value) or (bin_val - 2 == value):
            division_dict_weights[key] = 15
        elif ((bin_val + 3) == value) or (bin_val - 3 == value):
            division_dict_weights[key] = 2
        elif ((bin_val + 4) == value) or (bin_val - 4 == value):
            division_dict_weights[key] = 0
        else:
            x = 0
    return division_dict_weights


# # MAIN - UI

# In[40]:


def main():
    print("This program computes a percentage match value with schools in the IMRecruitable Database. Any failure to report information will have an effect on college matches.")
    
    # WEIGHTS
    time.sleep(5)
    print()
    
    user_state_live = input('To start, please enter the state that you live in with its 2-letter abbreviation (IL, CA, etc). ')
    print()
    
    print('There are 5 key categories when it comes to searching for colleges as an athlete: Cost, Academics, Athletics, Enrollment, and Majors. To best serve your needs, enter how much weight/preference you want to give to each category below, but make sure they add up to 100!')
    
    time.sleep(4)
    user_weight_cost = input('Please enter weight/preference for cost of attending college. ')
    user_weight_academics = input('Please enter weight/preference for the academic selectivity of college. ')
    user_weight_athletics = input('Please enter weight/preference for the athletic division of the college. ')
    user_weight_enrollment = input('Please enter weight/preference for size of the college and neighboring city. ')
    user_weight_majors = input('Please enter weight/preference for majors offered at the college. ')
    print()

    while not validate_weights(user_weight_cost, user_weight_academics, user_weight_athletics, user_weight_enrollment, user_weight_majors):
        print("You did not enter valid weights. Please try again.")
        user_weight_cost = input('Please enter weight/preference for cost of attending college. ')
        user_weight_academics = input('Please enter weight/preference for the academic selectivity of college. ')
        user_weight_athletics = input('Please enter weight/preference for the athletic division of the college. ')
        user_weight_enrollment = input('Please enter weight/preference for size of the college and neighboring city. ')
        user_weight_majors = input('Please enter weight/preference for majors offered at the college. ')
        print()
      
    user_weight_cost = int(user_weight_cost)
    user_weight_academics = int(user_weight_academics)
    user_weight_athletics = int(user_weight_athletics)
    user_weight_enrollment = int(user_weight_enrollment)
    user_weight_majors = int(user_weight_majors)
        

    # ACADEMIC SELECTIVITY --------------------------------------------------------------------------------------
    
    # SAT Input ------------------------------------------------------------------------------------------------
    # increment by 10
    user_SAT_str = input("Please enter your expected/completed SAT score or press <0> to not report: ")
    # Validation of SAT INPUT
    while not validate_SAT(user_SAT_str):
        print("You did not enter a valid SAT score. Please try again.")
        user_SAT_str = input("Please enter your expected/completed SAT score or press <0> to not report: ")
    # SAT Conversion
    user_SAT = int(user_SAT_str)
    
    user_SAT_val = sat_bin(user_SAT)
    
     # ACT Input  ------------------------------------------------------------------------------------------------
    user_ACT_str = input("Please enter your expected/completed ACT score or press <0> to not report: ")
    # Validation of ACT INPUT
    while not validate_ACT(user_ACT_str):
        print("You did not enter a valid ACT score. Please try again.")
        user_ACT_str = input("Please enter your expected/completed ACT score or press <0> to not report: ")
    # ACT Conversion
    user_ACT = int(user_ACT_str)
    
    user_ACT_val = act_bin(user_ACT)
    
    # GPA Input  ------------------------------------------------------------------------------------------------
    # ADD WEIGHTED/UNWEIGHTED PROMPT AND SCALES ETC...
    user_GPA_str = input("Please enter your high school GPA on the 4.0 scale or press <0> to not report: ")
    # Validation of GPA INPUT
    while not validate_GPA(user_GPA_str):
        print("You did not enter a valid GPA score on the 4.0 scale. Please try again.")
        user_GPA_str = input("Please enter your high school GPA on the 4.0 scale or press <0> to not report:  ")
    # GPA Conversion
    user_GPA = float(user_GPA_str)
    user_GPA_val = gpa_bin(user_GPA)
    
    # STATES------------------------------------
    button_states = widgets.Button(
      description="Select the states in which you are looking for colleges!\nNote: Close the window after you click SUBMIT.",
      disabled=False,
      button_style='', # 'success', 'info', 'warning', 'danger' or ''
      tooltip='Click me',
      layout={'width': 'max-content'},
      icon='check') # (FontAwesome names without the `fa-` prefix)
    output16 = widgets.Output()

    display(button_states, output16)
    
    #user_states = []
    #state_weighted = {}

    def on_button_clicked_states(b):
        global user_states
        global state_weighted
        
        with output16:
            window = Tk()
            window.geometry('200x250')

            list1 = Listbox(window, selectmode = "multiple", font=('Times', 25, 'bold'))

            list1.pack(expand = YES, fill = "both")

            states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 
                      'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 
                      'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 
                      'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 
                      'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 
                      'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
            states_abb = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 
                          'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 
                          'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
            comb_states = dict(zip(states, states_abb))

            for each_item in range(len(states)):

                list1.insert(END, states[each_item])

                # coloring alternative lines of listbox
                if each_item % 2 == 0:
                    background = 'yellow'
                    text = 'black'
                else:
                    background = 'black'
                    text = 'white'

                list1.itemconfig(each_item, bg = background, fg = text)


            def selected_item():
                global user_states
                
                selected_states = []

                for i in list1.curselection():
                    print(list1.get(i))
                    selected_states.append(comb_states[list1.get(i)])
                # print(selected_states)
                user_states = selected_states
                # window.quit()

            btn = Button(window, text='Submit', command=selected_item)
            btn.pack(side='bottom')
            list1.pack()

            window.mainloop()
            
            state_weighted = state_match(user_states)
            print(state_weighted)
            

    button_states.on_click(on_button_clicked_states)
        
    # ACCEPTANCE RATE RANGE
    output1 = widgets.Output()
    display(acr_widget, output1)
    
    
    def on_value_change1(change):
        global final_acr
        global acr_weighted
        with output1:
            final_acr = acceptance_rate_bin(change['new'])
            acr_weighted = acceptance_rate_match(final_acr)
            print(change['new'])
    acr_widget.observe(on_value_change1, names='value')
    

    
    # ENROLLMENT/SIZE -----------------------------------------------------------------------------------------------
    
    #user_enroll = interactive(enrollment_bin, {'manual': True},  val =enroll_widget)
    
    output2 = widgets.Output()
    display(enroll_widget, output2)
    def on_value_change2(change):
        global final_enroll
        global enroll_weighted
        with output2:
            final_enroll = enrollment_bin(change['new'])
            enroll_weighted = enrollment_match(final_enroll)
            print(change['new'])
    enroll_widget.observe(on_value_change2, names='value')

    
    #user_camp_size = interactive(campus_pop_bin,  {'manual': True}, val = campus_pop_widget)
    #display(user_camp_size)
    output3 = widgets.Output()
    display(campsize_widget, output3)
    def on_value_change3(change):
        global final_campsize
        global campsize_weighted
        with output3:
            final_campsize = campsize_bin(change['new'])
            campsize_weighted = campsize_match(final_campsize)
            print(change['new'])
    campsize_widget.observe(on_value_change3, names='value')

    output8 = widgets.Output()
    display(setting_widget, output8)
    def on_value_change8(change):
        global final_setting
        global setting_weighted
        with output8:
            final_setting = setting_bin(change['new'])
            setting_weighted = setting_match(final_setting)
            print(change['new'])
    setting_widget.observe(on_value_change8, names='value')
    
    # COST/AFFORDABILITY ------------------------------------------------------------------------------------------
    #tuition_typeX = interactive(check_tuition, {'manual': True}, t = check_tuition_widget)
    #display(tuition_typeX)
    output4 = widgets.Output()
    display(check_tuition_widget, output4)
    output5 = widgets.Output()
    display(tuitcost_widget,output5)
    def on_value_change4(change):
        global ttype1
        global tuit_val
        global tuit_weights
        with output4:
            ttype1 = check_tuition(change['new'])
            #print(change['new'])
            with output5:
                tuit_val = tuition_bin(change['new'])
                print(change['new'])
                if ttype1 == 1:
                    tuit_weights = tuition_in_match(tuit_val)
                elif ttype1 ==2:
                    tuit_weights = tuition_out_match(tuit_val)
    check_tuition_widget.observe(on_value_change4, names='value')
    tuitcost_widget.observe(on_value_change4, names = 'value')

   
    #tuitcost_widget.observe(on_value_change5, names ='value')
    
    #user_tuition = interactive(tuition_bin, {'manual': True}, val = tuitcost_widget)
    #display(user_tuition)
    
    #user_pnm = interactive(percent_need_bin, {'manual': True}, val = pnm_widget)
    #display(user_pnm)
    output6 = widgets.Output()
    display(pnm_widget, output6)
    def on_value_change6(change):
        global final_pnm
        global pnm_weighted
        with output6:
            final_pnm = pnm_bin(change['new'])
            pnm_weighted = pnm_match(final_pnm)
            print(change['new'])
    pnm_widget.observe(on_value_change6, names='value')
    
    
    # MAJOR -------------------------------------------------------------------------------------------------------
    
    # GONNA LEAVE BLANK FOR NOW
    
    # Athletic Selectivity ----------------------------------------------------------------------------------------
    #user_div = interactive(division_bin, {'manual':True}, div = division_widget)
    #display(user_div)
    output7 = widgets.Output()
    display(division_widget, output7)
    def on_value_change7(change):
        global final_division
        global division_weighted
        with output7:
            final_division = division_bin(change['new'])
            division_weighted = division_match(final_division)
            print(change['new'])
    division_widget.observe(on_value_change7, names='value')
    
    # SENDING TO FUNCTIONS -----------------------------------------------------------------------------------------
    sat_weighted = sat_match(user_SAT_val)
    
    act_weighted = act_match(user_ACT_val)
    
    gpa_weighted = gpa_match(user_GPA_val)
        
    
    # ARE YOU READY FOR MATCHES?
    button = widgets.Button(
      description='Are you ready to view your matches? You can no longer change the information above until you start over!.',
      disabled=False,
      button_style='', # 'success', 'info', 'warning', 'danger' or ''
      tooltip='Click me',
      layout={'width': 'max-content'},
      icon='check') # (FontAwesome names without the `fa-` prefix)
    output15 = widgets.Output()

    display(button, output15)

    def on_button_clicked(b):
        with output15:
            matches = matchmaker(sat_weighted, act_weighted, gpa_weighted, acr_weighted, user_weight_academics,
                                 enroll_weighted, campsize_weighted, setting_weighted, state_weighted, user_weight_enrollment, 
                                 tuit_weights, pnm_weighted, user_weight_cost, 
                                 division_weighted, user_weight_athletics)
            sorted_matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}
            print(sorted_matches)
            #print(user_states)
            #print(state_weighted)
            

    button.on_click(on_button_clicked)
  
                                    
main()


# # MATCHMAKER    
#     

# In[41]:


import collections, functools, operator
from operator import itemgetter
def matchmaker(sat, act, gpa, acr, academic_weight, enroll, campsize, setting, state, enroll_weight, tuit, pnm, cost_weight, 
               division, athletic_weight):
    sat_val = {}
    act_val = {}
    gpa_val = {}
    acr_val = {}
    enroll_val = {}
    campsize_val = {}
    setting_val = {}
    state_val = {}
    tuit_val = {}
    pnm_val = {}
    major_val = {}
    division_val = {}
    
    for key, value in sat.items():
        # sat_val[key] = value * WGT1_SAT * WGT_ACADEM
        sat_val[key] = value * WGT1_SAT * academic_weight * 0.01
    for key, value in act.items():
        # act_val[key] = value * WGT1_ACT * WGT_ACADEM
        act_val[key] = value * WGT1_ACT * academic_weight * 0.01
    for key, value in gpa.items():
        # gpa_val[key] = value * WGT1_GPA * WGT_ACADEM
        gpa_val[key] = value * WGT1_GPA * academic_weight * 0.01
    for key, value in acr.items():
        # acr_val[key] = value * WGT1_ACR * WGT_ACADEM
        acr_val[key] = value * WGT1_ACR * academic_weight * 0.01
    
    
    for key, value in enroll.items():
        # enroll_val[key] = value * WGT2_ENRO * WGT_ENROLL
        enroll_val[key] = value * WGT2_ENRO * enroll_weight * 0.01
    for key, value in campsize.items():
        # campsize_val[key] = value * WGT2_CAMP * WGT_ENROLL
        campsize_val[key] = value * WGT2_CAMP * enroll_weight * 0.01
    for key, value in setting.items():
        setting_val[key] = value * WGT2_SETT * enroll_weight * 0.01
    for key, value in state.items():
        state_val[key] = value * WGT2_STATE * enroll_weight * 0.01
        
    for key, value in tuit.items():
        # tuit_val[key] = value * WGT3_TUIT * WGT_COST
        tuit_val[key] = value * WGT3_TUIT * cost_weight * 0.01
    for key, value in pnm.items():
        # pnm_val[key] = value * WGT3_PNM * WGT_COST
        pnm_val[key] = value * WGT3_PNM * cost_weight * 0.01
        
    # MAJOR
    cd_major = pd.DataFrame(college_dat, columns = ['name', 'act_comp'])
    majors1 = []
    for ind in cd_major.index:
        majors1.append(cd_major['name'][ind])
    majors_dict = dict(zip(majors1, [100] * len(majors1)))
    
    for key, value in majors_dict.items():
        major_val[key] = value * WGT_MAJ
            
    for key, value in division.items():
        # division_val[key] = value * WGT5_DIV * WGT_ATH
        division_val[key] = value * WGT5_DIV * athletic_weight * 0.01
        
    
    #------------------------------------------------------------------------------------------------
    #initial_dict = {**sat_val, **act_val, **gpa_val, **acr_val, **enroll_val, ** campsize_val, 
                    #**major_val, **tuit_val, **pnm_val, **division_val}
        
    list1= [sat_val, act_val, gpa_val, acr_val, enroll_val, campsize_val, setting_val, state_val, major_val, tuit_val, pnm_val, division_val]
    result = dict(functools.reduce(operator.add, map(collections.Counter, list1)))
    return result


# In[ ]:





# ### 
