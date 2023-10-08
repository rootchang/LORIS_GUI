###############################################################################################
#Cancer immunotherapy response scoring system
# Aim: Scoring patient ICB response based on clinical features
# Description: A graphic user interface for quickly evaluating the objective ICB response probability and median
#              progression-free survival and overall survival time based on the clinical features of the patient.
# Input: Users can either provide feature information in a .txt file with many patients (see format in the
#        ./query_patients.txt), or manually input features of a single patient in the GUI.
###############################################################################################
import os.path
import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
from tkinter import filedialog
from datetime import datetime
from pkg_resources import resource_filename


#############################################################################################
#################################### Set global parameters ##################################
#############################################################################################
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
welcome_message = f"{current_time}   Welcome to LORIS2!"
print(welcome_message)

entry_fnIn = None
LLR_models = []
### LLR6-PanCancer
try:
    fnIn = 'model_Params/LLR6_panCancer_Param.txt'
    fnIn = resource_filename(__name__, fnIn)
    params_data = open(fnIn, 'r').readlines()
    params_dict = {}
    for line in params_data:
        if 'LLR_' not in line:
            if 'Cancer_types' in line:
                words = line.strip().split('\t')
                LLR6_PanCancer_cancerTypes = words[1:]
            continue
        words = line.strip().split('\t')
        param_name = words[0]
        params_val = [float(c) for c in words[1:]]
        params_dict[param_name] = params_val
    ### calculate LORIS formula
    scaler_mean_ = np.array(params_dict['LLR_mean'])
    scaler_scale_ = np.array(params_dict['LLR_scale'])
    clf_coef_ = np.array([params_dict['LLR_coef']])
    clf_intercept_ = np.array(params_dict['LLR_intercept'])
    coef_list = params_dict['LLR_coef'] / scaler_scale_
    interc = -sum(params_dict['LLR_coef'] * scaler_mean_ / scaler_scale_) + params_dict['LLR_intercept'][0]

    LLR6_PanCancer_coefs = list(coef_list[5:]) + [0]
    LLR6_PanCancer_cancerTypes = LLR6_PanCancer_cancerTypes + ['Not in training data']
    # LLR6_panCancer_featureNAs = ['TMB', 'systemic_tx_history', 'Albumin', 'NLR', 'Age']
    LLR6_panCancer_featureCoefs = coef_list[0:5]
    LLR6_panCancer_interc = interc
    LLR6_PanCancer_cancer_coef_dict = dict(zip(LLR6_PanCancer_cancerTypes, LLR6_PanCancer_coefs))

    ### read in LORIS-ORR/mOS/mPFS relationship files
    fnIn = 'model_Params/LLR6_panCancer_ORR_Table.txt'
    fnIn = resource_filename(__name__, fnIn)
    ORR_df = pd.read_csv(fnIn, sep='\t', index_col=0, header=0)
    fnIn = 'model_Params/LLR6_panCancer_PFS_Table.txt'
    fnIn = resource_filename(__name__, fnIn)
    PFS_df = pd.read_csv(fnIn, sep='\t', index_col=0, header=0)
    fnIn = 'model_Params/LLR6_panCancer_OS_Table.txt'
    fnIn = resource_filename(__name__, fnIn)
    OS_df = pd.read_csv(fnIn, sep='\t', index_col=0, header=0)
    LLR6_panCancer_ORR_PFS_OS_df = pd.concat([ORR_df, PFS_df, OS_df], axis=1, join='outer')
    LLR_models.append('LLR6(pan-cancer)')
except:
    1

