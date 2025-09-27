import plotly.graph_objects as go

def plot_comparison(telemetries, channels):
    """
    telemetries: dict with structure {label: telemetry_df}
    channels: list of telemetry channels to plot
    """
    figs = []

    for channel in channels:
        fig = go.Figure()
        for label, tel in telemetries.items():
            if channel not in tel.columns:
                continue
            fig.add_trace(go.Scatter(
                x=tel['Distance'],
                y=tel[channel],
                mode='lines',
                name=label
            ))

        fig.update_layout(
            title=f"{channel} Comparison",
            xaxis_title="Distance (m)",
            yaxis_title=channel,
            template="plotly_dark",
            height=400
        )
        figs.append(fig)

    return figs
