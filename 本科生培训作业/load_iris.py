import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris()
iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df["species"] = iris.target_names[iris.target] 
iris_df.to_csv('iris.csv', index=False)
print("数据集已保存为iris.csv")