import streamlit as st
import speedtest

# Function to perform internet speed test
def perform_speed_test(choice):
    st.subheader("Running Speed Test...")
    st.write("Please wait while the speed test completes...")

    # Initialize speedtest object
    st_test = speedtest.Speedtest()
    st_test.get_best_server()

    # Perform speed test based on user choice
    if choice == "Download Speed":
        speed = st_test.download() / 1_000_000  # Convert from bits/s to Mbps
        st.write(f"Download Speed: {speed:.2f} Mbps")
    elif choice == "Upload Speed":
        speed = st_test.upload() / 1_000_000  # Convert from bits/s to Mbps
        st.write(f"Upload Speed: {speed:.2f} Mbps")
    elif choice == "Ping":
        speed = st_test.results.ping  # Ping in milliseconds
        st.write(f"Ping: {speed:.2f} ms")
    else:
        st.error("Invalid choice")
        return

# Main function for Streamlit app
def main():
    st.title("Internet Speed Test")

    with st.form("SpeedTestForm"):
        st.write("Select the type of speed test:")
        choice = st.selectbox("", ["Download Speed", "Upload Speed", "Ping"])
        submit_button = st.form_submit_button("Run Speed Test")

        if submit_button:
            perform_speed_test(choice)

# Run the main function
if __name__ == "__main__":
    main()
