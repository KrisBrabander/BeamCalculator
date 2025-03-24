import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import os
import base64
from plotly.subplots import make_subplots

# Profiel bibliotheken
# HEA profielen (h, b, tw, tf)
HEA_PROFILES = {
    "HEA 100": (96, 100, 5.0, 8.0),
    "HEA 120": (114, 120, 5.0, 8.0),
    "HEA 140": (133, 140, 5.5, 8.5),
    "HEA 160": (152, 160, 6.0, 9.0),
    "HEA 180": (171, 180, 6.0, 9.5),
    "HEA 200": (190, 200, 6.5, 10.0),
    "HEA 220": (210, 220, 7.0, 11.0),
    "HEA 240": (230, 240, 7.5, 12.0),
    "HEA 260": (250, 260, 7.5, 12.5),
    "HEA 280": (270, 280, 8.0, 13.0),
    "HEA 300": (290, 300, 8.5, 14.0),
}

# HEB profielen (h, b, tw, tf)
HEB_PROFILES = {
    "HEB 100": (100, 100, 6.0, 10.0),
    "HEB 120": (120, 120, 6.5, 11.0),
    "HEB 140": (140, 140, 7.0, 12.0),
    "HEB 160": (160, 160, 8.0, 13.0),
    "HEB 180": (180, 180, 8.5, 14.0),
    "HEB 200": (200, 200, 9.0, 15.0),
    "HEB 220": (220, 220, 9.5, 16.0),
    "HEB 240": (240, 240, 10.0, 17.0),
    "HEB 260": (260, 260, 10.0, 17.5),
    "HEB 280": (280, 280, 10.5, 18.0),
    "HEB 300": (300, 300, 11.0, 19.0),
}

# IPE profielen (h, b, tw, tf)
IPE_PROFILES = {
    "IPE 80": (80, 46, 3.8, 5.2),
    "IPE 100": (100, 55, 4.1, 5.7),
    "IPE 120": (120, 64, 4.4, 6.3),
    "IPE 140": (140, 73, 4.7, 6.9),
    "IPE 160": (160, 82, 5.0, 7.4),
    "IPE 180": (180, 91, 5.3, 8.0),
    "IPE 200": (200, 100, 5.6, 8.5),
    "IPE 220": (220, 110, 5.9, 9.2),
    "IPE 240": (240, 120, 6.2, 9.8),
    "IPE 270": (270, 135, 6.6, 10.2),
    "IPE 300": (300, 150, 7.1, 10.7),
}

# UNP profielen (h, b, tw, tf)
UNP_PROFILES = {
    "UNP 80": (80, 45, 6.0, 8.0),
    "UNP 100": (100, 50, 6.0, 8.5),
    "UNP 120": (120, 55, 7.0, 9.0),
    "UNP 140": (140, 60, 7.0, 10.0),
    "UNP 160": (160, 65, 7.5, 10.5),
    "UNP 180": (180, 70, 8.0, 11.0),
    "UNP 200": (200, 75, 8.5, 11.5),
    "UNP 220": (220, 80, 9.0, 12.5),
    "UNP 240": (240, 85, 9.5, 13.0),
}

# Koker profielen (h, b, t)
KOKER_PROFILES = {
    "Koker 40x40x3": (40, 40, 3.0),
    "Koker 50x50x3": (50, 50, 3.0),
    "Koker 60x60x3": (60, 60, 3.0),
    "Koker 60x60x4": (60, 60, 4.0),
    "Koker 70x70x3": (70, 70, 3.0),
    "Koker 70x70x4": (70, 70, 4.0),
    "Koker 80x80x3": (80, 80, 3.0),
    "Koker 80x80x4": (80, 80, 4.0),
    "Koker 80x80x5": (80, 80, 5.0),
    "Koker 90x90x3": (90, 90, 3.0),
    "Koker 90x90x4": (90, 90, 4.0),
}

def get_profile_dimensions(profile_type, profile_name):
    """Haal de dimensies op voor een specifiek profiel"""
    if profile_type == "HEA":
        return HEA_PROFILES.get(profile_name)
    elif profile_type == "HEB":
        return HEB_PROFILES.get(profile_name)
    elif profile_type == "IPE":
        return IPE_PROFILES.get(profile_name)
    elif profile_type == "UNP":
        return UNP_PROFILES.get(profile_name)
    elif profile_type == "Koker":
        return KOKER_PROFILES.get(profile_name)
    return None

