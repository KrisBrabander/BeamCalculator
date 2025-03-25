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

def plot_beam_diagram(beam_length, supports, loads):
    """Teken professioneel balkschema"""
    fig = go.Figure()
    
    # Moderne kleuren
    colors = {
        'beam': '#2c3e50',  # Donkerblauw-grijs
        'support': '#3498db',  # Helder blauw
        'load': '#e74c3c',  # Rood
        'background': '#ffffff',  # Wit
        'grid': '#ecf0f1'  # Lichtgrijs
    }
    
    # Teken balk - modern en strak
    fig.add_trace(go.Scatter(
        x=[0, beam_length/1000],
        y=[0, 0],
        mode='lines',
        line=dict(color=colors['beam'], width=6),
        name='Balk'
    ))
    
    # Teken steunpunten
    for pos, type in supports:
        x_pos = pos/1000  # Convert to meters
        triangle_size = beam_length/50
        type = type.lower()
        
        if type == "inklemming":
            # Moderne inklemming met gevulde rechthoek en arcering
            fig.add_trace(go.Scatter(
                x=[x_pos, x_pos, x_pos+triangle_size/1000, x_pos+triangle_size/1000, x_pos],
                y=[-triangle_size/1000, triangle_size/1000, triangle_size/1000, -triangle_size/1000, -triangle_size/1000],
                fill="toself",
                mode='lines',
                line=dict(color=colors['support'], width=2),
                fillcolor=colors['support'],
                opacity=0.3,
                name='Inklemming',
                showlegend=True if type == "inklemming" else False
            ))
            # Moderne arcering met dunnere lijnen
            for i in range(5):
                offset = -triangle_size/1000 + i * triangle_size/500
                fig.add_trace(go.Scatter(
                    x=[x_pos, x_pos+triangle_size/1000],
                    y=[offset, offset],
                    mode='lines',
                    line=dict(color=colors['support'], width=1),
                    showlegend=False
                ))
                
        elif type == "scharnier":
            # Modern driehoekig support met vulling
            fig.add_trace(go.Scatter(
                x=[x_pos-triangle_size/1000, x_pos+triangle_size/1000, x_pos, x_pos-triangle_size/1000],
                y=[-triangle_size/1000, -triangle_size/1000, 0, -triangle_size/1000],
                fill="toself",
                mode='lines',
                line=dict(color=colors['support'], width=2),
                fillcolor=colors['support'],
                opacity=0.3,
                name='Scharnier',
                showlegend=True if type == "scharnier" else False
            ))
            
        elif type == "rol":
            # Moderne rol met cirkels
            fig.add_trace(go.Scatter(
                x=[x_pos-triangle_size/1000, x_pos+triangle_size/1000, x_pos, x_pos-triangle_size/1000],
                y=[-triangle_size/1000, -triangle_size/1000, 0, -triangle_size/1000],
                fill="toself",
                mode='lines',
                line=dict(color=colors['support'], width=2),
                fillcolor=colors['support'],
                opacity=0.3,
                name='Rol',
                showlegend=True if type == "rol" else False
            ))
            # Voeg cirkels toe voor rol effect
            circle_size = triangle_size/2000
            for i in [-1, 0, 1]:
                fig.add_trace(go.Scatter(
                    x=[x_pos + i*circle_size*2],
                    y=[-triangle_size/1000 - circle_size],
                    mode='markers',
                    marker=dict(size=6, color=colors['support']),
                    showlegend=False
                ))
    
    # Teken belastingen
    for load in loads:
        x_pos = load[0]/1000
        value = load[1]
        load_type = load[2]
        
        if load_type == "Puntlast":
            # Maak puntlast pijlen 1.5x langer dan verdeelde last pijlen
            arrow_height = beam_length/25  # Was /40, nu langer
            # Label boven de pijl
            fig.add_trace(go.Scatter(
                x=[x_pos],
                y=[arrow_height/1000 + arrow_height/4000],
                mode='text',
                text=[f'{value/1000:.1f} kN'],
                textposition='top center',
                textfont=dict(size=14, color=colors['load']),
                showlegend=False
            ))
            # Pijl
            fig.add_trace(go.Scatter(
                x=[x_pos, x_pos],
                y=[arrow_height/1000, 0],
                mode='lines',
                line=dict(color=colors['load'], width=3),
                showlegend=True,
                name='Puntlast'
            ))
            # Pijlpunt (driehoek)
            fig.add_shape(
                type="path",
                path=f"M {x_pos-arrow_height/3000} {arrow_height/3000} L {x_pos} 0 L {x_pos+arrow_height/3000} {arrow_height/3000} Z",
                fillcolor=colors['load'],
                line=dict(color=colors['load'], width=0),
            )
            
        elif load_type == "Verdeelde last":
            # Standaard hoogte voor verdeelde last
            arrow_height = beam_length/40
            length = load[3]/1000 if len(load) > 3 else (beam_length - load[0])/1000
            # Label boven de verdeelde last
            fig.add_trace(go.Scatter(
                x=[x_pos + length/2],
                y=[arrow_height/1000 + arrow_height/4000],
                mode='text',
                text=[f'{value/1000:.1f} kN/m'],
                textposition='top center',
                textfont=dict(size=14, color=colors['load']),
                showlegend=False
            ))
            
            # Verbindingslijn bovenaan
            fig.add_trace(go.Scatter(
                x=[x_pos, x_pos+length],
                y=[arrow_height/1000, arrow_height/1000],
                mode='lines',
                line=dict(color=colors['load'], width=3),
                showlegend=True,
                name='Verdeelde last'
            ))
            
            # Pijlen
            num_arrows = min(max(int(length*8), 4), 15)  # Meer pijlen voor vloeiender uiterlijk
            for i in range(num_arrows):
                arrow_x = x_pos + (i * length/(num_arrows-1))
                # Pijlsteel
                fig.add_trace(go.Scatter(
                    x=[arrow_x, arrow_x],
                    y=[arrow_height/1000, 0],
                    mode='lines',
                    line=dict(color=colors['load'], width=2),
                    showlegend=False
                ))
                # Pijlpunt (driehoek)
                fig.add_shape(
                    type="path",
                    path=f"M {arrow_x-arrow_height/4000} {arrow_height/4000} L {arrow_x} 0 L {arrow_x+arrow_height/4000} {arrow_height/4000} Z",
                    fillcolor=colors['load'],
                    line=dict(color=colors['load'], width=0),
                )
            
        elif load_type == "Driehoekslast":
            length = load[3]/1000
            # Label boven het hoogste punt
            fig.add_trace(go.Scatter(
                x=[x_pos + length],
                y=[beam_length/40/1000 + beam_length/40/4000],
                mode='text',
                text=[f'{value/1000:.1f} kN/m'],
                textposition='top center',
                textfont=dict(size=14, color=colors['load']),
                showlegend=False
            ))
            
            # Schuine lijn bovenaan
            fig.add_trace(go.Scatter(
                x=[x_pos, x_pos+length],
                y=[0, beam_length/40/1000],
                mode='lines',
                line=dict(color=colors['load'], width=3),
                showlegend=True,
                name='Driehoekslast'
            ))
            
            # Pijlen met variabele lengte
            num_arrows = min(max(int(length*8), 4), 15)  # Meer pijlen voor vloeiender uiterlijk
            for i in range(num_arrows):
                rel_pos = i/(num_arrows-1)
                arrow_x = x_pos + length * rel_pos
                current_height = (beam_length/40/1000) * rel_pos  # Hoogte op basis van positie
                
                # Pijlsteel
                fig.add_trace(go.Scatter(
                    x=[arrow_x, arrow_x],
                    y=[current_height, 0],
                    mode='lines',
                    line=dict(color=colors['load'], width=2),
                    showlegend=False
                ))
                # Pijlpunt (driehoek)
                arrow_size = (beam_length/40/4000) * rel_pos  # Pijlgrootte schaalt mee
                if rel_pos > 0:  # Alleen pijlpunten tekenen als er een steel is
                    fig.add_shape(
                        type="path",
                        path=f"M {arrow_x-arrow_size} {arrow_size} L {arrow_x} 0 L {arrow_x+arrow_size} {arrow_size} Z",
                        fillcolor=colors['load'],
                        line=dict(color=colors['load'], width=0),
                    )
            
        elif load_type == "Moment":
            # Label bij het moment
            fig.add_trace(go.Scatter(
                x=[x_pos],
                y=[beam_length/40/1000 + beam_length/40/4000],
                mode='text',
                text=[f'{value/1e6:.1f} kNm'],
                textposition='top center',
                textfont=dict(size=14, color=colors['load']),
                showlegend=False
            ))
            
            # Moment cirkel met pijl
            radius = beam_length/40/2000
            theta = np.linspace(-np.pi/2, 3*np.pi/2, 50)
            fig.add_trace(go.Scatter(
                x=x_pos + radius*np.cos(theta),
                y=radius*np.sin(theta),
                mode='lines',
                line=dict(color=colors['load'], width=3),
                showlegend=True,
                name='Moment'
            ))
            # Pijlpunt op cirkel
            arrow_angle = 3*np.pi/2
            arrow_size = radius/2
            fig.add_shape(
                type="path",
                path=f"M {x_pos + radius*np.cos(arrow_angle-0.2)} {radius*np.sin(arrow_angle-0.2)} L {x_pos + radius*np.cos(arrow_angle)} {radius*np.sin(arrow_angle)} L {x_pos + radius*np.cos(arrow_angle-0.2)} {radius*np.sin(arrow_angle+0.2)}",
                fillcolor=colors['load'],
                line=dict(color=colors['load'], width=3),
            )
    
    # Update layout voor moderne uitstraling
    fig.update_layout(
        title=dict(
            text="Balkschema en Belastingen",
            font=dict(size=24, color=colors['beam'])
        ),
        height=300,
        showlegend=True,
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            range=[-beam_length/20/1000, beam_length/20/1000],
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor=colors['beam'],
            showgrid=True,
            gridcolor=colors['grid'],
            gridwidth=1
        ),
        xaxis=dict(
            range=[-beam_length/20/1000, beam_length*1.1/1000],
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor=colors['beam'],
            showgrid=True,
            gridcolor=colors['grid'],
            gridwidth=1
        ),
        margin=dict(t=50, b=50, l=50, r=50),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor=colors['beam'],
            borderwidth=1
        )
    )
    
    return fig