### LLR6-NSCLC
try:
    fnIn = 'model_Params/LLR6_NSCLC_Param.txt'
    fnIn = resource_filename(__name__, fnIn)
    params_data = open(fnIn, 'r').readlines()
    params_dict = {}
    for line in params_data:
        if 'LLR_' not in line:
            continue
        words = line.strip().split('\t')
        param_name = words[0]
        params_val = [float(c) for c in words[1:]]
        params_dict[param_name] = params_val
    ### calculate LORIS formula
    scaler_mean_ = np.array(params_dict['LLR_mean'])
    scaler_scale_ = np.array(params_dict['LLR_scale'])
    clf_coef_ = np.array([params_dict['LLR_coef']])
    clf_intercept_ = np.array(params_dict['LLR_intercept'])
    coef_list = params_dict['LLR_coef'] / scaler_scale_
    interc = -sum(params_dict['LLR_coef'] * scaler_mean_ / scaler_scale_) + params_dict['LLR_intercept'][0]

    # LLR6_NSCLC_featureNAs = ['TMB', 'PDL1_TPS', 'systemic_tx_history', 'Albumin', 'NLR', 'Age']
    LLR6_NSCLC_featureCoefs = coef_list
    LLR6_NSCLC_interc = interc

    ### read in LORIS-ORR/mOS/mPFS relationship files
    fnIn = 'model_Params/LLR6_NSCLC_ORR_Table.txt'
    fnIn = resource_filename(__name__, fnIn)
    ORR_df = pd.read_csv(fnIn, sep='\t', index_col=0, header=0)
    fnIn = 'model_Params/LLR6_NSCLC_PFS_Table.txt'
    fnIn = resource_filename(__name__, fnIn)
    PFS_df = pd.read_csv(fnIn, sep='\t', index_col=0, header=0)
    fnIn = 'model_Params/LLR6_NSCLC_OS_Table.txt'
    fnIn = resource_filename(__name__, fnIn)
    OS_df = pd.read_csv(fnIn, sep='\t', index_col=0, header=0)
    LLR6_NSCLC_ORR_PFS_OS_df = pd.concat([ORR_df, PFS_df, OS_df], axis=1, join='outer')
    LLR_models.append('LLR6(NSCLC)')
except:
    1

### LLR5-PanCancer
try:
    fnIn = 'model_Params/LLR5_panCancer_Param.txt'
    fnIn = resource_filename(__name__, fnIn)
    params_data = open(fnIn, 'r').readlines()
    params_dict = {}
    for line in params_data:
        if 'LLR_' not in line:
            if 'Cancer_types' in line:
                words = line.strip().split('\t')
                LLR5_PanCancer_cancerTypes = words[1:]
            continue
        words = line.strip().split('\t')
        param_name = words[0]
        params_val = [float(c) for c in words[1:]]
        params_dict[param_name] = params_val
    ### calculate LORIS formula
    scaler_mean_ = np.array(params_dict['LLR_mean'])
    scaler_scale_ = np.array(params_dict['LLR_scale'])
    clf_coef_ = np.array([params_dict['LLR_coef']])
    clf_intercept_ = np.array(params_dict['LLR_intercept'])
    coef_list = params_dict['LLR_coef'] / scaler_scale_
    interc = -sum(params_dict['LLR_coef'] * scaler_mean_ / scaler_scale_) + params_dict['LLR_intercept'][0]

    LLR5_PanCancer_coefs = list(coef_list[4:]) + [0]
    LLR5_PanCancer_cancerTypes = LLR5_PanCancer_cancerTypes + ['Not in training data']
    # LLR6_panCancer_featureNAs = ['TMB', 'Albumin', 'NLR', 'Age']
    LLR5_panCancer_featureCoefs = coef_list[0:4]
    LLR5_panCancer_interc = interc
    LLR5_PanCancer_cancer_coef_dict = dict(zip(LLR5_PanCancer_cancerTypes, LLR5_PanCancer_coefs))

    ### read in LORIS-ORR/mOS/mPFS relationship files
    fnIn = 'model_Params/LLR5_panCancer_ORR_Table.txt'
    fnIn = resource_filename(__name__, fnIn)
    ORR_df = pd.read_csv(fnIn, sep='\t', index_col=0, header=0)
    fnIn = 'model_Params/LLR5_panCancer_PFS_Table.txt'
    fnIn = resource_filename(__name__, fnIn)
    PFS_df = pd.read_csv(fnIn, sep='\t', index_col=0, header=0)
    fnIn = 'model_Params/LLR5_panCancer_OS_Table.txt'
    fnIn = resource_filename(__name__, fnIn)
    OS_df = pd.read_csv(fnIn, sep='\t', index_col=0, header=0)
    LLR5_panCancer_ORR_PFS_OS_df = pd.concat([ORR_df, PFS_df, OS_df], axis=1, join='outer')
    LLR_models.append('LLR5(pan-cancer)')
except:
    1

