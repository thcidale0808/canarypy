import plotly.graph_objs as go
import streamlit as st


def render_ui(df):
    product_names = ["All"] + sorted(df["product_name"].unique().tolist())
    versions = ["All"] + sorted(df["release_version"].unique().tolist())

    st.markdown(
        "<h1 style='text-align: center; color: white;'>Product Performance</h1>",
        unsafe_allow_html=True,
    )
    selected_product = st.selectbox("Product", product_names)
    selected_version = st.selectbox("Version", versions)

    if selected_product == "All" and selected_version == "All":
        filtered_df = df
    elif selected_product == "All":
        filtered_df = df[df["release_version"] == selected_version]
    elif selected_version == "All":
        filtered_df = df[df["product_name"] == selected_product]
    else:
        filtered_df = df[
            (df["product_name"] == selected_product)
            & (df["release_version"] == selected_version)
        ]

    # Calculate metrics
    total_canary_signals = (
        filtered_df["success_canary_count"].sum()
        + filtered_df["failed_canary_count"].sum()
    )
    total_non_canary_signals = (
        filtered_df["success_non_canary_count"].sum()
        + filtered_df["failed_non_canary_count"].sum()
    )
    total_success_percentage = (
        (
            filtered_df["success_canary_count"].sum()
            + filtered_df["success_non_canary_count"].sum()
        )
        / filtered_df["total_count"].sum()
        * 100
    )
    total_failure_percentage = (
        (
            filtered_df["failed_canary_count"].sum()
            + filtered_df["failed_non_canary_count"].sum()
        )
        / filtered_df["total_count"].sum()
        * 100
    )

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"<h1 style='text-align: center; color: white;'>{int(total_canary_signals)}</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h4 style='text-align: center; color: white;'>Total Canary Signals</h4>",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"<h1 style='text-align: center; color: white;'>{int(total_non_canary_signals)}</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h4 style='text-align: center; color: white;'>Total Active Signals</h4>",
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"<h1 style='text-align: center; color: white;'>{round(total_success_percentage)}%</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h4 style='text-align: center; color: white;'>Percentage Success</h4>",
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"<h1 style='text-align: center; color: white;'>{round(total_failure_percentage)}%</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h4 style='text-align: center; color: white;'>Percentage Failure</h4>",
            unsafe_allow_html=True,
        )

    # Plotting
    fig = go.Figure()

    success_canary_percentage = (
        filtered_df["success_canary_count"] / filtered_df["total_count"]
    ) * 100
    success_non_canary_percentage = (
        filtered_df["success_non_canary_count"] / filtered_df["total_count"]
    ) * 100
    failed_canary_percentage = (
        filtered_df["failed_canary_count"] / filtered_df["total_count"]
    ) * 100
    failed_non_canary_percentage = (
        filtered_df["failed_non_canary_count"] / filtered_df["total_count"]
    ) * 100

    fig.add_trace(
        go.Scatter(
            x=filtered_df["hour"],
            y=success_canary_percentage,
            mode="lines+markers",
            name="Success Canary",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=filtered_df["hour"],
            y=success_non_canary_percentage,
            mode="lines+markers",
            name="Success Non-Canary",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=filtered_df["hour"],
            y=failed_canary_percentage,
            mode="lines+markers",
            name="Failed Canary",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=filtered_df["hour"],
            y=failed_non_canary_percentage,
            mode="lines+markers",
            name="Failed Non-Canary",
        )
    )

    fig.update_layout(
        title="Success and Failure Percentages Over Time",
        xaxis_title="Hour",
        yaxis_title="Percentage",
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        font=dict(color="white"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig)

    band_counts = (
        filtered_df.groupby("canary_band_number")
        .agg(
            {
                "success_canary_count": "sum",
                "success_non_canary_count": "sum",
                "failed_canary_count": "sum",
                "failed_non_canary_count": "sum",
            }
        )
        .reset_index()
    )

    band_counts["total_success_count"] = (
        band_counts["success_canary_count"] + band_counts["success_non_canary_count"]
    )
    band_counts["total_failure_count"] = (
        band_counts["failed_canary_count"] + band_counts["failed_non_canary_count"]
    )

    fig2 = go.Figure(
        data=[
            go.Bar(
                name="Success",
                x=band_counts["canary_band_number"],
                y=band_counts["total_success_count"],
            ),
            go.Bar(
                name="Failure",
                x=band_counts["canary_band_number"],
                y=band_counts["total_failure_count"],
            ),
        ]
    )

    fig2.update_layout(
        title="Total Count of Signals per Band Number",
        xaxis_title="Canary Band Number",
        yaxis_title="Total Count",
        barmode="stack",
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        font=dict(color="white"),
    )

    st.plotly_chart(fig2)