def get_profile_list(profile_type):
    """Krijg een lijst van alle profielen van een bepaald type"""
    if profile_type == "HEA":
        return list(HEA_PROFILES.keys())
    elif profile_type == "HEB":
        return list(HEB_PROFILES.keys())
    elif profile_type == "IPE":
        return list(IPE_PROFILES.keys())
    elif profile_type == "UNP":
        return list(UNP_PROFILES.keys())
    elif profile_type == "Koker":
        return list(KOKER_PROFILES.keys())
    return []

def calculate_I(profile_type, h, b, t_w, t_f=None):
    """Bereken traagheidsmoment voor verschillende profieltypes"""
    if profile_type == "Koker":
        h_i = h - 2*t_w
        b_i = b - 2*t_w
        return (b*h**3)/12 - (b_i*h_i**3)/12
    elif profile_type in ["I-profiel", "U-profiel"]:
        # Flens bijdrage
        I_f = 2 * (b*t_f**3/12 + b*t_f*(h/2 - t_f/2)**2)
        # Lijf bijdrage
        h_w = h - 2*t_f
        I_w = t_w*h_w**3/12
        return I_f + I_w
    return 0

def calculate_A(profile_type, h, b, t_w, t_f=None):
    """Bereken oppervlakte voor verschillende profieltypes"""
    if profile_type == "Koker":
        return (h * b) - ((h - 2*t_w) * (b - 2*t_w))
    elif profile_type in ["I-profiel", "U-profiel"]:
        # Flens oppervlakte
        A_f = 2 * (b * t_f)
        # Lijf oppervlakte
        h_w = h - 2*t_f
        A_w = t_w * h_w
        return A_f + A_w
    return 0

