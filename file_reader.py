import os

def read_file(filepath: str) -> str:
    if not filepath or not filepath.strip():
        raise ValueError("文件路径不能为空")

    abs_path = os.path.abspath(filepath)

    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"文件不存在: {abs_path}")

    if not os.path.isfile(abs_path):
        raise ValueError(f"路径不是文件: {abs_path}")

    supported_extensions = ('.txt', '.md', '.json')
    _, ext = os.path.splitext(abs_path)
    if ext.lower() not in supported_extensions:
        raise ValueError(f"不支持的文件格式: {ext}，仅支持 {', '.join(supported_extensions)}")

    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            raise ValueError("文件内容为空")
        return content
    except UnicodeDecodeError:
        try:
            with open(abs_path, 'r', encoding='gbk') as f:
                content = f.read()
            if not content.strip():
                raise ValueError("文件内容为空")
            return content
        except Exception as e:
            raise ValueError(f"文件编码错误，无法读取: {e}")
    except Exception as e:
        raise ValueError(f"读取文件失败: {e}")