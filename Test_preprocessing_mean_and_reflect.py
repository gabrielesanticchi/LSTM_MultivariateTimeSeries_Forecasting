# PRE PROCESSING

def symmetric_NaN_replacement(dataset):
    np_dataset = dataset.to_numpy()
    for col in range(0,(np_dataset.shape[1])):
        ss_idx = 0
        for row in range(1,(dataset.shape[0]-1)):
            if (np.isnan(np_dataset[row,col]) and (~np.isnan(np_dataset[row-1,col]))): # if a NaN is found, and it is the first one in the range -> start of a window
                ss_idx = row 
            if ((ss_idx != 0) and (~np.isnan(np_dataset[row+1,col]))): # end of the window has just be found 
                es_idx = row
                # perform symmetric interpolation
                for i in range(0,es_idx-ss_idx+1):
                    np_dataset[ss_idx+i,col] = np_dataset[ss_idx-i-1,col]
                ss_idx = 0
    dataset = pd.DataFrame(np_dataset, columns = dataset.columns)
    return dataset

# inspect_dataframe(dataset, dataset.columns) # original

# Dealing with flat zones 
boolidx = np.ones(dataset['Sponginess'].shape[0])
dataset_np = []
for i, col in enumerate(dataset.columns):
  diff_null = (dataset[col][0:dataset[col].shape[0]].diff() == 0)*1
  for j in range(0,dataset[col].shape[0]):
              if (diff_null[j] >= 1):
                  diff_null[j] = diff_null[j-1]+1
  boolidx = np.logical_and(boolidx, diff_null < 5)

dataset[~boolidx] = np.NaN
symmetric_NaN_replacement(dataset)

#Dealing with Meme creativity mean removal 
THRESHOLD = 1.3
real_value_idx = np.ones(dataset.shape[0])
real_value_idx = np.logical_and(real_value_idx, dataset['Meme creativity'] > THRESHOLD)
print(np.mean(dataset['Meme creativity']))
print(np.mean(dataset['Meme creativity'][~real_value_idx]))
print(np.mean(dataset['Meme creativity'][real_value_idx]))
dataset['Meme creativity'][~real_value_idx] = dataset['Meme creativity'][~real_value_idx] + np.mean(dataset['Meme creativity'][real_value_idx])


inspect_dataframe(dataset, dataset.columns) #pre processed