def plot_results(x, V, M, rotation, deflection):
    """Plot alle resultaten in één figuur met subplots"""
    # Maak subplot layout
    fig = make_subplots(
        rows=4, cols=1,
        subplot_titles=('Doorbuiging (mm)', 'Rotatie (rad)', 'Dwarskracht (kN)', 'Moment (kNm)'),
        vertical_spacing=0.08,
        shared_xaxes=True
    )
    
    # Doorbuiging (bovenste plot)
    fig.add_trace(
        go.Scatter(
            x=x/1000,  # Convert to meters
            y=deflection,  # Already in mm
            mode='lines',
            name='Doorbuiging',
            line=dict(color='#2980b9', width=2),
            fill='tozeroy',
            fillcolor='rgba(41, 128, 185, 0.3)'
        ),
        row=1, col=1
    )
    
    # Rotatie (tweede plot)
    fig.add_trace(
        go.Scatter(
            x=x/1000,  # Convert to meters
            y=rotation,  # In radians
            mode='lines',
            name='Rotatie',
            line=dict(color='#e67e22', width=2),
            fill='tozeroy',
            fillcolor='rgba(230, 126, 34, 0.3)'
        ),
        row=2, col=1
    )
    
    # Dwarskrachtenlijn (derde plot)
    fig.add_trace(
        go.Scatter(
            x=x/1000,  # Convert to meters
            y=[v/1000 for v in V],  # Convert to kN
            mode='lines',
            name='Dwarskracht',
            line=dict(color='#27ae60', width=2),
            fill='tozeroy',
            fillcolor='rgba(46, 204, 113, 0.3)'
        ),
        row=3, col=1
    )
    
    # Momentenlijn (onderste plot)
    fig.add_trace(
        go.Scatter(
            x=x/1000,  # Convert to meters
            y=[m/1000000 for m in M],  # Convert to kNm
            mode='lines',
            name='Moment',
            line=dict(color='#8e44ad', width=2),
            fill='tozeroy',
            fillcolor='rgba(142, 68, 173, 0.3)'
        ),
        row=4, col=1
    )
    
    # Update layout voor professionele uitstraling
    fig.update_layout(
        height=900,
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor='rgba(255, 255, 255, 0.8)'
        )
    )
    
    # Update x-assen
    for i in range(1, 5):
        fig.update_xaxes(
            row=i, col=1,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=True,
            zerolinecolor='rgba(0,0,0,0.2)',
            zerolinewidth=2,
            dtick=1  # 1m intervallen
        )
    
    # Update y-assen
    for i in range(1, 5):
        fig.update_yaxes(
            row=i, col=1,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=True,
            zerolinecolor='rgba(0,0,0,0.2)',
            zerolinewidth=2
        )
    
    # Voeg waarden toe bij belangrijke punten
    max_defl_idx = np.argmax(np.abs(deflection))
    max_rot_idx = np.argmax(np.abs(rotation))
    max_v_idx = np.argmax(np.abs(V))
    max_m_idx = np.argmax(np.abs(M))
    
    # Annotaties voor maximale waarden
    fig.add_annotation(
        x=x[max_defl_idx]/1000,
        y=deflection[max_defl_idx],
        text=f"{deflection[max_defl_idx]:.2f} mm",
        showarrow=True,
        arrowhead=2,
        row=1, col=1
    )
    
    fig.add_annotation(
        x=x[max_rot_idx]/1000,
        y=rotation[max_rot_idx],
        text=f"{rotation[max_rot_idx]:.4f} rad",
        showarrow=True,
        arrowhead=2,
        row=2, col=1
    )
    
    fig.add_annotation(
        x=x[max_v_idx]/1000,
        y=V[max_v_idx]/1000,
        text=f"{V[max_v_idx]/1000:.1f} kN",
        showarrow=True,
        arrowhead=2,
        row=3, col=1
    )
    
    fig.add_annotation(
        x=x[max_m_idx]/1000,
        y=M[max_m_idx]/1000000,
        text=f"{M[max_m_idx]/1000000:.1f} kNm",
        showarrow=True,
        arrowhead=2,
        row=4, col=1
    )
    
    # Update x-as label alleen op onderste plot
    fig.update_xaxes(title_text="Positie (m)", row=4, col=1)
    
    return fig

