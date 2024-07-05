import yaml
import hashlib

def load_yaml_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def generate_hash(*args):
    """Generate a hash for the given arguments."""
    hasher = hashlib.sha256()
    for arg in args:
        hasher.update(str(arg).encode())
    return hasher.hexdigest()

