
from streamlit_autorefresh import st_autorefresh
import streamlit as st
import boto3
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Smart Factory Digital Twin",
    page_icon="🏭",
    layout="wide"
)

# Automatic refresh every 10 seconds
st_autorefresh(interval=10000, key="factory_refresh")

# Dashboard heading
st.title("🏭 Smart Factory Digital Twin")
st.caption(
    "Machine monitoring using AWS Lambda and DynamoDB"
)


# Load readings from DynamoDB
@st.cache_data(ttl=5)
def load_data():
    dynamodb = boto3.resource(
        "dynamodb",
        region_name="us-east-1"
    )

    table = dynamodb.Table("FactoryReadings")

    response = table.scan()
    items = response.get("Items", [])

    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        items.extend(response.get("Items", []))

    return pd.DataFrame(items)


# Refresh button
if st.button("🔄 Refresh readings"):
    st.cache_data.clear()
    st.rerun()


try:
    df = load_data()

    if df.empty:
        st.warning(
            "No readings found. Run factory_simulator.py first."
        )

    else:
        # Prepare data
        for col in ["temperature", "vibration"]:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )

        df = df.sort_values(
            "timestamp", ascending=False
        )

        # Overview metrics
        st.subheader("📊 Factory Overview")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Total Readings",
            len(df)
        )

        c2.metric(
            "Machines",
            df["machine_id"].nunique()
        )

        c3.metric(
            "Alert Readings",
            int((df["status"] == "ALERT").sum())
        )

        # Latest readings table
        st.subheader("📋 Latest Machine Readings")

        st.dataframe(
            df.head(30),
            use_container_width=True,
            hide_index=True
        )

        # Temperature chart
        st.subheader("🌡️ Temperature Monitoring")

        st.line_chart(
            df.sort_values("timestamp"),
            x="timestamp",
            y="temperature",
            color="machine_id"
        )

        # Vibration chart
        st.subheader("📈 Vibration Monitoring")

        st.line_chart(
            df.sort_values("timestamp"),
            x="timestamp",
            y="vibration",
            color="machine_id"
        )

        # Individual machine health
        st.subheader("🏭 Individual Machine Health")

        for machine in sorted(
            df["machine_id"].dropna().unique()
        ):
            machine_data = df[
                df["machine_id"] == machine
            ]

            latest = machine_data.iloc[0]

            temperature = float(
                latest["temperature"]
            )

            vibration = float(
                latest["vibration"]
            )

            status = latest["status"]

            with st.expander(
                f"⚙️ {machine} — {status}",
                expanded=True
            ):
                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Temperature",
                    f"{temperature:.1f} °C"
                )

                c2.metric(
                    "Vibration",
                    f"{vibration:.1f}"
                )

                c3.metric(
                    "Machine Status",
                    "🚨 ALERT"
                    if status == "ALERT"
                    else "✅ NORMAL"
                )

                if status == "ALERT":
                    st.error(
                        "Abnormal reading detected. "
                        "Inspect temperature and vibration."
                    )
                else:
                    st.success(
                        "Readings are within configured limits."
                    )

                # Per-machine temperature history
                st.caption("Temperature History")

                st.line_chart(
                    machine_data.sort_values("timestamp"),
                    x="timestamp",
                    y="temperature"
                )

                # Per-machine vibration history
                st.caption("Vibration History")

                st.line_chart(
                    machine_data.sort_values("timestamp"),
                    x="timestamp",
                    y="vibration"
                )

        # Overall status summary
        st.subheader("🚨 Overall Machine Status")

        st.bar_chart(
            df["status"].value_counts()
        )

        st.caption(
            "Alert rules: temperature > 80 °C "
            "or vibration > 7. These are demonstration "
            "thresholds, not certified industrial safety limits."
        )

except Exception as e:
    st.error(f"Could not load AWS readings: {e}")