def calculate_reactions(beam_length, supports, loads):
    """Bereken reactiekrachten voor de steunpunten"""
    reactions = {}
    
    # Sorteer steunpunten op positie
    supports = sorted(supports, key=lambda x: x[0])
    
    # Check statische bepaaldheid
    n_reactions = sum(2 if type.lower() == "inklemming" else 1 for _, type in supports)
    is_hyperstatic = n_reactions > 3
    
    # Bereken belastingen
    total_force = 0
    total_moment = 0
    
    for load in loads:
        load_type = load[2]
        value = load[1]
        pos = load[0]
        
        if load_type == "Puntlast":
            total_force += value
            total_moment += value * pos
        elif load_type == "Moment":
            total_moment += value
        elif load_type == "Verdeelde last":
            length = load[3]
            total_force += value * length
            total_moment += value * length * (pos + length/2)
        elif load_type == "Driehoekslast":
            length = load[3]
            total_force += value * length / 2
            total_moment += value * length / 2 * (pos + 2*length/3)
    
    if is_hyperstatic:
        # Voor hyperstatische systemen: verdeel krachten proportioneel
        n_supports = len(supports)
        
        # Verdeel verticale kracht
        force_per_support = total_force / n_supports
        
        for pos, type in supports:
            if type.lower() == "inklemming":
                # Inklemming neemt ook moment op
                moment_share = total_moment / sum(1 for _, t in supports if t.lower() == "inklemming")
                reactions[pos] = {"Fy": force_per_support, "M": moment_share}
            else:
                reactions[pos] = {"Fy": force_per_support}
    else:
        # Voor statisch bepaalde systemen: los op via evenwicht
        if len(supports) == 1:
            # Enkele inklemming
            pos, type = supports[0]
            if type.lower() == "inklemming":
                reactions[pos] = {"Fy": total_force, "M": total_moment}
            else:
                st.error("Systeem is instabiel: enkele steun zonder inklemming")
                
        elif len(supports) == 2:
            # Twee steunpunten
            pos1, type1 = supports[0]
            pos2, type2 = supports[1]
            
            # Los op via momentevenwicht
            span = pos2 - pos1
            if span == 0:
                st.error("Steunpunten kunnen niet op dezelfde positie liggen")
                return reactions
            
            # Bereken reactiekrachten via momentevenwicht
            R2 = (total_moment - total_force * pos1) / span
            R1 = total_force - R2
            
            reactions[pos1] = {"Fy": R1}
            reactions[pos2] = {"Fy": R2}
            
            # Als er een inklemming is, bereken het moment
            if type1.lower() == "inklemming":
                reactions[pos1]["M"] = total_moment - R2 * span
            if type2.lower() == "inklemming":
                reactions[pos2]["M"] = -total_moment + R1 * span
                
        elif len(supports) == 3:
            # Drie steunpunten (hyperstatisch)
            # Gebruik vereenvoudigde benadering: verdeel kracht over middelste steunpunt
            pos1, type1 = supports[0]
            pos2, type2 = supports[1]
            pos3, type3 = supports[2]
            
            # Verdeel kracht 40% op middelste steun, 30% op buitenste steunen
            R2 = 0.4 * total_force
            R1 = R3 = 0.3 * total_force
            
            reactions[pos1] = {"Fy": R1}
            reactions[pos2] = {"Fy": R2}
            reactions[pos3] = {"Fy": R3}
            
            # Bereken momenten voor inklemmingen
            if type1.lower() == "inklemming":
                reactions[pos1]["M"] = total_moment / 3
            if type3.lower() == "inklemming":
                reactions[pos3]["M"] = -total_moment / 3
    
    return reactions

