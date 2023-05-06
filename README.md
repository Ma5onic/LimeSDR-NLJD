# Software-Based Non-Linear Junction Detector (NLJD)

A Non-Linear Junction Detector (NLJD) is a counter-surveillance tool commonly used for detecting hidden transmitters or other electronic items. This project aims to develop a software-based NLJD using a LimeSDR device, improving upon the traditional hardware-based NLJD by offering greater flexibility and ease of use.

## Overview

The software-based NLJD works by transmitting a clean, unmodulated RF signal at the target location and analyzing the received signal strengths of the detected second and third harmonics. By comparing the received signal strengths of these two harmonics, the operator can determine if the target location contains a dissimilar metal non-linear junction, such as rusty nails, or an actual P-N junction, like a diode or transistor.

## Benefits of a Software-Based NLJD

The software-based NLJD offers several improvements over traditional hardware-based NLJDs:

1.  **Ease of construction**: The use of a LimeSDR device simplifies the construction process, eliminating the need for sourcing rare or hard-to-find components.
2.  **Flexibility**: The software-based approach allows for easy updates and improvements to the system, as well as the potential for incorporating additional features.
3.  **Cost-effectiveness**: By using a LimeSDR device and open-source software, the overall cost of the project can be significantly reduced compared to traditional hardware-based solutions.

## How It Works

The software-based NLJD relies on the same principles as a traditional hardware-based NLJD. It uses a LimeSDR device to transmit a clean, unmodulated RF signal at the target location, and then analyzes the received signal strengths of the detected second and third harmonics.

By comparing the signal strengths and any modulations of the different harmonics generated, it is possible to differentiate between a true semiconductor P-N junction and a "nature junction" created between two dissimilar metals and a catalyst. True semiconductor P-N junctions tend to generate strong even harmonics (2nd, 4th, 6th, etc.), while dissimilar metals tend to create strong odd harmonics (3rd, 5th, 7th, etc.).

Additionally, a harmonic signal from a true semiconductor P-N junction will be "quiet" when audio demodulated, since the illumination RF carrier is clean and unmodulated, and those even-order harmonics will also be clean and unmodulated. In contrast, the odd-order harmonics from dissimilar metals will tend to be "noisy" or "scratchy" when audio demodulated.

## Project Structure

The software-based NLJD project will be built and documented as individual modules. This allows for time to test and develop all the components for the project, ensuring a reliable and effective solution.

## Additional Notes

While the software-based approach simplifies the construction process, it is still essential to consider isolation when working with radio projects of this type. This involves using well-shielded module boxes, double-shielded coax, and high-quality RF connectors to minimize interference and maximize performance.