### LLR5-NSCLC
try:
    fnIn = 'model_Params/LLR5_NSCLC_Param.txt'
    fnIn = resource_filename(__name__, fnIn)
    params_data = open(fnIn, 'r').readlines()
    params_dict = {}
    for line in params_data:
        if 'LLR_' not in line:
            continue
        words = line.strip().split('\t')
        param_name = words[0]
        params_val = [float(c) for c in words[1:]]
        params_dict[param_name] = params_val
    ### calculate LORIS formula
    scaler_mean_ = np.array(params_dict['LLR_mean'])
    scaler_scale_ = np.array(params_dict['LLR_scale'])
    clf_coef_ = np.array([params_dict['LLR_coef']])
    clf_intercept_ = np.array(params_dict['LLR_intercept'])
    coef_list = params_dict['LLR_coef'] / scaler_scale_
    interc = -sum(params_dict['LLR_coef'] * scaler_mean_ / scaler_scale_) + params_dict['LLR_intercept'][0]

    # LLR5_NSCLC_featureNAs = ['TMB', 'PDL1_TPS', 'Albumin', 'NLR', 'Age']
    LLR5_NSCLC_featureCoefs = coef_list
    LLR5_NSCLC_interc = interc

    ### read in LORIS-ORR/mOS/mPFS relationship files
    fnIn = 'model_Params/LLR5_NSCLC_ORR_Table.txt'
    fnIn = resource_filename(__name__, fnIn)
    ORR_df = pd.read_csv(fnIn, sep='\t', index_col=0, header=0)
    fnIn = 'model_Params/LLR5_NSCLC_PFS_Table.txt'
    fnIn = resource_filename(__name__, fnIn)
    PFS_df = pd.read_csv(fnIn, sep='\t', index_col=0, header=0)
    fnIn = 'model_Params/LLR5_NSCLC_OS_Table.txt'
    fnIn = resource_filename(__name__, fnIn)
    OS_df = pd.read_csv(fnIn, sep='\t', index_col=0, header=0)
    LLR5_NSCLC_ORR_PFS_OS_df = pd.concat([ORR_df, PFS_df, OS_df], axis=1, join='outer')
    LLR_models.append('LLR5(NSCLC)')
except:
    1

try:
    cancerTypes = LLR6_PanCancer_cancerTypes
except:
    try:
        cancerTypes = LLR5_PanCancer_cancerTypes
    except:
        cancerTypes = ['NSCLC']