def calculate_internal_forces(x, beam_length, supports, loads, reactions):
    """Bereken dwarskracht en moment op elke positie x"""
    V = np.zeros_like(x)  # Dwarskracht array
    M = np.zeros_like(x)  # Moment array
    
    # Sorteer steunpunten op positie
    supports = sorted(supports, key=lambda x: x[0])
    first_support_pos = supports[0][0] if supports else 0
    
    # Verwerk reactiekrachten eerst
    for pos, reaction in reactions.items():
        # Dwarskracht van reactiekracht (positief want het is een reactie)
        V += reaction["Fy"] * (x >= pos)
        # Moment van reactiekracht
        M += reaction["Fy"] * np.where(x >= pos, x - pos, 0)
        # Direct moment van inklemming
        if "M" in reaction:
            M += reaction["M"] * (x >= pos)
    
    # Verwerk belastingen
    for load in loads:
        pos = load[0]
        value = load[1]
        load_type = load[2]
        
        if load_type == "Puntlast":
            # Dwarskracht: stap bij puntlast
            V -= value * (x >= pos)
            # Moment: alleen na het aangrijpingspunt
            M -= value * np.where(x >= pos, x - pos, 0)
            
        elif load_type == "Verdeelde last":
            length = load[3] if len(load) > 3 else beam_length - pos
            end_pos = pos + length
            # Belast gebied
            mask = (x >= pos) & (x <= end_pos)
            after_mask = x > end_pos
            
            # Dwarskracht
            V[mask] -= value * (x[mask] - pos)  # Lineair toenemend in belast gebied
            V[after_mask] -= value * length  # Constante waarde na belast gebied
            
            # Moment
            M[mask] -= value * (x[mask] - pos)**2 / 2  # Kwadratisch in belast gebied
            M[after_mask] -= value * length * (x[after_mask] - (pos + length/2))  # Lineair na belast gebied
            
        elif load_type == "Driehoekslast":
            length = load[3]
            end_pos = pos + length
            # Belast gebied
            mask = (x >= pos) & (x <= end_pos)
            after_mask = x > end_pos
            
            # Relatieve x-positie voor driehoek (alleen binnen belast gebied)
            rel_x = np.zeros_like(x)
            rel_x[mask] = (x[mask] - pos) / length
            
            # Dwarskracht
            V[mask] -= value * length * (rel_x[mask]**2) / 2  # Kwadratisch in belast gebied
            V[after_mask] -= value * length / 2  # Constante waarde na belast gebied
            
            # Moment
            M[mask] -= value * length * (rel_x[mask]**3) / 6  # Kubisch in belast gebied
            M[after_mask] -= value * length * (x[after_mask] - (pos + 2*length/3)) / 2  # Lineair na belast gebied
            
        elif load_type == "Moment":
            # Direct moment alleen na het aangrijpingspunt
            M -= value * (x >= pos)
    
    # Zorg dat er geen moment is voor het eerste steunpunt
    M = np.where(x < first_support_pos, 0, M)
    V = np.where(x < first_support_pos, 0, V)
    
    return V, M

