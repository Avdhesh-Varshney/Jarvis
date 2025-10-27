import time

import pandas as pd
import pywhatkit
import streamlit as st


def validatePhoneNumber(phone_no):
  """
  Validate phone number format.

  Args:
    phone_no (str): Phone number to validate

  Returns:
    tuple: (is_valid, error_message)
  """
  phone_str = str(phone_no).strip()

  # Remove common separators
  phone_str = phone_str.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

  # Check if it starts with +
  if not phone_str.startswith("+"):
    return False, "Phone number must start with '+' followed by country code (e.g., +1234567890)"

  # Check if remaining characters are digits
  if not phone_str[1:].isdigit():
    return False, "Phone number must contain only digits after the '+' sign"

  # Check minimum length (country code + number should be at least 10 digits)
  if len(phone_str) < 11:
    return False, "Phone number is too short. Include country code (e.g., +1234567890)"

  # Check maximum length (most phone numbers with country code are under 15 digits)
  if len(phone_str) > 16:
    return False, "Phone number is too long"

  return True, None


def sendMsg(phone_no, message, wait_time=15):
  """
  Send WhatsApp message with improved error handling and validation.

  Args:
    phone_no (str): Phone number with country code (e.g., +1234567890)
    message (str): Message to send
    wait_time (int): Time to wait before sending (default: 15 seconds)

  Returns:
    tuple: (success, error_message)
  """
  try:
    # Validate phone number
    is_valid, error_msg = validatePhoneNumber(phone_no)
    if not is_valid:
      return False, error_msg

    # Validate message
    if not message or message.strip() == "":
      return False, "Message cannot be empty"

    # Calculate send time (current time + wait_time seconds)
    current_time = time.localtime()
    hour = current_time.tm_hour
    minute = current_time.tm_min + (wait_time // 60)

    # Handle minute overflow
    if minute >= 60:
      hour += minute // 60
      minute = minute % 60

    # Handle hour overflow
    if hour >= 24:
      hour = hour % 24

    # Send message using pywhatkit with proper timing
    pywhatkit.sendwhatmsg(phone_no, message, hour, minute, wait_time=wait_time, tab_close=True, close_time=3)

    return True, None

  except Exception as e:
    error_message = str(e)
    if "invalid country calling code" in error_message.lower():
      return False, f"Invalid country code in phone number: {phone_no}"
    elif "internet" in error_message.lower() or "connection" in error_message.lower():
      return False, "Network error. Please check your internet connection"
    else:
      return False, f"Failed to send message: {error_message}"


def whatsApp():
  st.markdown("### WhatsApp Automation 📨")
  st.write("This app sends a WhatsApp message to all the contacts in the CSV file.")

  st.info("📝 **Note**: Phone numbers must include country code (e.g., +1234567890)", icon="ℹ️")

  st.markdown("#### Upload a CSV file with phone numbers:")
  uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

  if uploaded_file is not None:
    try:
      df = pd.read_csv(uploaded_file)

      # Validate CSV structure
      if "phone_number" not in df.columns:
        st.error('CSV file must contain a column named "phone_number".', icon="🚫")
        st.info("Example CSV format:\n```\nphone_number\n+1234567890\n+9876543210\n```")
        return

      st.success(f"✅ CSV file loaded successfully! Found {len(df)} phone numbers.", icon="✅")

      # Display preview of phone numbers
      with st.expander("📋 Preview Phone Numbers"):
        st.dataframe(df.head(10))

      # Range selection
      col1, col2 = st.columns(2)
      with col1:
        bottom = st.number_input("Start from row:", min_value=0, max_value=len(df) - 1, value=0)
      with col2:
        top = st.number_input("End at row:", min_value=bottom + 1, max_value=len(df), value=min(bottom + 1, len(df)))

      # Message input
      message = st.text_area("Enter the message to send:", height=150, placeholder="Type your message here...")

      # Wait time configuration
      wait_time = st.slider(
        "Wait time before sending (seconds):", min_value=10, max_value=60, value=15, help="Time to wait before sending each message"
      )

      # Send button
      if st.button("📤 Send WhatsApp Messages", type="primary"):
        if not message or message.strip() == "":
          st.warning("Please enter a message to send.", icon="⚠️")
          return

        if top > len(df):
          st.error("The end row exceeds the total number of phone numbers in the CSV file.", icon="🚫")
          return

        # Create progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        success_count = 0
        failed_count = 0
        failed_numbers = []

        total_messages = top - bottom

        # Send messages
        for index, row in df.iterrows():
          if index >= bottom and index < top:
            phone_no = row["phone_number"]
            status_text.text(f"Sending message {index - bottom + 1}/{total_messages} to {phone_no}...")

            success, error_msg = sendMsg(phone_no, message, wait_time)

            if success:
              success_count += 1
              st.success(f"✅ Message sent to {phone_no}", icon="✅")
            else:
              failed_count += 1
              failed_numbers.append((phone_no, error_msg))
              st.error(f"❌ Failed to send to {phone_no}: {error_msg}", icon="🚫")

            # Update progress
            progress = (index - bottom + 1) / total_messages
            progress_bar.progress(progress)

        # Final summary
        status_text.empty()
        progress_bar.empty()

        st.divider()
        st.markdown("### 📊 Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
          st.metric("Total Messages", total_messages)
        with col2:
          st.metric("✅ Successful", success_count)
        with col3:
          st.metric("❌ Failed", failed_count)

        if failed_count > 0:
          with st.expander("❌ Failed Messages Details"):
            for phone, error in failed_numbers:
              st.error(f"**{phone}**: {error}")
        else:
          st.success("🎉 All messages sent successfully!", icon="🎉")

    except pd.errors.EmptyDataError:
      st.error("The uploaded CSV file is empty.", icon="🚫")
    except pd.errors.ParserError:
      st.error("Failed to parse CSV file. Please check the file format.", icon="🚫")
    except Exception as e:
      st.error(f"An unexpected error occurred: {str(e)}", icon="🚫")

  else:
    st.info("Please upload a CSV file to send messages.", icon="ℹ️")
    st.markdown("""
    **CSV Format Requirements:**
    - Must have a column named `phone_number`
    - Phone numbers must include country code (e.g., +1234567890)
    - Example:
    ```
    phone_number
    +1234567890
    +9876543210
    ```
    """)
