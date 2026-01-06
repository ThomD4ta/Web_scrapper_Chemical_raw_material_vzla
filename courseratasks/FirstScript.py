import socket

# Create socket
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to host on port 80 (HTTP)
mysock.connect(("data.pr4e.org", 80))

# Proper HTTP GET request with Host header
cmd = (
    "GET /romeo.txt HTTP/1.1\r\n"
    "Host: data.pr4e.org\r\n"
    "Connection: close\r\n"
    "\r\n"
)

mysock.send(cmd.encode())

# Receive full response
response = b""
while True:
    data = mysock.recv(512)
    if len(data) < 1:
        break
    response += data

mysock.close()

# Decode response
response_text = response.decode()

# Split headers and body
headers, body = response_text.split("\r\n\r\n", 1)

print("===== HEADERS =====")
print(headers)

print("\n===== DATA =====")
print(body)