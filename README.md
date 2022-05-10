本库为Abaqus python脚本储存库，其中包含微结构的生成脚本、后处理脚本、数据转换脚本。
# 版本解释
$\bullet$ Layup.py:为前处理及部分后处理脚本，包括模型前处理（Part、Property等基本模块）、提交Job、对odb文件数据的处理。

$\bullet$ PostProcessing.py:为后处理脚本，因为在提交作业计算完成后，odb可能生成不及时，而Layup脚本的命令执行速度又快，会报错。因此，将后处理单独分离出来，将后处理得出的数据导出保存为txt格式。

$\bullet$ DataToExcel.py:由于Data.txt文件转换需要openpyxl库，而目前没有解决abaqus运行脚本对第三方库报错的问题，因此，需要单独将Data.txt转换为Excel表格写一个脚本。
# 脚本代码解释
## Layup.py
