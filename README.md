# ITU-R P.528 Air-to-Ground Propagation Model

An interactive Streamlit dashboard for generating and visualizing propagation curves using the ITU-R P.528 recommendation for aeronautical mobile communications.

## 📡 Overview

This application implements the ITU-R P.528 propagation model with real-time parameter adjustment capabilities. It allows users to:

- **Visualize propagation curves** for multiple frequencies simultaneously
- **Adjust parameters in real-time**:
  - Frequency selection (100-1000 MHz)
  - Transmitter height (1-500m)
  - Receiver altitude (100-15000m)
  - Ground conductivity (10-100%)
  - Atmospheric absorption
  - Distance range and plot resolution
- **View detailed statistics** and path loss values
- **Export results** for further analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/wasiumee-rgb/p528-propagation-model.git
cd p528-propagation-model
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run p528_interactive_streamlit.py
```

4. Open your browser to `http://localhost:8501`

## 📊 Features

### Model Components
- **Free Space Path Loss**: Friis equation-based calculation
- **Ground Reflection Factor**: Two-ray ground reflection model
- **Atmospheric Absorption**: Frequency and distance-dependent attenuation

### Interactive Controls
- 🎚️ **Sliders**: Smooth parameter adjustment
- ☑️ **Checkboxes**: Enable/disable frequency curves
- 📊 **Real-time Plotting**: Instant graph updates
- 📋 **Data Tables**: Detailed path loss values

### Display Options
- High-quality matplotlib plots
- Color-coded frequency curves
- Configuration summary
- Statistics (min, max, average loss)
- Distance-based lookup table

## 🛠️ Configuration Parameters

### Frequencies
- Range: 100-1000 MHz
- Typical aviation bands:
  - VHF: 118-136 MHz (commercial aviation)
  - UHF: 225-400 MHz (military, navigation)

### Antenna Heights
- **TX Height** (Ground Station): 1-500m
  - Typical values: 10-50m
- **RX Height** (Aircraft): 100-15000m
  - Typical values: 1000-10000m for commercial aircraft

### Environmental Parameters
- **Ground Conductivity**: 10-100%
  - Dry land: ~20%
  - Fresh water: ~10-30%
  - Sea water: ~80-100%
- **Atmospheric Absorption**: 0.0-1.0 dB/km·GHz²

## 📚 ITU-R P.528 Background

The ITU-R P.528 recommendation (Propagation curves for aeronautical mobile and radionavigation services in the frequency range 125 kHz to 15.5 GHz) provides:

- Methods for predicting radio wave propagation for air-to-ground communications
- Path loss calculations based on frequency, distance, and antenna heights
- Accounting for ground reflection and atmospheric effects

### Key References
- ITU-R P.528-5: Propagation curves for aeronautical mobile and radionavigation services
- Free space path loss: Friis transmission equation
- Ground reflection: Two-ray propagation model

## 🔧 Customization

### Adding New Features
- Modify frequency ranges in the Streamlit interface
- Adjust model parameters in the `P528PropagationModel` class
- Add new propagation models (P.529, P.618, etc.)

### Extending the Model
```python
# Example: Add rain attenuation
def rain_attenuation(self, frequency_mhz, rainfall_rate_mm_per_hour):
    # Implementation here
    pass
```

## 📈 Example Use Cases

1. **Aviation Planning**: Predict communication range for ground-to-aircraft systems
2. **Network Coverage**: Plan VHF/UHF communication networks
3. **System Design**: Evaluate antenna placement and frequency selection
4. **Research**: Study propagation effects at different altitudes and frequencies

## 📝 License

This project is provided as-is for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report issues
- Suggest enhancements
- Submit pull requests

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

## 🙏 Acknowledgments

- ITU-R for the P.528 recommendation
- Streamlit team for the excellent web app framework
- NumPy, Matplotlib, and SciPy communities

---

**Last Updated**: 2026-02-25
**Version**: 1.0.0
