import os
import zipfile

# 设置源目录和目标目录的路径
source_dir = '/mnt/geogpt-gpfs/llm-course/ossutil_output/public/tianwen/datasets/books/mmd-en'
target_dir = '/mnt/geogpt-gpfs/llm-course/ossutil_output/public/tianwen/datasets/books/pdf-en/11'

# 用于存储所有需要打包的文件路径的列表
files_to_zip = []

# 遍历目标目录中的所有文件
for file_name in os.listdir(target_dir):
    # 构造目标文件的完整路径
    target_file_path = os.path.join(target_dir, file_name)
    
    # 检查目标文件是否为文件，并且文件名以.pdf结尾
    if os.path.isfile(target_file_path) and file_name.endswith('.pdf'):
        # 从文件名中去除.pdf后缀，获取基础名
        base_name_without_suffix = os.path.splitext(file_name)[0]
        
        # 检查源目录中是否存在同名的子目录
        if os.path.isdir(os.path.join(source_dir, base_name_without_suffix)):
            # 添加到列表中
            files_to_zip.append(target_file_path)

# 创建压缩文件的路径
zip_file_path = os.path.join(target_dir, 'matched_pdfs.zip')

# 创建压缩文件
with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file_path in files_to_zip:
        # 添加文件到压缩文件中
        zipf.write(file_path, os.path.basename(file_path))
        print(f"Added to zip: {file_path}")

# 删除源文件
for file_path in files_to_zip:
    # 这里删除的是目标目录中的PDF文件，因为它们已经被压缩
    os.remove(file_path)
    print(f"Deleted: {file_path}")

print("Cleanup complete.")