def plot_beam_diagram(beam_length, supports, loads, x=None, deflection=None):
    """Plot een schematische weergave van de balk met steunpunten en belastingen"""
    fig = go.Figure()
    
    # Bereken schalingsfactor voor doorbuiging
    if x is not None and deflection is not None and np.any(deflection != 0):
        max_defl = max(abs(np.max(deflection)), abs(np.min(deflection)))
        scale_factor = beam_length / (20 * max_defl) if max_defl > 0 else 1
    else:
        scale_factor = 1
        deflection = np.zeros_like(x) if x is not None else None

    # Teken de balk
    if x is not None and deflection is not None:
        # Teken vervormde balk
        scaled_deflection = deflection * scale_factor
        fig.add_trace(go.Scatter(
            x=x,
            y=scaled_deflection,
            mode='lines',
            name='Balk',
            line=dict(color='#7f8c8d', width=10),  # Dikkere grijze lijn
            hovertemplate='Positie: %{x:.0f} mm<br>Doorbuiging: %{text:.2f} mm',
            text=deflection
        ))
    else:
        # Teken onvervormde balk
        fig.add_trace(go.Scatter(
            x=[0, beam_length],
            y=[0, 0],
            mode='lines',
            name='Balk',
            line=dict(color='#7f8c8d', width=10)  # Dikkere grijze lijn
        ))

    # Teken steunpunten
    for pos, type in supports:
        y_pos = deflection[np.abs(x - pos).argmin()] * scale_factor if x is not None and deflection is not None else 0
        
        if type == "Vast":
            # Rechthoek voor vaste inklemming
            fig.add_trace(go.Scatter(
                x=[pos-5, pos-5, pos+5, pos+5, pos-5],
                y=[y_pos-40, y_pos+40, y_pos+40, y_pos-40, y_pos-40],
                fill="toself",
                mode='lines',
                name='Vaste inklemming',
                line=dict(color='#e74c3c', width=2),
                fillcolor='rgba(231, 76, 60, 0.3)'
            ))
            
            # Arcering voor inklemming
            for i in range(-35, 36, 10):
                fig.add_trace(go.Scatter(
                    x=[pos-15, pos-5],
                    y=[y_pos+i, y_pos+i],
                    mode='lines',
                    line=dict(color='#e74c3c', width=1),
                    showlegend=False
                ))
        else:
            # Driehoek voor scharnier
            fig.add_trace(go.Scatter(
                x=[pos-20, pos, pos+20],
                y=[y_pos-20, y_pos, y_pos-20],
                fill="toself",
                mode='lines',
                name='Scharnier',
                line=dict(color='#e74c3c', width=2),
                fillcolor='rgba(231, 76, 60, 0.3)'
            ))

    # Teken belastingen
    for load in loads:
        pos, value, type = load[:3]
        y_pos = deflection[np.abs(x - pos).argmin()] * scale_factor if x is not None and deflection is not None else 0
        
        if type == "Puntlast":
            # Pijl voor puntlast
            arrow_height = 60
            fig.add_trace(go.Scatter(
                x=[pos, pos],
                y=[y_pos + arrow_height, y_pos],
                mode='lines',
                name=f'F = {abs(value):.0f} N',
                line=dict(color='#3498db', width=3)
            ))
            
            # Pijlpunt
            head_size = 15
            fig.add_trace(go.Scatter(
                x=[pos-head_size/2, pos, pos+head_size/2],
                y=[y_pos + head_size, y_pos, y_pos + head_size],
                mode='lines',
                line=dict(color='#3498db', width=3),
                showlegend=False
            ))
            
        elif type == "Verdeelde last":
            # Verdeelde last met meerdere pijlen
            length = load[3]
            num_arrows = int(length / 200) + 2
            positions = np.linspace(pos, pos + length, num_arrows)
            arrow_height = 60
            
            # Lijn boven pijlen
            fig.add_trace(go.Scatter(
                x=[pos, pos + length],
                y=[y_pos + arrow_height, y_pos + arrow_height],
                mode='lines',
                name=f'q = {abs(value):.1f} N/mm',
                line=dict(color='#3498db', width=3)
            ))
            
            # Pijlen
            for p in positions:
                fig.add_trace(go.Scatter(
                    x=[p, p],
                    y=[y_pos + arrow_height, y_pos],
                    mode='lines',
                    line=dict(color='#3498db', width=2),
                    showlegend=False
                ))
                
                # Pijlpunt
                head_size = 10
                fig.add_trace(go.Scatter(
                    x=[p-head_size/2, p, p+head_size/2],
                    y=[y_pos + head_size, y_pos, y_pos + head_size],
                    mode='lines',
                    line=dict(color='#3498db', width=2),
                    showlegend=False
                ))
                
        elif type == "Moment":
            # Gebogen pijl voor moment
            radius = 30
            theta = np.linspace(-np.pi/2, np.pi, 50)
            x_circle = pos + radius * np.cos(theta)
            y_circle = y_pos + radius * np.sin(theta)
            
            fig.add_trace(go.Scatter(
                x=x_circle,
                y=y_circle,
                mode='lines',
                name=f'M = {abs(value):.0f} Nmm',
                line=dict(color='#9b59b6', width=3)
            ))
            
            # Pijlpunt
            arrow_x = [pos + radius * np.cos(np.pi),
                      pos + (radius + 10) * np.cos(np.pi),
                      pos + radius * np.cos(np.pi + np.pi/6)]
            arrow_y = [y_pos + radius * np.sin(np.pi),
                      y_pos + (radius + 10) * np.sin(np.pi),
                      y_pos + radius * np.sin(np.pi + np.pi/6)]
            fig.add_trace(go.Scatter(
                x=arrow_x,
                y=arrow_y,
                mode='lines',
                line=dict(color='#9b59b6', width=3),
                showlegend=False
            ))
    
    # Update layout
    margin = 100
    y_range = [-100, 100]
    if x is not None and deflection is not None:
        y_min = min(-100, np.min(scaled_deflection) - 50)
        y_max = max(100, np.max(scaled_deflection) + 50)
        y_range = [y_min, y_max]
    
    fig.update_layout(
        showlegend=True,
        xaxis=dict(
            range=[-margin, beam_length + margin],
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False
        ),
        yaxis=dict(
            range=y_range,
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
            scaleanchor="x",
            scaleratio=1
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=50, t=50, b=50),
        height=400
    )
    
    return fig

