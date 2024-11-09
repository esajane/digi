import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Parameters
bit_duration = 1 
sample_rate = 1000  

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def nrz_l(binary_data):
    signal = []
    for bit in binary_data:
        signal.extend([1 if bit == '1' else -1] * int(bit_duration * sample_rate))
    return signal

def nrz_i(binary_data, initial_high):
    signal = []
    current_level = 1 if initial_high else -1
    for bit in binary_data:
        if bit == '1':
            current_level *= -1
        signal.extend([current_level] * int(bit_duration * sample_rate))
    return signal

def bipolar_ami(binary_data, initial_high):
    signal = []
    last_nonzero = 1 if initial_high else -1
    for bit in binary_data:
        if bit == '1':
            last_nonzero *= -1
            signal.extend([last_nonzero] * int(bit_duration * sample_rate))
        else:
            signal.extend([0] * int(bit_duration * sample_rate))
    return signal

def pseudoternary(binary_data, initial_high):
    signal = []
    last_nonzero = 1 if initial_high else -1
    for bit in binary_data:
        if bit == '0':
            last_nonzero *= -1
            signal.extend([last_nonzero] * int(bit_duration * sample_rate))
        else:
            signal.extend([0] * int(bit_duration * sample_rate))
    return signal

def manchester(binary_data):
    signal = []
    for bit in binary_data:
        if bit == '1':
            signal.extend([1] * int(bit_duration * sample_rate / 2) + [-1] * int(bit_duration * sample_rate / 2))
        else:
            signal.extend([-1] * int(bit_duration * sample_rate / 2) + [1] * int(bit_duration * sample_rate / 2))
    return signal

def differential_manchester(binary_data, initial_high):
    signal = []
    current_level = 1 if initial_high else -1
    for bit in binary_data:
        if bit == '1':
            signal.extend([current_level] * int(bit_duration * sample_rate / 2) + [-current_level] * int(bit_duration * sample_rate / 2))
        else:
            current_level *= -1
            signal.extend([current_level] * int(bit_duration * sample_rate / 2) + [-current_level] * int(bit_duration * sample_rate / 2))
    return signal

# Streamlit app
st.title("Digital Signal Encoding Visualizer")
message = st.text_input("Enter a message to encode:")
encoding_type = st.selectbox("Select Encoding Type", ["NRZ-L", "NRZ-I", "Bipolar AMI", "Pseudoternary", "Manchester", "Differential Manchester"])

if encoding_type in ["NRZ-I", "Differential Manchester", "Bipolar AMI", "Pseudoternary"]:
    initial_level = st.selectbox("Select Initial Level", ["High", "Low"])
    initial_high = initial_level == "High"
else:
    initial_high = None  

if message:
    binary_data = text_to_binary(message)
    st.write(f"Binary Representation: {binary_data}")

    
    if encoding_type == "NRZ-L":
        signal = nrz_l(binary_data)
    elif encoding_type == "NRZ-I":
        signal = nrz_i(binary_data, initial_high)
    elif encoding_type == "Bipolar AMI":
        signal = bipolar_ami(binary_data, initial_high)
    elif encoding_type == "Pseudoternary":
        signal = pseudoternary(binary_data, initial_high)
    elif encoding_type == "Manchester":
        signal = manchester(binary_data)
    elif encoding_type == "Differential Manchester":
        signal = differential_manchester(binary_data, initial_high)
    else:
        st.write("Encoding not implemented.")
        signal = []

    if signal:
        time = np.arange(0, len(signal) / sample_rate, 1 / sample_rate)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.step(time, signal, where='post')
        ax.set_title(f"{encoding_type} Encoding")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.grid(True)
        
        st.pyplot(fig)
