import requests
import json
import random
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from statistics import mean
import pickle

def authen():
    # main
    #headers = {
        #'Authorization': 'token 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',  # replace <TOKEN> with your token
    #}
    # second
    #headers = {
        #'Authorization': 'token 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',
    #}
    # school
    #headers = {
        #'Authorization': 'token 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',
    #}
    # dummy
    headers = {
        'Authorization': 'token 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',
    }

    params = {
        'per_page': 100,
    }
    return headers, params

def percentage(uid,bin_size):
    response = session.get('https://api.github.com/users?since=' + str(uid), headers=authen()[0], params=authen()[1])
    data = response.json()
    start_id = data[0]['id']
    end_id = data[-1]['id']
    while end_id < bin_size + start_id:
        response = session.get('https://api.github.com/users?since=' + str(end_id), headers=authen()[0], params=authen()[1])
        new_data = response.json()
        if not new_data:
            break
        data += new_data
        end_id = new_data[-1]['id']
    total_len = (end_id - start_id) + 1
    return start_id,end_id,len(data)/total_len, total_len
    #print(f"percentage = {len(data)/total_len}")

def estimate_active_users(num_bins, num_sample_bins):
    df_all = pd.DataFrame(columns=['start_id', 'end_id', 'percentage', 'bin_number', 'bin_size', 'sample_bin_size'])
    for bin in num_bins:
        for sample in num_sample_bins:
            bin_size = 125285110 // bin
            bin_start_ids = [i * bin_size for i in range(bin)]
            bin_end_ids = [(i+1) * bin_size - 1 for i in range(bin)]
            sample_bin_start_ids = random.sample(bin_start_ids, sample)
            results = []
            for i in range(sample):
                bin_start_id, bin_end_id, bin_percentage, length = percentage(random.randint(sample_bin_start_ids[i],
                                                                                     sample_bin_start_ids[i] +
                                                                                     bin_size - 1))
                results.append([bin_start_id, bin_end_id, bin_percentage,
                                bin_start_ids.index(sample_bin_start_ids[i])+1, bin, sample])

                df_one = pd.DataFrame(results, columns=['start_id', 'end_id', 'percentage', 'bin_number', 'bin_size',
                                                        'sample_bin_size'])
                df_all = pd.concat([df_all,df_one])
    df_all.to_csv('test4.csv')
    return df_all

def one_bin_one_sample_baseline(bins, samples):
    df_all = pd.DataFrame(columns=['estimated_active', 'bin_size'])
    bin_size = 125285110 // bins
    bin_start_ids = [i * bin_size for i in range(bins)]
    #bin_end_ids = [(i+1) * bin_size - 1 for i in range(bins)]
    for i in range(25):
        results = []
        sample_bin_start_ids = random.sample(bin_start_ids, samples)
        for j in range(samples):
            bin_start_id, bin_end_id, bin_percentage, length = percentage(sample_bin_start_ids[j],bin_size)
            #print(bin_percentage)
            results.append(bin_percentage)
        print(results)
        estimated_active = mean(results) * bins * bin_size
        df_all.loc[len(df_all)] = [estimated_active,bin_size]
    df_all.to_csv('bin_size_'+ str(bin_size) +'_'+str(samples) +'.csv',index=False)
    #return

# Has to be run with multiples of 5 as samples value
def one_bin_one_sample_stratified(bins, samples):
    df_all = pd.DataFrame(columns=['estimated_active', 'bin_size'])
    bin_size = 125285110 // bins
    bin_start_ids = [i * bin_size for i in range(bins)]
    #bin_end_ids = [(i+1) * bin_size - 1 for i in range(bins)]
    #num_samples_bin = int(samples/5)
    for i in range(5):
        results = []
        for b in range(5):
            if b == 0:
                start = 0
                end = int(len(bin_start_ids) /5)
            else:
                start = int((len(bin_start_ids)/5) * b)
                end = int((len(bin_start_ids)/5)* (b+1))
            #print(len(bin_start_ids[start:end]),"actual length",(len(bin_start_ids)))
            sample_bin_start_ids = random.sample(bin_start_ids[start:end], samples)
            for j in range(int(samples/5)):
                bin_start_id, bin_end_id, bin_percentage, length = percentage(sample_bin_start_ids[j],bin_size)
                #print(bin_percentage)
                results.append(bin_percentage)
        print(results)
        estimated_active = mean(results) * bins * bin_size
        df_all.loc[len(df_all)] = [estimated_active,bin_size]
    df_all.to_csv('bin_size_'+ str(bin_size) +'_'+str(samples) +'_stratified_2.csv',index=False)
    #return

if __name__ == "__main__":
    # Total Number of users: 125285110
    # Number of times to get mean: 25

    # Testing out percentage function
    # bin_start_id, bin_end_id, bin_percentage, length = percentage(0,1000)

    # Running session to generate csv of one bin and sample size
    session = requests.Session()
    one_bin_one_sample_baseline(62500, 20)

# Plotting one estimated active for one bin and sample size

    # data_1 = pd.read_csv('bin_size_1002_1.csv')
    # data_5 = pd.read_csv('bin_size_1002_5.csv')
    # data_10 = pd.read_csv('bin_size_1002_10.csv')
    # data_20 = pd.read_csv('bin_size_1002_20.csv')
    # Bin size 2000 Only
    # data_20_1 = pd.read_csv('bin_size_2004_20_stratified.csv')
    # data_20_2 = pd.read_csv('bin_size_2004_20_stratified_2.csv')
    # data_20_3 = pd.read_csv('bin_size_2004_20.csv')
    # data_20 = pd.concat([data_20_1,data_20_2,data_20_3])

    # For baseline
    # data_dict = {'1': data_1.estimated_active_true.values, '5': data_5.estimated_active_true.values,
    #              '10': data_10.estimated_active_true.values, '20': data_20.estimated_active_true.values}
    # For Stratified
    # data_dict= {'5': data_5.estimated_active.values,
    #              '10': data_10.estimated_active.values, '20': data_20.estimated_active.values}
    # fig, ax = plt.subplots()
    # ax.boxplot(data_dict.values())
    # ax.set_xticklabels(data_dict.keys())
    # ax.set_title('Bin Size 1002 Active GitHub User Estimation')
    # ax.set_xlabel('Number of total bins sampled')
    # ax.set_ylabel('Estimated Number of Active GitHub Users')
    # plt.show()

