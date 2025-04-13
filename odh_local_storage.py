import json
import os
import threading
import gzip
import base64

class ODHLocalStorage:
    def __init__(self, db_name="odh_local_storage.db"):
        self.db_name = db_name
        self.lock = threading.Lock()
        self._load_data()

    def _load_data(self):
        with self.lock:
            try:
                with open(self.db_name, 'r') as f:
                    data = f.read()
                    if data:
                        self.data = json.loads(data)
                    else:
                        self.data = {}
            except FileNotFoundError:
                self.data = {}
            except json.JSONDecodeError:
                print("Error: Database file is corrupted. Starting with an empty database.")
                self.data = {}

    def _save_data(self):
        with self.lock:
            try:
                with open(self.db_name, 'w') as f:
                    json.dump(self.data, f, indent=4)
            except Exception as e:
                print(f"Error saving data to file: {e}")

    def set_item(self, key, value):
        with self.lock:
            self.data[key] = value
            self._save_data()

    def get_item(self, key, default=None):
        with self.lock:
            return self.data.get(key, default)

    def remove_item(self, key):
        with self.lock:
            if key in self.data:
                del self.data[key]
                self._save_data()

    def clear(self):
        with self.lock:
            self.data = {}
            self._save_data()

    def keys(self):
        with self.lock:
            return list(self.data.keys())

    def __len__(self):
        with self.lock:
            return len(self.data)

    def compress_and_set(self, key, value):
        with self.lock:
            # Convert value to JSON string
            value_str = json.dumps(value)
            # Compress the string
            compressed_data = gzip.compress(value_str.encode('utf-8'))
            # Encode the compressed data to base64
            base64_encoded_data = base64.b64encode(compressed_data).decode('utf-8')
            self.data[key] = base64_encoded_data
            self._save_data()

    def get_and_decompress(self, key):
        with self.lock:
            base64_encoded_data = self.data.get(key)
            if base64_encoded_data:
                # Decode the base64 encoded data
                compressed_data = base64.b64decode(base64_encoded_data.encode('utf-8'))
                # Decompress the data
                decompressed_data = gzip.decompress(compressed_data).decode('utf-8')
                # Load the JSON string
                return json.loads(decompressed_data)
            else:
                return None

if __name__ == '__main__':
    db = ODHLocalStorage("odh_storage.db")

    # Test basic set and get
    db.set_item("name", "ODH User")
    print(f"Name: {db.get_item('name')}")

    # Test compression
    complex_data = {"employees": [{"name": "John", "id": 1}, {"name": "Jane", "id": 2}]}
    db.compress_and_set("complex_data", complex_data)
    retrieved_data = db.get_and_decompress("complex_data")
    print(f"Retrieved data: {retrieved_data}")

    # Test remove
    db.remove_item("name")
    print(f"Name after remove: {db.get_item('name')}")

    # Test clear
    db.clear()
    print(f"Keys after clear: {db.keys()}")
