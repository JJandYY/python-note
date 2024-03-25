import py7zr
import zipfile
import rarfile

####################################
# 解压获取文件名
def un_zip(file_path):
    """
    解压zip包
    :param file_path:
    :return:
    """
    try:
        if not zipfile.is_zipfile(file_path):
            # logger.ERROR("File format error")
            return False, False
        zip_file = zipfile.ZipFile(file_path)
        # 压缩包内文件名，包含目录名
        dir_list = zip_file.namelist()
        zip_file.close()
    except Exception:
        # logger.ERROR(traceback.format_exc().replace('\n', ''))
        return False, False
    # 仅获取压缩包内文件名
    filename_list = list()
    if dir_list:
        filename_list = list(
            set([filename.rsplit('/', 1)[-1] for filename in dir_list if filename.rsplit('/', 1)[-1]]))
    return filename_list, dir_list


def un_rar(file_path):
    """
    解压rar包
    :param file_path:
    :return:
    """
    try:
        if not rarfile.is_rarfile(file_path):
            # logger.ERROR("File format error")
            return False, False
        rar_file = rarfile.RarFile(file_path)
        # 压缩包内文件名，包含目录名
        dir_list = rar_file.namelist()
        rar_file.close()
    except Exception:
        # logger.ERROR(traceback.format_exc().replace('\n', ''))
        return False, False
    # 仅获取压缩包内文件名
    filename_list = list()
    if dir_list:
        filename_list = list(
            set([filename.rsplit('/', 1)[-1] for filename in dir_list if filename.rsplit('/', 1)[-1]]))
    return filename_list, dir_list


def un_7z(file_path):
    """
    解压7z包
    :param file_path:
    :return:
    """
    try:
        if not py7zr.is_7zfile(file_path):
            # logger.ERROR("File format error")
            return False, False
        with py7zr.SevenZipFile(file_path, 'r') as f:
            files_info = f.files

        dir_list = [item.filename for item in files_info]
        dir_list.sort()
    except Exception:
        # logger.ERROR(traceback.format_exc().replace('\n', ''))
        return False, False
    # 仅获取压缩包内文件名
    filename_list = list()
    if dir_list:
        filename_list = list(
            set([filename.rsplit('/', 1)[-1] for filename in dir_list if filename.rsplit('/', 1)[-1]]))
    return filename_list, dir_list

####################################
# 转码
def trans_code(filename_list):
    """
    转码
    :param filename_list:
    :return:
    """
    for index in range(len(filename_list) - 1, -1, -1):
        try:
            filename_list[index] = filename_list[index].encode('cp437').decode('gbk')
        except UnicodeDecodeError:
            filename_list[index] = filename_list[index].encode('cp437').decode('utf-8')
        except UnicodeEncodeError:
            filename_list[index] = filename_list[index].encode('utf-8').decode('utf-8')
        except Exception:
            # logger.ERROR(traceback.format_exc().replace('\n', ''))
            return False
    return True


####################################
# 组装目录树
def directory_zip_tree(filename_list, save_file):
    """
    组装zip目录树
    :param filename_list:
    :param save_file:
    :return:
    """
    for a_item in filename_list:
        a_str = ""
        a_list = a_item.split("/")
        a_len = len(a_list)
        end = a_list.pop(-1)
        if end == "":
            a_len = len(a_list)
            end = a_list.pop(-1)
        if a_len > 1:
            nt = '    |' * (a_len - 1) + '-' * (a_len - 1)
            a_str = a_str + nt + end
        else:
            a_str = a_str + end
        a_str += '\r\n'
        save_file.write(a_str.encode())
    return True


def directory_7z_rar_tree(filename_list, save_file):
    """
    组装7z,rar目录树
    :param filename_list:
    :param save_file:
    :return:
    """
    str_list = list()
    for a_item in filename_list:
        a_list = a_item.split("/")
        for index, a_list_item in enumerate(a_list):
            a_str = ""
            str_1 = a_list_item + "/"
            if str_1 not in str_list:
                if index > 0:
                    a_str = a_str + '    |' * index + '-' * index + a_list_item
                    a_str += "\r\n"
                else:
                    a_str = a_str + a_list_item
                    a_str += "\r\n"
            str_list.append(str_1)
            save_file.write(a_str.encode())
    return True