def analyze_beam(beam_length, supports, loads, profile_type, height, width, wall_thickness, flange_thickness, E):
    """Analyseer de balk en bereken dwarskrachten, momenten, rotatie en doorbuiging"""
    # Aantal punten voor berekening
    n_points = 2001
    x = np.linspace(0, beam_length, n_points)
    dx = x[1] - x[0]
    
    # Bereken profiel eigenschappen
    A, I, W = calculate_profile_properties(profile_type, height, width, wall_thickness, flange_thickness)
    EI = E * I
    
    # Sorteer steunpunten op positie
    supports = sorted(supports, key=lambda x: x[0])
    
    # Bereken reactiekrachten
    reactions = calculate_reactions(beam_length, supports, loads)
    
    # Bereken interne krachten
    V, M = calculate_internal_forces(x, beam_length, supports, loads, reactions)
    
    # Arrays voor resultaten
    rotation = np.zeros_like(x)
    deflection = np.zeros_like(x)
    
    # Bereken doorbuiging voor elke last en steunpunt apart
    def elastic_line(F, a, x):
        """Bereken doorbuiging door puntlast F op positie a"""
        v = np.zeros_like(x)
        L = beam_length
        
        # Voor x ≤ a: v = Fx(L-a)(L-x)x/(6EIL)
        mask = x <= a
        v[mask] = F * x[mask] * (L-a) * (L-x[mask]) * x[mask] / (6 * EI * L)
        
        # Voor x > a: v = Fa(L-x)(L-a)x/(6EIL)
        mask = x > a
        v[mask] = F * a * (L-x[mask]) * (L-a) * x[mask] / (6 * EI * L)
        
        return v
    
    # 1. Bereken doorbuiging door belastingen
    for load in loads:
        load_type = load[2]
        value = load[1]
        pos = load[0]
        
        if load_type == "Puntlast":
            deflection += elastic_line(value, pos, x)
            
        elif load_type == "Verdeelde last":
            # Verdeel in 10 puntlasten
            length = load[3]
            n_points = 10
            dx_load = length / n_points
            for i in range(n_points):
                xi = pos + i * dx_load + dx_load/2
                Fi = value * dx_load
                deflection += elastic_line(Fi, xi, x)
                
        elif load_type == "Driehoekslast":
            # Verdeel in 10 puntlasten
            length = load[3]
            n_points = 10
            dx_load = length / n_points
            for i in range(n_points):
                xi = pos + i * dx_load + dx_load/2
                h = value * (i + 0.5) / n_points  # Hoogte op dit punt
                Fi = h * dx_load
                deflection += elastic_line(Fi, xi, x)
                
        elif load_type == "Moment":
            # Moment = koppel van twee tegengestelde krachten
            d = dx  # Kleine afstand voor koppel
            F = value / d  # Grootte van de krachten
            deflection += elastic_line(F, pos, x)
            deflection -= elastic_line(F, pos + d, x)
    
    # 2. Bereken correctiekrachten voor steunpunten
    while True:
        max_deflection = 0
        
        # Voor elk steunpunt
        for pos, type in supports:
            idx = np.abs(x - pos).argmin()
            d = deflection[idx]
            
            if abs(d) > 1e-10:  # Als er nog significante doorbuiging is
                # Pas een correctiekracht toe
                F = -d * EI / (pos * (beam_length - pos)**2)  # Geschatte correctiekracht
                deflection += elastic_line(F, pos, x)
                max_deflection = max(max_deflection, abs(d))
        
        if max_deflection < 1e-10:
            break
    
    # Bereken rotatie door differentiatie
    rotation[1:-1] = (deflection[2:] - deflection[:-2]) / (2*dx)
    rotation[0] = (deflection[1] - deflection[0]) / dx
    rotation[-1] = (deflection[-1] - deflection[-2]) / dx
    
    # Forceer exacte waarden bij steunpunten
    for pos, type in supports:
        idx = np.abs(x - pos).argmin()
        deflection[idx] = 0.0
        if type.lower() == "inklemming":
            rotation[idx] = 0.0
    
    return x, V, M, rotation, deflection