def plot_results(x, V, M, rotation, deflection):
    """Plot alle resultaten in één figuur met subplots, vergelijkbaar met professionele software"""
    # Maak een figuur met subplots
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            "Balkschema en Belastingen",
            "Dwarskrachtenlijn (kN)",
            "Momentenlijn (kNm)"
        ),
        vertical_spacing=0.12,
        row_heights=[0.4, 0.3, 0.3]
    )
    
    # Balkschema (bovenste plot)
    # Teken de balk zelf
    fig.add_trace(
        go.Scatter(
            x=x,
            y=[0]*len(x),
            mode='lines',
            name='Balk',
            line=dict(color='#3498db', width=6),
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Dwarskrachtenlijn (middelste plot)
    fig.add_trace(
        go.Scatter(
            x=x,
            y=[v/1000 for v in V],  # Converteer naar kN
            mode='lines',
            name='Dwarskracht',
            line=dict(color='#27ae60', width=2),
            fill='tozeroy',
            fillcolor='rgba(46, 204, 113, 0.3)'
        ),
        row=2, col=1
    )
    
    # Momentenlijn (onderste plot)
    fig.add_trace(
        go.Scatter(
            x=x,
            y=[m/1000000 for m in M],  # Converteer naar kNm
            mode='lines',
            name='Moment',
            line=dict(color='#8e44ad', width=2),
            fill='tozeroy',
            fillcolor='rgba(142, 68, 173, 0.3)'
        ),
        row=3, col=1
    )
    
    # Update layout voor professionele uitstraling
    fig.update_layout(
        height=900,
        showlegend=True,
        plot_bgcolor='rgba(240,240,240,0.8)',
        paper_bgcolor='white',
        font=dict(size=12),
        margin=dict(t=100),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(255, 255, 255, 0.8)'
        )
    )
    
    # Update x-assen
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255,255,255,0.9)',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='rgba(0,0,0,0.2)',
        title_text="Positie (m)",
        dtick=1  # Markering elke meter
    )
    
    # Update y-assen
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255,255,255,0.9)',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='rgba(0,0,0,0.5)',
        row=1, col=1
    )
    
    # Specifieke y-as labels
    fig.update_yaxes(title_text="", row=1, col=1)  # Geen y-as label voor balkschema
    fig.update_yaxes(title_text="V (kN)", row=2, col=1)
    fig.update_yaxes(title_text="M (kNm)", row=3, col=1)
    
    # Voeg waarden toe bij belangrijke punten
    max_shear = max(abs(min(V)), abs(max(V))) / 1000
    max_moment = max(abs(min(M)), abs(max(M))) / 1000000
    
    # Voeg annotaties toe voor maximale waarden
    max_v_idx = np.argmax(np.abs(V))
    max_m_idx = np.argmax(np.abs(M))
    
    fig.add_annotation(
        x=x[max_v_idx],
        y=V[max_v_idx]/1000,
        text=f"{V[max_v_idx]/1000:.1f} kN",
        showarrow=True,
        arrowhead=2,
        row=2, col=1
    )
    
    fig.add_annotation(
        x=x[max_m_idx],
        y=M[max_m_idx]/1000000,
        text=f"{M[max_m_idx]/1000000:.1f} kNm",
        showarrow=True,
        arrowhead=2,
        row=3, col=1
    )
    
    return fig

