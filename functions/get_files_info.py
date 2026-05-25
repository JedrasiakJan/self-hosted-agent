import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(absolute_path, directory))
        valid_target_dir = os.path.commonpath([absolute_path, target_directory]) == absolute_path 
        
        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'
            
        items = os.listdir(target_directory)
        lines = []
        for item in items:
            item_path = os.path.join(target_directory, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(lines)

    except Exception as e:
        return f'Error: {str(e)}'
