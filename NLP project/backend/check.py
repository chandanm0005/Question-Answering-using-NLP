import traceback
import sys

try:
    import torch
    print("Torch imported successfully! Version:", torch.__version__)
except Exception as e:
    print("Failed to import torch.")
    traceback.print_exc()

try:
    import tensorflow as tf
    print("Tensorflow imported successfully! Version:", tf.__version__)
except Exception as e:
    print("Failed to import tensorflow.")