def calculate_reactions(beam_length, supports, loads):
    """Bereken reactiekrachten voor alle belastingen"""
    # Sorteer steunpunten op positie
    supports = sorted(supports, key=lambda s: s[0])
    n = len(supports)
    
    # Matrix voor reactiekrachten
    A = np.zeros((3, 3))  # 3 vergelijkingen: ΣFy=0, ΣM_A=0, ΣM_B=0
    b = np.zeros(3)
    
    # Afstanden tot steunpunten
    x_A = supports[0][0]  # Positie eerste steunpunt
    x_B = supports[1][0]  # Positie tweede steunpunt
    L_AB = x_B - x_A     # Afstand tussen steunpunten
    
    # Vul matrix A voor evenwichtsvergelijkingen
    A[0] = [1, 0, 1]     # ΣFy=0: Va + Vb = F
    A[1] = [0, 1, 0]     # ΣFx=0: Ha = 0
    A[2] = [L_AB, 0, 0]  # ΣM_B=0: Va*L_AB = M_B
    
    # Bereken bijdrage van elke belasting
    for load in loads:
        pos, value, type = load[:3]
        x = pos - x_A  # Positie t.o.v. steunpunt A
        
        if type == "Puntlast":
            # Verticale kracht
            b[0] -= value  # ΣFy
            b[2] -= value * x  # ΣM_B
            
        elif type == "Moment":
            # Puntmoment
            b[2] -= value  # ΣM_B
            
        elif type == "Verdeelde last":
            # Gelijkmatig verdeelde belasting
            length = load[3]
            q = value
            F_total = q * length
            x_c = pos + length/2  # Zwaartepunt belasting
            
            b[0] -= F_total  # ΣFy
            b[2] -= F_total * (x_c - x_A)  # ΣM_B
            
        elif type == "Driehoekslast":
            # Lineair variërende belasting
            length = load[3]
            q_max = value
            F_total = 0.5 * q_max * length
            x_c = pos + 2*length/3  # Zwaartepunt driehoekslast
            
            b[0] -= F_total  # ΣFy
            b[2] -= F_total * (x_c - x_A)  # ΣM_B
    
    # Los reactiekrachten op
    try:
        reactions = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        reactions = np.linalg.lstsq(A, b, rcond=None)[0]
    
    return reactions[0], reactions[1], reactions[2]  # Va, Ha, Vb

def calculate_internal_forces(x, beam_length, supports, loads, reactions):
    """Bereken dwarskracht en moment op elke positie x"""
    Va, Ha, Vb = reactions
    x_A = supports[0][0]
    x_B = supports[1][0]
    
    V = np.zeros_like(x)  # Dwarskracht
    M = np.zeros_like(x)  # Moment
    
    # Voor elk punt x
    for i, xi in enumerate(x):
        # Initialiseer krachten op dit punt
        V_x = 0
        M_x = 0
        
        # Bijdrage van steunpunten
        if xi > x_A:
            V_x += Va
            M_x += Va * (xi - x_A)
        if xi > x_B:
            V_x += Vb
            M_x += Vb * (xi - x_B)
            
        # Bijdrage van belastingen
        for load in loads:
            pos, value, type = load[:3]
            
            if type == "Puntlast":
                if xi > pos:
                    V_x -= value
                    M_x -= value * (xi - pos)
                    
            elif type == "Moment":
                if xi > pos:
                    M_x -= value
                    
            elif type == "Verdeelde last":
                length = load[3]
                q = value
                if xi > pos:
                    if xi <= pos + length:
                        # Binnen belast gebied
                        l = xi - pos
                        V_x -= q * l
                        M_x -= q * l * l/2
                    else:
                        # Voorbij belast gebied
                        V_x -= q * length
                        M_x -= q * length * (xi - (pos + length/2))
                        
            elif type == "Driehoekslast":
                length = load[3]
                q_max = value
                if xi > pos:
                    if xi <= pos + length:
                        # Binnen belast gebied
                        l = xi - pos
                        q_x = q_max * (l/length)
                        V_x -= q_x * l/2
                        M_x -= q_x * l * l/6
                    else:
                        # Voorbij belast gebied
                        V_x -= q_max * length/2
                        M_x -= q_max * length/2 * (xi - (pos + 2*length/3))
        
        V[i] = V_x
        M[i] = M_x
    
    return V, M