@st.cache_data
def calculate_profile_properties(profile_type, height, width, wall_thickness, flange_thickness):
    """Cache profiel eigenschappen voor snellere berekeningen"""
    # Map profile types to calculation types
    calc_type = "Koker" if profile_type == "Koker" else ("U-profiel" if profile_type == "UNP" else "I-profiel")
    
    A = calculate_A(calc_type, height, width, wall_thickness, flange_thickness)
    I = calculate_I(calc_type, height, width, wall_thickness, flange_thickness)
    W = I / (height/2) if height > 0 else 0
    return A, I, W

def generate_pdf_report(beam_data, results_plot):
    """Genereer een professioneel PDF rapport"""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from io import BytesIO
    import plotly.io as pio
    from datetime import datetime
    
    # Converteer plotly figuur naar afbeelding
    img_bytes = pio.to_image(results_plot, format="png", width=800, height=600, scale=2)
    
    # Maak PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )
    
    # Definieer stijlen
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#2c3e50')
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#34495e')
    )
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#2c3e50')
    )
    
    # Start document opbouw
    elements = []
    
    # Header met logo en titel
    elements.append(Paragraph("BeamSolve Professional", title_style))
    elements.append(Paragraph(f"Rapport gegenereerd op {datetime.now().strftime('%d-%m-%Y %H:%M')}", body_style))
    elements.append(Spacer(1, 20))
    
    # Profiel informatie
    elements.append(Paragraph("1. Profiel Specificaties", heading_style))
    profile_data = [
        ["Type", beam_data["profile_type"]],
        ["Hoogte", f"{beam_data['height']} mm"],
        ["Breedte", f"{beam_data['width']} mm"],
        ["Wanddikte", f"{beam_data['wall_thickness']} mm"]
    ]
    if "flange_thickness" in beam_data and beam_data["flange_thickness"]:
        profile_data.append(["Flensdikte", f"{beam_data['flange_thickness']} mm"])
    
    profile_table = Table(profile_data, colWidths=[100, 200])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
    ]))
    elements.append(profile_table)
    elements.append(Spacer(1, 20))
    
    # Profiel eigenschappen
    elements.append(Paragraph("2. Profiel Eigenschappen", heading_style))
    properties_data = [
        ["Parameter", "Waarde", "Eenheid"],
        ["Oppervlakte", f"{beam_data['area']:.0f}", "mm²"],
        ["Traagheidsmoment", f"{beam_data['moment_of_inertia']:.0f}", "mm⁴"],
        ["Weerstandsmoment", f"{beam_data['section_modulus']:.0f}", "mm³"],
        ["Max. buigspanning", f"{beam_data['max_stress']:.1f}", "N/mm²"]
    ]
    
    properties_table = Table(properties_data, colWidths=[100, 100, 100])
    properties_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
    ]))
    elements.append(properties_table)
    elements.append(Spacer(1, 20))
    
    # Steunpunten
    elements.append(Paragraph("3. Steunpunten", heading_style))
    support_data = [["#", "Type", "Positie"]]
    for i, (pos, type) in enumerate(beam_data['supports'], 1):
        support_data.append([str(i), type, f"{pos} mm"])
    
    support_table = Table(support_data, colWidths=[50, 150, 100])
    support_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
    ]))
    elements.append(support_table)
    elements.append(Spacer(1, 20))
    
    # Belastingen
    elements.append(Paragraph("4. Belastingen", heading_style))
    load_data = [["#", "Type", "Waarde", "Positie", "Lengte"]]
    for i, load in enumerate(beam_data['loads'], 1):
        if len(load) == 4:  # Verdeelde of driehoekslast
            pos, val, type, length = load
            if type == "Verdeelde last":
                load_data.append([str(i), type, f"{val/1000:.1f} kN/m", f"{pos} mm", f"{length} mm"])
            elif type == "Driehoekslast":
                load_data.append([str(i), type, f"{val/1000:.1f} kN/m", f"{pos} mm", f"{length} mm"])
        else:  # Puntlast of moment
            pos, val, type = load
            if type == "Moment":
                load_data.append([str(i), type, f"{val/1e6:.1f} kNm", f"{pos} mm", "-"])
            else:
                load_data.append([str(i), type, f"{val/1000:.1f} kN", f"{pos} mm", "-"])
    
    load_table = Table(load_data, colWidths=[30, 100, 80, 80, 80])
    load_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
    ]))
    elements.append(load_table)
    elements.append(Spacer(1, 20))
    
    # Resultaten
    elements.append(Paragraph("5. Resultaten", heading_style))
    
    # Grafieken
    img_stream = BytesIO(img_bytes)
    img = Image(img_stream, width=160*mm, height=120*mm)
    elements.append(img)
    elements.append(Spacer(1, 10))
    
    # Maximale waarden
    elements.append(Paragraph("Maximale Waarden:", heading_style))
    max_data = [
        ["Parameter", "Waarde", "Eenheid"],
        ["Max. Doorbuiging", f"{beam_data['max_deflection']:.2f}", "mm"],
        ["Max. Rotatie", f"{beam_data['max_rotation']:.4f}", "rad"],
        ["Max. Dwarskracht", f"{beam_data['max_shear']/1000:.1f}", "kN"],
        ["Max. Moment", f"{beam_data['max_moment']/1000000:.1f}", "kNm"]
    ]
    
    max_table = Table(max_data, colWidths=[100, 100, 100])
    max_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
    ]))
    elements.append(max_table)
    
    # Footer
    elements.append(Spacer(1, 30))
    footer_text = "Berekend met BeamSolve Professional 2025"
    elements.append(Paragraph(footer_text, body_style))
    
    # Build PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf

