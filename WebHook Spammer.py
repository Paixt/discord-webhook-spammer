import http.client
import json
import threading
import time

print("GitHub Page: https://github.com/Paixt/discord-webhook-spammer")

def send_discord_webhook(message, webhook_url):
    # Extract the host and the path from the webhook URL
    if webhook_url.startswith("https://"):
        webhook_url = webhook_url[8:]
    host, path = webhook_url.split("/", 1)

    # Prepare the data
    data = {
        "content": message,
    }
    headers = {
        "Content-Type": "application/json"
    }
    json_data = json.dumps(data)

    # Send the request
    conn = http.client.HTTPSConnection(host)
    conn.request("POST", f"/{path}", body=json_data, headers=headers)
    response = conn.getresponse()

    if response.status == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status}")
        print("Response:", response.read().decode())

def send_messages(message, url, count):
    for _ in range(count):
        send_discord_webhook(message, url)
        time.sleep(0.5)  # Add a delay of 0.5 seconds between each webhook message

def main():
    num_webhooks = int(input("Enter number of webhooks to use: "))
    webhook_urls = []
    webhook_messages = []
    send_counts = []

    for i in range(num_webhooks):
        webhook_url = input(f"Enter webhook URL {i + 1}: ")
        webhook_urls.append(webhook_url)
        message = input(f"Enter message for webhook {i + 1}: ")
        webhook_messages.append(message)
        send_count = int(input(f"Enter number of times to send message for webhook {i + 1}: "))
        send_counts.append(send_count)

    threads = []

    for url, message, count in zip(webhook_urls, webhook_messages, send_counts):
        thread = threading.Thread(target=send_messages, args=(message, url, count))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
