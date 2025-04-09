import streamlit as st
import requests
import json
from io import BytesIO

# Title and description
st.title("📤 File Upload")
st.write("Upload a **PDF** or **Image (JPG, JPEG, PNG)** file to send to the API and view the structured response.")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "jpg", "jpeg", "png"])

# When file is uploaded
if uploaded_file:
    # Show file details
    st.write("### 📄 Uploaded File Details")
    st.write(f"**Filename:** {uploaded_file.name}")
    st.write(f"**File Type:** {uploaded_file.type}")
    st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")

    # API endpoint
    url = "https://rshackathon-ibeam.optisolbusiness.com/upload"

    # Prepare file for upload
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

    # Send POST request
    with st.spinner("Sending file to API..."):
        try:
            response = requests.post(url, files=files)
            response.raise_for_status()  # Raise an error for bad status codes
            response_json = response.json()

            # Show response
            st.success("✅ File uploaded successfully!")
            st.write("### 🧾 API Response (JSON):")
            st.json(response_json)

            # Prepare JSON for download
            json_bytes = BytesIO()
            json_bytes.write(json.dumps(response_json, indent=2).encode('utf-8'))
            json_bytes.seek(0)

            st.download_button(
                label="📥 Download JSON Response",
                data=json_bytes,
                file_name="api_response.json",
                mime="application/json"
            )

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error during request: {e}")
        except ValueError:
            st.error("❌ Failed to parse JSON from response.")