def calculate():
    result_label.config(text="Running...")
    root.update()  # Force GUI update to display "Running..."
    root.after(500) # sleep 0.5 second
    model_used = selected_model.get()
    if model_used == "None":
        result_label.config(text="Please select a model.")
        return
    fnIn = entry_fnIn.get()
    if fnIn:
        if os.path.exists(fnIn):
            try:
                data_df = pd.read_csv(fnIn, sep='\t', index_col=0, header=0)
                TMB = data_df['TMB']
                TMB = np.array([min(c,50) for c in TMB])
                Albumin = data_df['Albumin']
                Albumin = np.array(Albumin)
                NLR = data_df['NLR']
                NLR = np.array([min(c, 25) for c in NLR])
                Age = data_df['Age']
                Age = np.array([min(c, 85) for c in Age])
            except:
                result_label.config(text="Input file format error.")
                return
        else:
            result_label.config(text="Input file not exists.")
            return
        data_df['PatientScore'] = 0
        data_df['ORR'] = 0
        data_df['ORR025'] = 0
        data_df['ORR975'] = 0
        data_df['mPFS_months'] = 0
        data_df['mPFS025_months'] = 0
        data_df['mPFS975_months'] = 0
        data_df['mOS_months'] = 0
        data_df['mOS025_months'] = 0
        data_df['mOS975_months'] = 0
    else:
        try:
            TMB = min(float(entry_TMB.get()),50)
            Albumin = float(entry_Albumin.get())
            NLR = min(float(entry_NLR.get()),25)
            Age = min(float(entry_Age.get()),85)
        except:
            result_label.config(text="Invalid input. Please check your input carefully.")
            return
    if model_used in ["LLR6(pan-cancer)","LLR6(NSCLC)"]:
        if fnIn:
            try:
                History = data_df['History']
                History = np.array(History)
            except:
                result_label.config(text="Feature 'History' error in input file.")
                return
        else:
            try:
                History = float(selected_history.get())  # 0 or 1
            except:
                result_label.config(text="Invalid input. History not set.")
                return
        if model_used == "LLR6(pan-cancer)":
            if fnIn:
                try:
                    cancerType = data_df['CancerType']
                    cancerType = np.array(cancerType)
                except:
                    result_label.config(text="Feature 'CancerType' error in input file.")
                    return
                try:
                    cancerCoef = [LLR6_PanCancer_cancer_coef_dict[c] for c in cancerType]
                except:
                    result_label.config(text="Unrecognized cancer type found in input file.")
                    return
            else:
                cancerType = selected_cancer.get()
                if cancerType == "None":
                    result_label.config(text="Invalid input. Cancer type not set.")
                    return
                cancerCoef = LLR6_PanCancer_cancer_coef_dict[cancerType]
            S = TMB * LLR6_panCancer_featureCoefs[0] + History * LLR6_panCancer_featureCoefs[1] + \
                Albumin * LLR6_panCancer_featureCoefs[2] + NLR * LLR6_panCancer_featureCoefs[3] + \
                Age * LLR6_panCancer_featureCoefs[4] + cancerCoef + LLR6_panCancer_interc
            LORIS = 1 / (1 + np.exp(-S))
            if fnIn:
                for sample_i in range(len(LORIS)):
                    LORIS_temp = int(round(LORIS[sample_i] * 100))
                    data_df.iloc[sample_i,7:] = [LORIS[sample_i]] + list(LLR6_panCancer_ORR_PFS_OS_df.iloc[LORIS_temp, :])
                fnOut = fnIn[0:-4]+'_out.txt'
                data_df.to_csv(fnOut, sep='\t', index=True, header=True)
                result_label.config(text="Prediction done. See result in output file.")
            else:
                LORIS_temp = int(round(LORIS*100))
                ORR,ORR025,ORR975,mPFS_months,mPFS025_months,mPFS975_months,mOS_months,mOS025_months,mOS975_months = LLR6_panCancer_ORR_PFS_OS_df.iloc[LORIS_temp,:]
                result_text = (
                        "Patient score: %.2f\n" % LORIS +
                        "Obj. response odds: %d (%d,%d)%%\n" % (ORR * 100, ORR025 * 100, ORR975 * 100) +
                        "Median PFS: %d (%d,%d) months\n" % (mPFS_months, mPFS025_months, mPFS975_months) +
                        "Median OS: %d (%d,%d) months" % (mOS_months, mOS025_months, mOS975_months)
                )
                result_label.config(text=result_text)
        elif model_used == "LLR6(NSCLC)":
            if fnIn:
                try:
                    PDL1 = data_df['PDL1']
                    PDL1 = np.array(PDL1)
                except:
                    result_label.config(text="Feature 'PDL1' error in input file.")
                    return
            else:
                try:
                    PDL1 = float(entry_PDL1.get())
                    if (PDL1 <0) or (PDL1 > 100):
                        int('a')
                except:
                    result_label.config(text="Invalid input. PDL1 value error.")
                    return
            S = TMB * LLR6_NSCLC_featureCoefs[0] + PDL1 * LLR6_NSCLC_featureCoefs[1] + \
                History * LLR6_NSCLC_featureCoefs[2] + Albumin * LLR6_NSCLC_featureCoefs[3] + \
                NLR * LLR6_NSCLC_featureCoefs[4] + Age * LLR6_NSCLC_featureCoefs[5] + LLR6_NSCLC_interc
            LORIS = 1 / (1 + np.exp(-S))
            if fnIn:
                for sample_i in range(len(LORIS)):
                    LORIS_temp = int(round(LORIS[sample_i] * 100))
                    data_df.iloc[sample_i,7:] = [LORIS[sample_i]] + list(LLR6_NSCLC_ORR_PFS_OS_df.iloc[LORIS_temp, :])
                fnOut = fnIn[0:-4]+'_out.txt'
                data_df.to_csv(fnOut, sep='\t', index=True, header=True)
                result_label.config(text="Prediction done. See result in output file.")
            else:
                LORIS_temp = int(round(LORIS*100))
                ORR,ORR025,ORR975,mPFS_months,mPFS025_months,mPFS975_months,mOS_months,mOS025_months,mOS975_months = LLR6_NSCLC_ORR_PFS_OS_df.iloc[LORIS_temp,:]
                result_text = (
                        "Patient score: %.2f\n" % LORIS +
                        "Obj. response odds: %d (%d,%d)%%\n" % (ORR * 100, ORR025 * 100, ORR975 * 100) +
                        "Median PFS: %d (%d,%d) months\n" % (mPFS_months, mPFS025_months, mPFS975_months) +
                        "Median OS: %d (%d,%d) months" % (mOS_months, mOS025_months, mOS975_months)
                )
                result_label.config(text=result_text)
    elif model_used == "LLR5(pan-cancer)":
        if fnIn:
            try:
                cancerType = data_df['CancerType']
                cancerType = np.array(cancerType)
            except:
                result_label.config(text="Feature 'CancerType' error in input file.")
                return
            try:
                cancerCoef = [LLR5_PanCancer_cancer_coef_dict[c] for c in cancerType]
            except:
                result_label.config(text="Unrecognized cancer type found in input file.")
                return
        else:
            cancerType = selected_cancer.get()
            if cancerType == "None":
                result_label.config(text="Invalid input. Cancer type not set.")
                return
            cancerCoef = LLR5_PanCancer_cancer_coef_dict[cancerType]
        S = TMB * LLR5_panCancer_featureCoefs[0] + \
            Albumin * LLR5_panCancer_featureCoefs[1] + NLR * LLR5_panCancer_featureCoefs[2] + \
            Age * LLR5_panCancer_featureCoefs[3] + cancerCoef + LLR5_panCancer_interc
        LORIS = 1 / (1 + np.exp(-S))
        if fnIn:
            for sample_i in range(len(LORIS)):
                LORIS_temp = int(round(LORIS[sample_i] * 100))
                data_df.iloc[sample_i, 7:] = [LORIS[sample_i]] + list(LLR5_panCancer_ORR_PFS_OS_df.iloc[LORIS_temp, :])
            fnOut = fnIn[0:-4] + '_out.txt'
            data_df.to_csv(fnOut, sep='\t', index=True, header=True)
            result_label.config(text="Prediction done. See result in output file.")
        else:
            LORIS_temp = int(round(LORIS * 100))
            ORR, ORR025, ORR975, mPFS_months, mPFS025_months, mPFS975_months, mOS_months, mOS025_months, \
            mOS975_months = LLR5_panCancer_ORR_PFS_OS_df.iloc[LORIS_temp,:]
            result_text = (
                    "Patient score: %.2f\n" % LORIS +
                    "Obj. response odds: %d (%d,%d)%%\n" % (ORR * 100, ORR025 * 100, ORR975 * 100) +
                    "Median PFS: %d (%d,%d) months\n" % (mPFS_months, mPFS025_months, mPFS975_months) +
                    "Median OS: %d (%d,%d) months" % (mOS_months, mOS025_months, mOS975_months)
            )
            result_label.config(text=result_text)
    elif model_used == "LLR5(NSCLC)":
        if fnIn:
            try:
                PDL1 = data_df['PDL1']
                PDL1 = np.array(PDL1)
            except:
                result_label.config(text="Feature 'PDL1' error in input file.")
                return
        else:
            try:
                PDL1 = float(entry_PDL1.get())
                if (PDL1 < 0) or (PDL1 > 100):
                    int('a')
            except:
                result_label.config(text="Invalid input. PDL1 value error.")
                return
        S = TMB * LLR5_NSCLC_featureCoefs[0] + PDL1 * LLR5_NSCLC_featureCoefs[1] + \
            Albumin * LLR5_NSCLC_featureCoefs[2] + \
            NLR * LLR5_NSCLC_featureCoefs[3] + Age * LLR5_NSCLC_featureCoefs[4] + LLR5_NSCLC_interc
        LORIS = 1 / (1 + np.exp(-S))
        if fnIn:
            for sample_i in range(len(LORIS)):
                LORIS_temp = int(round(LORIS[sample_i] * 100))
                data_df.iloc[sample_i, 7:] = [LORIS[sample_i]] + list(LLR5_NSCLC_ORR_PFS_OS_df.iloc[LORIS_temp, :])
            fnOut = fnIn[0:-4] + '_out.txt'
            data_df.to_csv(fnOut, sep='\t', index=True, header=True)
            result_label.config(text="Prediction done. See result in output file.")
        else:
            LORIS_temp = int(round(LORIS * 100))
            ORR, ORR025, ORR975, mPFS_months, mPFS025_months, mPFS975_months, mOS_months, mOS025_months, \
            mOS975_months = LLR5_NSCLC_ORR_PFS_OS_df.iloc[LORIS_temp,:]
            result_text = (
                    "Patient score: %.2f\n" % LORIS +
                    "Obj. response odds: %d (%d,%d)%%\n" % (ORR * 100, ORR025 * 100, ORR975 * 100) +
                    "Median PFS: %d (%d,%d) months\n" % (mPFS_months, mPFS025_months, mPFS975_months) +
                    "Median OS: %d (%d,%d) months" % (mOS_months, mOS025_months, mOS975_months)
            )
            result_label.config(text=result_text)


