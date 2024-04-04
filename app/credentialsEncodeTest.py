import base64



def to_base64(string_credentials):
    # 00597861+rest@tvh.com:nTCenr4A62y2E3JFWrgbqFh8
    sample_string_bytes = string_credentials.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


if __name__ == "__main__":
    creds = "00597861+rest@tvh.com:nTCenr4A62y2E3JFWrgbqFh8"
    print(to_base64(creds))