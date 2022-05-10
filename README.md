本库为Abaqus python脚本储存库，其中包含微结构的生成脚本、后处理脚本、数据转换脚本。
# 简介
1. Layup.py:为前处理及部分后处理脚本，包括模型前处理（Part、Property等基本模块）、提交Job、对odb文件数据的处理。

2. PostProcessing.py:为后处理脚本，因为在提交作业计算完成后，odb可能生成不及时，而Layup脚本的命令执行速度又快，会报错。因此，将后处理单独分离出来，将后处理得出的数据导出保存为txt格式。

3. DataToExcel.py:由于Data.txt文件转换需要openpyxl库，而目前没有解决abaqus运行脚本对第三方库报错的问题，因此，需要单独将Data.txt转换为Excel表格写一个脚本。
# 环境依赖
本库中的脚本基于python 3.9.6版本开发的，虽然abaqus的python版本为2.7，但目前的脚本并未出现兼容问题，因此可以正常使用，如果报错可以考虑此问题。