def exit_program():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    goodbye_message = f"{current_time}   Thank you for using LORIS!"
    print(goodbye_message)
    root.destroy()  # Close the main window and exit the program


def browse_file():
    file_path = filedialog.askopenfilename()
    entry_fnIn.delete(0, tk.END)
    entry_fnIn.insert(0, file_path)

def main():
    1

if __name__ == "__main__":
    main()



#############################################################################################
################################### Create the main window ##################################
#############################################################################################
root = tk.Tk()
root.title("Cancer immunotherapy response scoring system")
# Set the initial window size
root.geometry("400x400")  # Width x Height

# Create labels and entry fields
label_TMB = ttk.Label(root, text="TMB (Mut/Mb):")
entry_TMB = ttk.Entry(root)

label_PDL1 = ttk.Label(root, text="PDL1_TPS (%):")
entry_PDL1 = ttk.Entry(root)

label_Albumin = ttk.Label(root, text="Albumin (g/dL):")
entry_Albumin = ttk.Entry(root)

label_NLR = ttk.Label(root, text="NLR:")
entry_NLR = ttk.Entry(root)

label_Age = ttk.Label(root, text="Age:")
entry_Age = ttk.Entry(root)

label_fnIn = ttk.Label(root, text="Input from file:")
entry_fnIn = ttk.Entry(root)
browse_button = ttk.Button(root, text="...", command=browse_file, width=1)