def analyze_beam(beam_length, supports, loads, profile_type, height, width, wall_thickness, flange_thickness, E):
    """Analyseer de balk en bereken momenten, dwarskrachten, rotaties en doorbuigingen"""
    # Discretisatie
    n_points = 200
    x = np.linspace(0, beam_length, n_points)
    dx = x[1] - x[0]
    
    # Bereken traagheidsmoment
    I = calculate_I(profile_type, height, width, wall_thickness, flange_thickness)
    
    # Bereken reactiekrachten
    reactions = calculate_reactions(beam_length, supports, loads)
    
    # Bereken interne krachten
    V, M = calculate_internal_forces(x, beam_length, supports, loads, reactions)
    
    # Bereken rotatie en doorbuiging met numerieke integratie
    EI = E * I
    
    # Eerste integratie voor rotatie (θ = ∫M/EI dx)
    theta = np.zeros_like(x)
    for i in range(1, len(x)):
        theta[i] = theta[i-1] + (M[i-1] / EI) * dx
    
    # Tweede integratie voor doorbuiging (w = ∫θ dx)
    w = np.zeros_like(x)
    for i in range(1, len(x)):
        w[i] = w[i-1] + theta[i-1] * dx
    
    # Pas randvoorwaarden toe
    support_indices = [np.abs(x - pos).argmin() for pos, _ in supports]
    
    # Los randvoorwaarden op met matrix methode
    n_constraints = sum(2 if type == "Vast" else 1 for _, type in supports)
    A_bc = np.zeros((n_constraints, 2))  # 2 onbekenden: C1 (rotatie) en C2 (verplaatsing)
    b_bc = np.zeros(n_constraints)
    
    row = 0
    for idx, (_, type) in zip(support_indices, supports):
        if type == "Vast":
            # w = 0 en θ = 0
            A_bc[row] = [x[idx], 1]  # Voor w
            b_bc[row] = -w[idx]
            row += 1
            A_bc[row] = [1, 0]  # Voor θ
            b_bc[row] = -theta[idx]
            row += 1
        else:
            # Alleen w = 0
            A_bc[row] = [x[idx], 1]
            b_bc[row] = -w[idx]
            row += 1
    
    # Los correcties op
    try:
        C = np.linalg.solve(A_bc[:row], b_bc[:row])
    except np.linalg.LinAlgError:
        C = np.linalg.lstsq(A_bc[:row], b_bc[:row], rcond=None)[0]
    
    # Pas correcties toe
    theta += C[0]  # Rotatie correctie
    w += C[0] * x + C[1]  # Verplaatsing correctie
    
    return x, V, M, theta, w

