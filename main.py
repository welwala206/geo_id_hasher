import hashlib
import pandas as pd
import re
import argparse
import os

class FileProcessor:
    def __init__(self, path):
        self.path = path

    def hash_id(self, id):
        return hashlib.sha3_512(str(id).encode()).hexdigest()

    def read_xlsx(self, file_path):
        return pd.read_excel(file_path, dtype=str)

    def write_xlsx(self, file_path, data):
        data.to_excel(file_path, index=False)

    def read_csv(self, file_path):
        return pd.read_csv(file_path, dtype=str, encoding='utf-8')

    def write_csv(self, file_path, data):
        data.to_csv(file_path, index=False)

    def replace_id_in_data(self, data):
        id_pattern = re.compile(r'^\d{11}$')
        for column in data.columns:
            if data[column].apply(lambda x: bool(id_pattern.match(str(x)))).any():
                data[column] = data[column].apply(self.hash_id)
        return data

    def process_file(self, file_path):
        file_name = os.path.basename(file_path)
        dir_name = os.path.dirname(file_path)
        output_file_path = os.path.join(dir_name, "hashed_" + file_name)
        
        if file_path.endswith('.csv'):
            data = self.read_csv(file_path)
            data = self.replace_id_in_data(data)
            self.write_csv(output_file_path, data)
        elif file_path.endswith('.xlsx'):
            data = self.read_xlsx(file_path)
            data = self.replace_id_in_data(data)
            self.write_xlsx(output_file_path, data)
        else:
            print("Unsupported file format")

    def process_directory(self, directory_path):
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if file_path.endswith('.csv') or file_path.endswith('.xlsx'):
                self.process_file(file_path)

    def run(self):
        if os.path.isdir(self.path):
            self.process_directory(self.path)
        else:
            self.process_file(self.path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a CSV or XLSX file or all such files in a directory.')
    parser.add_argument('path', type=str, help='Path to the CSV or XLSX file or directory containing such files')
    args = parser.parse_args()
    processor = FileProcessor(args.path)
    processor.run()