# Create the dropdown menu
history_option = ttk.Label(root, text="Systemic tx history:")
options = ["None", 0, 1]
selected_history = tk.StringVar(value=options[0])  # Set the default option
history_option_menu = ttk.OptionMenu(root, selected_history, *options)

cancer_option = ttk.Label(root, text="Cancer type:")
options = ["None"] + cancerTypes
selected_cancer = tk.StringVar(value=options[0])  # Set the default option
cancer_option_menu = ttk.OptionMenu(root, selected_cancer, *options)

model_option = ttk.Label(root, text="Select model:")
options = ["None"] + LLR_models
selected_model = tk.StringVar(value=options[0])  # Set the default option
model_option_menu = ttk.OptionMenu(root, selected_model, *options)

# calculate and exit buttons
calculate_button = ttk.Button(root, text="Calculate", command=calculate)
exit_button = ttk.Button(root, text="Exit", command=exit_program)  # Added Exit button

# Define custom styles for buttons (with custom colors)
style = ttk.Style()
style.theme_use('alt')
style.configure('TButton', font=('American typewriter', 14), background='#228B22',
                foreground='white')  # 228B22  232323
style.map('TButton', background=[('active', '#ff0000')])

result_label = ttk.Label(root, text="")

# Layout
label_TMB.grid(row=0, column=0, sticky='e')
entry_TMB.grid(row=0, column=1)

label_PDL1.grid(row=1, column=0, sticky='e')
entry_PDL1.grid(row=1, column=1)

label_Albumin.grid(row=2, column=0, sticky='e')
entry_Albumin.grid(row=2, column=1)

label_NLR.grid(row=3, column=0, sticky='e')
entry_NLR.grid(row=3, column=1)

label_Age.grid(row=4, column=0, sticky='e')
entry_Age.grid(row=4, column=1)

history_option.grid(row=5, column=0, sticky='e')
history_option_menu.grid(row=5, column=1)

cancer_option.grid(row=6, column=0, sticky='e')
cancer_option_menu.grid(row=6, column=1)

label_fnIn.grid(row=7, column=0, sticky='e')
entry_fnIn.grid(row=7, column=1, columnspan=2)  #
browse_button.grid(row=7, column=3, sticky='e')

model_option.grid(row=8, column=0, sticky='e')
model_option_menu.grid(row=8, column=1)

calculate_button.grid(row=9, column=0)
exit_button.grid(row=9, column=1)  # Place the Exit button next to Calculate button
result_label.grid(row=10, column=0, columnspan=2)

# Start the GUI application
root.mainloop()