def generate_report_html(beam_data, results_plot):
    """Genereer een HTML rapport"""
    
    # Converteer plots naar base64 images
    img_bytes = results_plot.to_image(format="png")
    img_base64 = base64.b64encode(img_bytes).decode()
    plot_image = f"data:image/png;base64,{img_base64}"
    
    # HTML template
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                padding: 20px;
                background: #f8f9fa;
                margin-bottom: 30px;
                border-radius: 8px;
            }}
            .section {{
                margin-bottom: 30px;
                padding: 20px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #f8f9fa;
            }}
            img {{
                max-width: 100%;
                height: auto;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                color: #666;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>BeamSolve Professional</h1>
            <h2>Technisch Rapport</h2>
            <p>Gegenereerd op: {datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
        </div>

        <div class="section">
            <h3>1. Invoergegevens</h3>
            <table>
                <tr><th>Parameter</th><th>Waarde</th></tr>
                <tr><td>Profieltype</td><td>{beam_data['profile_type']}</td></tr>
                <tr><td>Hoogte</td><td>{beam_data['dimensions']['height']} mm</td></tr>
                <tr><td>Breedte</td><td>{beam_data['dimensions']['width']} mm</td></tr>
                <tr><td>Wanddikte</td><td>{beam_data['dimensions']['wall_thickness']} mm</td></tr>
                <tr><td>Overspanning</td><td>{beam_data['length']} mm</td></tr>
                <tr><td>E-modulus</td><td>{beam_data['E']} N/mm²</td></tr>
            </table>
        </div>

        <div class="section">
            <h3>2. Steunpunten</h3>
            <table>
                <tr><th>Positie</th><th>Type</th></tr>
                {chr(10).join([f'<tr><td>{pos} mm</td><td>{type}</td></tr>' for pos, type in beam_data['supports']])}
            </table>
        </div>

        <div class="section">
            <h3>3. Belastingen</h3>
            <table>
                <tr><th>Type</th><th>Waarde</th><th>Positie</th><th>Lengte</th></tr>
                {chr(10).join([f'<tr><td>{load[2]}</td><td>{load[1]} N</td><td>{load[0]} mm</td><td>{load[3] if len(load) > 3 else "-"} mm</td></tr>' for load in beam_data['loads']])}
            </table>
        </div>

        <div class="section">
            <h3>4. Resultaten</h3>
            <table>
                <tr><th>Parameter</th><th>Waarde</th></tr>
                <tr><td>Maximaal moment</td><td>{beam_data['results']['max_M']:.2f} Nmm</td></tr>
                <tr><td>Maximale doorbuiging</td><td>{beam_data['results']['max_deflection']:.2f} mm</td></tr>
                <tr><td>Maximale rotatie</td><td>{beam_data['results']['max_rotation']:.6f} rad</td></tr>
            </table>
        </div>

        <div class="section">
            <h3>5. Grafieken</h3>
            <h4>5.1 Analyse Resultaten</h4>
            <img src="{plot_image}" alt="Analyse">
        </div>

        <div class="footer">
            <p>BeamSolve Professional {datetime.now().year}</p>
        </div>
    </body>
    </html>
    """
    
    return html

def save_report(html_content, output_path):
    """Sla het rapport op als HTML bestand"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return output_path

# Initialize session state
if 'loads' not in st.session_state:
    st.session_state.loads = []
if 'load_count' not in st.session_state:
    st.session_state.load_count = 0
if 'supports' not in st.session_state:
    st.session_state.supports = []
if 'calculations' not in st.session_state:
    st.session_state.calculations = []
if 'units' not in st.session_state:
    st.session_state.units = {
        'length': 'mm',
        'force': 'N',
        'stress': 'MPa'
    }

def main():
    st.set_page_config(page_title="BeamSolve Professional", layout="wide")
    
    # Sidebar voor invoer
    with st.sidebar:
        st.title("BeamSolve Professional")
        st.markdown("---")
        
        # Profiel selectie
        st.subheader("1. Profiel")
        col1, col2 = st.columns(2)
        with col1:
            profile_type = st.selectbox("Type", ["HEA", "HEB", "IPE", "UNP", "Koker"])
        with col2:
            profile_name = st.selectbox("Naam", get_profile_list(profile_type))
        
        # Haal profiel dimensies op
        dimensions = get_profile_dimensions(profile_type, profile_name)
        if dimensions:
            if profile_type == "Koker":
                height, width, wall_thickness = dimensions
                flange_thickness = wall_thickness
            else:
                height, width, wall_thickness, flange_thickness = dimensions
        
        # Toon dimensies
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Hoogte", f"{height} mm")
            st.metric("Breedte", f"{width} mm")
        with col2:
            st.metric("Wanddikte", f"{wall_thickness} mm")
            if profile_type != "Koker":
                st.metric("Flensdikte", f"{flange_thickness} mm")
        
        # E-modulus
        E = st.number_input("E-modulus", value=210000.0, step=1000.0, format="%.0f", help="N/mm²")
        
        st.markdown("---")
        
        # Overspanning
        st.subheader("2. Overspanning")
        beam_length = st.number_input("Lengte", value=3000.0, step=100.0, format="%.0f", help="mm")
        
        # Steunpunten
        st.subheader("3. Steunpunten")
        num_supports = st.number_input("Aantal", min_value=2, max_value=4, value=2)
        
        supports = []
        for i in range(num_supports):
            col1, col2 = st.columns(2)
            with col1:
                pos = st.number_input(
                    f"Positie {i+1}",
                    value=0.0 if i == 0 else beam_length if i == 1 else beam_length/2,
                    min_value=0.0,
                    max_value=beam_length,
                    step=100.0,
                    format="%.0f",
                    help="mm"
                )
            with col2:
                type = st.selectbox(
                    f"Type {i+1}",
                    ["Vast", "Scharnier"],
                    index=0 if i == 0 else 1
                )
            supports.append((pos, type))
        
        # Belastingen
        st.subheader("4. Belastingen")
        num_loads = st.number_input("Aantal", min_value=0, max_value=5, value=1)
        
        loads = []
        for i in range(num_loads):
            st.markdown(f"**Belasting {i+1}**")
            
            col1, col2 = st.columns(2)
            with col1:
                load_type = st.selectbox(
                    "Type",
                    ["Puntlast", "Verdeelde last", "Moment", "Driehoekslast"],
                    key=f"load_type_{i}"
                )
            with col2:
                if load_type == "Moment":
                    unit = "Nmm"
                elif load_type in ["Verdeelde last", "Driehoekslast"]:
                    unit = "N/mm"
                else:
                    unit = "N"
                    
                value = st.number_input(
                    f"Waarde ({unit})",
                    value=1000.0,
                    step=100.0,
                    format="%.1f",
                    key=f"load_value_{i}"
                )
            
            col1, col2 = st.columns(2)
            with col1:
                position = st.number_input(
                    "Positie",
                    value=beam_length/2,
                    min_value=0.0,
                    max_value=beam_length,
                    step=100.0,
                    format="%.0f",
                    help="mm",
                    key=f"load_pos_{i}"
                )
            
            if load_type in ["Verdeelde last", "Driehoekslast"]:
                with col2:
                    length = st.number_input(
                        "Lengte",
                        value=1000.0,
                        min_value=0.0,
                        max_value=beam_length - position,
                        step=100.0,
                        format="%.0f",
                        help="mm",
                        key=f"load_length_{i}"
                    )
                loads.append((position, value, load_type, length))
            else:
                loads.append((position, value, load_type))
    
    # Hoofdgedeelte
    if st.sidebar.button("Bereken", type="primary", use_container_width=True):
        # Voer analyse uit
        x, V, M, rotation, deflection = analyze_beam(beam_length, supports, loads, profile_type, height, width, wall_thickness, flange_thickness, E)
        
        # Toon resultaten
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Analyse Resultaten")
            
            # Plot alle resultaten
            results_plot = plot_results(x, V, M, rotation, deflection)
            st.plotly_chart(results_plot, use_container_width=True)
            
            # Maximale waarden
            max_vals = {
                "Dwarskracht": f"{max(abs(np.min(V)), abs(np.max(V))):.0f} N",
                "Moment": f"{max(abs(np.min(M)), abs(np.max(M))):.0f} Nmm",
                "Rotatie": f"{max(abs(np.min(rotation)), abs(np.max(rotation))):.6f} rad",
                "Doorbuiging": f"{max(abs(np.min(deflection)), abs(np.max(deflection))):.2f} mm"
            }
            
            st.subheader("Maximale Waarden")
            cols = st.columns(4)
            for i, (key, val) in enumerate(max_vals.items()):
                cols[i].metric(key, val)
        
        with col2:
            st.subheader("Profiel Details")
            I = calculate_I(profile_type, height, width, wall_thickness, flange_thickness)
            W = I / (height/2)
            A = calculate_A(profile_type, height, width, wall_thickness, flange_thickness)
            
            st.metric("Oppervlakte", f"{A:.0f} mm²")
            st.metric("Traagheidsmoment", f"{I:.0f} mm⁴")
            st.metric("Weerstandsmoment", f"{W:.0f} mm³")
            
            # Spanningen
            st.subheader("Spanningen")
            max_moment = max(abs(min(M)), abs(max(M)))
            sigma = max_moment / W
            st.metric("Max. buigspanning", f"{sigma:.1f} N/mm²")
            
            # Toetsing
            st.subheader("Toetsing")
            f_y = 235  # Vloeigrens S235
            UC = sigma / f_y
            st.metric("Unity Check", f"{UC:.2f}", help="UC ≤ 1.0")
            
            if UC > 1.0:
                st.error("Profiel voldoet niet! Kies een zwaarder profiel.")
            elif UC > 0.9:
                st.warning("Profiel zwaar belast. Overweeg een zwaarder profiel.")
            else:
                st.success("Profiel voldoet ruim.")
            
            # Download rapport
            st.markdown("---")
            if st.button("Download Rapport", type="secondary", use_container_width=True):
                # Genereer rapport
                beam_data = {
                    "profile_type": profile_type,
                    "profile_name": profile_name,
                    "dimensions": {
                        "height": height,
                        "width": width,
                        "wall_thickness": wall_thickness,
                        "flange_thickness": flange_thickness
                    },
                    "properties": {
                        "A": A,
                        "I": I,
                        "W": W
                    },
                    "results": {
                        "max_V": max(abs(np.min(V)), abs(np.max(V))),
                        "max_M": max_moment,
                        "max_deflection": max(abs(np.min(deflection)), abs(np.max(deflection))),
                        "max_rotation": max(abs(np.min(rotation)), abs(np.max(rotation))),
                        "max_stress": sigma,
                        "unity_check": UC
                    }
                }
                
                # Genereer rapport
                html_content = generate_report_html(beam_data, results_plot)
                output_dir = "reports"
                os.makedirs(output_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(output_dir, f"beamsolve_report_{timestamp}.html")
                save_report(html_content, output_path)
                st.success(f"Rapport opgeslagen als: {output_path}")

if __name__ == "__main__":
    main()
