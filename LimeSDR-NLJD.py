#This code is untested and provided "as is". Follow the laws when transmitting signals.
#It is just a template for how NLJ detection could theoretically be performed with an SDR
"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

GNU Affero General Public License v3.0 summary:

Permissions:
- Commercial use
- Distribution
- Modification
- Patent use
- Private use

Conditions:
- Disclose source: Source code must be made available when the licensed material is distributed.
- License and copyright notice: A copy of the license and copyright notice must be included with the licensed material.
- Network use is distribution: Users who interact with the licensed material via network are given the right to receive a copy of the source code.
- Same license: Modifications must be released under the same license when distributing the licensed material. In some cases, a similar or related license may be used.
- State changes: Changes made to the licensed material must be documented.

Limitations:
- Liability: This license includes a limitation of liability.
- Warranty: This license explicitly states that it does NOT provide any warranty.

"""

import numpy as np
import time
from scipy.signal import chirp, find_peaks, stft
from pyLMS7002M import LimeSDR
import threading
import queue

# Constants
SAMPLE_RATE = 20e6  # Sample rate for SDR device
FREQUENCY_BANDS = [  # Frequency bands to be scanned
    (2.4e9, 2.4835e9),
    (5.15e9, 5.35e9),
]
NUM_SAMPLES = 1000000  # Number of samples per signal
THRESHOLD = 50  # Threshold for peak detection
AMPLITUDE = 20  # Amplitude of transmitted signal
WINDOW_SIZE = 256  # Window size for STFT
OVERLAP = 128  # Overlap between windows for STFT
SLEEP_TIME = 0.1  # Sleep time between operations


def setup_limesdr():
    limesdr_device = LimeSDR()
    if limesdr_device.connect():
        limesdr_device.configure(FREQUENCY_BANDS[0][0], SAMPLE_RATE, 'auto', 'auto')
    return limesdr_device

def generate_signal(frequency_start, frequency_end):
    t = np.linspace(0, NUM_SAMPLES / SAMPLE_RATE, NUM_SAMPLES)
    spread_spectrum_signal = chirp(t, f0=frequency_start, f1=frequency_end, t1=t[-1], method='quadratic')
    modulated_signal = AMPLITUDE * np.exp(1j * 2 * np.pi * spread_spectrum_signal * t)
    return modulated_signal.astype(np.complex64).tobytes()

def analyze_received_signal(signal):
    _, _, Zxx = stft(signal, fs=SAMPLE_RATE, window='hann', nperseg=WINDOW_SIZE, noverlap=OVERLAP)
    magnitude = np.abs(Zxx)
    peaks, _ = find_peaks(magnitude.flatten(), threshold=THRESHOLD)
    return peaks, magnitude

def transmitter(limesdr_device, signal_queue):
    while True:
        spread_spectrum_signal = signal_queue.get()
        limesdr_device.transmit_and_receive(spread_spectrum_signal, NUM_SAMPLES)
        time.sleep(SLEEP_TIME)

def receiver(limesdr_device, analysis_queue):
    while True:
        received_signal = limesdr_device.rx_buffer
        received_signal = np.frombuffer(received_signal, dtype=np.complex64)
        analysis_queue.put(received_signal)
        time.sleep(SLEEP_TIME)

def analyzer(analysis_queue):
    while True:
        received_signal = analysis_queue.get()
        peaks, magnitude = analyze_received_signal(received_signal)

        # Identify second and third harmonics
        second_harmonic_peaks = []
        third_harmonic_peaks = []

        for peak in peaks:
            freq = peak * SAMPLE_RATE / NUM_SAMPLES
            for band in FREQUENCY_BANDS:
                if band[0] * 2 <= freq <= band[1] * 2:
                    second_harmonic_peaks.append(peak)
                elif band[0] * 3 <= freq <= band[1] * 3:
                    third_harmonic_peaks.append(peak)

        # Print the results
        print("Second harmonic peaks detected at:")
        for peak in second_harmonic_peaks:
            print(f"{peak * SAMPLE_RATE / NUM_SAMPLES} Hz")

        print("\nThird harmonic peaks detected at:")
        for peak in third_harmonic_peaks:
            print(f"{peak * SAMPLE_RATE / NUM_SAMPLES} Hz")

        time.sleep(SLEEP_TIME)

def main():
    limesdr_device = setup_limesdr()

    signal_queue = queue.Queue()
    analysis_queue = queue.Queue()

    transmitter_thread = threading.Thread(target=transmitter, args=(limesdr_device, signal_queue))
    receiver_thread = threading.Thread(target=receiver, args=(limesdr_device, analysis_queue))
    analyzer_thread = threading.Thread(target=analyzer, args=(analysis_queue,))

    transmitter_thread.start()
    receiver_thread.start()
    analyzer_thread.start()

    FREQUENCY_SETTLING_TIME = 0.2

    try:
        while True:
            for band in FREQUENCY_BANDS:
                # Set the frequency and wait for it to settle
                limesdr_device.set_frequency(band[0])
                time.sleep(FREQUENCY_SETTLING_TIME)

                spread_spectrum_signal = generate_signal(band[0], band[1])
                signal_queue.put(spread_spectrum_signal)
                time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        print("Stopping...")

    transmitter_thread.join()
    receiver_thread.join()
    analyzer_thread.join()

    limesdr_device.disconnect()

if __name__ == "__main__":
    main()
