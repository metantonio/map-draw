import numpy as np
import pandas as pd

def excel_GMS2UTM():
    df_excel = pd.read_excel('data.xls', sheet_name="GMS_a_UTM")
    df_excel_columnas = df_excel.columns
    #print("Excel Heads: \n", df_excel_columnas)
    df_dataset_lenght = df_excel.iloc[0,0]
    #print("\n Dataset lenght: ",df_dataset_lenght)
    #variables = int(input("\n How many variables for inputs exist? (x1, x2, ...)\n"))
    norte_GMS=[]
    este_GMS=[]
    feature=[]
    for i in range(df_dataset_lenght):
        norte_GMS.append(df_excel.iloc[i,6]) #el index en para extraer data de columnas empieza en 0, por eso es columna 6 y no 7
        este_GMS.append(df_excel.iloc[i,11])
        feature.append([df_excel.iloc[i,6],df_excel.iloc[i,11]])
        #print("\n Norte: " + str(norte_GMS[i]) + " Este: " + str(este_GMS[i]))
    data = pd.DataFrame(feature, columns=["Norte/Sur","Este/Oeste"])
    print("\n initial data: \n", data)
    #print(feature)
    #print("\n initial weights \n", weights)
    return data, norte_GMS, este_GMS, feature
  
def save_csv(data, weights, bias, l_rate, epochs, epoch_loss, loss, average_loss):
    print("\n Weights: \n",weights)
    df= pd.DataFrame({'Weights':weights, 'Epoch':epochs})
    #df["Data"] = data
    #df["Weights"]=weights
    #df["epochs"]=epochs
    #df["epoch_loss"]=epoch_loss
    print(df)
    df["Average_loss"]=average_loss
    #df.to_csv('results.csv', index=False, decimal=",", columns=["Weights", "Epoch"])
    with pd.ExcelWriter('results.xlsx', mode='w') as writer:
        return df.to_excel(writer, sheet_name="results")
    #return df.to_csv('results.csv', index=False, decimal=",", columns=["Weights", "Epoch"])
    
    
    
#HERE FINISH DEFINITIONS OF FUNCTIONS
    
