import os


def list_all_files_recursive(folder_path):
    # 하위 폴더까지 포함한 모든 파일 리스트 가져오기
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            if '.DS_Store' in filename:
                continue
            files.append(os.path.join(root, filename))
    return files
