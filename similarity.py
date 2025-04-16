import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import matplotlib.pyplot as plt
import seaborn as sns



'''获取pkl原始数据'''
def get_pkl(file_path):
    f = open(file_path, 'rb')
    pkl = []
    while True:
        try:
            inf  = pickle.load(f)
            pkl.append(inf)
        except:
            break

    return pkl  #pkl[i][0][0]—为一条数据(一个列表)

'''提取pkl文件每一条数据，存为一个列表'''
def get_basedata(nums_of_dataitems, pkl):
    k = 0
    base_data = []
    while k < nums_of_dataitems:
        base_data.append(pkl[k][0][0])
        k += 1

    return base_data    #base_data[i] 即为一条数据(一个列表)

def get_baselable(pkl, groups):
    #pkl[k][1]
    k = 0
    lables = []
    while k < groups:
        if type(pkl[k][1]) == list:
            temp = ''
            for i in range(len(pkl[k][1])):
                temp += '-'
                temp += pkl[k][1][i]
            lables.append(temp)
        else:
            lables.append(pkl[k][1])
        k += 1

    return  lables


'''规范化每一条数据，即将5ms 的5个数据合并为一个数据'''
def normalize_data_items(nums_of_dataitems, trace_length, base_data):
    trace_time = trace_length * 1000
    normalize_data = []
    k = 0
    while k < nums_of_dataitems:
        normalize_data.append([])
        k += 1
    i = 0
    while i < nums_of_dataitems:
        for j in range(0,trace_time,5):
            temp = 0
            for k in range(0,5):
                temp += base_data[i][j+k]
            normalize_data[i].append(temp)
        i += 1

    return normalize_data


'''数据合并，将len(normalize_data) / nums_of_groups 条数据合并为一组，最后返回的数据组数量为nums_of_group'''
def final_data(normalize_data, nums_of_group):
    to_matlab_data = []
    items_of_group = int(len(normalize_data) / nums_of_group)
    length_of_item = len(normalize_data[0])

    k = 0
    while k < nums_of_group:
        to_matlab_data.append([])
        k += 1

    id = 0
    for i in range(0,len(normalize_data),items_of_group):
        for j in range(0,length_of_item):
            temp = 0
            for k in range(0,items_of_group):
                temp += normalize_data[i+k][j]
            temp = int(temp / items_of_group)
            to_matlab_data[id].append(temp)

        id += 1

    return to_matlab_data

''' 不用baseline 减'''
def processing_data(file_path, nums_of_dataitems, trace_length, nums_of_group):
    pkl = get_pkl(file_path)
    base_data = get_basedata(nums_of_dataitems, pkl)
    normalize_data = normalize_data_items(nums_of_dataitems, trace_length, base_data)
    to_matlab_data = final_data(normalize_data, nums_of_group)
    # for i in range(len(to_matlab_data)):
    #     for j in range(len(to_matlab_data[i])):
    #         to_matlab_data[i][j] = baseline - to_matlab_data[i][j]
    return to_matlab_data



# 示例：假设你的时序数据存储在一个10x25000的矩阵中，每行为一组时序数据
# 这里随机生成一些时序数据，实际情况中你会用你的数据替代
path = r"D:\Project_of_postgraduate\Biger-fish\bigger-fish-main\Second\Trace\doubao\img_doubao.com_100_25s.pkl"
path1 = r"D:\Project_of_postgraduate\Biger-fish\bigger-fish-main\Second\Trace\doubao\word_doubao.com_100_25s.pkl"
trace = processing_data(path, 100, 25, 10)
trace = np.array(trace)
# 对每一行进行规范化，将其缩放到 0-1 之间
trace_normalized = trace / trace.max(axis=1, keepdims=True)

trace1 = processing_data(path1, 100, 25, 10)
trace1 = np.array(trace1)
# 对每一行进行规范化，将其缩放到 0-1 之间
trace_normalized1 = trace1 / trace1.max(axis=1, keepdims=True)

# 从 trace_normalized 中提取前 5 组数据
trace_part = trace_normalized[:5, :]  # 取前5行

# 从 trace_normalized1 中提取后 5 组数据
trace1_part = trace_normalized1[-5:, :]  # 取后5行

similarity_trace = np.vstack((trace_part, trace1_part))
# 计算余弦相似度
similarity_matrix = cosine_similarity(similarity_trace)

# 输出相似度矩阵
print("余弦相似度矩阵：")
print(similarity_matrix)



# 可视化相似度矩阵，不显示具体的数值
plt.figure(figsize=(10, 8))
sns.heatmap(similarity_matrix, cmap='coolwarm')  # 移除 annot 参数，隐藏数值
plt.title('Cosine Similarity Matrix')
plt.show()