def save_report(report_content, output_path):
    """Sla het rapport op"""
    with open(output_path, 'wb') as f:
        f.write(report_content)

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
if 'export_count' not in st.session_state:
    st.session_state.export_count = 0

def main():
    st.set_page_config(
        page_title="BeamSolve Professional",
        page_icon="🏗️",
        layout="wide"
    )
    
    # Header
    col1, col2 = st.columns([3,1])
    with col1:
        st.title("🏗️ BeamSolve Professional")
        st.markdown("Geavanceerde balkberekeningen voor constructeurs")
    with col2:
        st.markdown("### 📊 Versie")
        st.markdown("""
        <div style='background-color: #f8f9fa; padding: 10px; border-radius: 5px;'>
        <small>
        ⭐ Free Edition<br>
        <span style='color: #6c757d;'>2/2 Exports Beschikbaar</span>
        </small>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Initialisatie sessie variabelen
    if 'export_count' not in st.session_state:
        st.session_state.export_count = 0
    
    # Test voorbeeld (zoals in de afbeelding)
    if st.sidebar.button("Laad Testvoorbeeld", type="secondary"):
        st.session_state.test_example = True
        # Balk van 18m met 3 steunpunten
        st.session_state.beam_length = 18000  # 18m in mm
        st.session_state.supports = [
            (3000, "Scharnier"),   # C op 3m
            (9000, "Scharnier"),   # D op 9m
            (15000, "Scharnier"),  # B op 15m
        ]
        st.session_state.loads = [
            # Driehoekslast van 50 kN/m over 4m
            (3000, 50, "Driehoekslast", 4000),
            # Verdeelde last van 20 kN/m over rest
            (9000, 20, "Verdeelde last", 6000),
            # Puntlast van 100 kN
            (9000, 100, "Puntlast")
        ]
        st.session_state.profile_type = "HEA"
        st.session_state.profile_name = "HEA 300"
    
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
        num_supports = st.number_input("Aantal", min_value=1, max_value=4, value=1)
        
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
                    ["Inklemming", "Scharnier", "Rol"],
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
            
            # Alleen lengte vragen bij verdeelde en driehoekslasten
            if load_type in ["Verdeelde last", "Driehoekslast"]:
                with col2:
                    # Bereken maximale lengte op basis van positie
                    max_length = min(beam_length - position, beam_length)
                    # Als er een bestaande waarde is, gebruik die (maar begrens het)
                    default_length = min(1000.0, max_length)
                    if f"load_length_{i}" in st.session_state:
                        default_length = min(st.session_state[f"load_length_{i}"], max_length)
                    
                    length = st.number_input(
                        "Lengte",
                        value=default_length,
                        min_value=0.0,
                        max_value=max_length,
                        step=100.0,
                        format="%.0f",
                        help="mm",
                        key=f"load_length_{i}"
                    )
                    # Voeg belasting toe met lengte
                    loads.append((position, value, load_type, length))
            else:
                # Voeg puntlast of moment toe zonder lengte
                loads.append((position, value, load_type))
    
    # Hoofdgedeelte
    if st.sidebar.button("Bereken", type="primary", use_container_width=True):
        # Voer analyse uit
        x, V, M, rotation, deflection = analyze_beam(beam_length, supports, loads, profile_type, height, width, wall_thickness, flange_thickness, E)
        
        # Teken balkschema
        beam_fig = plot_beam_diagram(beam_length, supports, loads)
        st.plotly_chart(beam_fig, use_container_width=True)
        
        # Resultaten header
        st.markdown("""
        <style>
        .results-header {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .results-section {
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            border: 1px solid #e9ecef;
            margin-bottom: 20px;
        }
        </style>
        <div class="results-header">
        <h2>📊 Berekeningsresultaten</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Grafieken sectie
        st.markdown("""
        <div class="results-section">
        <h3>📈 Grafieken</h3>
        </div>
        """, unsafe_allow_html=True)
        
        results_plot = plot_results(x, V, M, rotation, deflection)
        st.plotly_chart(results_plot, use_container_width=True)
        
        # Maximale waarden en profiel eigenschappen
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="results-section">
            <h3>📏 Maximale Waarden</h3>
            </div>
            """, unsafe_allow_html=True)
            
            max_vals = {
                "Dwarskracht": [f"{max(abs(np.min(V)), abs(np.max(V)))/1000:.1f}", "kN"],
                "Moment": [f"{max(abs(np.min(M)), abs(np.max(M)))/1e6:.1f}", "kNm"],
                "Rotatie": [f"{max(abs(np.min(rotation)), abs(np.max(rotation))):.4f}", "rad"],
                "Doorbuiging": [f"{max(abs(np.min(deflection)), abs(np.max(deflection))):.2f}", "mm"]
            }
            
            for key, (val, unit) in max_vals.items():
                st.metric(key, f"{val} {unit}")
        
        with col2:
            st.markdown("""
            <div class="results-section">
            <h3>🔧 Profiel Eigenschappen</h3>
            </div>
            """, unsafe_allow_html=True)
            
            A, I, W = calculate_profile_properties(profile_type, height, width, wall_thickness, flange_thickness)
            properties = {
                "Oppervlakte": [f"{A:.0f}", "mm²"],
                "Traagheidsmoment": [f"{I:.0f}", "mm⁴"],
                "Weerstandsmoment": [f"{W:.0f}", "mm³"]
            }
            
            for key, (val, unit) in properties.items():
                st.metric(key, f"{val} {unit}")
            
            # Spanningen
            max_moment = max(abs(np.min(M)), abs(np.max(M)))
            sigma = max_moment / W
            st.metric("Max. buigspanning", f"{sigma:.1f} N/mm²")
        
        # PDF Export sectie
        st.markdown("""
        <div class="results-section">
        <h3>📑 Rapport Exporteren</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Maak een dictionary met alle beam data
        beam_data = {
            "profile_type": profile_type,
            "height": height,
            "width": width,
            "wall_thickness": wall_thickness,
            "flange_thickness": flange_thickness,
            "beam_length": beam_length,
            "supports": supports,
            "loads": loads,
            "max_deflection": max(abs(np.min(deflection)), abs(np.max(deflection))),
            "max_rotation": max(abs(np.min(rotation)), abs(np.max(rotation))),
            "max_shear": max(abs(np.min(V)), abs(np.max(V))),
            "max_moment": max(abs(np.min(M)), abs(np.max(M)))
        }
        
        # Demo export knop (beperkt tot 2 exports)
        remaining_exports = 2 - st.session_state.export_count
        if remaining_exports > 0:
            try:
                pdf_content = generate_pdf_report(beam_data, results_plot)
                col1, col2 = st.columns([3,1])
                with col1:
                    if st.download_button(
                        label=f"⬇️ Download Rapport (PDF) - {remaining_exports} export(s) over",
                        data=pdf_content,
                        file_name="beamsolve_report.pdf",
                        mime="application/pdf",
                        key="download_report"
                    ):
                        st.session_state.export_count += 1
                with col2:
                    st.markdown(f"<small>💡 Tip: Sla dit rapport op voor later gebruik</small>", unsafe_allow_html=True)
                        
                if remaining_exports == 1:
                    st.warning("⚠️ Dit is je laatste gratis export. Upgrade naar Professional voor onbeperkt gebruik!")
            except Exception as e:
                st.error(f"Fout bij genereren rapport: {str(e)}")
        else:
            st.error("🔒 Je hebt je gratis exports gebruikt. Upgrade naar Professional voor onbeperkt gebruik!")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💎 Upgrade naar Professional", type="primary"):
                    st.markdown("### Contact voor Professional Licentie")
                    st.info("Neem contact op via info@beamsolve.nl voor een Professional licentie.")
            with col2:
                st.markdown("""
                <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px;'>
                <h4>💎 Professional Voordelen</h4>
                <ul>
                <li>Onbeperkt PDF exports</li>
                <li>Geavanceerde belastingcombinaties</li>
                <li>Excel/CAD export</li>
                <li>Email support</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
