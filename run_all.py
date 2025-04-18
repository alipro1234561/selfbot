import subprocess

# لیست فایل‌هایی که باید اجرا شوند
files = [
    "راهنما.py",
    "سیو اکانت.py",
    "client.py",
    "session.py",
    "1.py", "2.py", "3.py", "4.py", "5.py", "6.py", "7.py",
    "8.py", "9.py", "10.py", "11.py", "12.py", "13.py", "14.py",
    "15.py", "16.py", "17.py", "18.py", "19.py", "20.py", "21.py",
    "22.py", "23.py", "24.py", "25.py", "26.py", "27.py", "28.py",
    "29.py", "30.py", "31.py", "32.py", "33.py", "34.py", "35.py"
]

# اجرای تمام فایل‌ها به صورت همزمان
processes = []
for file in files:
    processes.append(subprocess.Popen(["python", file]))

# منتظر ماندن تا همه پروسس‌ها تمام شوند
for process in processes:
    process.wait()