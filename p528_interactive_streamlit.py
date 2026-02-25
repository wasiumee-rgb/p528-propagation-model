"""
Interactive ITU-R P.528 Propagation Model Dashboard
Run with: streamlit run p528_interactive_streamlit.py
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import special

# Page configuration
st.set_page_config(
    page_title="P.528 Propagation Curves",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

class P528PropagationModel:
    """
    ITU-R P.528 propagation model for air-to-ground communications
    """
    
    def __init__(self):
        """Initialize model parameters"""
        self.c = 3e8  # Speed of light (m/s)
        
    def free_space_path_loss(self, distance_km, frequency_mhz):
        """
        Calculate free space path loss (Friis equation)
        PL(dB) = 20*log10(4*pi*d*f/c)
        """
        if distance_km <= 0:
            return 0
        distance_m = distance_km * 1000
        frequency_hz = frequency_mhz * 1e6
        path_loss = 20 * np.log10(4 * np.pi * distance_m * frequency_hz / self.c)
        return path_loss
    
    def ground_reflection_factor(self, distance_km, frequency_mhz, tx_height_m, rx_height_m, ground_conductivity):
        """
        Calculate ground reflection factor based on distance and antenna heights
        """
        if distance_km <= 0:
            return 0
        
        distance_m = distance_km * 1000
        wavelength_m = self.c / (frequency_mhz * 1e6)
        
        # Path difference for ground-reflected ray
        path_diff = 2 * (tx_height_m * rx_height_m) / distance_m
        
        # Phase difference
        phase = 2 * np.pi * path_diff / wavelength_m
        
        # Reflection coefficient (depends on ground conductivity)
        # Higher conductivity → stronger reflection
        reflection_coeff = min(0.95, 0.5 + ground_conductivity / 100)
        
        # Combined signal (direct + reflected)
        # Using phasor addition
        combined = np.sqrt(1 + reflection_coeff**2 + 2*reflection_coeff*np.cos(phase))
        
        return 20 * np.log10(combined)
    
    def p528_path_loss(self, distance_km, frequency_mhz, tx_height_m=10, 
                      rx_height_m=1000, ground_conductivity=50, atmospheric_absorption=0):
        """
        Calculate total ITU-R P.528 path loss
        """
        if distance_km <= 0:
            return 0
        
        # Free space path loss
        pl_free = self.free_space_path_loss(distance_km, frequency_mhz)
        
        # Ground reflection factor
        reflection_factor = self.ground_reflection_factor(
            distance_km, frequency_mhz, tx_height_m, rx_height_m, ground_conductivity
        )
        
        # Atmospheric absorption loss (simplified)
        # increases with frequency and distance
        atm_loss = atmospheric_absorption * distance_km * (frequency_mhz / 1000)**2
        
        # Total path loss
        total_loss = pl_free + reflection_factor + atm_loss
        return total_loss
    
    def generate_curves(self, frequencies_mhz, max_distance_km=200, 
                       tx_height_m=10, rx_height_m=1000, 
                       ground_conductivity=50, atmospheric_absorption=0, 
                       num_points=150):
        """Generate propagation curves"""
        distances = np.linspace(1, max_distance_km, num_points)
        path_losses = {}
        
        for freq in frequencies_mhz:
            losses = [self.p528_path_loss(d, freq, tx_height_m, rx_height_m, 
                                         ground_conductivity, atmospheric_absorption)
                     for d in distances]
            path_losses[freq] = np.array(losses)
        
        return distances, path_losses


# Initialize model
model = P528PropagationModel()

# Title
st.title("📡 ITU-R P.528 Air-to-Ground Propagation Model")
st.markdown("**Interactive Dashboard for Aeronautical Mobile Communications**")
st.markdown("---")

# Create three columns: sidebar parameters, main plot, and statistics
col_params, col_plot = st.columns([1, 2.5])

with col_params:
    st.subheader("⚙️ Configuration")
    
    # Frequency selection
    st.write("**Frequencies (MHz)**")
    freq1_col, freq1_en = st.columns([3, 1])
    with freq1_col:
        freq1 = st.number_input("F1", value=118, min_value=100, max_value=1000, step=1, label_visibility="collapsed")
    with freq1_en:
        freq1_enabled = st.checkbox("✓", value=True, key="freq1", label_visibility="collapsed")
    
    freq2_col, freq2_en = st.columns([3, 1])
    with freq2_col:
        freq2 = st.number_input("F2", value=136, min_value=100, max_value=1000, step=1, label_visibility="collapsed")
    with freq2_en:
        freq2_enabled = st.checkbox("✓", value=True, key="freq2", label_visibility="collapsed")
    
    freq3_col, freq3_en = st.columns([3, 1])
    with freq3_col:
        freq3 = st.number_input("F3", value=242, min_value=100, max_value=1000, step=1, label_visibility="collapsed")
    with freq3_en:
        freq3_enabled = st.checkbox("✓", value=True, key="freq3", label_visibility="collapsed")
    
    freq4_col, freq4_en = st.columns([3, 1])
    with freq4_col:
        freq4 = st.number_input("F4", value=400, min_value=100, max_value=1000, step=1, label_visibility="collapsed")
    with freq4_en:
        freq4_enabled = st.checkbox("✓", value=True, key="freq4", label_visibility="collapsed")
    
    # Collect enabled frequencies
    frequencies = []
    if freq1_enabled:
        frequencies.append(freq1)
    if freq2_enabled:
        frequencies.append(freq2)
    if freq3_enabled:
        frequencies.append(freq3)
    if freq4_enabled:
        frequencies.append(freq4)
    
    st.divider()
    
    # Distance range
    st.write("**Distance Range**")
    max_distance = st.slider(
        "Maximum Distance",
        min_value=50, max_value=500, value=200, step=10, label_visibility="collapsed"
    )
    
    st.divider()
    
    # Antenna heights
    st.write("**Antenna Heights**")
    tx_height = st.slider(
        "TX Height (Ground Station)",
        min_value=1, max_value=500, value=10, step=5, label_visibility="collapsed"
    )
    st.caption(f"📍 TX: {tx_height}m")
    
    rx_height = st.slider(
        "RX Height (Aircraft Altitude)",
        min_value=100, max_value=15000, value=1000, step=100, label_visibility="collapsed"
    )
    st.caption(f"✈️ RX: {rx_height}m")
    
    st.divider()
    
    # Environmental parameters
    st.write("**Environment**")
    ground_conductivity = st.slider(
        "Ground Conductivity",
        min_value=10, max_value=100, value=50, step=5, label_visibility="collapsed"
    )
    st.caption(f"🌍 {ground_conductivity}% (dry land ≈20%, salt water ≈100%)")
    
    atmospheric_abs = st.slider(
        "Atmospheric Absorption",
        min_value=0.0, max_value=1.0, value=0.1, step=0.05, label_visibility="collapsed"
    )
    st.caption(f"☁️ {atmospheric_abs:.2f} dB/km·GHz²")
    
    st.divider()
    
    # Resolution
    st.write("**Plot Resolution**")
    resolution = st.slider(
        "Number of Points",
        min_value=50, max_value=300, value=150, step=10, label_visibility="collapsed"
    )

# Generate data
if len(frequencies) > 0:
    distances, path_losses = model.generate_curves(
        frequencies_mhz=frequencies,
        max_distance_km=max_distance,
        tx_height_m=tx_height,
        rx_height_m=rx_height,
        ground_conductivity=ground_conductivity,
        atmospheric_absorption=atmospheric_abs,
        num_points=resolution
    )
    
    # Create plot
    with col_plot:
        fig, ax = plt.subplots(figsize=(12, 7))
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        
        for idx, freq in enumerate(frequencies):
            ax.plot(distances, path_losses[freq], 
                   label=f'{freq} MHz', 
                   linewidth=2.5,
                   color=colors[idx % len(colors)],
                   marker='o',
                   markersize=4,
                   markevery=max(1, len(distances)//15))
        
        # Customize plot
        ax.set_xlabel('Distance (km)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Path Loss (dB)', fontsize=12, fontweight='bold')
        ax.set_title(f'ITU-R P.528 Propagation Curves', fontsize=14, fontweight='bold', pad=15)
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
        ax.legend(fontsize=11, loc='upper left', framealpha=0.95, edgecolor='black')
        ax.set_xlim(0, max_distance)
        
        fig.patch.set_facecolor('white')
        st.pyplot(fig, use_container_width=True)

st.divider()

# Data table and statistics
if len(frequencies) > 0:
    col_table, col_stats = st.columns([1.5, 1])
    
    with col_table:
        st.subheader("📋 Path Loss Values")
        
        distance_select = st.select_slider(
            "Distance (km):",
            options=[int(d) for d in distances[::max(1, len(distances)//20)]],
            value=int(distances[len(distances)//2]),
            label_visibility="collapsed"
        )
        
        # Find closest distance index
        closest_idx = np.argmin(np.abs(distances - distance_select))
        
        # Create table data
        table_data = []
        for freq in frequencies:
            pl = path_losses[freq][closest_idx]
            table_data.append({"Frequency": f"{freq} MHz", "Path Loss": f"{pl:.2f} dB"})
        
        st.dataframe(table_data, use_container_width=True, hide_index=True)
    
    with col_stats:
        st.subheader("📊 Statistics")
        
        for idx, freq in enumerate(frequencies):
            max_loss = np.max(path_losses[freq])
            min_loss = np.min(path_losses[freq])
            avg_loss = np.mean(path_losses[freq])
            
            with st.expander(f"{freq} MHz", expanded=(idx==0)):
                st.metric("Max Loss", f"{max_loss:.1f} dB")
                st.metric("Min Loss", f"{min_loss:.1f} dB")
                st.metric("Avg Loss", f"{avg_loss:.1f} dB")

# Configuration summary
st.divider()
st.subheader("⚙️ Current Configuration Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"""
    **Transmitter Setup**
    - Height: {tx_height} m
    - Frequencies: {', '.join([f'{f} MHz' for f in frequencies]) if frequencies else 'None selected'}
    """)

with col2:
    st.info(f"""
    **Receiver Setup**
    - Altitude: {rx_height} m
    - Distance Range: 1 - {max_distance} km
    - Resolution: {resolution} points
    """)

with col3:
    st.info(f"""
    **Environmental**
    - Ground Conductivity: {ground_conductivity}%
    - Atmospheric Absorption: {atmospheric_abs:.2f} dB/km·GHz²
    """)

st.divider()

# Help section
with st.expander("ℹ️ About P.528 Model"):
    st.markdown("""
    ### ITU-R P.528 Propagation Model
    
    The ITU-R P.528 recommendation provides methods for predicting the propagation of radio waves 
    for air-to-ground communications in the aeronautical mobile service.
    
    **Key Components:**
    - **Free Space Path Loss**: Initial attenuation based on distance and frequency
    - **Ground Reflection**: Accounts for multipath effects from ground reflections
    - **Atmospheric Absorption**: Additional loss due to oxygen, water vapor, and precipitation
    
    **Ground Conductivity Reference:**
    - Fresh water: ~10-30%
    - Land/soil: ~10-30%
    - Sea water: ~80-100%
    
    **Typical Aviation Frequencies:**
    - VHF: 118-136 MHz (commercial aviation voice)
    - UHF: 225-400 MHz (military, navigation)
    
    **Height Ranges:**
    - Ground stations: 1-100m
    - Aircraft: 100-15000m (cruise altitude for commercial aircraft ~10000m)
    """)
