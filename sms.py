import serial # type: ignore
import sqlite3
import time
import re

# Configure the serial connection
ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)

def read_sms():
    ser.write(b'AT+CMGF=1\r')  # Set text mode
    time.sleep(1)
    
    ser.write(b'AT+CMGL="REC UNREAD"\r')  # Read unread messages
    time.sleep(2)
    
    response = ser.read(1000).decode('utf-8')
    
    messages = parse_messages(response)
    return messages

def parse_messages(response):
    # Extract phone numbers and messages
    pattern = r'\+CMGL: \d+,"REC UNREAD",".*?","(.+?)".*?\n(.+?)\r'
    matches = re.findall(pattern, response, re.DOTALL)
    
    sms_list = []
    for match in matches:
        phone_number = match[0]
        message = match[1].strip()
        sms_list.append((phone_number, message))
    
    return sms_list

def save_attendance(student_id, name):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO attendance (student_id, name) VALUES (?, ?)", (student_id, name))
    conn.commit()
    conn.close()
    print(f"Attendance recorded for {name} ({student_id})")

def process_sms():
    messages = read_sms()
    for phone, msg in messages:
        parts = msg.split(',')
        if len(parts) == 2:
            student_id = parts[0].strip()
            name = parts[1].strip()
            save_attendance(student_id, name)

if __name__ == "__main__":
    while True:
        process_sms()
        time.sleep(10)  # Check for new SMS every 10 seconds
